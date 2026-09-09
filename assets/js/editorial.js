(function(){'use strict';
 document.querySelectorAll('[data-demo]').forEach(function(demo){
  var type=demo.dataset.demo;
  function time(n){return String(Math.floor(n)).padStart(2,'0')+':'+(n%1?'30':'00');}
  function update(){
   if(type==='review'){
    var v=Number(demo.querySelector('[name=volume]').value),a=Number(demo.querySelector('[name=accuracy]').value);
    demo.querySelector('[data-volume]').textContent=v.toLocaleString('en');demo.querySelector('[data-accuracy]').textContent=a+'%';
    demo.querySelector('[data-clean]').style.width=a+'%';demo.querySelector('[data-review]').style.width=(100-a)+'%';
    demo.querySelector('[data-result]').textContent=Math.round(v*(1-a/100)).toLocaleString('en')+' documents';
   }else if(type==='schedule'){
    var start=Number(demo.querySelector('[name=start]').value),end=start+2,overlap=start<11&&end>9;
    demo.querySelector('[data-start]').textContent=time(start);demo.querySelector('[data-order]').style.left=((start-8)/8*100)+'%';
    demo.querySelector('[data-result]').textContent=overlap?'Conflict: both orders use the machine from '+time(Math.max(9,start))+' to '+time(Math.min(11,end))+'.':'No overlap: Order B runs '+time(start)+' to '+time(end)+'.';
   }
  }
  demo.addEventListener('input',update);update();
 });
}());
