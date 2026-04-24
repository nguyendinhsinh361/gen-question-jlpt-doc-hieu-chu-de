# Rules: HTML Template, Clean HTML, CSV Schema & QC Automation (R9, R10, R11)

> **Scope**: Đọc hiểu chủ đề (主張理解 / thematic) — **CHỈ N1 & N2**.

## R9. HTML Template bắt buộc

### R9.1 Template skeleton

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Japanese title ngắn]</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: #f9fafb;
            color: #111827;
            line-height: 2.0;
            word-break: keep-all;
            line-break: strict;
            overflow-wrap: break-word;
            margin: 0;
            padding: 40px 20px;
        }
        .passage {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 56px 64px;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            font-size: 16px;
        }
        .passage p { margin: 0 0 1em 0; text-indent: 1em; }
        .passage .no-indent { text-indent: 0; }
        .ellipsis {
            text-align: center;
            font-size: 0.9em;
            color: #6b7280;
            margin: 0.8em 0;
            text-indent: 0;
        }
        .marker { font-weight: bold; color: #1e40af; }
        .annotations {
            margin-top: 2em;
            padding-top: 1em;
            border-top: 1px dashed #d1d5db;
            font-size: 0.9em;
            color: #374151;
            line-height: 1.7;
        }
        .annotations p { margin: 0.3em 0; text-indent: 0; }
        .source {
            margin-top: 1.2em;
            text-align: right;
            font-size: 0.88em;
            color: #4b5563;
            text-indent: 0;
        }
        ruby { ruby-align: center; ruby-position: over; vertical-align: baseline; }
        ruby rt { font-size: 0.55em; color: #374151; letter-spacing: 0.02em; line-height: 1; vertical-align: top; }
        u { text-decoration: underline; text-decoration-thickness: 1.5px; }
    </style>
</head>
<body>
<div class="passage">
    <p>[Para 1 — hook / topic introduction]</p>
    <p>[Para 2 — context / common view được tác giả phản biện]</p>
    <p>[Para 3 — introduce author's position với <span class="marker">①</span><u>key phrase</u>]</p>
    <p class="ellipsis">（中略）</p>
    <p>[Para 4 — further argument với <span class="marker">②</span><u>another key phrase</u>]</p>
    <p>[Para 5 — counter-argument addressed]</p>
    <p>[Para 6 — conclusion / thesis restated — Q3 author_opinion test ở đây, KHÔNG marker]</p>
    <div class="annotations">
        <p>注1　xxx ：yyy</p>
    </div>
    <p class="source">（[fake author]「[fake title]」による）</p>
</div>
</body>
</html>
```

### R9.2 Layout Rules

- **Container**: `max-width: 800px` — width cố định cho đọc hiểu chủ đề
- **Paragraph**: **6–10 paragraph cho N1, 5–8 cho N2** (essay logic chặt, mỗi `<p>` = 1 bước)
- **Markers ①②**: 1-2 marker cho câu reference (câu 1, câu 2). **KHÔNG marker ở câu cuối tổng kết**
- **Source line**: N1 rất nên (64% data), N2 optional (26% data)
- **Annotation 注**: N1 rất nên (60%), N2 nên (51%) — 1-2 chú thích
- **`(中略)` ellipsis**: optional — 1 lần per bài, giữa 2 đoạn logic chính

### R9.3 Fake Source Line (tuyệt đối KHÔNG dùng tên thật)

Format: `（[fake author]「[fake title]」による）` hoặc với media:
- `（[author]「[title]」○○新聞による）` (xã luận báo chí)
- `（[author]「[title]」による）` (tiểu luận độc lập)
- `（[author]「[title]」による。一部改変）` (có "一部改変")

**Rule:**
- Author: tên Nhật tự chế (2-4 chữ, họ + tên)
- Media fake: `朝○新聞`, `○○新聞`, `月刊○○`
- **KHÔNG** dùng tên tác giả / tên báo có thật

### R9.4 Data Pattern Percentage

| Pattern | N1 | N2 | Skill Rule |
|---------|----|----|------------|
| `<p>` | 100% | 100% | BẮT BUỘC |
| `<br>` | 28% | 31% | **KHÔNG dùng** |
| `<u>` underline | **88%** | 26% | Dùng cho cụm reference |
| `<span>` (ngoài marker) | 8% | 36% | **KHÔNG dùng** trừ `.marker` |
| `<ruby>` | 0% | 9% | Max 0-3 (N1) / 0-5 (N2) |
| 注 annotation | **60%** | 51% | Khuyến nghị 1-2 |
| marker ①②③ | **76%** | 48% | 1-2 (N1 rất nên) |
| source line | **64%** | 26% | N1 rất nên, N2 optional |
| `(中略)` | 28% | 19% | Optional, 1 lần/bài |
| blank `[ ]` | 8% | 4% | Hiếm, không khuyến khích |
| `<table>` | 0% | 4% | **KHÔNG dùng** |

---

## R10. Clean HTML Extraction

### R10.1 Quy tắc clean HTML

Clean HTML (lưu vào CSV column `text_read`) là body-only, attributes stripped, `<rt>` text removed, whitespace collapsed:

1. Chỉ giữ content trong `<body>`
2. Bỏ attributes của mọi tag (class, id, style) — chỉ `<tag>` thuần
3. Bỏ nội dung trong `<rt>`, `<style>`, `<script>`
4. Collapse whitespace
5. Bỏ empty tags `<tag></tag>`

Ví dụ output clean:
```
<div><p>言葉は単なる意思伝達の道具ではなく...</p><p><span>①</span><u>この柔軟性</u>こそが...</p><div><p>注1 決定論：原因によって結果が一意に定まるという考え方。</p></div><p>（山口和彦「言葉と思考の未来」による）</p></div>
```

### R10.2 count_body_chars() — Python reference

```python
from html.parser import HTMLParser
import re

class BodyTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts, self.skip_depth, self.in_body = [], 0, False

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        if tag in ('rt', 'style', 'script'):
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ('rt', 'style', 'script'):
            self.skip_depth -= 1

    def handle_data(self, d):
        if self.in_body and self.skip_depth == 0:
            self.texts.append(d)

def count_body_chars(html_string: str) -> int:
    ext = BodyTextExtractor()
    ext.feed(html_string)
    text = ''.join(ext.texts)
    return len(re.sub(r'[ \t\n\r\u3000]', '', text))
```

**Rules:**
- Count từ **full HTML file**, không từ clean version
- Skip `<rt>` (furigana), `<style>`, `<script>`
- Remove whitespace: space, tab, newline, full-width space (　)

Bundled script:
```bash
python3 <skill>/scripts/process_html.py --count-only --file <html-file>
```

---

## R11. CSV Schema — question_sheet.csv (45 cột)

### R11.1 Column layout

| Column | Value | Note |
|--------|-------|------|
| `_id` | `{LEVEL}_{uuid4().hex}` | vd `N1_a1b2c3d4...` |
| `level` | `N1` hoặc `N2` | **CHỈ 2 level** |
| `tag` | Topic tiếng Việt | từ `rules/topic.json` |
| `jp_char_count` | `count_body_chars()` | str |
| `kind` | `"đọc hiểu chủ đề"` | fixed |
| `general_audio` | `""` | luôn empty |
| `general_image` | `""` | luôn empty |
| `text_read` | Clean HTML | từ `process_html.py` |
| `text_read_vn` | `""` | luôn empty |
| `text_read_en` | `""` | luôn empty |
| `question_label_1..3` | 7 labels với prefix `question_` | populate đủ 3 câu |
| `question_1..3` | Câu hỏi tiếng Nhật | populate đủ 3 câu |
| `question_image_1..3` | `""` | luôn empty |
| `answer_1..3` | 4 options `\n` separated, KHÔNG prefix | populate đủ |
| `correct_answer_1..3` | `"1"` / `"2"` / `"3"` / `"4"` | 1-based |
| `explain_vn_1..3` / `explain_en_1..3` | 3-part format | populate đủ |
| `question_4..5` (+ label, image, answer, correct, explain) | `""` | **KHÔNG populate** (chỉ 3 câu) |

### R11.2 Per-level population

| Level | Q Count | Fill cols | Empty cols |
|-------|---------|-----------|-----------|
| **N1** | 3 | `question_label_1..3` + related | `question_label_4..5` + related = "" |
| **N2** | 3 | `question_label_1..3` + related | `question_label_4..5` + related = "" |

### R11.3 Câu cuối label check (BẮT BUỘC)

```python
TAIL_LABELS_OK = {"question_author_opinion", "question_content_match"}

def last_label_ok(level: str, questions: list[dict]) -> bool:
    if not questions:
        return False
    return questions[-1].get("label") in TAIL_LABELS_OK
```

Nếu câu cuối label không thuộc `TAIL_LABELS_OK` → **REJECT**, gen lại Q3.

### R11.4 Label diversity rule

Trong 1 row, ≥ 2 label phải khác nhau (tính cả 3 câu):

```python
labels = [row[f"question_label_{i}"] for i in range(1, 4) if row[f"question_label_{i}"]]
assert len(set(labels)) >= 2, "Phải có ≥ 2 labels khác nhau trong 3 câu"
```

---

## QC Automation Scripts

### check_html()

```python
def check_html(level: str, full_html: str) -> list[str]:
    """Return list of errors. Empty = pass."""
    errs = []
    chars = count_body_chars(full_html)

    # Char range
    target = {"N1": (1000, 1200), "N2": (900, 1100)}
    hard_reject = {"N1": 950, "N2": 850}
    if level not in target:
        errs.append(f"Level {level} không thuộc scope đọc hiểu chủ đề (chỉ N1/N2).")
    else:
        lo, hi = target[level]
        if chars < hard_reject[level]:
            errs.append(f"HARD_REJECT: {chars} chars < {hard_reject[level]}")
        elif chars < lo:
            errs.append(f"UNDER_TARGET: {chars} chars (target {lo}-{hi})")
        elif chars > hi + 100:
            errs.append(f"OVER_TARGET: {chars} chars (target {lo}-{hi})")

    # Forbidden patterns
    if "<br>" in full_html.replace("<br/>", "").replace("<br />", ""):
        errs.append("Phát hiện <br> — không được dùng, chuyển sang <p> thuần.")
    if "<table" in full_html:
        errs.append("Phát hiện <table> — đọc hiểu chủ đề không dùng table.")
    if "朝日新聞" in full_html or "読売新聞" in full_html or "毎日新聞" in full_html or "日経新聞" in full_html:
        errs.append("Dùng tên báo có thật — thay bằng tên fake.")

    # Ellipsis count
    ellipsis_count = full_html.count("（中略）") + full_html.count("(中略)")
    if ellipsis_count > 1:
        errs.append(f"'(中略)' xuất hiện {ellipsis_count} lần — tối đa 1 lần/bài.")

    return errs
```

### check_csv_row()

```python
def check_csv_row(row: dict) -> list[str]:
    errs = []
    level = row.get("level", "")
    if level not in {"N1", "N2"}:
        errs.append(f"Level {level!r} ngoài scope (chỉ N1/N2).")
    if row.get("kind", "") != "đọc hiểu chủ đề":
        errs.append(f"kind phải là 'đọc hiểu chủ đề', đang là {row.get('kind')!r}.")
    if row.get("general_image") or row.get("general_audio"):
        errs.append("general_image / general_audio phải empty.")

    # Q1-3 populate
    labels = []
    for i in range(1, 4):
        label = row.get(f"question_label_{i}", "")
        if not label:
            errs.append(f"Q{i}: thiếu label.")
            continue
        if not label.startswith("question_"):
            errs.append(f"Q{i}: label {label!r} thiếu prefix 'question_'.")
        labels.append(label)
        # answer format
        ans = row.get(f"answer_{i}", "")
        opts = ans.split("\n") if ans else []
        if len(opts) != 4:
            errs.append(f"Q{i}: answer phải có 4 options \\n-separated (hiện {len(opts)}).")
        for opt in opts:
            if opt.strip() and opt.strip()[:2] in {"1.", "2.", "3.", "4.", "1)", "2)"}:
                errs.append(f"Q{i}: option có prefix — rules/questions.md R6.1 cấm.")
                break

    # Q4-5 empty
    for i in range(4, 6):
        if row.get(f"question_label_{i}") or row.get(f"question_{i}"):
            errs.append(f"Q{i}: phải empty (đọc hiểu chủ đề chỉ 3 câu).")

    # Label diversity
    if len(labels) >= 2 and len(set(labels)) < 2:
        errs.append(f"Các câu cùng label — cần ≥ 2 labels khác nhau.")

    # Tail label rule
    TAIL_OK = {"question_author_opinion", "question_content_match"}
    if len(labels) == 3 and labels[-1] not in TAIL_OK:
        errs.append(f"Câu cuối label={labels[-1]!r} — phải thuộc {sorted(TAIL_OK)}.")

    return errs
```

### Smoke test trước khi commit batch

```bash
# Count + validate chars
python3 <skill>/scripts/process_html.py --validate --html-dir assets/html/doc_hieu_chu_de

# Fill QA cho 1 row
python3 <skill>/scripts/fill_qa.py --csv sheets/samples_v1.csv --row-id N1_xxx --level N1 \
    --q1-label question_reference --q1 "..." --a1 "..." --ca1 2 --evn1 "..." --een1 "..." \
    --q2-label question_reason_explanation --q2 "..." --a2 "..." --ca2 3 --evn2 "..." --een2 "..." \
    --q3-label question_author_opinion --q3 "..." --a3 "..." --ca3 1 --evn3 "..." --een3 "..."
```
