#!/usr/bin/env python3
"""
Fill Q&A data vào CSV một cách an toàn cho đọc hiểu chủ đề (multi-question 3 câu) —
tự động handle comma, newline, quoting. Agent BẮT BUỘC dùng script này, không edit
CSV bằng tay.

Đọc hiểu chủ đề (主張理解 / thematic) có 3 câu hỏi per bài (CHỈ N1 & N2):
    - N1: 3 câu  → populate question_{1,2,3}, empty question_{4,5}
          câu cuối PHẢI là `question_author_opinion` hoặc `question_content_match`
    - N2: 3 câu  → populate question_{1,2,3}, empty question_{4,5}
          câu cuối PHẢI là `question_author_opinion` hoặc `question_content_match`

Usage (ví dụ N1 — 3 câu):
    python3 fill_qa.py \\
        --csv sheets/samples_v1.csv \\
        --row-id N1_abc123 \\
        --level N1 \\
        --q1-label question_reference \\
        --q1 "「①このような現象」とあるが、何を指しているか。" \\
        --a1 "選択肢1
選択肢2
選択肢3
選択肢4" \\
        --ca1 2 \\
        --evn1 "..." \\
        --een1 "..." \\
        --q2-label question_reason_explanation \\
        --q2 "..." \\
        --a2 "A\\nB\\nC\\nD" \\
        --ca2 3 --evn2 "..." --een2 "..." \\
        --q3-label question_author_opinion \\
        --q3 "この文章で筆者が最も言いたいことはどれか。" \\
        --a3 "A\\nB\\nC\\nD" \\
        --ca3 1 --evn3 "..." --een3 "..."

question-label hợp lệ (7 loại — BẮT BUỘC question_ prefix):
    question_content_match, question_reason_explanation, question_reference,
    question_meaning_interpretation, question_content_mismatch, question_author_opinion,
    question_fill_in_the_blank
"""
import argparse
import csv
import os
import sys

CSV_FIELDNAMES = [
    "_id", "level", "tag", "jp_char_count", "kind", "general_audio", "general_image",
    "text_read", "text_read_vn", "text_read_en",
    "question_label_1", "question_1", "question_image_1", "answer_1", "correct_answer_1", "explain_vn_1", "explain_en_1",
    "question_label_2", "question_2", "question_image_2", "answer_2", "correct_answer_2", "explain_vn_2", "explain_en_2",
    "question_label_3", "question_3", "question_image_3", "answer_3", "correct_answer_3", "explain_vn_3", "explain_en_3",
    "question_label_4", "question_4", "question_image_4", "answer_4", "correct_answer_4", "explain_vn_4", "explain_en_4",
    "question_label_5", "question_5", "question_image_5", "answer_5", "correct_answer_5", "explain_vn_5", "explain_en_5",
]

VALID_LABELS = {
    "question_content_match",
    "question_reason_explanation",
    "question_reference",
    "question_meaning_interpretation",
    "question_content_mismatch",
    "question_author_opinion",
    "question_fill_in_the_blank",
}

# Đọc hiểu chủ đề CHỈ có N1 và N2 (spec JLPT không có N3/N4/N5)
EXPECTED_Q_COUNT = {
    "N1": 3,
    "N2": 3,
}

# Rule câu cuối theo level (spec JLPT — main idea / thesis test)
# Cả N1 và N2 spec focus "overall intended points and ideas" → câu cuối = thesis
LAST_LABEL_RULES = {
    "N1": {"question_author_opinion", "question_content_match"},
    "N2": {"question_author_opinion", "question_content_match"},
}


def validate_answer_string(raw: str, slot_idx: int) -> str:
    """Validate 4 options, no prefix, return cleaned '\\n'-joined string."""
    opts = [x.strip() for x in raw.strip().split("\n") if x.strip()]
    if len(opts) != 4:
        print(
            f"❌ answer_{slot_idx} phải có đúng 4 lựa chọn (thấy {len(opts)}).\n"
            f"   Options: {opts}",
            file=sys.stderr,
        )
        sys.exit(1)
    for i, opt in enumerate(opts, 1):
        # Chặn prefix kiểu "1. ", "1)", "①", "1、"
        if (
            opt[:2].strip() in ("1.", "2.", "3.", "4.", "1)", "2)", "3)", "4)")
            or opt[:1] in ("①", "②", "③", "④")
            or (len(opt) >= 2 and opt[0] in "1234" and opt[1] in "．、)")
        ):
            print(
                f"❌ answer_{slot_idx} option {i} chứa prefix ('{opt[:2]}'). "
                f"Bỏ prefix đi, chỉ ghi nội dung thuần.",
                file=sys.stderr,
            )
            sys.exit(1)
    return "\n".join(opts)


