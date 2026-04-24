# HANDOVER — Đọc Hiểu Chủ Đề Skill

Tài liệu giao/nhận cho skill **jlpt-reading-thematic** (主張理解 / đọc hiểu chủ đề). Đọc file này trước khi chạy batch gen hoặc khi bàn giao cho team mới.

## 1. Mục đích

Gen dữ liệu huấn luyện AI cho **dạng "đọc hiểu chủ đề"** (主張理解) của JLPT. Mỗi bài gồm:

- 1 đoạn văn Nhật **dạng xã luận / phê bình / luận thuyết** (900–1200 ký tự tuỳ level)
- **Đúng 3 câu hỏi** multiple-choice 4 đáp án cho cả N1 và N2
- Câu hỏi cuối BẮT BUỘC test **thesis / luận điểm tổng thể** (`question_author_opinion` hoặc `question_content_match`)
- Giải thích tiếng Việt + tiếng Anh cho từng câu

**Scope hẹp — CHỈ N1 và N2**. Theo `rules/question_format.json`, N3/N4/N5 KHÔNG có kind "đọc hiểu chủ đề", nên skill hard-block các level đó (status `UNSUPPORTED_LEVEL`, exit 1).

So với các phase trước:

| Phase | Kind | Levels | Chars | Q/bài | Container | Style |
|-------|------|--------|-------|-------|-----------|-------|
| 0 | tìm thông tin | N1-N5 | varies | 1 | — (có PNG) | Ads / bảng lịch |
| 1 | đoạn văn ngắn | N1-N5 | 80–290 | 1 | 640px | Ngắn gọn |
| 2 | đoạn văn vừa | N1-N5 | 250–620 | 2–3 | 720px | Essay ngắn |
| 3 | đoạn văn dài | N1 + N3 | 550–1150 | 3–4 | 780px | Essay/thư dài |
| **4** | **đọc hiểu chủ đề** | **N1 + N2** | **900–1200** | **3** | **800px** | **Xã luận / phê bình thuần** |

**Đọc hiểu chủ đề = workload cao nhất series** (bài dài, văn abstract, distractor tinh vi nhất). Khuyến nghị batch rất nhỏ (3-4 bài/lần).

## 2. Cấu trúc project

```
gen-question-doc-hieu-chu-de/
├── data/                                       # Sample JSON từ đề JLPT cũ
│   ├── doc_hieu_chu_de_n1_clean.json           # 25 samples
│   └── doc_hieu_chu_de_n2_clean.json           # 41 samples
├── .claude/skills/jlpt-reading-thematic/
│   ├── SKILL.md                                # Main skill definition
│   ├── scripts/
│   │   ├── process_html.py                     # Count + clean HTML + CSV upsert (3 Q)
│   │   └── load_references.py                  # Pretty-print JSON cho gen agent
│   └── references/
│       ├── sample-analysis.md                  # Phân tích pattern N1/N2
│       └── html-patterns.md                    # HTML template 800px + marker strategy
├── .gemini/skills/jlpt-reading-thematic/       # Mirror identical của .claude/
├── assets/html/doc_hieu_chu_de/                # Output HTML files (runtime)
├── sheets/                                     # Output CSV files (runtime)
├── rules/                                      # Schema & spec
│   ├── question_sheet.csv                      # 45-col CSV header
│   ├── question_format.json                    # Xác nhận N1=3, N2=3
│   ├── kind_mission_mapping.json
│   ├── mission.json                            # Question label catalog
│   └── topic.json
├── HANDOVER.md                                 # (file này)
└── PROMPTS.md                                  # Prompt templates cho gen agent
```

## 3. Pipeline chuẩn

### Bước 1 — Load references (calibrate style)

```bash
cd /path/to/gen-question-doc-hieu-chu-de
python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --stats
python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --level N1 --count 1 --seed 42
python3 .claude/skills/jlpt-reading-thematic/scripts/load_references.py --level N2 --count 1 --seed 42
```

