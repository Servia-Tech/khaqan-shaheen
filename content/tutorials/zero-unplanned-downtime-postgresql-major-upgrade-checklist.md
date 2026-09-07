---
title: "A PostgreSQL major-version upgrade with no unplanned downtime: the checklist"
description: Upgrade a production PostgreSQL database to 16 using logical replication, a rehearsed cutover and a rollback window, then rebuild backups and monitoring.
date: 2026-09-08
type: tutorial
tags: [postgresql, upgrade, logical-replication, backup]
---

# A PostgreSQL major-version upgrade with no unplanned downtime: the checklist

By the end of this you will be able to plan and run a PostgreSQL major-version upgrade on a database the business cannot do without, choose between pg_upgrade and logical replication with your eyes open, and leave behind a better recovery position than you started with. It is for engineers who own a production database.

## What you need

- The old server on PostgreSQL 10 or later for built-in logical replication (older publishers need the pglogical extension instead)
- A new server with PostgreSQL 16 installed and network access to the old one
- Spare capacity for a rehearsal clone
- Superuser on both databases and root on both hosts
- A way to stop every application that writes to the database, and a list of what those applications are

## Two ways to do it

`pg_upgrade` and logical replication solve different problems, and the choice decides the shape of the whole project.

`pg_upgrade` rewrites the catalogue in place and, in `--link` mode, hard-links the data files instead of copying them, so even a large database upgrades in minutes. It runs on one host with both sets of binaries installed. Once you start the new cluster after a link-mode upgrade, the old cluster cannot be started again; the way back is a backup. It needs a window with the application stopped. Run `pg_upgrade --check` first, every time, because it finds missing extensions and incompatible data types while there is still time to fix them. On Debian and Ubuntu the `pg_upgradecluster` wrapper from postgresql-common drives it, with a method option for link mode. Planner statistics are not carried over, so the new cluster runs slowly until `vacuumdb --all --analyze-in-stages` has been through it.

Logical replication streams row changes from the old server to a new one, which can be on different hardware, a different operating system and a different major version. The application keeps running against the old server while the new one catches up, and the cutover is a connection-string change measured in seconds. The price is a list of things it does not do. Every replicated table needs a primary key, or a `REPLICA IDENTITY`, or updates and deletes on it fail on the publisher. It copies data, not schema: you create the tables on the new server yourself. It does not replicate sequences, so their values are copied by hand at cutover. It does not replicate DDL, so any schema change during the replication window must be applied to both sides, and the sane policy is to forbid them. It does not copy large objects either.

| | pg_upgrade --link | Logical replication |
|---|---|---|
| Application outage | Minutes, in a planned window | Seconds at cutover |
| Change host or OS at the same time | No | Yes |
| Rollback after cutover | Restore from backup | Old server kept read-only |
| Primary key needed on every table | No | Yes, or REPLICA IDENTITY |
| Copies sequences and schema | Yes | No, done by hand |
| Effort | Low | High |

When the database is the thing the whole business runs on, and the sites using it span time zones so there is no quiet hour, logical replication earns its extra effort. The rest of this is that runbook.

## The runbook

### 1. Audit tables without primary keys

Run this on the old server. Anything it returns needs a primary key added, or `ALTER TABLE ... REPLICA IDENTITY FULL` as a slower fallback.

```sql
SELECT n.nspname, c.relname
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND NOT EXISTS (
      SELECT 1 FROM pg_index i
      WHERE i.indrelid = c.oid AND i.indisprimary
  )
ORDER BY 1, 2;
```

An ERP that has been through several application upgrades will have a handful: old relation tables and leftovers from abandoned modules. Decide each one deliberately.

### 2. Audit extensions and collation versions

List what the old server uses, then confirm each one is available on the new binaries:

```sql
SELECT extname, extversion FROM pg_extension;               -- old server
SELECT name, default_version FROM pg_available_extensions;  -- new server
```

Collation is the quieter risk. Text sort order comes from the operating system's C library, and a new host with a newer glibc can sort accented and mixed-case strings differently. With logical replication every index is built fresh on the new server, so you avoid corrupted indexes, but the application may see a different `ORDER BY` for the same names. With `pg_upgrade` onto a new host, reindex every index on text columns. PostgreSQL 15 and later records `datcollversion` in `pg_database` and warns on a mismatch; take the warning seriously.

