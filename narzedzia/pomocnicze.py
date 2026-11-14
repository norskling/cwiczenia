#!/usr/bin/env python3
"""Pomocnicze komendy rutyny.

  python3 pomocnicze.py slug
      Wypisuje nowy losowy 10-znakowy slug, którego nie ma jeszcze w c/.

  python3 pomocnicze.py dokument spec.json wynik.html
      Buduje HTML dokumentu na Drive („Lekcja M: materiały na lekcję” albo „Lekcja N: słownictwo i zadania”).
      Wynik wgrywa się przez create_file z textContent, contentMimeType text/html (konwersja do Google Docs).
      Spec: {"title","note"?,"sections":[
               {"h":"…","links":[{"label","url","desc"}]}      lista linków
             | {"h":"…","table":{"head":[…],"rows":[[…]]}}     tabela słownictwa
             | {"h":"…","steps":["tekst z <a href>…</a>", …]}  lista numerowana (zadanie domowe)
             | {"h":"…","p":"tekst"} ]}
"""
import json, sys, os, random, string, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape


def slug():
    used = {f[:-5] for f in os.listdir(os.path.join(ROOT, "c")) if f.endswith(".html")}
    while True:
        s = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        if s not in used:
            return s


def dokument(spec):
    o = [f'<html><head><meta charset="utf-8"><title>{E(spec["title"])}</title></head>'
         '<body style="font-family:Arial,sans-serif">', f'<h1>{E(spec["title"])}</h1>']
    if spec.get("note"):
        o.append(f'<p><i>{E(spec["note"])}</i></p>')
    for s in spec["sections"]:
        if s.get("h"):
            o.append(f'<h2>{E(s["h"])}</h2>')
        if "links" in s:
            o.append("<ul>" + "".join(
                f'<li>{E(l["label"])}: <a href="{E(l["url"])}">{E(l.get("name", l["label"]))}</a>'
                f'{(" (" + E(l["desc"]) + ")") if l.get("desc") else ""}</li>' for l in s["links"]) + "</ul>")
        if "table" in s:
            t = s["table"]
            cell = 'style="border:1px solid #E2EDF2;padding:6px 10px"'
            o.append('<table style="border-collapse:collapse">')
            o.append("<tr>" + "".join(f'<th {cell} bgcolor="#EAF7FB">{E(h)}</th>' for h in t["head"]) + "</tr>")
            o += ["<tr>" + "".join(f"<td {cell}>{E(c)}</td>" for c in r) + "</tr>" for r in t["rows"]]
            o.append("</table>")
        if "steps" in s:
            o.append("<ol>" + "".join(f"<li>{x}</li>" for x in s["steps"]) + "</ol>")
        if "p" in s:
            o.append(f'<p>{E(s["p"])}</p>')
    o.append("</body></html>")
    return "\n".join(o)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "slug":
        print(slug())
    elif cmd == "dokument":
        open(sys.argv[3], "w", encoding="utf-8").write(dokument(json.load(open(sys.argv[2], encoding="utf-8"))))
        print(sys.argv[3])
    else:
        sys.exit(__doc__)
