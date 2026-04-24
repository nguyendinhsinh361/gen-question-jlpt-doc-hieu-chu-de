#!/usr/bin/env python3
"""
process_html.py — Pipeline for JLPT "đọc hiểu chủ đề" (thematic / 主張理解) HTML files.

Does three things — NO screenshot:
  1. Count visible body characters (JLPT standard)
  2. Extract clean HTML (no attributes / no <rt> text / collapsed whitespace)
  3. Append / update rows in the 45-column question_sheet.csv
     — populates 3 câu hỏi (cả N1 và N2)

This skill applies only to N1 and N2. Other levels are rejected với UNSUPPORTED_LEVEL.

Usage
-----
# Count chars only
python3 process_html.py --count-only --file assets/html/doc_hieu_chu_de/N1_abcdef.html

# Validate Target Range
python3 process_html.py --validate --html-dir assets/html/doc_hieu_chu_de

# Full pipeline — RECOMMENDED: JSON file cho 3 questions
python3 process_html.py \
    --file assets/html/doc_hieu_chu_de/N1_abcdef.html \
    --csv sheets/samples_v1.csv \
    --tag "xã luận công nghệ" \
    --questions-json /tmp/qs.json

# Full pipeline — CLI flags (3 câu per bài)
python3 process_html.py \
    --file assets/html/doc_hieu_chu_de/N1_abcdef.html \
    --csv sheets/samples_v1.csv \
    --tag "xã luận công nghệ" \
    --q1-label question_reference --q1 "..." --a1 "A|B|C|D" --c1 2 --ev1 "..." --ee1 "..." \
    --q2-label question_reason_explanation --q2 "..." --a2 "A|B|C|D" --c2 3 --ev2 "..." --ee2 "..." \
    --q3-label question_author_opinion --q3 "..." --a3 "A|B|C|D" --c3 1 --ev3 "..." --ee3 "..."

# Refresh char count + text_read (giữ câu hỏi)
python3 process_html.py --refresh --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv

Questions JSON format
---------------------
{
  "questions": [
    {
      "label": "question_reference",
      "question": "①「この傾向の根底」とあるが、何を指すか。",
      "answers": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
      "correct": 2,
      "explain_vn": "...",
      "explain_en": "..."
    },
    { ... 2 more — last one MUST be author_opinion/content_match ... }
  ]
}
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# ── Constants ───────────────────────────────────────────────────────

KIND = "đọc hiểu chủ đề"

# Target ranges (P25–P75 của data mẫu + spec chính thức).
# Chỉ N1 & N2 — N3/N4/N5 không có kind này.
TARGET_RANGE = {
    "N1": (1000, 1200),
    "N2": (900, 1100),
}
HARD_REJECT = {
    "N1": 950,
    "N2": 850,
}
# Số câu hỏi chuẩn per level (từ rules/question_format.json)
EXPECTED_Q_COUNT = {
    "N1": 3,
    "N2": 3,
}

# Labels được chấp nhận cho câu cuối (thesis/overall)
TAIL_LABELS_OK = {"question_author_opinion", "question_content_match"}

CSV_FIELDNAMES = [
    "_id", "level", "tag", "jp_char_count", "kind", "general_audio", "general_image",
    "text_read", "text_read_vn", "text_read_en",
    "question_label_1", "question_1", "question_image_1", "answer_1", "correct_answer_1", "explain_vn_1", "explain_en_1",
    "question_label_2", "question_2", "question_image_2", "answer_2", "correct_answer_2", "explain_vn_2", "explain_en_2",
    "question_label_3", "question_3", "question_image_3", "answer_3", "correct_answer_3", "explain_vn_3", "explain_en_3",
    "question_label_4", "question_4", "question_image_4", "answer_4", "correct_answer_4", "explain_vn_4", "explain_en_4",
    "question_label_5", "question_5", "question_image_5", "answer_5", "correct_answer_5", "explain_vn_5", "explain_en_5",
]

FILENAME_RE = re.compile(r"^(N[1-5])_([0-9a-fA-F]{8,})$")


# ── Character Counting ──────────────────────────────────────────────

class BodyTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts: list[str] = []
        self.skip_depth = 0
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        if tag in ("rt", "style", "script"):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("rt", "style", "script"):
            self.skip_depth -= 1

    def handle_data(self, d):
        if self.in_body and self.skip_depth == 0:
            self.texts.append(d)


def count_body_chars(html_string: str) -> int:
    ext = BodyTextExtractor()
    ext.feed(html_string)
    text = "".join(ext.texts)
    return len(re.sub(r"[ \t\n\r\u3000]", "", text))


# ── Clean HTML Extraction ───────────────────────────────────────────

class CleanHTMLExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result: list[str] = []
        self.skip_depth = 0
        self.in_body = False
        self.body_done = False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
            return
        if not self.in_body or self.body_done:
            return
        if tag in ("style", "script", "rt"):
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return
        self.result.append(f"<{tag}>")

    def handle_startendtag(self, tag, attrs):
        if not self.in_body or self.body_done or self.skip_depth > 0:
            return
        if tag in ("style", "script", "rt"):
            return
        self.result.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag == "body":
            self.body_done = True
            return
        if not self.in_body or self.body_done:
            return
        if tag in ("style", "script", "rt"):
            self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return
        self.result.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.in_body or self.body_done or self.skip_depth > 0:
            return
        self.result.append(data)


def clean_html(full_html: str) -> str:
    ext = CleanHTMLExtractor()
    ext.feed(full_html)
    raw = "".join(ext.result)
    raw = re.sub(r"\s+", " ", raw)
    raw = re.sub(r"\s*<", "<", raw)
    raw = re.sub(r">\s*", ">", raw)
    raw = re.sub(r"<(\w+)></\1>", "", raw)
    return raw.strip()


# ── Filename / ID helpers ───────────────────────────────────────────

def parse_filename(path: str) -> tuple[str | None, str]:
    stem = Path(path).stem
    m = FILENAME_RE.match(stem)
    if m:
        return m.group(1).upper(), stem
    return None, stem


# ── Validation ──────────────────────────────────────────────────────

def classify_char_count(level: str | None, chars: int) -> str:
    if level not in TARGET_RANGE:
        # N3/N4/N5 không có đọc hiểu chủ đề
        return "UNSUPPORTED_LEVEL"
    lo, hi = TARGET_RANGE[level]
    hard = HARD_REJECT[level]
    if chars < hard:
        return "HARD_REJECT"
    if chars < lo:
        return "UNDER_TARGET"
    if chars > hi + 100:
        return "OVER_TARGET"
    return "OK"


def validate_file(html_path: str) -> dict:
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    level, name = parse_filename(html_path)
    chars = count_body_chars(html)
    status = classify_char_count(level, chars)
    target = TARGET_RANGE.get(level) if level else None
    return {
        "file": html_path,
        "name": name,
        "level": level,
        "chars": chars,
        "target": target,
        "status": status,
    }


# ── Question helpers ────────────────────────────────────────────────

def format_answers(answers: list[str]) -> str:
    # R6.1: 4 options newline-separated, KHÔNG prefix ("1.", "①", ...)
    return "\n".join(a.strip() for a in answers)


def parse_answers_pipe(pipe_string: str) -> list[str]:
    return [s.strip() for s in pipe_string.split("|")]


def validate_question_list(level: str | None, questions: list[dict]) -> list[str]:
    """Return list of warnings. Non-empty = có vấn đề."""
    warnings = []
    expected = EXPECTED_Q_COUNT.get(level, None)
    actual = len(questions)
    if level not in EXPECTED_Q_COUNT:
        warnings.append(f"Level {level} không thuộc scope đọc hiểu chủ đề (chỉ N1/N2).")
    elif actual != expected:
        warnings.append(f"Số câu hỏi là {actual}, nhưng level {level} yêu cầu {expected}.")
    for i, q in enumerate(questions, 1):
        if not q.get("question"):
            warnings.append(f"Q{i}: thiếu `question`")
        if not q.get("label"):
            warnings.append(f"Q{i}: thiếu `label`")
        ans = q.get("answers", [])
        if len(ans) != 4:
            warnings.append(f"Q{i}: phải có đúng 4 đáp án (hiện {len(ans)})")
        correct = q.get("correct")
        if not (isinstance(correct, int) and 1 <= correct <= 4):
            warnings.append(f"Q{i}: `correct` phải là int 1-4 (hiện {correct!r})")
        if not q.get("explain_vn"):
            warnings.append(f"Q{i}: thiếu `explain_vn`")
        if not q.get("explain_en"):
            warnings.append(f"Q{i}: thiếu `explain_en`")
    labels = [q.get("label") for q in questions]
    if len(questions) >= 2 and len(set(labels)) < 2:
        warnings.append(f"Tất cả {len(questions)} câu cùng label={labels[0]} — cần ≥ 2 labels khác nhau.")
    # Check câu cuối là author_opinion/content_match
    if actual == expected and expected and labels:
        tail = labels[-1]
        if tail not in TAIL_LABELS_OK:
            warnings.append(
                f"Câu cuối (Q{actual}) có label={tail!r} — đọc hiểu chủ đề yêu cầu câu cuối "
                f"là {sorted(TAIL_LABELS_OK)} (tổng thể / thesis)."
            )
    return warnings


# ── CSV Operations ──────────────────────────────────────────────────

def empty_row() -> dict:
    return {field: "" for field in CSV_FIELDNAMES}


def build_csv_row(
    html_path: str,
    *,
    tag: str = "",
    questions: list[dict] = None,
) -> tuple[dict, list[str]]:
    """Build row + return (row, warnings)."""
    with open(html_path, "r", encoding="utf-8") as f:
        full_html = f.read()
    level, name = parse_filename(html_path)
    if level is None:
        raise ValueError(
            f"Filename '{Path(html_path).name}' không đúng format {{LEVEL}}_{{uuid32hex}}.html"
        )
    char_count = count_body_chars(full_html)
    cleaned = clean_html(full_html)

    row = empty_row()
    row.update({
        "_id": name,
        "level": level,
        "tag": tag,
        "jp_char_count": str(char_count),
        "kind": KIND,
        "general_audio": "",
        "general_image": "",
        "text_read": cleaned,
        "text_read_vn": "",
        "text_read_en": "",
    })

    questions = questions or []
    warnings = validate_question_list(level, questions) if questions else []

    for i, q in enumerate(questions, 1):
        if i > 5:
            warnings.append(f"Bỏ qua Q{i}: CSV chỉ hỗ trợ tối đa 5 câu.")
            break
        row[f"question_label_{i}"] = q.get("label", "")
        row[f"question_{i}"] = q.get("question", "")
        row[f"question_image_{i}"] = ""
        ans = q.get("answers", []) or []
        row[f"answer_{i}"] = format_answers(ans) if ans else ""
        correct = q.get("correct", "")
        row[f"correct_answer_{i}"] = str(correct) if correct != "" else ""
        row[f"explain_vn_{i}"] = q.get("explain_vn", "")
        row[f"explain_en_{i}"] = q.get("explain_en", "")

    return row, warnings


def load_csv(csv_path: str) -> list[dict]:
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(csv_path: str, rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDNAMES})


def upsert_row(existing: list[dict], new_row: dict) -> list[dict]:
    key = new_row.get("_id", "")
    for i, row in enumerate(existing):
        if row.get("_id", "") == key and key:
            existing[i] = new_row
            return existing
    existing.append(new_row)
    return existing


def refresh_row(existing_row: dict, html_path: str) -> dict:
    with open(html_path, "r", encoding="utf-8") as f:
        full_html = f.read()
    chars = count_body_chars(full_html)
    cleaned = clean_html(full_html)
    existing_row["jp_char_count"] = str(chars)
    existing_row["kind"] = KIND
    existing_row["text_read"] = cleaned
    existing_row["general_image"] = ""
    return existing_row


# ── Question collection (CLI flags → questions list) ────────────────

def collect_questions_from_cli(args) -> list[dict]:
    """Extract questions from --q1/--q1-label/--a1/--c1/--ev1/--ee1 flags (up to q5)."""
    questions = []
    for i in range(1, 6):
        q_text = getattr(args, f"q{i}", None)
        q_label = getattr(args, f"q{i}_label", None)
        if not q_text and not q_label:
            continue
        ans_pipe = getattr(args, f"a{i}", "") or ""
        correct = getattr(args, f"c{i}", None)
        ev = getattr(args, f"ev{i}", "") or ""
        ee = getattr(args, f"ee{i}", "") or ""
        questions.append({
            "label": q_label or "",
            "question": q_text or "",
            "answers": parse_answers_pipe(ans_pipe) if ans_pipe else [],
            "correct": int(correct) if correct is not None else None,
            "explain_vn": ev,
            "explain_en": ee,
        })
    return questions


def load_questions_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    qs = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(qs, list):
        raise ValueError(f"Invalid questions JSON: {path} — expected list or {{\"questions\": [...]}}")
    return qs


# ── CLI modes ───────────────────────────────────────────────────────

def cmd_count(files: list[str]) -> int:
    print(f"Counting {len(files)} file(s)...\n")
    any_hard_reject = False
    for f in files:
        info = validate_file(f)
        marker = ""
        status = info["status"]
        if status == "HARD_REJECT":
            marker = "  🚫 HARD REJECT"
            any_hard_reject = True
        elif status == "UNDER_TARGET":
            marker = "  ⚠️  UNDER TARGET"
        elif status == "OVER_TARGET":
            marker = "  ⚠️  OVER TARGET"
        elif status == "UNSUPPORTED_LEVEL":
            marker = "  ❌ UNSUPPORTED (chỉ N1/N2)"
        tgt = f"target {info['target'][0]}-{info['target'][1]}" if info["target"] else ""
        print(f"  {info['name']}: {info['chars']} chars [{info['level']}] {tgt}{marker}")
    return 1 if any_hard_reject else 0


def cmd_validate(files: list[str]) -> int:
    print(f"Validating {len(files)} file(s)...\n")
    fails = 0
    for f in files:
        info = validate_file(f)
        ok = info["status"] == "OK"
        status = info["status"]
        if status == "HARD_REJECT":
            badge = "🚫"
        elif status == "UNSUPPORTED_LEVEL":
            badge = "❌"
        elif not ok:
            badge = "⚠️ "
        else:
            badge = "✅"
        tgt = f"target {info['target'][0]}-{info['target'][1]}" if info["target"] else "target ?"
        print(f"  {badge} {info['name']}: {info['chars']} chars [{info['level']}] {tgt} — {status}")
        if not ok:
            fails += 1
    print(f"\n{len(files) - fails}/{len(files)} files OK.")
    return 1 if fails else 0


def cmd_refresh(files: list[str], csv_path: str) -> None:
    rows = load_csv(csv_path)
    by_id = {r.get("_id", ""): r for r in rows}
    updated, added = 0, 0
    for f in files:
        level, name = parse_filename(f)
        if level is None:
            print(f"  [skip] {Path(f).name} — filename không hợp lệ")
            continue
        if name in by_id:
            refresh_row(by_id[name], f)
            updated += 1
        else:
            row, _ = build_csv_row(f)
            rows.append(row)
            added += 1
    write_csv(csv_path, rows)
    print(f"Refreshed {updated} existing row(s), added {added} new row(s) → {csv_path}")


def cmd_single_full(args) -> None:
    questions = []
    if args.questions_json:
        questions = load_questions_json(args.questions_json)
    else:
        questions = collect_questions_from_cli(args)

    if not questions:
        print("⚠️  Không có question nào (cần --questions-json hoặc --q1/--q2/...).", file=sys.stderr)
        sys.exit(2)

    row, warnings = build_csv_row(args.file, tag=args.tag or "", questions=questions)

    level = row["level"]
    chars = int(row["jp_char_count"])
    status = classify_char_count(level, chars)

    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")

    if status == "UNSUPPORTED_LEVEL":
        print(f"❌ {row['_id']}: level {level} không thuộc đọc hiểu chủ đề (chỉ N1/N2). Không commit.")
        sys.exit(1)
    if status == "HARD_REJECT":
        print(f"🚫 {row['_id']}: {chars} chars — dưới Hard Reject ({HARD_REJECT[level]}). GEN LẠI, không commit CSV.")
        sys.exit(1)
    if status == "UNDER_TARGET":
        print(f"⚠️  {row['_id']}: {chars} chars — dưới Target Range {TARGET_RANGE[level]}. Cân nhắc bổ sung.")

    rows = load_csv(args.csv)
    rows = upsert_row(rows, row)
    write_csv(args.csv, rows)
    expected_q = EXPECTED_Q_COUNT.get(level, "?")
    print(f"✅ Upserted {row['_id']} ({chars} chars, {level}, {len(questions)} câu — expected {expected_q}) → {args.csv}")


def collect_files(args) -> list[str]:
    if args.file:
        return [args.file]
    if args.html_dir:
        return sorted(
            os.path.join(args.html_dir, f)
            for f in os.listdir(args.html_dir)
            if f.endswith(".html")
        )
    print("Provide --file or --html-dir", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser(
        description="Process JLPT 'đọc hiểu chủ đề' HTML files (no screenshot, 3 questions, N1+N2 only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", help="Single HTML file")
    ap.add_argument("--html-dir", help="Directory with HTML files")
    ap.add_argument("--csv", default="sheets/samples_v1.csv", help="CSV file path")

    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--count-only", action="store_true")
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--refresh", action="store_true")

    ap.add_argument("--tag", help="Topic tag")
    ap.add_argument("--questions-json", help="Path to JSON file with questions array")

    for i in range(1, 6):
        ap.add_argument(f"--q{i}-label", dest=f"q{i}_label",
                        help=f"question_label_{i}")
        ap.add_argument(f"--q{i}", dest=f"q{i}",
                        help=f"Câu hỏi {i} tiếng Nhật")
        ap.add_argument(f"--a{i}", dest=f"a{i}",
                        help=f"Answer {i}: 4 đáp án ngăn cách |")
        ap.add_argument(f"--c{i}", dest=f"c{i}", type=int,
                        help=f"Correct {i}: 1-4")
        ap.add_argument(f"--ev{i}", dest=f"ev{i}",
                        help=f"Explain VN {i}")
        ap.add_argument(f"--ee{i}", dest=f"ee{i}",
                        help=f"Explain EN {i}")

    args = ap.parse_args()
    files = collect_files(args)

    if args.count_only:
        sys.exit(cmd_count(files))
    if args.validate:
        sys.exit(cmd_validate(files))
    if args.refresh:
        cmd_refresh(files, args.csv)
        return

    if args.file and (args.questions_json or any(getattr(args, f"q{i}", None) for i in range(1, 6))):
        cmd_single_full(args)
        return

    if args.html_dir and not args.file:
        print("⚠️  Chạy --html-dir mà không có mode. Mặc định count.\n")
        sys.exit(cmd_count(files))
    sys.exit(cmd_count(files))


if __name__ == "__main__":
    main()
