---
name: jlpt-doc-hieu-chu-de
description: >
  Generate JLPT "đọc hiểu chủ đề" (thematic comprehension / 主張理解) reading comprehension
  passages as styled HTML files and output CSV training data for AI fine-tuning. Each
  passage is an abstract/logical Japanese essay of 900–1200 characters — typically an
  editorial, critique, or philosophical essay — testing grasp of the author's overall
  thesis and main arguments via 3 multiple-choice questions per passage.
  **CHỈ áp dụng N1 (3 câu, ~1000-1200 chars) và N2 (3 câu, ~900-1100 chars)** —
  N3/N4/N5 KHÔNG có dạng này.
  Skill này bao gồm TOÀN BỘ luồng: gen → QC loop (checklist PASS/FAIL) → sửa. Gen từng bài
  một, kiểm tra đến khi đạt chất lượng mới chuyển sang bài tiếp theo. Output chỉ gồm HTML +
  CSV (không có screenshot PNG).
  Skill này chỉ dành riêng cho dạng "đọc hiểu chủ đề" (主張理解).
  Use this skill whenever the user wants to: gen bài đọc hiểu chủ đề, tạo nội dung
  thematic comprehension, generate JLPT 主張理解 passages, produce AI fine-tuning data
  for the "đọc hiểu chủ đề" section of JLPT N1 or N2, kiểm tra chất lượng, quality check,
  review bài, QC.
  Also trigger when the user mentions: gen bài đọc hiểu chủ đề, tạo thematic passage,
  generate JLPT 主張理解 / thematic reading, editorial essay N1/N2.
---

# JLPT 主張理解 / Đọc Hiểu Chủ Đề — Workflow

> **🔒 NGUYÊN TẮC CỐT LÕI — ZERO-TOLERANCE (BẮT BUỘC):**
> 1. **Gen từng bài một** — không batch rồi QC sau
> 2. **Agent tự QC** — đọc lại bài + câu hỏi, tự đánh giá từng mục, log PASS/FAIL
> 3. **🚨 1 FAIL = CHƯA XONG** — sửa → QC lại TỪ ĐẦU → lặp đến khi ALL PASS. **TUYỆT ĐỐI CẤM:**
>    - Skip mục FAIL hoặc mark "tạm thời để đó"
>    - Tự ý sang bài tiếp khi còn ≥ 1 FAIL ở bài hiện tại
>    - Ghi PASS mà không thực sự đọc lại nội dung và verify
>    - "Hợp lý hoá" lỗi (vd "char count chỉ vượt 5 ký tự thì OK") — nếu rule nói FAIL thì là FAIL
> 4. **🔒 5 GATE bắt buộc** giữa các BƯỚC (0→1, 1→2, 2→3, 3→4, 4→5) — KHÔNG qua gate = KHÔNG được sang bước tiếp. Mỗi gate phải log explicit "GATE X→Y PASSED" trước khi tiếp tục.


## Cấu trúc file

| File | Nội dung | Đọc khi |
|------|----------|---------|
| `SKILL.md` (file này) | Workflow + QC Checklist | Luôn đọc đầu tiên |
| `rules/content.md` | R1 chủ đề N1/N2 + R2 layout/char counts/Q count/paragraph count + R7 formats + R8 visual (marker, `<u>`, 注, source, `(中略)`) | Gen HTML |
| `rules/vocabulary.md` | R3 từ vựng/ngữ pháp + R4 furigana (N1/N2) | Gen HTML + QC |
| `rules/questions.md` | R5 câu hỏi 3 câu + R6 đáp án/6 bẫy + TAIL RULE + coverage | Gen Q&A + QC |
| `rules/technical.md` | R9 HTML template 800px + R10 clean HTML + R11 CSV schema | Gen HTML + CSV |
| `references/html-patterns.md` | Template chi tiết per level + marker strategy 3 patterns | Tra cứu khi gen HTML |
| `references/sample-analysis.md` | Phân tích định lượng data mẫu N1/N2 | Hiểu tần suất pattern |
| `scripts/process_html.py` | Xử lý HTML → CSV + count + validate + 3-question support | Gen CSV + QC |
| `scripts/fill_qa.py` | Điền Q&A vào CSV (quote an toàn, 3 câu, tail label rule) | Sau khi gen Q&A |
| `scripts/load_references.py` | Load sample JSON để calibrate | BƯỚC 0 chuẩn bị |

## Outputs Per Passage

1. **Styled HTML** → `assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html`
2. **Clean HTML** → CSV column `text_read` (no attributes, no `<rt>` content)
3. **CSV row** → `sheets/samples_v1.csv` với 3 câu hỏi populate (question_4, question_5 + related cols empty)

**KHÔNG có screenshot PNG.** CSV column `general_image` luôn `""`.

## Scope — CHỈ N1 và N2

| Level | Có "đọc hiểu chủ đề"? | Q Count | Char Range | Focus spec |
|-------|-----------------------|---------|------------|------------|
| **N1** | ✅ có | **3** | **1000–1200** | overall intended points and ideas |
| **N2** | ✅ có | **3** | **900–1100** | overall intended points and ideas |
| N3    | ❌ KHÔNG có           | —       | —          | — |
| N4    | ❌ KHÔNG có           | —       | —          | — |
| N5    | ❌ KHÔNG có           | —       | —          | — |

> **⛔ KHÔNG gen N3, N4, N5 cho dạng đọc hiểu chủ đề** — sẽ bị reject bởi spec.

## Số câu hỏi per level (BẮT BUỘC)