### 3. Prepare the publisher

On the old server, `wal_level` must be `logical`, which needs one restart. That restart is the only planned interruption before cutover, so schedule it.

```sql
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;
-- restart the server, then:
CREATE ROLE upgrade_repl WITH REPLICATION LOGIN PASSWORD '...';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO upgrade_repl;
CREATE PUBLICATION upgrade_pub FOR ALL TABLES;
```

Add a `pg_hba.conf` line for the new server's address against the database itself, not the `replication` pseudo-database. Logical replication connects like an ordinary client.

### 4. Prepare the subscriber

Copy roles and schema to the new server, using the new server's `pg_dump` against the old one (a newer `pg_dump` can read an older server; the reverse is not true):

```bash
pg_dumpall -h old-db -U postgres --globals-only | psql -h new-db -U postgres
pg_dump -h old-db -U postgres --schema-only --no-publications --no-subscriptions erp \
    | psql -h new-db -U postgres erp
```

Then subscribe. This creates a replication slot on the publisher and starts the initial copy of every table.

```sql
CREATE SUBSCRIPTION upgrade_sub
    CONNECTION 'host=old-db dbname=erp user=upgrade_repl password=...'
    PUBLICATION upgrade_pub;
```

Raise `max_sync_workers_per_subscription` on the subscriber first if the database is large, so several tables copy at once.

### 5. Monitor the lag

Watch the initial copy finish, then watch the ongoing lag. On the subscriber:

```sql
SELECT srrelid::regclass, srsubstate
FROM pg_subscription_rel WHERE srsubstate <> 'r';   -- empty when the copy is done

SELECT subname, received_lsn, latest_end_lsn, last_msg_receipt_time
FROM pg_stat_subscription;

SELECT subname, apply_error_count, sync_error_count
FROM pg_stat_subscription_stats;                     -- should stay at zero
```

On the publisher, the slot's lag in bytes:

```sql
SELECT slot_name, active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) AS lag
FROM pg_replication_slots;
```

One warning from experience. A replication slot that nobody is consuming holds WAL forever, and the old server's disk fills up. If you abandon the exercise, drop the slot.

### 6. Rehearse on a clone

Restore a backup of production to a spare machine and run the whole sequence from it to a throwaway PostgreSQL 16, timing every step. Then point a copy of the application at the result and use it. Not a benchmark: the real workflows. In an ERP that means creating orders, confirming manufacturing, posting invoices and running the slowest reports, because a heavily customised application is where major-version changes bite. Query plans move. Deprecated behaviour disappears. Something that worked for years throws an error on a data type nobody remembered. Each of those is cheap to find on the clone and expensive to find live. Rehearse the rollback as well. Then rehearse once more with someone else reading the steps aloud.

### 7. Freeze the application

At the agreed time, stop everything that writes: the application server and all its worker processes, its scheduler, integrations, reporting jobs, any script anyone has ever set up. Then confirm from the database side:

```sql
SELECT usename, application_name, client_addr, state
FROM pg_stat_activity WHERE datname = 'erp';
```

Anything still connected that is not you or the replication role gets found now, not after cutover.

### 8. Wait for lag zero, then copy the sequences

Run the slot query from step 5 until the lag is zero and stays there for a minute. Then copy the sequence values, which replication never touched. Generate the statements on the old server and run them on the new:

```sql
SELECT format('SELECT setval(%L, %s, true);',
              format('%I.%I', schemaname, sequencename), last_value)
FROM pg_sequences
WHERE last_value IS NOT NULL;
```

```bash
psql -h old-db -At -f copy_sequences.sql erp | psql -h new-db erp
```

Do this after the freeze and after lag zero, not before. Sequences advance while the application runs, and a sequence set too low produces duplicate key errors on the first insert after cutover.

### 9. Switch, analyse, and open the doors

Detach the subscription so the new server stops following the old one, build planner statistics, then change the application's connection string and start it.

```sql
ALTER SUBSCRIPTION upgrade_sub DISABLE;
ALTER SUBSCRIPTION upgrade_sub SET (slot_name = NONE);
DROP SUBSCRIPTION upgrade_sub;
-- on the old server:
SELECT pg_drop_replication_slot('upgrade_sub');
```

```bash
vacuumdb -h new-db -U postgres --all --analyze-in-stages
```