def add_question_args(parser: argparse.ArgumentParser, idx: int, required: bool) -> None:
    grp = parser.add_argument_group(f"Question {idx} ({'required' if required else 'optional'})")
    grp.add_argument(
        f"--q{idx}-label",
        dest=f"q{idx}_label",
        help=f"question_label_{idx} (1 trong {sorted(VALID_LABELS)})",
    )
    grp.add_argument(f"--q{idx}", dest=f"q{idx}", help=f"Câu hỏi {idx} tiếng Nhật")
    grp.add_argument(
        f"--a{idx}",
        dest=f"a{idx}",
        help=f"answer_{idx}: 4 đáp án newline-separated, KHÔNG prefix",
    )
    grp.add_argument(f"--ca{idx}", dest=f"ca{idx}", help=f"correct_answer_{idx} (1-4)")
    grp.add_argument(
        f"--evn{idx}",
        dest=f"evn{idx}",
        help=f"Explanation VN {idx} (3-part format)",
    )
    grp.add_argument(
        f"--een{idx}",
        dest=f"een{idx}",
        help=f"Explanation EN {idx} (3-part format)",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fill Q&A data vào CSV đọc hiểu chủ đề (3 questions per bài, N1/N2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--csv", required=True, help="Đường dẫn file CSV (vd sheets/samples_v1.csv)")
    parser.add_argument("--row-id", required=True, help="_id của row cần update")
    parser.add_argument(
        "--level",
        required=True,
        choices=sorted(EXPECTED_Q_COUNT.keys()),
        help="N1|N2 — đọc hiểu chủ đề CHỈ có 2 level này (không N3/N4/N5)",
    )
    # Q1-Q5 all optional at argparse level; we validate theo level sau
    for i in range(1, 6):
        add_question_args(parser, i, required=False)
    args = parser.parse_args()

    level = args.level
    expected = EXPECTED_Q_COUNT[level]

    # Validate CSV exists
    csv_path = args.csv
    if not os.path.exists(csv_path):
        print(f"❌ CSV không tồn tại: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # Read CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Find row
    target = None
    for row in rows:
        if row.get("_id") == args.row_id:
            target = row
            break
    if target is None:
        print(
            f"❌ Row _id={args.row_id} không tìm thấy trong {csv_path}\n"
            f"   Hãy chạy process_html.py để tạo row trước.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Collect provided questions
    provided = []
    for i in range(1, 6):
        q_text = getattr(args, f"q{i}", None)
        q_label = getattr(args, f"q{i}_label", None)
        a_raw = getattr(args, f"a{i}", None)
        ca = getattr(args, f"ca{i}", None)
        evn = getattr(args, f"evn{i}", None)
        een = getattr(args, f"een{i}", None)
        has_any = any(x is not None for x in (q_text, q_label, a_raw, ca, evn, een))
        if has_any:
            # Check tất cả field bắt buộc của slot này
            missing = []
            if not q_label: missing.append(f"--q{i}-label")
            if not q_text: missing.append(f"--q{i}")
            if not a_raw: missing.append(f"--a{i}")
            if not ca: missing.append(f"--ca{i}")
            if not evn: missing.append(f"--evn{i}")
            if not een: missing.append(f"--een{i}")
            if missing:
                print(
                    f"❌ Q{i} có một số flag nhưng thiếu: {missing}. "
                    f"Một slot phải đủ 6 flag hoặc không có gì cả.",
                    file=sys.stderr,
                )
                sys.exit(1)
            provided.append(i)

    # Validate số câu hỏi = expected cho level
    if len(provided) != expected:
        print(
            f"❌ Level {level} cần đúng {expected} câu hỏi, provided {len(provided)} (slots: {provided}).\n"
            f"   Đọc hiểu chủ đề N1/N2 đều 3 câu (--q1..--q3).",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate slot liên tiếp từ 1 (không được provide q1 + q3 mà skip q2)
    if provided != list(range(1, expected + 1)):
        print(
            f"❌ Phải provide slots liên tiếp từ 1. Got {provided}, expected {list(range(1, expected + 1))}.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate labels
    labels = [getattr(args, f"q{i}_label") for i in provided]
    for i, lbl in zip(provided, labels):
        if lbl not in VALID_LABELS:
            print(
                f"❌ --q{i}-label='{lbl}' không hợp lệ.\n"
                f"   Các label hợp lệ: {sorted(VALID_LABELS)}",
                file=sys.stderr,
            )
            sys.exit(1)

    # Validate label diversity (≥ 2 unique)
    unique = set(labels)
    if len(unique) < 2:
        print(
            f"❌ Tất cả {expected} câu dùng cùng label={labels[0]} — cần ≥ 2 labels khác nhau.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate câu cuối theo spec level (thesis test)
    last_label = labels[-1]
    if last_label not in LAST_LABEL_RULES[level]:
        allowed = sorted(LAST_LABEL_RULES[level])
        print(
            f"❌ Câu cuối (Q{expected}) label='{last_label}' không hợp lệ cho level {level}.\n"
            f"   Level {level} câu cuối PHẢI là: {allowed}\n"
            f"   Lý do: Spec JLPT đọc hiểu chủ đề test 'overall intended points and ideas'.\n"
            f"          Câu cuối BẮT BUỘC test THESIS TỔNG THỂ (author_opinion / content_match).\n"
            f"          CẤM câu cuối = reference/reason/meaning (test cục bộ 1 đoạn).",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate correct_answer mỗi câu
    for i in provided:
        ca = getattr(args, f"ca{i}")
        if ca not in ("1", "2", "3", "4"):
            print(f"❌ --ca{i} phải là 1-4 (thấy '{ca}')", file=sys.stderr)
            sys.exit(1)

    # Validate + clean answer per slot
    cleaned_answers = {}
    for i in provided:
        a_raw = getattr(args, f"a{i}")
        cleaned_answers[i] = validate_answer_string(a_raw, i)

    # Fill fields cho slots được provide
    for i in provided:
        target[f"question_label_{i}"] = getattr(args, f"q{i}_label")
        target[f"question_{i}"] = getattr(args, f"q{i}")
        target[f"question_image_{i}"] = ""
        target[f"answer_{i}"] = cleaned_answers[i]
        target[f"correct_answer_{i}"] = getattr(args, f"ca{i}")
        target[f"explain_vn_{i}"] = getattr(args, f"evn{i}")
        target[f"explain_en_{i}"] = getattr(args, f"een{i}")

    # Clear các slot còn lại
    for i in range(expected + 1, 6):
        for fld in (
            f"question_label_{i}",
            f"question_{i}",
            f"question_image_{i}",
            f"answer_{i}",
            f"correct_answer_{i}",
            f"explain_vn_{i}",
            f"explain_en_{i}",
        ):
            target[fld] = ""

    # Đảm bảo general_image luôn rỗng (đọc hiểu chủ đề không có screenshot)
    target["general_image"] = ""

    # Write back
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDNAMES})

    # Summary
    print(f"✅ Đã fill {expected} câu hỏi cho {args.row_id} ({level}) trong {csv_path}")
    for i in provided:
        lbl = getattr(args, f"q{i}_label")
        q = getattr(args, f"q{i}")
        ca = getattr(args, f"ca{i}")
        opts = cleaned_answers[i].split("\n")
        print(f"  Q{i} [{lbl}]: {q[:60]}{'...' if len(q) > 60 else ''}")
        for j, opt in enumerate(opts, 1):
            marker = "  ✓" if str(j) == ca else ""
            print(f"     ({j}) {opt[:50]}{'...' if len(opt) > 50 else ''}{marker}")
        print(f"     correct_answer_{i}: {ca}")
    print(f"  Last label: {labels[-1]} (OK for {level})")


if __name__ == "__main__":
    main()
