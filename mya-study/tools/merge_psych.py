"""Merge the per-chapter psych parts into one flashcard set and one practice exam.

Reads  psych/parts/ch{3,4,5}_cards.txt and ch{3,4,5}_exam.md
Writes psych/flashcards/Psych_Ch3-5_Flashcards.txt  (terms tagged "(Ch N)")
       psych/Psych_Ch3-5_Practice_Exam.md          (sections prefixed "Chapter N ·")
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PSYCH = ROOT / "psych"
WW, WD = "\\ww\\", "\\wd\\"
CHAPTERS = [3, 4, 5]

def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"\(.*?\)", "", t.lower())).strip()

def merge_cards():
    out, seen = [], {}
    for ch in CHAPTERS:
        text = (PSYCH / "parts" / f"ch{ch}_cards.txt").read_text(encoding="utf-8").strip()
        for card in text.split(WW):
            term, defn = card.split(WD)
            term, defn = term.strip(), defn.strip()
            assert term and defn and "\n" not in card, (ch, card[:60])
            key = norm(term)
            if key in seen:
                print(f"  duplicate term: '{term}' (Ch {ch}) also in Ch {seen[key]}")
            seen.setdefault(key, ch)
            out.append(f"{term} (Ch {ch}){WD}{defn}")
    dest = PSYCH / "flashcards" / "Psych_Ch3-5_Flashcards.txt"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(WW.join(out), encoding="utf-8")
    print(f"cards: {len(out)} -> {dest.relative_to(ROOT)}")

QSTART = re.compile(r"^\*\*(\d+)\.\*\*(.*)$")
ANS = re.compile(r"^\*\*(\d+)\.(\s*\(?[A-D]\)?[.:]?\*\*.*)$")

def merge_exam():
    body, key, offset, total = [], [], 0, 0
    for ch in CHAPTERS:
        lines = (PSYCH / "parts" / f"ch{ch}_exam.md").read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("#").strip()                      # e.g. "Chapter 3: Consciousness"
        k = next(i for i, l in enumerate(lines) if re.match(r"^#+\s*Answer Key", l))
        qs_part, key_part = lines[1:k], lines[k + 1:]
        nums = []
        started = False
        for l in qs_part:
            if l.startswith("## "):
                body.append(f"## Chapter {ch} · {l[3:].strip()}"); started = True; continue
            m = QSTART.match(l)
            if m:
                if not started:
                    body.append(f"## {title}"); started = True
                nums.append(int(m.group(1)))
                body.append(f"**{int(m.group(1)) + offset}.**{m.group(2)}"); continue
            if l.strip() == "---" or l.startswith("# "):
                continue
            if started:
                body.append(l)
        assert nums == list(range(1, len(nums) + 1)), (ch, "questions not numbered 1..N")
        knums = []
        for l in key_part:
            m = ANS.match(l)
            if m:
                knums.append(int(m.group(1)))
                key.append(f"**{int(m.group(1)) + offset}.{m.group(2)}"); continue
            if l.strip() and l.strip() != "---" and key:
                key.append(l)
        assert knums == nums, (ch, "answer key does not match questions")
        print(f"  Ch {ch}: {len(nums)} questions -> {offset + 1}..{offset + len(nums)}")
        offset += len(nums)
    text = ["# Psychology Practice Exam: Chapters 3–5", ""] + body + ["", "---", "", "## Answer Key", ""] + \
           [x for l in key for x in (l, "")]
    dest = PSYCH / "Psych_Ch3-5_Practice_Exam.md"
    dest.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8")
    print(f"exam: {offset} questions -> {dest.relative_to(ROOT)}")

if __name__ == "__main__":
    merge_cards()
    merge_exam()