Run the rehearsal's checks again, briefly, before telling users.

### 10. Keep the old server read-only for a rollback window

Do not switch the old server off. Make it read-only and unreachable by the application, and leave it that way for an agreed period.

```sql
ALTER ROLE erp_app NOLOGIN;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'erp_app';
ALTER SYSTEM SET default_transaction_read_only = on;
SELECT pg_reload_conf();
```

Rolling back inside that window means pointing the application at the old server again and re-keying what was entered in between. If that is unacceptable, set up a reverse publication from new to old before you open the application, so the old server follows the new one. It is more work, and it is the only rollback that keeps the data.

### 11. Rebuild backups, recovery and monitoring

A new server has no backups until you make them. I treat the migration as the moment to rebuild the whole recovery position, because it is the one time everybody agrees it matters.

With pgBackRest: on the new server set `archive_mode = on` and `archive_command = 'pgbackrest --stanza=main archive-push %p'` (a restart for `archive_mode`), then:

```bash
pgbackrest --stanza=main stanza-create
pgbackrest --stanza=main check
pgbackrest --stanza=main --type=full backup
```

The `check` command proves that WAL archiving works end to end, which is the part people skip. Then prove the restore. Point in time recovery to a chosen moment looks like this on a scratch machine:

```bash
pgbackrest --stanza=main --delta --type=time \
    "--target=2026-09-08 10:15:00+04" --target-action=promote restore
```

If you prefer plain tools, `pg_basebackup -D /backup/base -Fp -Xs -P` plus the same `archive_command` into a safe directory gives you a base backup and continuous WAL; recovery uses `restore_command` and `recovery_target_time` in `postgresql.conf` with a `recovery.signal` file. Either way, restore to a second machine and open the application against it before you call it done. A backup that has never been restored is a hope, not a position.

Monitoring on the new server should alert on at least: `pg_stat_archiver.failed_count` rising, backup age, replication slot lag if any slots remain, disk space on the data and WAL volumes, connection count near `max_connections`, and transactions open for longer than a few minutes.

## The checklist

| Phase | Item | Done |
|---|---|---|
| Audit | Tables without primary keys resolved | |
| Audit | Extensions available on the new binaries | |
| Audit | Collation and glibc versions compared | |
| Audit | Every writer to the database listed | |
| Prepare | `wal_level = logical`, restart done | |
| Prepare | Replication role, `pg_hba.conf`, publication | |
| Prepare | Globals and schema restored on the new server | |
| Prepare | Subscription created, initial copy complete | |
| Rehearse | Full runbook run on a clone, steps timed | |
| Rehearse | Application tested against the clone | |
| Rehearse | Rollback rehearsed | |
| Cutover | Schema changes frozen on both sides | |
| Cutover | Application and every writer stopped | |
| Cutover | `pg_stat_activity` clean | |
| Cutover | Lag zero and stable | |
| Cutover | Sequences copied | |
| Cutover | Subscription dropped, slot dropped, statistics built | |
| Cutover | Connection string switched, application checked | |
| Cutover | Old server read-only, app role locked | |
| After | WAL archiving and `pgbackrest check` passing | |
| After | Restore and point in time recovery proven | |
| After | Monitoring and alerts live | |
| After | Old server decommissioned at end of window | |

## Common questions

### Why not use pg_upgrade when it is so much faster?

Use it when you can take the window and you are staying on the same host. It is less work and fewer moving parts, and `--link` mode makes the outage short. Logical replication is for the cases pg_upgrade cannot cover: no acceptable window, a move to new hardware or a new operating system at the same time, or a rollback that must not depend on a restore.

### Can I skip the rehearsal if the database is small?

No. The rehearsal is not about size, it is about the application. A small database under a heavily customised application has the same query-plan changes, the same deprecated behaviour and the same extension gaps as a large one. The clone is also where you time the steps, and the timings are what let you promise a window and keep it.

### What happens if someone changes the schema during replication?

A new table on the publisher is not on the subscriber, so replication for it fails, and a column added on one side but not the other stops the apply worker with an error in `pg_stat_subscription_stats`. Freeze schema changes for the whole window, including application module updates that alter tables. If one gets through, apply the same change on the subscriber, then `ALTER SUBSCRIPTION upgrade_sub REFRESH PUBLICATION` to pick up new tables.