Gen agent đọc 1 sample cùng level (bài dài abstract — đọc 1 là đủ) để học:
- Độ dài (P25–P75: N1 ≈ 1061–1169, N2 ≈ 924–1073)
- Chủ đề (N1 = triết học / xã luận cao cấp; N2 = xã luận công nghệ / văn hóa đời sống)
- Cấu trúc thesis + 3-4 luận điểm + conclusion
- `(中略)` pattern cho lược đoạn

**KHÔNG bắt chước styling data gốc 100%** — data có `<br>` và 4 câu N1 (68% — noise). Chỉ học **thesis structure + question pattern**.

### Bước 2 — Gen HTML + câu hỏi từ LLM

LLM dùng prompt trong `PROMPTS.md` (template N1 / N2) để gen ra:

1. HTML file đầy đủ (có `<!DOCTYPE>`, Noto Sans JP CSS, `max-width: 800px`)
2. **Đúng 3 câu** cho cả N1 và N2, mỗi câu 4 đáp án + đáp án đúng
3. Giải thích VN + EN cho từng câu
4. **Câu cuối BẮT BUỘC là `question_author_opinion` hoặc `question_content_match`**
5. Source line khuyến nghị (N1 64% nên có, N2 26% optional)
6. Annotation 注 khuyến nghị (N1 60%, N2 51% → 1-2 cái)
7. `(中略)` optional (N1 28%, N2 19%) — dùng khi muốn lược đoạn logic

Output khuyến nghị ở dạng JSON file `questions.json`:

```json
{
  "questions": [
    {
      "label": "question_reference",
      "question": "①「この柔軟性」とあるが、どのような柔軟性か。",
      "answers": ["A option", "B option", "C option", "D option"],
      "correct": 2,
      "explain_vn": "...",
      "explain_en": "..."
    },
    {
      "label": "question_reason_explanation",
      "question": "筆者は、なぜ...と考えているのか。",
      "answers": ["A", "B", "C", "D"],
      "correct": 3,
      "explain_vn": "...",
      "explain_en": "..."
    },
    {
      "label": "question_author_opinion",
      "question": "この文章で筆者が最も言いたいことはどれか。",
      "answers": ["A", "B", "C", "D"],
      "correct": 1,
      "explain_vn": "...",
      "explain_en": "..."
    }
  ]
}
```

### Bước 3 — Save HTML

Tên file: `{LEVEL}_{uuid4().hex}.html`. Ví dụ: `N1_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6.html`.

```python
import uuid
filename = f"N1_{uuid.uuid4().hex}.html"
```

Save vào `assets/html/doc_hieu_chu_de/`.

### Bước 4 — Process + commit CSV (2 cách)

**Cách A (KHUYẾN NGHỊ) — JSON file chứa tất cả 3 câu hỏi**:

```bash
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
    --file assets/html/doc_hieu_chu_de/N1_abc123...html \
    --csv sheets/samples_v1.csv \
    --tag "triết học ngôn ngữ" \
    --questions-json /tmp/qs.json
```

**Cách B — CLI flags (3 câu, prone to error)**:

```bash
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
    --file assets/html/doc_hieu_chu_de/N2_abc123...html \
    --csv sheets/samples_v1.csv \
    --tag "xã luận công nghệ" \
    --q1-label question_reference --q1 "①..." --a1 "A|B|C|D" --c1 2 --ev1 "..." --ee1 "..." \
    --q2-label question_reason_explanation --q2 "なぜ..." --a2 "A|B|C|D" --c2 3 --ev2 "..." --ee2 "..." \
    --q3-label question_author_opinion --q3 "筆者が最も言いたいこと..." --a3 "A|B|C|D" --c3 1 --ev3 "..." --ee3 "..."
```

Script sẽ:

- Count `jp_char_count` từ full HTML (skip `<rt>`, whitespace)
- Extract clean HTML (bỏ attribute, collapse whitespace, bỏ `<rt>`)
- **Validate level** (N1/N2 only) — block commit nếu N3/N4/N5
- **Validate đúng 3 câu** — warning nếu khác 3
- **Validate ≥ 2 labels khác nhau** — warning
- **Validate câu cuối = `question_author_opinion`/`question_content_match`** — warning
- **Hard-reject** nếu dưới threshold (N1<950, N2<850) — exit 1, không commit CSV
- Cảnh báo nếu dưới Target Range hoặc vượt xa Target (> hi + 100)
- Upsert row vào CSV (45 columns) theo `_id` = filename, populate `question_1..question_3`

### Bước 5 — Validate batch

```bash
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
    --validate --html-dir assets/html/doc_hieu_chu_de
```

Exit 0 = tất cả pass; 1 = có file fail (UNDER_TARGET / HARD_REJECT / UNSUPPORTED_LEVEL).

### Bước 6 — Refresh sau khi edit HTML

Giữ câu hỏi cũ, chỉ refresh `jp_char_count` + `text_read`:

```bash
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py \
    --refresh --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv
```

## 4. Target ranges & số câu (BẮT BUỘC)

| Level | Target Range | Hard Reject | Số câu/bài | Combo đề xuất |
|-------|--------------|-------------|-----------|---------------|
| N1    | 1000–1200    | < 950       | **3**     | reference + reason + **author_opinion** (câu cuối) |
| N2    | 900–1100     | < 850       | **3**     | reference + reason + **author_opinion** (câu cuối) |

> **Scope hẹp**: N3, N4, N5 KHÔNG có kind này. Nếu tệp `.html` mang tên `N3_*` đi qua pipeline, script sẽ báo `UNSUPPORTED_LEVEL` và KHÔNG commit vào CSV.

> **Data vs Spec**: Data N1 gốc 68% có 4 câu, 32% có 3 câu. Skill **LUÔN follow SPEC** — cả N1 và N2 = 3 câu. N2 data khớp spec (95% 3 câu).

> **Câu cuối BẮT BUỘC**: Câu 3 phải test **thesis tổng thể**, không được test 1 đoạn riêng lẻ:
> - **Ưu tiên**: `question_author_opinion` — "筆者が最も言いたいことはどれか" hoặc "筆者の主張と一致するものはどれか"
> - **Alternative**: `question_content_match` — "この文章の内容と合っているものはどれか"
> - **CẤM**: `question_reference`, `question_reason_explanation`, `question_meaning_interpretation` ở câu cuối

## 5. CSV Schema (45 columns)

Populate 3 câu hỏi, các cột 4-5 để trống:

| Column | Value |
|--------|-------|
| `_id`  | `{LEVEL}_{uuid32hex}` (`LEVEL` ∈ {N1, N2}) |
| `level` | N1 hoặc N2 |
| `tag`  | Topic label |
| `jp_char_count` | Result `count_body_chars()` |
| `kind` | Always `đọc hiểu chủ đề` |
| `general_audio` | "" |
| `general_image` | "" (empty — no PNG) |
| `text_read` | Clean HTML |
| `text_read_vn` / `text_read_en` | "" |
| `question_label_1` | Label câu 1 |
| `question_1` | Câu hỏi 1 tiếng Nhật |
| `question_image_1` | "" |
| `answer_1` | `1. A\n2. B\n3. C\n4. D` |
| `correct_answer_1` | 1-4 |
| `explain_vn_1` / `explain_en_1` | Giải thích câu 1 |
| `question_label_2`..`explain_en_2` | Câu 2 (BẮT BUỘC) |
| `question_label_3`..`explain_en_3` | Câu 3 (BẮT BUỘC — author_opinion/content_match) |
| `question_label_4`..`explain_en_4` | **""** |
| `question_label_5`..`explain_en_5` | **""** |

## 6. Quality Gates

Trước khi coi 1 batch là xong:

- [ ] 100% file qua Hard Reject threshold
- [ ] ≥ 80% file nằm trong Target Range
- [ ] 100% file có `level` ∈ {N1, N2}
- [ ] **100% row có ĐÚNG 3 câu hỏi** (cả N1 và N2)
- [ ] **Trong 1 bài, ≥ 2 `question_label` khác nhau**
- [ ] **Câu 3 luôn là `question_author_opinion` hoặc `question_content_match`** (tổng thể)
- [ ] Các câu hỏi trong 1 bài KHÔNG test cùng 1 đoạn / 1 ý
- [ ] Marker `①②` trong HTML khớp với câu hỏi reference
- [ ] **Bài N1 có 6–10 paragraph, N2 có 5–8 paragraph**
- [ ] **Mỗi bài có thesis rõ ràng** (tóm tắt được trong 1-2 câu)
- [ ] Batch ≥ 3 bài có ≥ 2 `tag` khác nhau
- [ ] 0 file có furigana dạng "Ab" (cấm 週かん, 友だち)
- [ ] 100% file có `general_image = ""`
- [ ] 100% row có `kind = "đọc hiểu chủ đề"`
- [ ] 0 row có `question_4` hoặc `question_5` non-empty
- [ ] Mỗi câu có 4 đáp án trong `answer_X`, `correct_answer_X` là 1–4
- [ ] `explain_vn_X` + `explain_en_X` đều non-empty cho 3 câu
- [ ] Bài là luận thuyết / editorial / critique — KHÔNG kể chuyện thuần
- [ ] Source line (nếu có): author + title đều fake, KHÔNG tên thật

## 7. Edge cases & pitfalls

1. **Gen 4 câu cho N1** — SAI, dù data gốc 68% có 4 câu. Follow spec 3 câu.
2. **Gen 2 câu** — SAI, đọc hiểu chủ đề **BẮT BUỘC 3 câu**.
3. **Gen bài level N3/N4/N5** — HARD-BLOCKED bởi script. N3 dài thì dùng skill `jlpt-reading-long-passage` (Phase 3).
4. **Câu 3 không phải author_opinion/content_match** — SAI, script báo warning. PHẢI fix trước commit.
5. **Bài là câu chuyện / kỷ niệm cá nhân** — SAI. Đọc hiểu chủ đề = editorial/critique thuần, PHẢI có thesis và lập luận.
6. **Thesis không rõ ràng** — người đọc không tóm tắt được ý tác giả → câu 3 không có đáp án đúng rõ.
7. **3 câu cùng test 1 đoạn** — SAI, mỗi câu test 1 phần khác của bài.
8. **Marker ①② không match câu hỏi** — câu `①「cụm từ」とあるが` phải có `<span class="marker">①</span><u>cụm từ</u>` trong HTML.
9. **Char count dưới target** vì chỉ 3-4 paragraph — phải **6-10 paragraph** (N1) hoặc **5-8 paragraph** (N2).
10. **Distractor quá dễ** — đọc hiểu chủ đề yêu cầu distractor **tinh vi nhất series**: sai ở nuance, sai mệnh đề, sai mức độ, trộn 2 luận điểm, paraphrase sai, polarity đảo.
11. **Source line dùng tên thật** (朝日新聞, 村上春樹, ...) — SAI, luôn fake.
12. **Data gốc có `<br>` / `<span>` ngoài marker** — KHÔNG bắt chước; dùng `<p>` thuần + chỉ `.marker` span.
13. **Furigana quá nhiều** — data N1 0% ruby, N2 9%. Giới hạn tối đa 3 (N1) / 5 (N2) cặp, ưu tiên 0.
14. **Correct index conversion** — JSON `correctAnswer` là 0-based, CSV `correct_answer_X` là 1-based.
15. **Dạng "Ab" (週かん, 友だち)** — tuyệt đối không. Full kanji + ruby HOẶC full hiragana.
16. **Container width** = **800px** (rộng nhất 4 phase). Đừng nhầm với 780 của đoạn văn dài.
17. **Văn phong quá phổ thông cho N1** — N1 phải là luận thuyết cao cấp, có keigo/grammar N1 (～にほかならない, ～ざるを得ない, ～にとって…に他ならない).
18. **`(中略)` đặt sai chỗ** — KHÔNG đặt đầu/cuối bài, chỉ giữa 2 khối logic lớn.
19. **Abuse `(中略)`** — 1 lần/bài là đủ, không quá 2 lần.
20. **N2 văn phong giống bài vừa** — N2 đọc hiểu chủ đề phải có thesis rõ + lập luận, KHÔNG chỉ là kể/mô tả như đoạn văn vừa.