| Level | Q Count | Slots populate | Slots empty | Câu cuối cần |
|-------|---------|----------------|-------------|--------------|
| **N1** | 3       | `question_{1,2,3}` | `question_{4,5}` | **`question_author_opinion`** (ưu tiên) hoặc **`question_content_match`** |
| **N2** | 3       | `question_{1,2,3}` | `question_{4,5}` | **`question_author_opinion`** (ưu tiên) hoặc **`question_content_match`** |

> **⛔ COVERAGE RULE**: 3 câu hỏi trong 1 bài PHẢI test 3 đoạn/ý KHÁC NHAU. Q1/Q2 test 2 đoạn cụ thể, Q3 test thesis tổng thể.
> **⛔ LABEL DIVERSITY**: ≥ 2 label khác nhau trong 1 bài.
> **⛔ CÂU CUỐI RULE**: Cả N1 và N2 — câu 3 = `question_author_opinion` hoặc `question_content_match`. Câu cuối KHÔNG test 1 đoạn riêng lẻ, KHÔNG có marker.

---

# WORKFLOW

## BƯỚC 0: CHUẨN BỊ (1 lần cho batch)

1. **Đọc `rules/rule_doc_hieu.md`** — **Bộ Tiêu Chí Đánh Giá Đọc Hiểu JLPT toàn diện** từ giáo viên (source-of-truth, 11 phần: 4 tiêu chí, 程度 ±, 書き下ろし/による, ①② 下線 注 (中略), **文体の統一 (thể chia)**, furigana per level, 8 loại câu hỏi, **7 loại bẫy** (5 chuẩn + Single-side cho 統合理解 + Peripheral Source cho N1 khi 注 dài), tiêu chí chi tiết per level).
   **Phần áp dụng trực tiếp cho dạng đọc hiểu chủ đề (主張理解 / 長文)** — CHỈ N1 và N2:
   - Phần 1 (Tổng quan & Nguyên tắc 程度) — biên ± per level; có thể trích nguồn thực + ghi `（著者名「タイトル」による）`; (中略) cho phép
   - Phần 2 (Hình thức) — ①② thường có, 注 bắt buộc
   - **Phần 2.4 (Thể chia nhất quán 文体の統一)** — N1/N2 dùng **普通形** (だ・である). Văn bản editorial + câu hỏi + 4 đáp án phải **thống nhất thể** — toàn bộ 普通形 cho dạng 主張理解.
   - Phần 3 (Furigana) — bảng quy tắc per level
   - Phần 4 (8 loại câu hỏi) — đặc biệt **author_opinion** (BẮT BUỘC câu cuối), reference, reason_explanation, fill_in_the_blank, meaning_interpretation (N1)
   - Phần 5 (7 loại bẫy = 5 chuẩn + Single-side + Peripheral Source) — đặc biệt Reversal/Scope/Mixing/Misinterpretation cho câu thesis
   - **Phần 9.4 (N2 主張理解 ~900字, 3 câu)**, **Phần 10.5 (N1 主張理解 ~1000字, 3 câu)** — tiêu chí chi tiết 4 chiều; cấu trúc 前提→論拠→例示→反論処理→主張
   - Phần 11 (Bảng so sánh tổng hợp) — tra cứu nhanh.
2. **Đọc rules skill**: `rules/content.md` + `rules/vocabulary.md` + `rules/technical.md` + `rules/questions.md`
3. **Đọc `rules/kanji_jlpt_sensei.csv`** — dùng để tra level từng kanji khi quyết định furigana
4. **Scan `sheets/samples_v1.csv` và `data/doc_hieu_chu_de_n{1,2}_clean.json`** — xem format, topic đã dùng → chọn format chưa/ít dùng
5. **Load 2-3 sample calibrate style**:
   ```bash
   python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --level N1 --count 2
   python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --level N2 --count 2
   ```
6. **Lập kế hoạch batch**: mỗi bài gán format + topic + combo question_label khác nhau theo distribution của level. Topic chọn **tiếng Anh** từ cột `en` của `rules/topic.json` (đa dạng ≥ 2 category trong batch > 3 bài).

---

### 🔒 GATE 0→1 — KHÔNG QUA = KHÔNG ĐƯỢC GEN

Trước khi bắt đầu BƯỚC 1, agent PHẢI confirm bằng cách tick từng item:

- [ ] Đã đọc `rules/rule_doc_hieu.md` (đặc biệt Phần 1, 2, **2.4 thể chia**, 3, 4, 5, các phần per-level applicable, 11)
- [ ] Đã đọc đủ 4 file: `rules/content.md` + `rules/vocabulary.md` + `rules/technical.md` + `rules/questions.md`
- [ ] Đã đọc `rules/kanji_jlpt_sensei.csv` (sẵn sàng tra furigana)
- [ ] Đã chạy `load_references.py --level {LEVEL} --count 2` và đọc samples
- [ ] Đã scan `sheets/samples_v1.csv` để biết topic + label đã dùng
- [ ] Đã có kế hoạch batch (format + topic + label per bài)

❌ **Bất kỳ item nào CHƯA tick → quay lại BƯỚC 0**, KHÔNG được gen.
✅ Khi 6/6 tick → log `GATE 0→1 PASSED — ready to gen` rồi sang BƯỚC 1.

---

## BƯỚC 1→5: LẶP CHO TỪNG BÀI

### BƯỚC 1: GEN HTML + CÁC CÂU HỎI

> Đọc: `rules/content.md` + `rules/vocabulary.md` + `rules/technical.md` + `rules/questions.md`
> Tham khảo: `references/html-patterns.md` cho template per level + 3 marker strategy patterns

