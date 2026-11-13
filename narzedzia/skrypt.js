<script>
const TOTAL=60;const solved=new Set();
function mark(n,ok,msg){
  const f=document.getElementById('f'+n);
  f.className='fb '+(ok?'ok':'bad');f.textContent=msg;
  if(ok)solved.add(n);
  document.getElementById('score').textContent=solved.size;
  document.getElementById('done').style.display=solved.size===TOTAL?'block':'none';
}
function norm(s){return s.toLowerCase().replace(/[.,!?;:"«»„”'’]/g,' ').replace(/\s+/g,' ').trim()}
function checkText(n,answers,okMsg){
  const v=norm(document.getElementById('t'+n).value);
  if(!v){mark(n,false,'Wpisz odpowiedź.');return}
  const ok=answers.map(norm).includes(v);
  mark(n,ok,ok?okMsg:'Jeszcze nie. Sprawdź formę i szyk, spróbuj ponownie albo kliknij „Pokaż odpowiedź”.');
}
function showSol(n){document.getElementById('s'+n).style.display='block'}
document.querySelectorAll('.opts').forEach(g=>{
  g.querySelectorAll('.opt').forEach(b=>b.addEventListener('click',()=>{
    const n=+g.dataset.q, ok=b.textContent===g.dataset.correct;
    g.querySelectorAll('.opt').forEach(x=>x.classList.remove('ok','bad'));
    b.classList.add(ok?'ok':'bad');
    if(ok)g.querySelectorAll('.opt').forEach(x=>x.disabled=true);
    mark(n,ok,ok?g.dataset.ok:'Jeszcze nie. Spróbuj inną opcję.');
  }));
});
function checkMatch(n,key){
  let good=0;const all=Object.keys(key).length;
  for(const id in key){const s=document.getElementById(id);const ok=s.value===key[id];if(ok)good++;
    s.style.borderColor=s.value?(ok?'var(--ok)':'var(--bad)'):'var(--border)';}
  mark(n,good===all,good===all?'Dobrze. Wszystkie pary pasują.':'Poprawnie: '+good+' z '+all+'. Popraw zaznaczone na czerwono.');
}
</script>
