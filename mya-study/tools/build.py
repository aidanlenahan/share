"""Build mya-study/index.html from the practice-problem markdown and flashcard files.

Usage:  python tools/build.py            (run from anywhere; paths are relative to mya-study/)

Each group needs a practice file (`**N.** stem`, four `- A.`..`- D.` options, then
`## Answer Key` with `**N. X.** explanation`) and a Quizlet flashcard file
(`term\\wd\\definition\\ww\\...`). Reference-dropdown content lives in tools/ref.json.
"""
import json, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

SUBJECTS = [("chem", "Chemistry"), ("psych", "Psychology")]
GROUPS = [
    # subject, slug, tab name, practice file, flashcard file, Quizlet URL
    ("chem", "7-8", "Lectures 7–8", "chem/Lectures_7-8_Practice_Problems.md", "chem/flashcards/Lectures_7-8_Flashcards.txt",
     "https://quizlet.com/1167794903/mya-chem-lectures-7-8-flash-cards/"),
    ("chem", "9-10", "Lectures 9–10", "chem/Lectures_9-10_Practice_Problems.md", "chem/flashcards/Lectures_9-10_Flashcards.txt",
     "https://quizlet.com/1226874419/mya-chem-lectures-9-10-flash-cards/"),
    ("chem", "11", "Lecture 11", "chem/Lecture_11_Practice_Problems.md", "chem/flashcards/Lecture_11_Flashcards.txt",
     "https://quizlet.com/1226999150/mya-chem-lecture-11-flash-cards/"),
    ("chem", "ch12", "Chapter 12", "chem/Chapter_12_Practice_Problems.md", "chem/flashcards/Chapter_12_Flashcards.txt",
     "https://quizlet.com/1227000035/mya-chem-chapter-12-flash-cards/"),
    ("chem", "ch13", "Chapter 13", "chem/Chapter_13_Practice_Problems.md", "chem/flashcards/Chapter_13_Flashcards.txt",
     "https://quizlet.com/1227000552/mya-chem-chapter-13-flash-cards/"),
    ("chem", "8-9", "Lectures 8–9", "chem/Lectures_8-9_Practice_Problems.md", "chem/flashcards/Lectures_8-9_Flashcards.txt",
     "https://quizlet.com/1227360162/mya-chem-lectures-8-9-flash-cards"),
    ("psych", "psych-3-5", "Chapters 3–5", "psych/Psych_Ch3-5_Practice_Exam.md", "psych/flashcards/Psych_Ch3-5_Flashcards.txt",
     "https://quizlet.com/1230928513/"),
]

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s

def block(lines):
    """Render a small markdown fragment: paragraphs, bullet lists, tables."""
    out, i = [], 0
    lines = [l.rstrip() for l in lines]
    while i < len(lines):
        l = lines[i]
        if not l.strip() or l.strip() == "---":
            i += 1; continue
        if l.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            t = "<table>"
            for r, row in enumerate(rows):
                tag = "th" if r == 0 else "td"
                t += "<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>"
            out.append(t + "</table>"); continue
        if re.match(r"\s*[-*] ", l):
            items = []
            while i < len(lines) and re.match(r"\s*[-*] ", lines[i]):
                items.append(inline(re.sub(r"^\s*[-*] ", "", lines[i]))); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"); continue
        if l.startswith("#"):
            out.append(f"<p class='sub'>{inline(l.lstrip('#').strip())}</p>"); i += 1; continue
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("|", "- ", "* ", "#")):
            para.append(lines[i].strip()); i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "".join(out)

QSTART = re.compile(r"^\*\*(\d+)\.\*\*\s*(.*)$")
OPT = re.compile(r"^\s*[-*]?\s*\(?([A-D])[.)]\s+(.*)$")
ANS = re.compile(r"^\*\*(\d+)\.\s*\(?([A-D])\)?[.:]?\*\*\s*(.*)$")

def parse(path):
    text = path.read_text(encoding="utf-8").splitlines()
    k = next(i for i, l in enumerate(text) if re.match(r"^#+\s*Answer Key", l))
    body, key = text[:k], text[k + 1:]
    sections, cur, q = [], None, None
    for l in body[1:]:
        m = QSTART.match(l)
        if l.startswith("## "):
            cur = {"title": l[3:].strip(), "qs": []}; sections.append(cur); q = None; continue
        if m:
            if cur is None:
                cur = {"title": "", "qs": []}; sections.append(cur)
            q = {"n": int(m.group(1)), "stem": [m.group(2)], "opts": {}}; cur["qs"].append(q); continue
        if q is None:
            continue
        om = OPT.match(l)
        if om:
            q["opts"][om.group(1)] = om.group(2).strip(); continue
        if not q["opts"]:
            q["stem"].append(l)
    answers, last = {}, None
    for l in key:
        m = ANS.match(l)
        if m:
            last = int(m.group(1)); answers[last] = [m.group(2), [m.group(3)]]
        elif last and l.strip() and not l.startswith("#"):
            answers[last][1].append(l)
    out, seen = [], set()
    for s in sections:
        m = re.search(r"\b(Chapter|Lecture)\s+(\d+)", s["title"])
        tag = (("Ch " if m.group(1) == "Chapter" else "L ") + m.group(2)) if m else ""
        qs = []
        for q in s["qs"]:
            assert set(q["opts"]) == set("ABCD"), (path.name, q["n"], sorted(q["opts"]))
            assert q["n"] not in seen, (path.name, "duplicate number", q["n"]); seen.add(q["n"])
            a, exp = answers[q["n"]]
            qs.append({"n": q["n"], "stem": block(q["stem"]),
                       "opts": [[L, inline(q["opts"][L])] for L in "ABCD"],
                       "ans": a, "exp": block(exp), "tag": tag})
        if qs: out.append({"title": s["title"], "qs": qs})
    assert set(answers) == seen, (path.name, "answer key mismatch", sorted(set(answers) ^ seen))
    if len({q["tag"] for sec in out for q in sec["qs"]}) < 2:
        for sec in out:
            for q in sec["qs"]: q["tag"] = ""
    return out

def main():
    ref = json.loads((TOOLS / "ref.json").read_text(encoding="utf-8"))
    data = []
    for subject, slug, name, exam, cards, quizlet in GROUPS:
        if not (ROOT / exam).exists() or not (ROOT / cards).exists():
            print(f"SKIP {slug}: missing {exam if not (ROOT / exam).exists() else cards}"); continue
        secs = parse(ROOT / exam)
        n = sum(len(s["qs"]) for s in secs)
        card_text = (ROOT / cards).read_text(encoding="utf-8")
        ncards = len(card_text.split("\\ww\\"))
        assert card_text.count("\\wd\\") == ncards, (cards, "separator mismatch")
        r = ref.get(slug, {})
        data.append({"subject": subject, "slug": slug, "name": name, "title": r.get("subtitle", ""),
                     "intro": r.get("ref_html", ""), "sections": secs, "count": n, "cards": ncards, "quizlet": quizlet})
        print(f"{subject:6} {slug:10} {n:3} questions {ncards:4} cards")
    present = {g["subject"] for g in data}
    payload = {"subjects": [{"id": i, "name": nm} for i, nm in SUBJECTS if i in present], "groups": data}
    tpl = (TOOLS / "template.html").read_text(encoding="utf-8")
    assert tpl.count("/*__DATA__*/null") == 1
    (ROOT / "index.html").write_text(
        tpl.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    print("wrote index.html")

if __name__ == "__main__":
    main()
