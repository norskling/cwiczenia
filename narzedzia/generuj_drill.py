#!/usr/bin/env python3
"""Generuje stronę muntlig drill Norskling z pliku JSON.

Muntlig drill = rozmowa na czas. Każda karta: pytanie do rozmowy, stoper 2 lub 4 min,
słowa pomocnicze i oppfølgingsspørsmål dla lektorki.

Użycie: python3 generuj_drill.py spec.json wynik.html
Spec: {"pill","title","title_hl","intro","meta":[...],"how":"...","default_min":2,
       "cards":[{"q":"pytanie po norwesku","pl":"tłumaczenie (opcjonalnie)","role":"opis sytuacji (opcjonalnie)",
                 "words":["słowo","..."],"followups":["pytanie","..."]}]}
"""
import json, sys, html, os
D = os.path.dirname(os.path.abspath(__file__)); E = html.escape
EXTRA = """
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px;margin-bottom:16px}
.card.active{border-color:var(--is);box-shadow:0 10px 30px rgba(13,31,45,.07)}
.card .num{font-family:"Space Grotesk",sans-serif;font-weight:700;color:var(--fjord);font-size:.8rem;text-transform:uppercase;letter-spacing:.12em;margin-bottom:6px}
.card .q{font-family:"Space Grotesk",sans-serif;color:var(--natt);font-size:1.45rem;font-weight:700;letter-spacing:-.02em;line-height:1.25;margin:0}
.card .pl{font-size:.92rem;margin:4px 0 0}
.card .role{font-size:.95rem;color:var(--natt);background:var(--tint);border-radius:8px;padding:8px 12px;margin:10px 0 0}
.lbl{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--fjord);margin:16px 0 8px}
.words{display:flex;flex-wrap:wrap;gap:8px}
.words span{background:var(--tint);color:var(--natt);border:1px solid var(--border);border-radius:100px;padding:5px 12px;font-size:.95rem}
.fu{display:none;margin:0;padding-left:20px;color:var(--natt)}
.fu li{margin:4px 0}
.card.showfu .fu{display:block}
.timer{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:18px;padding-top:16px;border-top:1px solid var(--border)}
.clock{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.9rem;color:var(--natt);min-width:92px;font-variant-numeric:tabular-nums}
.clock.end{color:var(--bad)}
.track{flex:1 1 100%;height:6px;background:var(--tint);border-radius:3px;overflow:hidden;order:9}
.track i{display:block;height:100%;width:0;background:var(--is);transition:width .25s linear}
.seg{display:inline-flex;border:1.5px solid var(--border);border-radius:8px;overflow:hidden}
.seg button{font:inherit;font-size:.95rem;background:none;border:0;color:var(--fjord);padding:9px 14px;cursor:pointer;min-height:44px}
.seg button.on{background:var(--fjord);color:#fff}
.timer .btn,.timer .ghost{margin-top:0}
.how{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--is);border-radius:16px;padding:18px 22px;margin-bottom:20px;color:var(--natt)}
.tools{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 20px}
.tools .ghost{margin-top:0}
@media (max-width:600px){.card .q{font-size:1.25rem}.timer .btn{width:auto}}
"""
def main(sp, out):
    s = json.load(open(sp, encoding="utf-8"))
    dm = int(s.get("default_min", 2))
    style = open(os.path.join(D, "styl.css"), encoding="utf-8").read().replace("</style>", EXTRA + "</style>")
    body = []
    for n, c in enumerate(s["cards"], 1):
        pl = f'<p class="pl">{E(c["pl"])}</p>' if c.get("pl") else ""
        role = f'<p class="role">{E(c["role"])}</p>' if c.get("role") else ""
        words = "".join(f"<span>{E(w)}</span>" for w in c.get("words", []))
        fu = "".join(f"<li>{E(x)}</li>" for x in c.get("followups", []))
        body.append(f'''<section class="card" id="c{n}" data-min="{dm}">
<div class="num">Pytanie {n} z {len(s["cards"])}</div>
<p class="q">{E(c["q"])}</p>{pl}{role}
<div class="lbl">Słowa pomocnicze</div><div class="words">{words}</div>
<div class="lbl">Oppfølgingsspørsmål <button class="ghost" style="margin:0 0 0 8px;padding:4px 10px;min-height:0;font-size:.8rem" onclick="fu({n})">pokaż</button></div>
<ol class="fu">{fu}</ol>
<div class="timer"><span class="clock" id="k{n}">{dm:02d}:00</span>
<span class="seg"><button class="{"on" if dm==2 else ""}" onclick="setMin({n},2,this)">2 min</button><button class="{"on" if dm==4 else ""}" onclick="setMin({n},4,this)">4 min</button></span>
<button class="btn" id="b{n}" onclick="go({n})">Start</button><button class="ghost" onclick="reset({n})">Od nowa</button>
<div class="track"><i id="p{n}"></i></div></div>
</section>''')
    meta = "".join(f"<span>{E(m)}</span>" for m in s.get("meta", []) + [f'{len(s["cards"])} pytań'])
    page = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(s.get("doc_title","Muntlig drill Norskling"))}</title>
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
  <div class="tools"><button class="ghost" onclick="allFu(true)">Pokaż wszystkie oppfølgingsspørsmål</button><button class="ghost" onclick="allFu(false)">Ukryj</button></div>
{chr(10).join(body)}
</main>
<script>
const T={{}};
function fmt(s){{s=Math.max(0,Math.ceil(s));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}}
function st(n){{const c=document.getElementById('c'+n);return T[n]||(T[n]={{total:+c.dataset.min*60,left:+c.dataset.min*60,run:false,id:null,last:0}})}}
function draw(n){{const t=st(n),k=document.getElementById('k'+n);k.textContent=fmt(t.left);k.classList.toggle('end',t.left<=0);
  document.getElementById('p'+n).style.width=(100*(1-t.left/t.total))+'%';
  document.getElementById('b'+n).textContent=t.run?'Pauza':(t.left<t.total&&t.left>0?'Wznów':'Start')}}