1. **Gen `_id`** = `{LEVEL}_{uuid.uuid4().hex}` (full 32-char hex). Level ∈ {N1, N2}.
2. **Chọn format** từ R7 (`rules/content.md`) — 4 formats: xã luận cao cấp / tiểu luận triết học (N1), xã luận trung cấp / tiểu luận cá nhân (N2).
3. **Chọn `tag`** (topic) — **tiếng Anh** từ cột `en` của `rules/topic.json`, đa dạng trong batch
4. **Chọn combo `question_label`** theo level (R5):
   - **N1** (3 câu): Combo 1 `reference(①) + reason + author_opinion` (phổ biến nhất)
   - **N1** khác: Combo 2 `meaning(①) + reason + author_opinion` | Combo 3 `reference(①) + reference(②) + author_opinion` | Combo 4 `reference(①) + reason + content_match`
   - **N2** (3 câu): Combo 1 `reference(①) + reason + author_opinion` (phổ biến nhất)
   - **N2** khác: Combo 2/3/4 — xem `rules/questions.md` R5
   - **Câu cuối**: Cả 2 level — `question_author_opinion` (ưu tiên) hoặc `question_content_match`
5. **Plan thesis + 2-3 supporting arguments** — viết trước trong đầu: thesis là gì, 2-3 supporting points, counter-argument nếu có
6. **Gen HTML** theo rules → save `assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html`
   - Container `max-width: 800px; margin: 0 auto; padding: 56px 64px; line-height: 2.0`
   - `word-break: keep-all` (đảm bảo xuống dòng sạch ở ranh giới từ)
   - `<p>` thuần, KHÔNG `<br>` giữa câu (đọc hiểu chủ đề KHÔNG có exception)
   - **Paragraph count**: N1 = 6-10, N2 = 5-8 (mỗi `<p>` = 1 bước logic)
   - Marker ①② chỉ cho câu 1/2 reference/meaning; **câu cuối KHÔNG marker**
   - Furigana chỉ cho từ vượt level (tra `rules/kanji_jlpt_sensei.csv`) — data 0-9% nên giữ ít
   - **Source line**: N1 rất nên có (data 64%), N2 optional (data 26%)
   - **Annotation 注**: N1 rất nên có (data 60%, 1-2 cái), N2 nên có (51%, 1-2 cái)
   - **`(中略)` ellipsis**: optional, 1 lần/bài, giữa 2 đoạn logic chính (data N1=28%, N2=19%)
7. **Gen 3 câu hỏi + 4 đáp án mỗi câu** theo `rules/questions.md`:
   - 4 options ngăn cách `\n`, KHÔNG số thứ tự `1.`, `①`, `1)`
   - `correct_answer_i` = integer 1-4
   - Mỗi distractor PHẢI dùng info/ý THẬT từ bài (1 trong 6 loại bẫy: Reversal/Detail swap/Scope/Misinterpretation/Part of truth/Mixing)
   - Paraphrase: đáp án đúng KHÔNG copy > 4 từ (N1) hoặc > 5 từ (N2) liên tiếp
   - Giải thích `explain_vn_i` + `explain_en_i` theo format 3 phần
   - **Câu 3 BẮT BUỘC** là `question_author_opinion` hoặc `question_content_match` (thesis tổng thể)
8. **Tạo CSV row** bằng `process_html.py` hoặc `fill_qa.py` (⚠️ **dùng script, KHÔNG sửa CSV tay**):
   ```bash
   # Recommended cho 3 câu: JSON
   python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
     --file assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html \
     --csv sheets/samples_v1.csv \
     --tag "{topic_vn}" \
     --questions-json /tmp/qs.json
   ```
   Hoặc dùng `fill_qa.py` với flags per-question:
   > **⛔ KHÔNG ĐƯỢC sửa CSV bằng tay. Commas + newlines trong nội dung (`100,000円`, `A\nB\nC\nD`) sẽ làm vỡ cột.**
   ```bash
   # Ví dụ N1 (3 câu)
   python3 .claude/skills/jlpt-reading-thematic/scripts/fill_qa.py \
     --csv sheets/samples_v1.csv --row-id {LEVEL}_{uuid} --level N1 \
     --q1-label question_reference --q1 "..." --a1 "A\nB\nC\nD" --ca1 2 --evn1 "..." --een1 "..." \
     --q2-label question_reason_explanation --q2 "..." --a2 "A\nB\nC\nD" --ca2 3 --evn2 "..." --een2 "..." \
     --q3-label question_author_opinion --q3 "..." --a3 "A\nB\nC\nD" --ca3 1 --evn3 "..." --een3 "..."
   ```

---

### 🔒 GATE 1→2 — KHÔNG QUA = KHÔNG ĐƯỢC QC

Trước khi sang BƯỚC 2 (QC), agent PHẢI confirm:

- [ ] File HTML đã save vào `assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html` (verify file tồn tại)
- [ ] CSV row đã tạo bằng `process_html.py` (KHÔNG sửa CSV tay)
- [ ] `_id` đúng format `{LEVEL}_{uuid32}` (không tạm thời, không placeholder)
- [ ] Tất cả Q + 4 đáp án + correct_answer + explain_vn + explain_en đã fill (không "TODO", không empty)
- [ ] Đã đọc lại file HTML vừa gen (mở file, đọc content) — KHÔNG dựa vào "tôi nhớ tôi đã gen"

❌ Bất kỳ item nào CHƯA confirm → quay lại BƯỚC 1 fix, KHÔNG được QC.
✅ Khi 5/5 tick → log `GATE 1→2 PASSED — ready to QC` rồi sang BƯỚC 2.

---

### BƯỚC 2: ⛔ QC — AGENT TỰ ĐÁNH GIÁ CHECKLIST

