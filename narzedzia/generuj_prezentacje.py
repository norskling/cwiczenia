#!/usr/bin/env python3
"""Generuje prezentację Norskling (.pptx) z pliku JSON. Potem plik wgrywa się na Drive z konwersją do Google Slides.

Użycie: python3 generuj_prezentacje.py spec.json wynik.pptx

Spec: {"label":"A2 · LEKCJA 2","slides":[...]}  Typy slajdów:
  tytul       {"type":"tytul","title","subtitle","note"?}
  plan        {"type":"plan","title","items":[...]}                          (I dag skal vi)
  tabela      {"type":"tabela","title","hl"?,"intro"?,"head":[...],"rows":[[...]],"widths"?:[...]}
  przyklady   {"type":"przyklady","title","hl"?,"items":[...],"note"?}       (zdania z życia kursanta)
  chipy       {"type":"chipy","title","items":[...],"note"?}                 (krótkie słowa/zwroty)
  zle_dobrze  {"type":"zle_dobrze","title","pairs":[["źle","dobrze"],...]}
  rozmowa     {"type":"rozmowa","title","hl"?,"qs":[...],"phrases"?:[...],"tip"?}
  podsumowanie{"type":"podsumowanie","title","items":[...]}
Zasada Moniki: po każdym slajdzie teorii (tabela, przyklady, chipy, zle_dobrze) musi wystąpić slajd rozmowy,
zanim pojawi się kolejny slajd teorii. Skrypt przerywa pracę, gdy zasada jest złamana.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from norskling_pptx import *  # noqa: F401,F403  (p, slide, box, text, table, talk, kolory)

THEORY = {"tabela", "przyklady", "chipy", "zle_dobrze"}


def check(slides):
    pending = None
    for i, s in enumerate(slides, 1):
        t = s["type"]
        if t in THEORY:
            if pending:
                sys.exit(f"Błąd: slajd {i} ({s.get('title')}) to teoria, a po slajdzie teorii {pending} nie było slajdu rozmowy.")
            pending = f"{i} ({s.get('title')})"
        elif t == "rozmowa":
            pending = None
    if pending:
        sys.exit(f"Błąd: po slajdzie teorii {pending} brakuje slajdu rozmowy.")


def build(spec):
    L = spec["label"]
    for s in spec["slides"]:
        t = s["type"]
        if t == "tytul":
            sl = p.slides.add_slide(blank); bg(sl)
            box(sl, 0, 0, 0.35, 7.5, fill=IS, line=None, rad=False)
            pill(sl, "NORSKLING · " + L, x=1.2, y=1.6)
            text(sl, 1.2, 2.4, 11, 1.4, s["title"], font="Space Grotesk", bold=True, color=NATT, size=54)
            box(sl, 1.25, 3.75, 1.2, 0.08, fill=IS, line=None, rad=False)
            text(sl, 1.2, 4.1, 11, 1.0, s.get("subtitle", ""), size=24, color=SKY)
            if s.get("note"): text(sl, 1.2, 6.2, 11, 0.5, s["note"], size=14, color=SKY)
        elif t == "plan":
            sl = slide(L, s["title"])
            for i, it in enumerate(s["items"]):
                y = 2.45 + i * 0.85
                box(sl, 0.8, y, 11.7, 0.7)
                text(sl, 1.05, y + 0.12, 0.6, 0.5, str(i + 1), font="Space Grotesk", bold=True, color=IS, size=22)
                text(sl, 1.7, y + 0.14, 10.5, 0.5, it, size=20, color=NATT, bold=True)
        elif t == "tabela":
            sl = slide(L, s["title"], s.get("hl"))
            y = 2.45
            if s.get("intro"):
                text(sl, 0.8, y, 11.7, 0.6, s["intro"], size=17); y += 0.7
            n = len(s["head"]); widths = s.get("widths") or [11.7 / n] * n
            rows = [s["head"]] + s["rows"]
            rh = min(0.55, (7.0 - y) / len(rows))
            table(sl, 0.8, y, widths, rows, size=16 if len(rows) > 7 else 18, rowh=rh)
        elif t == "przyklady":
            sl = slide(L, s["title"], s.get("hl"))
            n = len(s["items"]); step = min(0.85, 4.2 / max(n, 1))
            for i, it in enumerate(s["items"]):
                y = 2.45 + i * step
                box(sl, 0.8, y, 11.7, step - 0.12)
                text(sl, 1.1, y + (step - 0.12 - 0.5) / 2, 11.2, 0.5, it, size=20, color=NATT)
            if s.get("note"): text(sl, 0.8, 6.85, 11.7, 0.5, s["note"], size=15, color=FJORD, bold=True)
        elif t == "chipy":
            sl = slide(L, s["title"], s.get("hl"))
            cols = 4; w = 2.75
            for i, it in enumerate(s["items"]):
                r, c = divmod(i, cols)
                x, y = 0.8 + c * (w + 0.23), 2.45 + r * 0.95
                b = box(sl, x, y, w, 0.75, fill=TINT, line=BOR); b.adjustments[0] = 0.5
                text(sl, x, y + 0.14, w, 0.5, it, size=19, color=NATT, bold=True, align=PP_ALIGN.CENTER)
            if s.get("note"): text(sl, 0.8, 6.6, 11.7, 0.5, s["note"], size=17, color=FJORD, bold=True)
        elif t == "zle_dobrze":
            sl = slide(L, s["title"], s.get("hl"))
            text(sl, 0.8, 2.35, 5.7, 0.4, "ŹLE", size=13, bold=True, color=BAD)
            text(sl, 6.8, 2.35, 5.7, 0.4, "DOBRZE", size=13, bold=True, color=OK)
            for i, (bad, good) in enumerate(s["pairs"]):
                y = 2.8 + i * 0.85
                box(sl, 0.8, y, 5.7, 0.7); text(sl, 1.05, y + 0.12, 5.3, 0.5, bad, size=19, color=BAD)
                box(sl, 6.8, y, 5.7, 0.7); text(sl, 7.05, y + 0.12, 5.3, 0.5, good, size=19, color=OK, bold=True)
        elif t == "rozmowa":
            talk(L, s["title"], s.get("hl"), s["qs"], s.get("phrases"), s.get("tip"))
        elif t == "podsumowanie":
            sl = slide(L, s["title"])
            for i, it in enumerate(s["items"]):
                y = 2.45 + i * 0.85
                box(sl, 0.8, y, 11.7, 0.7)
                text(sl, 1.05, y + 0.14, 11.2, 0.5, [[("✓  ", {"color": OK, "bold": True}), (it, {"color": NATT})]], size=20)
        else:
            sys.exit(f"Nieznany typ slajdu: {t}")


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    check(spec["slides"])
    build(spec)
    p.save(sys.argv[2])
    print(f"{sys.argv[2]}: {len(spec['slides'])} slajdów")