function beep(){{try{{const a=new (window.AudioContext||window.webkitAudioContext)();[0,.35,.7].forEach(d=>{{const o=a.createOscillator(),g=a.createGain();o.frequency.value=880;o.connect(g);g.connect(a.destination);g.gain.setValueAtTime(.2,a.currentTime+d);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d+.3);o.start(a.currentTime+d);o.stop(a.currentTime+d+.3)}})}}catch(e){{}}}}
function stopAll(ex){{for(const k in T)if(+k!==ex&&T[k].run){{clearInterval(T[k].id);T[k].run=false;draw(+k);document.getElementById('c'+k).classList.remove('active')}}}}
function go(n){{const t=st(n);if(t.run){{clearInterval(t.id);t.run=false;draw(n);return}}
  if(t.left<=0)t.left=t.total;stopAll(n);t.run=true;t.last=Date.now();document.getElementById('c'+n).classList.add('active');
  t.id=setInterval(()=>{{const now=Date.now();t.left-=(now-t.last)/1000;t.last=now;
    if(t.left<=0){{t.left=0;clearInterval(t.id);t.run=false;beep();document.getElementById('c'+n).classList.remove('active')}}draw(n)}},250);draw(n)}}
function reset(n){{const t=st(n);clearInterval(t.id);t.run=false;t.left=t.total;document.getElementById('c'+n).classList.remove('active');draw(n)}}
function setMin(n,m,b){{const c=document.getElementById('c'+n);c.dataset.min=m;b.parentNode.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));
  const t=st(n);clearInterval(t.id);t.run=false;t.total=t.left=m*60;c.classList.remove('active');draw(n)}}
function fu(n){{const c=document.getElementById('c'+n);c.classList.toggle('showfu');c.querySelector('.lbl .ghost').textContent=c.classList.contains('showfu')?'ukryj':'pokaż'}}
function allFu(o){{document.querySelectorAll('.card').forEach(c=>{{c.classList.toggle('showfu',o);c.querySelector('.lbl .ghost').textContent=o?'ukryj':'pokaż'}})}}
</script>
</body>
</html>
'''
    open(out, "w", encoding="utf-8").write(page); print(out, len(s["cards"]), "kart")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