> **ĐÂY LÀ BƯỚC QUAN TRỌNG NHẤT. KHÔNG ĐƯỢC BỎ QUA.**
>
> Agent phải **đọc lại** file HTML vừa gen + **TOÀN BỘ** câu hỏi/đáp án trong CSV,
> rồi **tự đánh giá từng mục** bên dưới. Log kết quả theo format:
>
> ```
> QC: {_id}  |  Level: N1  |  Q count: 3/3  |  Labels: [reference, reason, author_opinion]
> ────────────────────────────────
> [ 1] ✅ PASS — Char count (1087 chars, range 1000-1200)
> [ 2] ❌ FAIL — Flow text (found 2x 。<br>)
> [ 3] ✅ PASS — Container CSS (800px, margin auto)
> ...
> ────────────────────────────────
> ⚠️ 1 FAIL → sửa rồi QC lại
> ```
>
> **⛔ KHÔNG ĐƯỢC tự PASS mà không đọc lại nội dung. Phải confirm từng mục cho TẤT CẢ câu hỏi.**

---

### 🔒 GATE 2→3 — KHÔNG QUA = KHÔNG ĐƯỢC ĐÁNH GIÁ CHECKLIST

Trước khi vào BƯỚC 3 (đánh giá 33 mục checklist), agent PHẢI cam kết:

- [ ] **TÔI SẼ kiểm tra ĐẦY ĐỦ 33 mục** — không skip, không "tạm bỏ qua", không "mục này hiển nhiên PASS"
- [ ] **TÔI SẼ đọc lại HTML + CSV thực tế** trước khi tick mục — KHÔNG dựa vào "tôi đoán/nhớ"
- [ ] **TÔI SẼ log explicit PASS/FAIL** cho từng mục với evidence (số ký tự, dòng nội dung, trích dẫn)
- [ ] **TÔI SẼ KHÔNG markup hàng loạt PASS** — phải đánh giá độc lập từng mục
- [ ] **TÔI SẼ đặc biệt cẩn thận** mục self-solve (BẮT BUỘC giải lại bài từ đầu, không nhìn correct_answer)

❌ Bất kỳ cam kết nào CHƯA tick → quay lại BƯỚC 2 (đọc lại checklist instructions).
✅ Khi 5/5 tick → log `GATE 2→3 PASSED — bắt đầu đánh giá 33 mục checklist`.

---

### BƯỚC 3: ⛔ CHECKLIST — TẤT CẢ PHẢI PASS

> **Quy tắc: 1 FAIL = chưa xong. Sửa → QC lại từ đầu → lặp đến khi ALL PASS.**
> **Tổng: 33 checks ở 4 phần (A HTML 12, B content 6, C questions/answers + C2 verify 11, D multi-question coverage 4).**

#### PHẦN A: HTML (12 checks)

Agent đọc lại file HTML và kiểm tra:

| # | Check | Cách verify | PASS nếu |
|---|-------|-------------|----------|
| 1 | **Scope level** | Đọc filename `{LEVEL}_...` | Level ∈ {N1, N2}. **N3/N4/N5 = FAIL ngay, không apply** |
| 2 | **Char count** | Chạy `process_html.py --count-only --file ...` | Trong Target Range: N1 1000-1200, N2 900-1100 |
| 3 | **Không Hard Reject** | So với Hard Reject threshold | ≥ N1:950, N2:850 |
| 4 | **Flow text** | Tìm `。<br>` trong HTML | Không có `。<br>` nào (đọc hiểu chủ đề KHÔNG có exception) |
| 5 | **Container CSS** | Xem CSS | `max-width: 800px`, `margin: 0 auto`, `padding: 56px 64px`, `line-height: 2.0`, `word-break: keep-all` |
| 6 | **`.passage` div** | Xem HTML structure | Có `<div class="passage">` bọc nội dung |
| 7 | **White background** | Xem CSS | `.passage` có `background: white`, body `#f9fafb` |
| 8 | **Paragraph count** | Đếm `<p>` trong `.passage` | N1: 6-10 đoạn. N2: 5-8 đoạn |
| 9 | **Furigana format** | Tìm ngoặc `漢字(かんじ)` hoặc `漢字【かんじ】` | Không có — tất cả furigana dùng `<ruby><rt>` |
| 10 | **Ruby có `<rt>` không rỗng** | Xem mọi `<ruby>...</ruby>` | Tất cả đều có `<rt>` chứa furigana **không rỗng** (vd `<ruby>媒体<rt>ばいたい</rt></ruby>`). CẤM `<ruby>媒体</ruby>` (thiếu rt) hoặc `<ruby>媒体<rt></rt></ruby>` (rt rỗng). Auto-check: `process_html.py --validate` |
| 11 | **Ruby count + Visual đúng level** | Đếm `<ruby>` + xem marker/annotation/source | Ruby: N1 ≤ 5, N2 ≤ 8. Visual phù hợp: N1 source nên có (64%) + 注 nên có (60%), N2 注 nên có (51%), marker khớp câu reference |
| 12 | **`(中略)` tối đa 1 lần** | Đếm `(中略)` + `（中略）` trong HTML | Không quá 1 lần per bài; nếu có, phải ở giữa bài (không đầu/cuối) |

#### PHẦN B: NỘI DUNG & TỪ VỰNG (6 checks)

