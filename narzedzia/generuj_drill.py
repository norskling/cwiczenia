#!/usr/bin/env python3
"""Generuje stronę muntlig drill Norskling z pliku JSON.

Muntlig drill = quiz rozmowy na czas. Jedno pytanie na ekranie, przycisk do następnego pytania,
osobne przyciski do słów kluczowych i pytań pomocniczych (oppfølgingsspørsmål), stoper 2 lub 4 min.

Użycie: python3 generuj_drill.py spec.json wynik.html
Spec: {"pill","title","title_hl","intro","meta":[...],"how":"...","default_min":2,
       "cards":[{"q":"pytanie po norwesku","pl":"tłumaczenie (opcjonalnie)","role":"opis sytuacji (opcjonalnie)",
                 "words":["słowo","..."],"followups":["pytanie","..."]}]}
"""
import json, sys, html, os
D = os.path.dirname(os.path.abspath(__file__)); E = html.escape
EXTRA = """
.quiz{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:26px;box-shadow:0 10px 30px rgba(13,31,45,.06)}
.qtop{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px}
.num{font-family:"Space Grotesk",sans-serif;font-weight:700;color:var(--fjord);font-size:.8rem;text-transform:uppercase;letter-spacing:.12em}
.dots{display:flex;gap:6px}.dots i{width:10px;height:10px;border-radius:50%;background:var(--border)}.dots i.on{background:var(--is)}.dots i.done{background:var(--fjord)}
.card{display:none}.card.cur{display:block}
.card .q{font-family:"Space Grotesk",sans-serif;color:var(--natt);font-size:1.7rem;font-weight:700;letter-spacing:-.02em;line-height:1.25;margin:0}
.card .pl{font-size:.92rem;margin:6px 0 0}
.card .role{font-size:.95rem;color:var(--natt);background:var(--tint);border-radius:8px;padding:8px 12px;margin:12px 0 0}
.panel{display:none;margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--tint)}
.panel.open{display:block}
.lbl{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--fjord);margin:0 0 8px}
.words{display:flex;flex-wrap:wrap;gap:8px}
.words span{background:#fff;color:var(--natt);border:1px solid var(--border);border-radius:100px;padding:5px 12px;font-size:.95rem}
.fu{margin:0;padding-left:20px;color:var(--natt)}.fu li{margin:5px 0}
.helpers{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.helpers .ghost{margin-top:0}.helpers .ghost.on{background:var(--fjord);color:#fff;border-color:var(--fjord)}
.timer{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:18px;padding-top:16px;border-top:1px solid var(--border)}
.clock{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.9rem;color:var(--natt);min-width:92px;font-variant-numeric:tabular-nums}
.clock.end{color:var(--bad)}
.track{flex:1 1 100%;height:6px;background:var(--tint);border-radius:3px;overflow:hidden;order:9}
.track i{display:block;height:100%;width:0;background:var(--is);transition:width .25s linear}
.seg{display:inline-flex;border:1.5px solid var(--border);border-radius:8px;overflow:hidden}
.seg button{font:inherit;font-size:.95rem;background:none;border:0;color:var(--fjord);padding:9px 14px;cursor:pointer;min-height:44px}
.seg button.on{background:var(--fjord);color:#fff}
.timer .btn,.timer .ghost{margin-top:0}
.nav{display:flex;justify-content:space-between;gap:10px;margin-top:22px}
.nav .btn,.nav .ghost{margin-top:0}
.how{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--is);border-radius:16px;padding:18px 22px;margin-bottom:20px;color:var(--natt)}
.fin{display:none;text-align:center;padding:20px 0}.fin.cur{display:block}
.fin p{font-family:"Space Grotesk",sans-serif;font-size:1.5rem;font-weight:700;color:var(--natt);margin:0 0 6px}
@media (max-width:600px){.card .q{font-size:1.35rem}.timer .btn{width:auto}.nav .btn{width:auto}}
"""
JS = """
const $=x=>document.getElementById(x);
let cur=1,total=MIN*60,left=total,run=false,id=null,last=0;
function fmt(s){s=Math.max(0,Math.ceil(s));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function draw(){$('k').textContent=fmt(left);$('k').classList.toggle('end',left<=0);$('p').style.width=(100*(1-left/total))+'%';
  $('b').textContent=run?'Pauza':(left<total&&left>0?'Wznów':'Start')}
function beep(){try{const a=new (window.AudioContext||window.webkitAudioContext)();[0,.35,.7].forEach(d=>{const o=a.createOscillator(),g=a.createGain();o.frequency.value=880;o.connect(g);g.connect(a.destination);g.gain.setValueAtTime(.2,a.currentTime+d);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d+.3);o.start(a.currentTime+d);o.stop(a.currentTime+d+.3)})}catch(e){}}
function go(){if(run){clearInterval(id);run=false;draw();return}if(left<=0)left=total;run=true;last=Date.now();
  id=setInterval(()=>{const now=Date.now();left-=(now-last)/1000;last=now;if(left<=0){left=0;clearInterval(id);run=false;beep()}draw()},250);draw()}
function reset(){clearInterval(id);run=false;left=total;draw()}
function setMin(m){$('m2').classList.toggle('on',m==2);$('m4').classList.toggle('on',m==4);total=m*60;reset()}
function tog(k){if(cur>N)return;const o=$(k+cur).classList.toggle('open');$('b'+k).classList.toggle('on',o)}
function move(d){const n=cur+d;if(n<1||n>N+1)return;
  if(cur<=N){$('c'+cur).classList.remove('cur');$('w'+cur).classList.remove('open');$('f'+cur).classList.remove('open')}else $('fin').classList.remove('cur');
  cur=n;$('bw').classList.remove('on');$('bf').classList.remove('on');
  for(let i=1;i<=N;i++)$('d'+i).className=i<cur?'done':(i==cur?'on':'');
  if(cur<=N){$('c'+cur).classList.add('cur');$('lab').textContent='Pytanie '+cur+' z '+N;$('ctl').style.display=''}
  else{$('fin').classList.add('cur');$('lab').textContent='Koniec';$('ctl').style.display='none'}
  $('prev').style.visibility=cur==1?'hidden':'visible';$('next').style.visibility=cur>N?'hidden':'visible';
  $('next').textContent=cur==N?'Zakończ →':'Następne pytanie →';reset()}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1)});
$('prev').style.visibility='hidden';draw();
"""
def main(sp, out):
    s = json.load(open(sp, encoding="utf-8"))
    dm = int(s.get("default_min", 2)); N = len(s["cards"])
    style = open(os.path.join(D, "styl.css"), encoding="utf-8").read().replace("</style>", EXTRA + "</style>")
    body = []
    for n, c in enumerate(s["cards"], 1):
        pl = f'<p class="pl">{E(c["pl"])}</p>' if c.get("pl") else ""
        role = f'<p class="role">{E(c["role"])}</p>' if c.get("role") else ""
        words = "".join(f"<span>{E(w)}</span>" for w in c.get("words", []))
        fu = "".join(f"<li>{E(x)}</li>" for x in c.get("followups", []))
        cls = "card cur" if n == 1 else "card"
        body.append(f'<section class="{cls}" id="c{n}">\n<p class="q">{E(c["q"])}</p>{pl}{role}\n'
                    f'<div class="panel" id="w{n}"><div class="lbl">Słowa kluczowe</div><div class="words">{words}</div></div>\n'
                    f'<div class="panel" id="f{n}"><div class="lbl">Pytania pomocnicze (oppfølgingsspørsmål)</div><ol class="fu">{fu}</ol></div>\n</section>')
    dots = "".join(f'<i id="d{n}"' + (' class="on"' if n == 1 else '') + '></i>' for n in range(1, N + 1))
    meta = "".join(f"<span>{E(m)}</span>" for m in s.get("meta", []) + [f'{N} pytań'])
    on2 = "on" if dm == 2 else ""; on4 = "on" if dm == 4 else ""
    title = E(s.get("doc_title", "Muntlig drill Norskling"))
    page = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
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
    <div class="qtop"><span class="num" id="lab">Pytanie 1 z {N}</span><span class="dots">{dots}</span></div>
{chr(10).join(body)}
    <div class="fin" id="fin"><p>Koniec pytań</p><span class="muted">Dobra robota! Lektorka zapisuje uwagi do kolejnej lekcji.</span></div>
    <div id="ctl">
      <div class="helpers"><button class="ghost" id="bw" onclick="tog('w')">Słowa kluczowe</button><button class="ghost" id="bf" onclick="tog('f')">Pytania pomocnicze</button></div>
      <div class="timer"><span class="clock" id="k">{dm:02d}:00</span>
        <span class="seg"><button id="m2" class="{on2}" onclick="setMin(2)">2 min</button><button id="m4" class="{on4}" onclick="setMin(4)">4 min</button></span>
        <button class="btn" id="b" onclick="go()">Start</button><button class="ghost" onclick="reset()">Od nowa</button>
        <div class="track"><i id="p"></i></div></div>
    </div>
    <div class="nav"><button class="ghost" id="prev" onclick="move(-1)">← Poprzednie</button><button class="btn" id="next" onclick="move(1)">Następne pytanie →</button></div>
  </div>
</main>
<script>
const N={N},MIN={dm};{JS}</script>
</body>
</html>
"""
    open(out, "w", encoding="utf-8").write(page); print(out, N, "pytań (quiz)")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
