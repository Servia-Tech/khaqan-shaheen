#!/usr/bin/env python3
"""Move the site to a custom domain in one run, once the domain is bought and DNS is set.

Usage:  python switch_domain.py khaqanshaheen.com
What it does, in order, stopping at the first failure:
  1. Checks DNS: the apex must have the four GitHub Pages A records and www a CNAME to servia-tech.github.io.
  2. Sets the custom domain on the GitHub Pages site (API), which also starts HTTPS provisioning.
  3. Writes the CNAME file, rewrites BASE in build.py and every hard-coded URL in index.html, press.html,
     robots.txt and the host-root repo, rebuilds, commits and pushes.
  4. Waits for HTTPS, then resubmits every URL to IndexNow with a key file on the new host.
The old github.io URLs keep working: GitHub redirects them to the new domain.

Needs: the Servia-Tech PAT in C:/Users/Lenovo/servia_credentials/SERVIA-CREDENTIALS.md, git on PATH, requests.
"""
import pathlib
import re
import socket
import subprocess
import sys
import time

import requests

ROOT = pathlib.Path(__file__).parent
OLD = "https://servia-tech.github.io/khaqan-shaheen"
GH_IPS = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}
REPO = "Servia-Tech/khaqan-shaheen"
ROOT_REPO = pathlib.Path(r"C:/Users/Lenovo/github/servia-tech.github.io")


def token():
    creds = pathlib.Path(r"C:/Users/Lenovo/servia_credentials/SERVIA-CREDENTIALS.md").read_text(encoding="utf-8", errors="replace")
    return re.search(r"ghp_[A-Za-z0-9]+", creds).group(0)


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit(f"failed: {cmd}")
    return r.stdout


def check_dns(domain):
    try:
        ips = {a[4][0] for a in socket.getaddrinfo(domain, 443, socket.AF_INET)}
    except socket.gaierror:
        sys.exit(f"{domain} does not resolve yet. Add the A records at the registrar and wait a few minutes.")
    if not ips & GH_IPS:
        sys.exit(f"{domain} resolves to {ips}, not to GitHub Pages. Set A records to {sorted(GH_IPS)}.")
    try:
        www = {a[4][0] for a in socket.getaddrinfo("www." + domain, 443, socket.AF_INET)}
        print("www resolves to", sorted(www))
    except socket.gaierror:
        print("www." + domain, "does not resolve; add CNAME www -> servia-tech.github.io (optional but recommended)")
    print("DNS ok:", domain, "->", sorted(ips))


def set_pages_domain(domain):
    h = {"Authorization": f"token {token()}", "Accept": "application/vnd.github+json"}
    r = requests.put(f"https://api.github.com/repos/{REPO}/pages", headers=h, json={"cname": domain, "https_enforced": False}, timeout=30)
    print("pages custom domain:", r.status_code, (r.text or "")[:120])
    if r.status_code not in (200, 204):
        sys.exit("could not set the custom domain")


def rewrite(domain):
    new = f"https://{domain}"
    (ROOT / "CNAME").write_text(domain + "\n", encoding="utf-8")
    for f in ["build.py", "index.html", "press.html", "robots.txt", "README.md"]:
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        s = s.replace(OLD + "/", new + "/").replace(OLD, new)
        p.write_text(s, encoding="utf-8")
    # host root repo: redirect and sitemap index point at the new home
    for f in ["index.html", "robots.txt", "sitemap.xml", "llms.txt"]:
        p = ROOT_REPO / f
        if p.exists():
            s = p.read_text(encoding="utf-8").replace(OLD + "/", new + "/").replace(OLD, new)
            p.write_text(s, encoding="utf-8")
    print("rewrote URLs to", new)


def build_and_push(domain):
    run("python build.py")
    run("git add -A")
    run(f'git commit -m "Move to {domain}" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"')
    run(f"git push https://Servia-Tech:{token()}@github.com/{REPO}.git main")
    run("git add -A", cwd=ROOT_REPO)
    run(f'git commit -m "Point host root at {domain}" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"', cwd=ROOT_REPO)
    run(f"git push https://Servia-Tech:{token()}@github.com/Servia-Tech/servia-tech.github.io.git main", cwd=ROOT_REPO)
    print("pushed both repos")


def wait_https(domain):
    for i in range(60):
        try:
            r = requests.get(f"https://{domain}/", timeout=20)
            if r.status_code == 200:
                print("HTTPS live after", i * 20, "seconds")
                return
        except Exception:
            pass
        time.sleep(20)
    print("HTTPS not live after 20 minutes; GitHub may still be provisioning the certificate. Re-run the IndexNow step later.")


def indexnow(domain):
    key = pathlib.Path(r"C:/Users/Lenovo/servia_credentials/indexnow_key_khaqan_site.txt").read_text().strip()
    keyfile = ROOT / f"{key}.txt"
    if not keyfile.exists():
        keyfile.write_text(key + "\n", encoding="utf-8")
    sm = requests.get(f"https://{domain}/sitemap.xml", timeout=20).text
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    r = requests.post("https://api.indexnow.org/IndexNow", json={"host": domain, "key": key, "keyLocation": f"https://{domain}/{key}.txt", "urlList": urls}, timeout=30)
    print("IndexNow", len(urls), "URLs ->", r.status_code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = sys.argv[1].lower().strip().rstrip("/").replace("https://", "").replace("http://", "")
    check_dns(d)
    set_pages_domain(d)
    rewrite(d)
    build_and_push(d)
    wait_https(d)
    indexnow(d)
    print("done. Next: enforce HTTPS in the repo's Pages settings once the certificate shows, and add the new property in Search Console.")
