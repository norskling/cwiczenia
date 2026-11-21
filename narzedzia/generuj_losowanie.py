#!/usr/bin/env python3
"""Generuje stronę „losowanie” Norskling: ćwiczenie ustne z losowanym pytaniem / kartą.

Przycisk „Losuj” pokazuje losową kartę (bez powtórzeń, aż skończą się karty), przycisk „Podpowiedź”
odkrywa słowa kluczowe i przykład, opcjonalny stoper (min w "timer", np. [1,2]).

Użycie: python3 generuj_losowanie.py spec.json wynik.html
Spec: {"doc_title","pill","title","title_hl","intro","meta":[...],"how":"...","timer":[1,2]?,"label":"Pytanie"?,
       "cards":[{"q":"treść karty","pl":"tłumaczenie/opis"?,"words":["..."]?,"example":"przykładowa odpowiedź"?}]}
"""
import json, sys, html, os
D = os.path.dirname(os.path.abspath(__file__)); E = html.escape
EXTRA = """
.quiz{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:26px;box-shadow:0 10px 30px rgba(13,31,45,.06)}
.qtop{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px}
.num{font-family:"Space Grotesk",sans-serif;font-weight:700;color:var(--fjord);font-size:.8rem;text-transform:uppercase;letter-spacing:.12em}
.stage{min-height:150px;display:flex;flex-direction:column;justify-content:center}
.q{font-family:"Space Grotesk",sans-serif;color:var(--natt);font-size:1.8rem;font-weight:700;letter-spacing:-.02em;line-height:1.25;margin:0}
.q.idle{color:var(--skygge);font-size:1.2rem;font-weight:600}
.pl{font-size:.95rem;margin:8px 0 0}
.panel{display:none;margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--tint)}
.panel.open{display:block}
.lbl{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--fjord);margin:0 0 8px}
.words{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px}
.words span{background:#fff;color:var(--natt);border:1px solid var(--border);border-radius:100px;padding:5px 12px;font-size:.95rem}
.ex{color:var(--natt);margin:0}
.ctl{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.ctl .btn,.ctl .ghost{margin-top:0}
.timer{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:18px;padding-top:16px;border-top:1px solid var(--border)}
.clock{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.7rem;color:var(--natt);min-width:86px;font-variant-numeric:tabular-nums}
.clock.end{color:var(--bad)}
.seg{display:inline-flex;border:1.5px solid var(--border);border-radius:8px;overflow:hidden}
.seg button{font:inherit;font-size:.95rem;background:none;border:0;color:var(--fjord);padding:9px 14px;cursor:pointer;min-height:44px}
.seg button.on{background:var(--fjord);color:#fff}
.timer .ghost{margin-top:0}
.how{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--is);border-radius:16px;padding:18px 22px;margin-bottom:20px;color:var(--natt)}
@media (max-width:600px){.q{font-size:1.4rem}.ctl .btn{width:100%}}
"""
JS = """
const $=x=>document.getElementById(x);let pool=[],seen=0,cur=-1;
function refill(){pool=[...Array(C.length).keys()];for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]]}}
function draw(){if(!pool.length){refill();seen=0}cur=pool.pop();seen++;const c=C[cur];
  $('q').className='q';$('q').textContent=c.q;$('pl').textContent=c.pl||'';
  $('w').innerHTML=(c.words||[]).map(w=>'<span>'+w.replace(/</g,'&lt;')+'</span>').join('');$('ex').textContent=c.example?('Przykład: '+c.example):'';
  $('hp').classList.remove('open');$('bh').style.display=(c.words&&c.words.length)||c.example?'':'none';
  $('lab').textContent='Wylosowano '+seen+' z '+C.length;$('bd').textContent='Losuj kolejne';if(T.length)reset()}
function hint(){$('hp').classList.toggle('open')}
let total=(T[0]||1)*60,left=total,run=false,id=null,last=0;
function fmt(s){s=Math.max(0,Math.ceil(s));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function tdraw(){if(!T.length)return;$('k').textContent=fmt(left);$('k').classList.toggle('end',left<=0);$('b').textContent=run?'Pauza':(left<total&&left>0?'Wznów':'Start')}
function beep(){try{const a=new (window.AudioContext||window.webkitAudioContext)();[0,.35,.7].forEach(d=>{const o=a.createOscillator(),g=a.createGain();o.frequency.value=880;o.connect(g);g.connect(a.destination);g.gain.setValueAtTime(.2,a.currentTime+d);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d+.3);o.start(a.currentTime+d);o.stop(a.currentTime+d+.3)})}catch(e){}}
function go(){if(run){clearInterval(id);run=false;tdraw();return}if(left<=0)left=total;run=true;last=Date.now();
  id=setInterval(()=>{const now=Date.now();left-=(now-last)/1000;last=now;if(left<=0){left=0;clearInterval(id);run=false;beep()}tdraw()},250);tdraw()}
function reset(){clearInterval(id);run=false;left=total;tdraw()}
function setMin(m){T.forEach(x=>$('m'+x).classList.toggle('on',x==m));total=m*60;reset()}
document.addEventListener('keydown',e=>{if(e.key===' '&&e.target===document.body){e.preventDefault();draw()}});
refill();tdraw();
"""
def main(sp, out):
    s = json.load(open(sp, encoding="utf-8")); T = s.get("timer", [])
    style = open(os.path.join(D, "styl.css"), encoding="utf-8").read().replace("</style>", EXTRA + "</style>")
    N = len(s["cards"]); meta = "".join(f"<span>{E(m)}</span>" for m in s.get("meta", []) + [f"{N} kart"])
    timer = ""
    if T:
        segs = "".join(f'<button id="m{m}" class="{"on" if i == 0 else ""}" onclick="setMin({m})">{m} min</button>' for i, m in enumerate(T))
        timer = (f'<div class="timer"><span class="clock" id="k">{T[0]:02d}:00</span><span class="seg">{segs}</span>'
                 f'<button class="btn" id="b" onclick="go()" style="margin-top:0">Start</button><button class="ghost" onclick="reset()">Od nowa</button></div>')
    cards = json.dumps([{k: c[k] for k in ("q", "pl", "words", "example") if c.get(k)} for c in s["cards"]], ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(s.get("doc_title", "Losowanie Norskling"))}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
{style}
</head>
<body>
<main class="wrap">
  <span class="pill">{E(s["pill"])}</span>
  <h1>{E(s["title"])} <span>{E(s["title_hl"])}</span></h1>
  <div class="bar"></div>
  <p class="intro">{E(s["intro"])}</p>
  <div class="meta">{meta}</div>
  <div class="how">{E(s["how"])}</div>
  <div class="quiz">
    <div class="qtop"><span class="num" id="lab">{E(s.get("label", "Kliknij „Losuj”"))}</span></div>
    <div class="stage"><p class="q idle" id="q">Kliknij „Losuj”, żeby wylosować pierwszą kartę.</p><p class="pl" id="pl"></p></div>
    <div class="panel" id="hp"><div class="lbl">Podpowiedź</div><div class="words" id="w"></div><p class="ex" id="ex"></p></div>
    <div class="ctl"><button class="btn" id="bd" onclick="draw()">Losuj</button><button class="ghost" id="bh" onclick="hint()" style="display:none">Podpowiedź</button></div>
    {timer}
  </div>
</main>
<script>
const C={cards},T={json.dumps(T)};{JS}</script>
</body>
</html>
"""
    open(out, "w", encoding="utf-8").write(page); print(out, N, "kart (losowanie)")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