| # | Check | Cách verify | PASS nếu |
|----|-------|-------------|----------|
| 13 | **Chủ đề đúng level** | Đọc nội dung, đối chiếu R1 | N1: xã luận cao cấp/tiểu luận triết học. N2: xã luận trung cấp/tiểu luận cá nhân có luận điểm |
| 14 | **Format editorial/critique (KHÔNG kể chuyện)** | Đọc toàn bài | Bài là editorial/critique có thesis + chuỗi lập luận; KHÔNG phải tùy bút kể chuyện thuần |
| 15 | **Thesis rõ ràng** | Đọc toàn bài | Có thể tóm tắt thesis trong 1-2 câu; thesis xuất hiện rõ ít nhất 1 chỗ (mở đầu, giữa, hoặc cuối) |
| 16 | **Không mơ hồ (test 2 cách hiểu)** | Đọc từng câu, thử hiểu theo cách 2 | Chỉ có DUY NHẤT 1 cách hiểu hợp lý cho từng câu hỏi |
| 17 | **Từ vựng đúng level** | Đọc từng từ, đối chiếu R3 | Key terms ≤ level, không dùng ngữ pháp vượt level. N1 văn luận thuyết cao cấp (`～にほかならない`/`～ざるを得ない`). N2 formal trung cấp |
| 18 | **Furigana đúng từ (tra CSV)** | Tra từng kanji trong `rules/kanji_jlpt_sensei.csv` | Mọi từ có kanji vượt level đều có `<ruby><rt>`. Không thừa furigana cho từ đúng level. Không dạng "Ab" (媒たい) |

#### PHẦN C: CÂU HỎI & ĐÁP ÁN (11 checks — áp dụng cho TỪNG câu hỏi)

Agent đọc TOÀN BỘ câu hỏi + 4 đáp án từ CSV và đánh giá từng câu (Q1, Q2, Q3):

| # | Check | Cách verify | PASS nếu |
|----|-------|-------------|----------|
| 19 | **Số câu hỏi đúng level** | Xem CSV đếm slot đã fill | Cả N1 và N2: Q1+Q2+Q3 có content, Q4+Q5 empty |
| 20 | **question_label đúng intent (mỗi câu)** | Đối chiếu R5 với nội dung từng câu | Label có `question_` prefix, khớp với dạng câu hỏi thực tế |
| 21 | **≥ 2 label khác nhau trong bài** | Đếm unique labels | ≥ 2 labels khác nhau (lý tưởng ≥ 3) |
| 22 | **Câu cuối đúng spec (cả 2 level)** | Xem `question_label_3` | **Cả N1 và N2**: câu 3 = `question_author_opinion` hoặc `question_content_match` |
| 23 | **Marker khớp câu hỏi (mỗi câu)** | So marker trong HTML với câu hỏi | Mọi `question_reference`/`question_meaning_interpretation` có `<u>` + marker ①/② trong HTML tương ứng. **Câu 3 tổng kết KHÔNG có marker** |
| 24 | **Answer format (mỗi câu)** | Xem 4 đáp án trong CSV | Đúng 4 options ngăn cách `\n`, KHÔNG `1.`/`①`/`1)` prefix. Độ dài tương đương (ratio < 2.0) |
| 25 | **correct_answer (mỗi câu + batch)** | Xem giá trị `correct_answer_i` | Integer 1-4. Scan batch: không lặp cùng vị trí ≥ 3 bài liên tiếp |
| 26 | **Paraphrase đáp án đúng (mỗi câu)** | So đáp án đúng với bài gốc | KHÔNG trùng cụm ≥ 4 từ liên tiếp (N1) hoặc ≥ 5 từ (N2) |
| 27 | **Distractor đa dạng bẫy (mỗi câu)** | Phân loại 3 distractor | ≥ 3 loại bẫy khác nhau trong (6: Reversal/Detail swap/Scope/Misinterpretation/Part of truth/Mixing). Câu 3 thường dùng Scope/Mixing/Misinterpretation |
| 28 | **Distractor có căn cứ trong bài (mỗi câu)** | Với mỗi đáp án sai: trích được câu/vị trí trong bài để bác bỏ | KHÔNG bịa. Mỗi distractor dùng info/concept từ bài nhưng sai ngữ cảnh |
| 29 | **Explanations 3 phần (mỗi câu)** | Đọc `explain_vn_i` + `explain_en_i` | Có đủ 3 phần: đáp án đúng (trích vị trí) + đáp án sai (nêu loại bẫy) + tóm tắt. Cả VN và EN đầy đủ |

#### PHẦN C2: VERIFY ĐÁP ÁN (⛔ QUAN TRỌNG NHẤT) — 2 checks

> **Agent tự giải từng câu từ đầu — KHÔNG nhìn đáp án đã gen.**
> Đây là bước bắt lỗi distractor bịa, câu hỏi ambiguous, sai `correct_answer`.

| # | Check | Cách verify | PASS nếu |
|----|-------|-------------|----------|
| 30 | **Tự giải Q1→Q3** | Đọc bài + từng câu hỏi, tự chọn đáp án từ đầu (KHÔNG nhìn `correct_answer_i`) | TẤT CẢ kết quả tự chọn KHỚP với `correct_answer_i` trong CSV |
| 31 | **Distractor self-test (toàn bộ câu)** | Với TỪNG đáp án sai trong TỪNG câu: trích dẫn chính xác câu/vị trí trong bài dùng để bác bỏ | Mọi distractor đều trích được. Không trích được = BỊA → FAIL |

#### PHẦN D: MULTI-QUESTION COVERAGE (2 checks)

> **Đặc biệt quan trọng cho đọc hiểu chủ đề**: 3 câu phải test 3 đoạn/ý KHÁC NHAU, câu 3 là tổng thể.

| # | Check | Cách verify | PASS nếu |
|----|-------|-------------|----------|
| 32 | **Mỗi câu hỏi test đoạn/ý KHÁC nhau** | Xác định paragraph/ý mà mỗi câu hỏi chỉ vào | Q1, Q2 test 2 đoạn KHÁC NHAU. Q3 test THESIS TỔNG THỂ (không 1 đoạn). Không có 2 câu trùng đoạn |
| 33 | **Marker khớp câu hỏi tương ứng** | Với mỗi `①`/`②` trong HTML, confirm có câu hỏi hỏi về nó. Câu 3 không có marker | Không có marker dư (không câu hỏi hỏi) và không câu hỏi reference/meaning nào hỏi marker không tồn tại. **Câu 3 KHÔNG có marker** |

