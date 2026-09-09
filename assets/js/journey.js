(function(){
 'use strict';
 var map=document.querySelector('.system-map');
 var reduced=matchMedia('(prefers-reduced-motion: reduce)');
 var paused=reduced.matches;
 var toggle=document.querySelector('.motion-toggle');
 function motion(){document.documentElement.classList.toggle('motion-paused',paused);if(toggle){toggle.textContent=paused?'Enable motion':'Pause motion';toggle.setAttribute('aria-pressed',String(paused));}}
 if(toggle)toggle.addEventListener('click',function(){paused=!paused;motion();});
 motion();reduced.addEventListener('change',function(e){paused=e.matches;motion();});
 if(map){
  map.addEventListener('pointermove',function(e){if(paused||e.pointerType==='touch')return;var r=map.getBoundingClientRect();map.style.setProperty('--ry',((e.clientX-r.left)/r.width-.5)*16+'deg');map.style.setProperty('--rx',-((e.clientY-r.top)/r.height-.5)*12+'deg');});
  map.addEventListener('pointerleave',function(){map.style.removeProperty('--rx');map.style.removeProperty('--ry');});
 }
 var topics={
  erp:{title:'One ERP. Every site.',text:'Production, sales, inventory, procurement, accounting, HR and maintenance connected through one Odoo instance. Explore the decisions behind running it across six sites in five countries.',href:'work/one-erp-six-sites-five-countries.html',label:'Explore the ERP case study'},
  ai:{title:'AI inside the workflow.',text:'Five systems in daily use: document OCR, certificate verification, a sales agent, voice automation and centralised chat. Start with the sales agent and its connection to the ERP.',href:'work/ai-sales-agent-whatsapp-and-web.html',label:'Explore the AI sales agent'},
  data:{title:'Change the foundation. Keep the business running.',text:'A production PostgreSQL migration from 9.5 to 16, supported by backup, recovery, replication and monitoring. Read the migration story and its operational constraints.',href:'work/postgresql-9-5-to-16-migration.html',label:'Explore the database migration'},
  security:{title:'One identity. Clear access.',text:'Google Workspace single sign-on, two-factor authentication and role-based access across a multi-site operation. See the approach to replacing locally held passwords.',href:'work/identity-and-access-rebuild.html',label:'Explore identity and access'}
 };
 document.querySelectorAll('[data-system]').forEach(function(button){button.addEventListener('click',function(){var item=topics[button.dataset.system];if(!item)return;document.querySelectorAll('[data-system]').forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});document.querySelector('#system-title').textContent=item.title;document.querySelector('#system-description').textContent=item.text;var link=document.querySelector('#system-link');link.href=item.href;link.textContent=item.label+' →';});});
 var pending=false;function progress(){pending=false;var d=document.documentElement;d.style.setProperty('--read',String(scrollY/Math.max(1,d.scrollHeight-innerHeight)));}
 addEventListener('scroll',function(){if(!pending){pending=true;requestAnimationFrame(progress);}},{passive:true});progress();
 // Content stays visible without JS; motion is only an enhancement.
 if('IntersectionObserver' in window&&!paused){var observer=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('reveal-ready');observer.unobserve(e.target);}});},{threshold:.08});document.querySelectorAll('main > section').forEach(function(section){var heading=section.querySelector('h2');if(heading)heading.classList.add('reveal-item');observer.observe(section);});}
}());
