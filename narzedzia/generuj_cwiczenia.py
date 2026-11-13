#!/usr/bin/env python3
"""Generuje stronę ćwiczeń Norskling z pliku JSON.

Użycie: python3 generuj_cwiczenia.py spec.json wynik.html

Spec: {"pill","title","title_hl","intro","meta":[...],"parts":[{"title","intro","text":{...}?,"tasks":[...]}]}
Typy zadań:
  choice : {"type":"choice","h","hint","options":[...],"correct","ok"}
  fill   : {"type":"fill","h","hint"?,"sentence":"... ___ ...","answers":[...],"ok"}
  rewrite: {"type":"rewrite","h","given","start","answers":[...],"full","ok"}
  match  : {"type":"match","h","hint","pairs":[[lewy,prawy],...],"ok"?}
Strona: noindex, tylko imię kursanta, styl z narzedzia/styl.css.
"""
import json, sys, html, os, random
D = os.path.dirname(os.path.abspath(__file__))
E = html.escape
def js(s): return E(json.dumps(s, ensure_ascii=False))
INP = 'autocomplete="off" autocapitalize="off" spellcheck="false"'

def task(n, t):
    o = [f'<section class="task" data-id="{n}">', f'<h2>{n}. {E(t["h"])}</h2>']
    if t.get("hint"): o.append(f'<p class="hint">{t["hint"]}</p>')
    k = t["type"]
    if k == "choice":
        o.append(f'<div class="opts" data-q="{n}" data-correct="{E(t["correct"])}" data-ok="{E(t["ok"])}">')
        o += [f'<button class="opt">{E(x)}</button>' for x in t["options"]]
        o.append('</div><div class="fb" id="f%d"></div>' % n)
    elif k in ("fill", "rewrite"):
        if k == "fill":
            a, b = t["sentence"].split("___")
            o.append(f'<div class="inline sent">{E(a)}<input type="text" id="t{n}" aria-label="Odpowiedź" {INP}>{E(b)}</div>')
            sol = t["answers"][0]
        else:
            o.append(f'<p class="given">{E(t["given"])}</p>')
            o.append(f'<div class="rw"><span>{E(t["start"])}</span><input type="text" id="t{n}" aria-label="Dokończ zdanie" {INP}></div>')
            sol = t["full"]
        o.append(f'<div class="row"><button class="btn" onclick="checkText({n},{js(t["answers"])},{js(t["ok"])})">Sprawdź</button>'
                 f'<button class="ghost" onclick="showSol({n})">Pokaż odpowiedź</button></div>')
        o.append(f'<div class="fb" id="f{n}"></div><div class="sol" id="s{n}">Wzorcowa odpowiedź: <b>{E(sol)}</b></div>')
    elif k == "match":
        rights = sorted(p[1] for p in t["pairs"])
        opts = '<option value="">wybierz…</option>' + "".join(f"<option>{E(r)}</option>" for r in rights)
        o.append('<div class="match">')
        key = {}
        for i, (l, r) in enumerate(t["pairs"]):
            o.append(f'<span class="w">{E(l)}</span><select id="m{n}_{i}">{opts}</select>')
            key[f"m{n}_{i}"] = r
        o.append('</div>')
        o.append(f'<button class="btn" onclick="checkMatch({n},{js(key)})">Sprawdź</button><div class="fb" id="f{n}"></div>')
    o.append('</section>')
    return "\n".join(o)

def main(spec_path, out):
    s = json.load(open(spec_path, encoding="utf-8"))
    style = open(os.path.join(D, "styl.css"), encoding="utf-8").read()
    script = open(os.path.join(D, "skrypt.js"), encoding="utf-8").read()
    body, n = [], 0
    for p in s["parts"]:
        body.append(f'<h2 class="part">{E(p["title"])}</h2>')
        if p.get("intro"): body.append(f'<p class="partintro">{E(p["intro"])}</p>')
        if p.get("text"):
            paras = "".join(f"<p>{E(x)}</p>" for x in p["text"]["paragraphs"])
            body.append(f'<div class="text"><h2>{E(p["text"]["title"])}</h2>{paras}</div>')
        for t in p["tasks"]:
            n += 1; body.append(task(n, t))
    script = script.replace("const TOTAL=60", f"const TOTAL={n}")
    meta = "".join(f"<span>{E(m)}</span>" for m in s.get("meta", []) + [f"{n} zadań"])
    page = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(s.get("doc_title","Ćwiczenia Norskling"))}</title>
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
  <div class="progress"><span>Twój wynik</span><b><span id="score">0</span> / {n}</b></div>
{chr(10).join(body)}
  <div class="done" id="done"><h2>Wszystko zrobione: {n} / {n}</h2><p>Pokaż ten wynik lektorce na następnej lekcji.</p></div>
</main>
{script}
</body>
</html>
'''
    open(out, "w", encoding="utf-8").write(page)
    print(out, n, "zadań")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