## 8. Sample patterns theo data (tóm tắt, chi tiết xem `references/sample-analysis.md`)

| Pattern | N1 | N2 |
|---------|----|----|
| Char P25–P75 | 1061–1169 | 924–1073 |
| Char Min–Max | 1030–1353 | 901–1564 |
| Số câu 3 | 32% | 95% |
| Số câu 4 | 68% (noise) | 5% |
| Có `<u>` underline | **88%** | 26% |
| Có marker ①②③ | **76%** | 48% |
| Có 注 annotation | **60%** | 51% |
| Có source line | **64%** | 26% |
| Có `(中略)` | 28% | 19% |
| Có `<ruby>` | **0%** | 9% |
| Có fill_in_blank `[ ]` | 8% | 4% |
| Có `<br>` (KHÔNG mimic) | 28% | 31% |

**Key insights**:

- **N1 = xã luận / triết học cao cấp**: rất nhiều underline (88%), marker cao (76%), source line cao (64%), annotation (60%). Bài dài chặt chẽ, thesis tổng quát ở cuối hoặc đầu.
- **N2 = xã luận văn hóa / công nghệ / đời sống**: ít underline hơn, annotation vừa (51%), source line ít hơn (26%). Bài dễ tiếp cận hơn, thesis thường rõ hơn.
- **Cả 2 level `(中略)` là đặc trưng** — đặc biệt N1 (28%). Đây là pattern chỉ có ở đọc hiểu chủ đề, không có ở Phase 3.
- **`question_author_opinion` cao**: cả N1 và N2 đều có tỷ lệ câu cuối = author_opinion / content_match trên 90% data.

## 9. Status output của process_html.py

Khi chạy `--validate` hoặc `--refresh`, mỗi file được classify:

| Status | Nghĩa | Block commit? |
|--------|-------|---------------|
| `OK` | Trong target range | ❌ |
| `UNDER_TARGET` | Dưới target nhưng trên hard reject | ❌ (warning only) |
| `OVER_TARGET` | Vượt xa target (> hi + 100) | ❌ (warning only) |
| `HARD_REJECT` | Dưới threshold (N1<950, N2<850) | ✅ (exit 1) |
| `UNSUPPORTED_LEVEL` | Level không phải N1/N2 | ✅ (exit 1) |
| `UNKNOWN_LEVEL` | Tên file không match regex `^N[1-5]_[0-9a-f]{8,}\.html$` | ✅ (exit 1) |

## 10. Tương lai (Phase 5)

- Phase 5: `đọc hiểu tổng hợp` (N1/N2 ~600, 2 đoạn A+B, 2 câu so sánh view, label = `question_comprehensive_understanding`)
- Post-pipeline: bổ sung `text_read_vn` / `text_read_en` nếu cần bản dịch
- CSV consolidation: merge CSVs của 5 skill thành 1 `sheets/master.csv` để train

## 11. Liên hệ

- Skill owner: Nguyễn Đình Sinh <sinhnd@eupgroup.net>
- Phase trước: `../gen-question-doan-van-dai/` (đoạn văn dài, N1+N3)
- Phase 2 reference: `../gen-question-doan-van-vua/` (đoạn văn vừa, 2-3 câu)
- Phase 1 reference: `../gen-question-doan-van-ngan/` (đoạn văn ngắn, 1 câu)
- Phase 0 reference: `../gen-question-jlpt/` (tìm thông tin, có screenshot)
- Master plan: `../PLAN_5_DANG_DOC_HIEU.md`
