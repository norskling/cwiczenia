#!/usr/bin/env python3
"""Generuje stronę muntlig drill Norskling z pliku JSON.

Użycie: python3 generuj_drill.py spec.json wynik.html
Spec: {"pill","title","title_hl","intro","meta":[...],"how":"...",
       "sections":[{"title","intro","items":[{"cue","prompt","answer","note"?}]}]}
cue = podpowiedź po polsku (opcjonalna), prompt = to, co mówi lektorka, answer = wzorcowa odpowiedź.
"""
import json, sys, html, os
D = os.path.dirname(os.path.abspath(__file__)); E = html.escape
EXTRA = """
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:18px 22px;margin-bottom:12px}
.card .num{font-family:"Space Grotesk",sans-serif;font-weight:700;color:var(--fjord);font-size:.85rem;margin-bottom:4px}
.card .cue{font-size:.9rem;margin:0 0 4px}
.card .prompt{color:var(--natt);font-size:1.15rem;font-weight:600;margin:0}
.card .ans{display:none;margin-top:12px;padding:10px 14px;border-radius:8px;background:var(--tint);color:var(--natt)}
.card .ans small{display:block;color:var(--skygge);margin-top:4px}
.card.open .ans{display:block}
.card .ghost{margin-top:12px}
.tools{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 20px}
.how{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--is);border-radius:16px;padding:18px 22px;margin-bottom:20px;color:var(--natt)}
"""
def main(sp, out):
    s = json.load(open(sp, encoding="utf-8"))
    style = open(os.path.join(D, "styl.css"), encoding="utf-8").read().replace("</style>", EXTRA + "</style>")
    body, n = [], 0
    for sec in s["sections"]:
        body.append(f'<h2 class="part">{E(sec["title"])}</h2>')
        if sec.get("intro"): body.append(f'<p class="partintro">{E(sec["intro"])}</p>')
        for it in sec["items"]:
            n += 1
            cue = f'<p class="cue">{E(it["cue"])}</p>' if it.get("cue") else ""
            note = f'<small>{E(it["note"])}</small>' if it.get("note") else ""
            body.append(f'<div class="card" id="c{n}"><div class="num">{n}</div>{cue}<p class="prompt">{E(it["prompt"])}</p>'
                        f'<button class="ghost" onclick="tog({n})">Pokaż odpowiedź</button>'
                        f'<div class="ans">{E(it["answer"])}{note}</div></div>')
    meta = "".join(f"<span>{E(m)}</span>" for m in s.get("meta", []) + [f"{n} kart"])
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
  <div class="tools"><button class="ghost" onclick="all_(true)">Pokaż wszystkie odpowiedzi</button><button class="ghost" onclick="all_(false)">Ukryj wszystkie</button></div>
{chr(10).join(body)}
</main>
<script>
function tog(n){{const c=document.getElementById('c'+n);c.classList.toggle('open');c.querySelector('.ghost').textContent=c.classList.contains('open')?'Ukryj odpowiedź':'Pokaż odpowiedź'}}
function all_(o){{document.querySelectorAll('.card').forEach(c=>{{c.classList.toggle('open',o);c.querySelector('.ghost').textContent=o?'Ukryj odpowiedź':'Pokaż odpowiedź'}})}}
</script>
</body>
</html>
'''
    open(out, "w", encoding="utf-8").write(page); print(out, n, "kart")
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