---

### 🔒 GATE 3→4 — KHÔNG QUA = KHÔNG ĐƯỢC SỬA

Sau khi đánh giá 33 mục, agent PHẢI confirm trước khi vào fix loop:

- [ ] Đã hoàn tất đánh giá ĐẦY ĐỦ 33/33 mục (không thiếu mục nào)
- [ ] Đã liệt kê **chính xác** danh sách các mục FAIL (số mục + lý do FAIL)
- [ ] Mỗi FAIL có **diagnosis cụ thể** (sửa cái gì, ở đâu, theo rule nào)
- [ ] Phân biệt rõ **fix HTML** (cần `--refresh` CSV sau) vs **fix CSV** (chỉ cần `fill_qa.py`) vs **fix Q&A logic** (gen lại distractor)

> **🚨 LƯU Ý ĐẶC BIỆT:**
> - Nếu **≥ 50% mục FAIL** → bài này hỏng tổng thể → **GEN LẠI TỪ ĐẦU** (giữ `_id`), KHÔNG fix vá
> - Nếu **mục #25/#26 (self-solve) FAIL** → đáp án có vấn đề logic → BẮT BUỘC review lại bài + Q+A, có thể GEN LẠI
> - Nếu **char count FAIL > Hard Reject** → GEN LẠI HOÀN TOÀN (giữ `_id`)

❌ Bất kỳ item nào CHƯA tick → quay lại BƯỚC 3 đánh giá lại.
✅ Khi 4/4 tick → log `GATE 3→4 PASSED — fix list: [#x, #y, #z] với diagnoses` rồi sang BƯỚC 4.

---

### BƯỚC 4: SỬA & LẶP LẠI

> **⛔ Khi sửa HTML, CẬP NHẬT CSV — chạy lại `process_html.py --refresh` để cập nhật `text_read`, `jp_char_count` trong CSV.**
>
> **🚨 ĐẶC BIỆT khi sửa `<ruby>` thiếu/rỗng `<rt>`:** Đây là lỗi PHỔ BIẾN — agent hay chỉ sửa HTML mà QUÊN refresh CSV → CSV cột `text_read` vẫn chứa ruby hỏng → AI fine-tuning data BỊ HỎNG.
> Workflow BẮT BUỘC khi sửa ruby:
> 1. Sửa HTML: thay `<ruby>媒体</ruby>` → `<ruby>媒体<rt>ばいたい</rt></ruby>`
> 2. **BẮT BUỘC** chạy: `python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py --refresh --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv`
> 3. Verify: `python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py --validate --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv` — output PHẢI có dòng `✅ CSV ...: 0 row với broken ruby`. Nếu vẫn báo `🚫 CSV ... có N row với broken ruby` → CSV chưa sync, chạy lại `--refresh`.
>
> Không có screenshot nên KHÔNG cần chạy lại screenshot script.

| Nếu FAIL | Hành động | Sau đó |
|-----------|-----------|--------|
| #1 (scope level) | Level sai → REJECT, không gen lại — đọc hiểu chủ đề chỉ có N1/N2 | Không tiếp tục |
| #2, #3 (chars) | Bổ sung/cắt nội dung. Nếu Hard Reject → gen lại hoàn toàn | Chạy `--refresh` → QC lại |
| #4 (flow text) | Sửa `<br>` → `</p><p>` | Chạy `--refresh` → QC lại |
| #5, #6, #7 (CSS/structure) | Sửa CSS/structure HTML (800px, 56px 64px, line-height 2.0) | Chạy `--refresh` → QC lại |
| #8 (paragraph count) | Chia/gộp paragraph đạt N1:6-10, N2:5-8 | Chạy `--refresh` → QC lại |
| #9, #10, #11 (ruby/visual) | Sửa ruby tags hoặc thêm marker/source/annotation theo level | Chạy `--refresh` → QC lại |
| #12 (`(中略)` abuse) | Bỏ bớt `(中略)` (tối đa 1 lần) hoặc di chuyển vào giữa bài | Chạy `--refresh` → QC lại |
| #13-#17 | Gen lại nội dung (giữ _id): đảm bảo editorial + thesis + từ vựng level | Chạy `--refresh` → QC lại |
| #18 (furigana tra CSV) | Sửa ruby tags (tra lại `rules/kanji_jlpt_sensei.csv`) | Chạy `--refresh` → QC lại |
| #19 (số câu hỏi) | Thêm/xóa câu bằng `fill_qa.py` để đúng 3 slot | QC lại |
| #20, #21 (labels) | Sửa label trong `fill_qa.py` (dùng đủ `question_` prefix + đa dạng) | QC lại |
| #22 (câu cuối label) | Sửa câu cuối = `question_author_opinion` hoặc `question_content_match` (cả 2 level) | QC lại |
| #23 (marker ko khớp) | Sửa HTML (thêm/bớt marker) hoặc sửa câu hỏi. Câu 3 không được có marker | Chạy `--refresh` nếu sửa HTML → QC lại |
| #24, #25, #26 (đáp án) | Sửa đáp án bằng `fill_qa.py` | QC lại |
| #27 (distractor bẫy) | Viết lại distractor dùng 1 trong 6 loại bẫy | QC lại |
| #28 (distractor bịa) | Viết lại distractor dùng info thật từ bài | QC lại |
| #29 (explanation) | Viết lại explain 3 phần đầy đủ cho từng câu | QC lại |
| #30, #31 (self-solve) | Đáp án có thể sai → xem lại bài vs. đáp án | Sửa đáp án hoặc bài. QC lại |
| #32 (coverage trùng) | Sửa các câu để hỏi đoạn khác nhau. Q3 phải tổng thể (không 1 đoạn) | QC lại |
| #33 (marker dư/thiếu / câu 3 có marker) | Thêm/bớt marker trong HTML hoặc sửa câu hỏi. Bỏ marker ở câu 3 | Chạy `--refresh` → QC lại |

**Lệnh refresh CSV sau khi sửa HTML:**
```bash
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
  --refresh \
  --file assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html \
  --csv sheets/samples_v1.csv
```

> **Vòng lặp BẮT BUỘC: sửa → refresh CSV (nếu sửa HTML) → quay lại BƯỚC 2 (QC lại TẤT CẢ 33 mục TỪ ĐẦU, KHÔNG chỉ check mục đã FAIL) → nếu còn FAIL thì lặp lại.**
> **Tối đa 5 vòng. Sau 5 vòng vẫn FAIL → báo lỗi cho user, KHÔNG bỏ qua, KHÔNG sang bài tiếp.**
>
> **🚨 CẤM TUYỆT ĐỐI:**
> - Mark "đủ tốt rồi" khi còn ≥ 1 FAIL
> - Bỏ qua mục FAIL với lý do "minor"
> - Sang bài tiếp khi bài hiện tại chưa ALL PASS
> - QC lại chỉ mục đã sửa mà không check lại 33 mục (vì sửa 1 chỗ có thể làm vỡ chỗ khác)

### 🔒 GATE 4→5 — KHÔNG QUA = KHÔNG ĐƯỢC HOÀN THÀNH

Trước khi log "ALL PASSED", agent PHẢI confirm:

- [ ] Đã chạy QC checklist 33 mục TRỌN VẸN ở vòng cuối (không skip)
- [ ] **TẤT CẢ 33/33 mục đều PASS** (không có FAIL nào, không có "skip", không có "n/a")
- [ ] Nếu có sửa HTML trong loop → đã chạy `process_html.py --refresh` để sync CSV
- [ ] Đã chạy `process_html.py --validate` cho file hiện tại — KHÔNG có broken ruby trong cả HTML lẫn CSV
- [ ] Self-solve thực sự thực hiện: agent tự giải bài + chọn đáp án mà không nhìn correct_answer → KHỚP

❌ Bất kỳ item nào CHƯA tick → quay lại BƯỚC 4 sửa tiếp.
✅ Khi 5/5 tick → cho phép sang BƯỚC 5.

---

### BƯỚC 5: ✅ HOÀN THÀNH → BÀI TIẾP THEO

Chỉ khi **TẤT CẢ 33 checks PASS + GATE 4→5 PASSED** → log:
```
🎉 ALL PASSED (33/33) — {_id} hoàn thành — 3 câu hỏi ({labels})
GATE 4→5 PASSED — bài này hoàn tất, sang bài tiếp.
```
→ Chuyển sang bài tiếp theo (quay lại GATE 0→1 nếu là bài đầu batch, hoặc BƯỚC 1 nếu cùng batch).

**Batch size**: 3-4 bài/lần (văn abstract, gen chậm + đòi hỏi chất lượng cao nhất).

---

## BƯỚC CUỐI: VERIFY BATCH (sau khi gen xong TẤT CẢ bài)

Sau khi hoàn thành toàn bộ batch, chạy verify toàn bộ:

```bash
# 1. Validate tất cả file HTML (char count + broken ruby)
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
  --validate --html-dir assets/html/doc_hieu_chu_de

# 2. Đếm số rows trong CSV + check số câu hỏi + last-label rule
python3 -c "
import csv
expected_q = {'N1': 3, 'N2': 3}
last_rules = {'N1': ['question_author_opinion', 'question_content_match'],
              'N2': ['question_author_opinion', 'question_content_match']}
with open('sheets/samples_v1.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
print(f'Total rows: {len(rows)}')
bad = 0
for r in rows:
    lv = r.get('level')
    if lv not in expected_q:
        continue
    want = expected_q[lv]
    got = sum(1 for i in range(1, 6) if r.get(f'question_{i}', '').strip())
    if got != want:
        bad += 1
        print(f\"  ❌ {r['_id']} ({lv}): {got} câu, expected {want}\")
        continue
    last_lbl = r.get(f'question_label_{want}', '')
    if last_lbl not in last_rules[lv]:
        bad += 1
        print(f\"  ❌ {r['_id']} ({lv}): câu cuối = {last_lbl}, expected {last_rules[lv]}\")
print(f'Multi-question OK: {len(rows) - bad}/{len(rows)}')
for level in ['N1','N2']:
    n = sum(1 for r in rows if r.get('level') == level)
    print(f'  {level}: {n}')
"
```

### Batch-level checklist

- [ ] Mỗi bài có `_id` unique, đúng format `{LEVEL}_{uuid}`, Level ∈ {N1, N2}
- [ ] `kind` = `đọc hiểu chủ đề` trong tất cả rows
- [ ] `level` chỉ là N1 hoặc N2 (KHÔNG có N3/N4/N5)
- [ ] `general_image` = `""` (empty) — KHÔNG có PNG
- [ ] `general_audio` = `""` (empty)
- [ ] Char count trong Target Range (N1:1000-1200, N2:900-1100)
- [ ] Không bài nào dưới Hard Reject threshold (N1:950, N2:850)
- [ ] Paragraph count N1:6-10, N2:5-8
- [ ] Furigana chỉ cho từ vượt level, không dạng "Ab", mọi `<ruby>` có `<rt>`
- [ ] Ruby tags count ≤ expected (N1:5, N2:8)
- [ ] **Mỗi bài có đúng 3 câu hỏi** (cả N1 và N2) — Q4, Q5 slot empty
- [ ] **Cả N1 và N2 câu 3 = `question_author_opinion` hoặc `question_content_match`**
- [ ] `question_label_i` có `question_` prefix (7 labels hợp lệ)
- [ ] Trong 1 bài có ≥ 2 label khác nhau (lý tưởng ≥ 3)
- [ ] Mỗi câu hỏi có 4 đáp án ngăn cách `\n` (KHÔNG số thứ tự)
- [ ] `correct_answer_i` phân bố đều 1-4 trong batch
- [ ] Distractor dùng info từ bài (không bịa), ≥ 3 loại bẫy khác nhau per câu
- [ ] `explain_vn_i` + `explain_en_i` đủ 3 phần cho mọi câu
- [ ] Marker trong text khớp câu hỏi (`①` ↔ Q reference). **Câu 3 KHÔNG có marker**
- [ ] **Multi-question coverage**: Q1/Q2 test 2 đoạn KHÁC NHAU. Q3 test thesis tổng thể
- [ ] Bài có **thesis rõ ràng** (có thể tóm tắt trong 1-2 câu)
- [ ] `text_read` clean — không attribute, không class, không `<rt>` content
- [ ] `<p>` thuần, không `<br>` giữa câu
- [ ] `(中略)` xuất hiện ≤ 1 lần per bài (ở giữa, không đầu/cuối)
- [ ] Annotation (注) giải thích bằng **tiếng Nhật đơn giản**, KHÔNG tiếng Anh/Việt
- [ ] Source line dùng tên tác giả/báo tự chế (KHÔNG dùng tên thật — 朝日/読売/毎日/日経/村上春樹/夏目漱石/...)
- [ ] Trong batch, tag đa dạng ≥ 2 category (nếu batch > 3)

---

## Reference Data & Samples

Data mẫu có sẵn trong `data/`:

| Level | File | Samples |
|-------|------|---------|
| N1 | `doc_hieu_chu_de_n1_clean.json` | 25 |
| N2 | `doc_hieu_chu_de_n2_clean.json` | 41 |

N3, N4, N5 **KHÔNG CÓ** file data cho đọc hiểu chủ đề — không applicable.

Load bằng:
```bash
# Stats N1/N2
python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --stats

# 2 random samples N1
python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --level N1 --count 2
```

**LƯU Ý khi đọc data gốc**:
- Data gốc DÙNG `<br>` 28-31% — thói quen xấu. Output HTML skill KHÔNG theo.
- Data gốc có `<span>` bọc paragraph (N2: 36%) — output KHÔNG cần trừ `.marker`.
- Data gốc N1 thường có 4 câu hỏi (68%) — skill follow spec `EXPECTED_Q_COUNT` = 3, không bắt chước data.
- Data gốc N2 khớp spec (95% có 3 câu) — OK.
- Data gốc ruby = 0% (N1), 9% (N2) — skill giữ ít ruby.
- `(中略)` là đặc trưng của đọc hiểu chủ đề. N1 28%, N2 19% — optional, dùng để tăng authenticity (mô phỏng việc lược bớt đoạn từ bản gốc).

Chi tiết phân tích từng level xem `references/sample-analysis.md`.

---

## Common errors (dạng đọc hiểu chủ đề hay gặp)

1. **Gen level ngoài N1/N2** — SAI, skill này CHỈ N1/N2 (spec JLPT đọc hiểu chủ đề không có N3/N4/N5)
2. **N1 gen 4 câu (bắt chước data)** — SAI, spec N1 = 3 câu
3. **Câu cuối là reference/reason/meaning** — SAI. PHẢI là `question_author_opinion` hoặc `question_content_match`
4. **Câu 3 có marker ①②③** — SAI, câu cuối test tổng thể, không marker
5. **Bài chỉ 3-4 paragraph** — SAI, N1 cần 6-10, N2 cần 5-8 paragraph
6. **Bài kể chuyện / thuật sự** — SAI. Đọc hiểu chủ đề = editorial/critique, phải có thesis và chuỗi luận điểm
7. **Thiếu thesis rõ ràng** — bài phải phát biểu rõ quan điểm tác giả ít nhất 1 chỗ
8. **Tất cả câu dùng cùng 1 label** — SAI, cần ≥ 2 labels khác nhau
9. **2-3 câu cùng hỏi 1 đoạn** — SAI, coverage rule yêu cầu đoạn khác nhau
10. **Marker `①` trong bài nhưng không có câu hỏi reference** — marker vô nghĩa
11. **Câu hỏi hỏi `①` nhưng HTML không có marker** — câu hỏi không thể trả lời
12. **Thiếu source line ở N1** — giảm authenticity (data 64%)
13. **N1 không có annotation** — giảm authenticity (data 60%)
14. **Dùng `<br>` giữa câu** — SAI, dùng `<p>` thuần
15. **Ruby quá nhiều (> 5 cho N1, > 8 cho N2)** — đọc hiểu chủ đề thực tế gần như không có ruby
16. **Abuse `(中略)` > 1 lần/bài** — SAI, tối đa 1 lần
17. **Distractor yếu** — đọc hiểu chủ đề yêu cầu distractor **tinh vi nhất**: sai nuance, sai mệnh đề, sai mức độ, trộn 2 luận điểm
18. **Dùng tên tác giả/báo có thật** — SAI, luôn fake
19. **Quên `question_` prefix trong label** — label phải là `question_content_match`, không phải `content_match`

---

## Cảnh báo bảo mật dữ liệu

> **🚫 KHÔNG ĐƯỢC GHI VÀO THƯ MỤC `rules/`** — `rules/question_sheet.csv`, `rules/topic.json`, `rules/kanji_jlpt_sensei.csv`, `rules/question_format.json`, `rules/mission.json`, `rules/rule_doc_hieu.md` là file tham chiếu, chỉ đọc. Mọi dữ liệu gen phải ghi vào `sheets/samples_v1.csv`.
