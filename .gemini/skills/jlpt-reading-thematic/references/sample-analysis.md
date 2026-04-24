# Sample Analysis — Đọc Hiểu Chủ Đề Reference Data

Phân tích định lượng dữ liệu mẫu thực tế ở `data/doc_hieu_chu_de_n{1,2}_clean.json` để gen agent biết **chính xác** mức độ dài, số câu hỏi, và pattern HTML cho N1/N2.

Số liệu chạy bằng `load_references.py --stats` + phân tích pattern HTML của `general_text_read`.

## 0. Scope — CHỈ N1 & N2

| Level | Có "đọc hiểu chủ đề"? | Spec (từ `question_format.json`) |
|-------|----------------------|----------------------------------|
| N1    | ✅                   | `question_parent=1, question_child=3` — focus "overall intended points and ideas" |
| N2    | ✅                   | `question_parent=1, question_child=3` — focus "overall intended points and ideas" |
| N3    | ❌                   | Spec JLPT không có đọc hiểu chủ đề ở N3 |
| N4    | ❌                   | — |
| N5    | ❌                   | — |

Skill này chỉ handle N1 và N2.

## 1. Phân Bố Độ Dài (`jp_char_count`)

| Level | Samples | Min  | P25  | P50  | P75  | Avg  | Max  |
|-------|---------|------|------|------|------|------|------|
| N1    | 25      | 1030 | 1061 | 1101 | 1169 | 1126 | 1353 |
| N2    | 41      |  901 |  924 |  982 | 1073 | 1034 | 1564 |

**Kết luận**:
- **N1 target** = 1000–1200 (slightly wider than P25-P75 1061-1169, để chứa bài hơi ngắn hơn spread data)
- **N2 target** = 900–1100 (P25-P75 924-1073, bao được >50% data)
- **Hard reject**: N1<950 (dưới Min data 1030 có buffer 80), N2<850 (dưới Min data 901 có buffer 51)
- Max N1=1353, N2=1564 là outlier (bài đặc biệt dài) → skill cho phép đến HI+100 = 1300 (N1) / 1200 (N2), quá nữa coi là OVER_TARGET

## 2. Số Câu Hỏi Per Sample

| Level | 2q | 3q | 4q | 5q | Dominant vs Spec |
|-------|-----|-----|-----|-----|------------------|
| N1    | 0  | 8 (32%)  | **17 (68%)** | 0 | Data 4q nhưng SPEC = 3q |
| N2    | 2 (5%) | **39 (95%)** | 0 | 0 | Khớp spec — 3q |

**Mismatch giữa data & spec**:
- `rules/question_format.json` spec: **Cả N1 và N2 = 3 câu**
- Data N1 hay có 4 câu (68%) — **legacy dataset noise** (đề cũ ghép thêm câu)
- Data N2 khớp spec (95% 3 câu)
- **Skill FOLLOW SPEC** — luôn gen ĐÚNG 3 câu cho cả 2 level

## 3. Pattern HTML Phổ Biến

| Pattern | N1 | N2 |
|---------|----|----|
| Có `<p>` | ~100% | ~100% |
| Có `<br>` | 28% | 31% |
| Có `<ruby>` | **0%** | 9% |
| Có `<u>` underline | **88%** | 26% |
| Có `<span>` (ngoài marker) | 8% | 36% |
| Có 注 annotation | **60%** | 51% |
| Có marker ①②③ | **76%** | 48% |
| Có source line `（...による）` | **64%** | 26% |
| Có `(中略)` | 28% | 19% |
| Có blank `[ ]` | 8% | 4% |
| Có `<table>` | 0% | 4% |

### Nhận xét Quan Trọng

1. **`<u>` underline N1 = 88%** — rất cao. Bài N1 đọc hiểu chủ đề hầu như luôn có cụm từ được gạch chân để hỏi. Skill dùng `<u>` cho MỌI cụm reference.

2. **Marker ①②③ N1 = 76%, N2 = 48%** — N1 gần như luôn có ít nhất 1 marker cho câu reference. Skill khuyến nghị 1-2 marker per bài (cả 2 level).

3. **Source line N1 = 64%** — đặc trưng xã luận/tiểu luận cao cấp. **Rất khuyến nghị** N1. N2 chỉ 26% — optional.

4. **Annotation 注 cả 2 level 50%+** — bài editorial có thuật ngữ cần chú thích. Khuyến nghị 1-2 chú thích.

5. **`(中略)` là đặc trưng của đọc hiểu chủ đề** — 28% N1, 19% N2. Dùng khi muốn lược đoạn logic → tăng authenticity (mô phỏng bản gốc editorial dài hơn).

6. **`<ruby>` N1 = 0%, N2 = 9%** — đề đọc hiểu chủ đề thực tế **gần như không dùng furigana**. Skill cho phép 0-3 (N1) / 0-5 (N2) cặp, ưu tiên 0.

7. **`<br>` 28-31%** — data có nhưng skill KHÔNG bắt chước, dùng `<p>` thuần.

8. **`<span>` N2 = 36%** — nhiều nhưng chủ yếu là wrapper trong JSON export, không phải styling cần mimic. Skill chỉ dùng `<span class="marker">`.

9. **Blank `[ ]` gần như không** — đọc hiểu chủ đề không có fill_in_the_blank.

10. **`<table>` N2 = 4% là noise** — không có bài đọc hiểu chủ đề nào thực sự cần bảng. Skill KHÔNG dùng.

## 4. Distribution Đề Xuất Per Level

### N1 (3 câu/bài) — spec focus "overall intended points and ideas"

Combo ưu tiên:

**Combo 1** (phổ biến nhất — 50%+ nên dùng):
- Q1: `question_reference` (với marker ①)
- Q2: `question_reason_explanation`
- Q3: **`question_author_opinion`** (BẮT BUỘC câu cuối)

**Combo 2** (essay analytic):
- Q1: `question_meaning_interpretation` (với marker ①)
- Q2: `question_reason_explanation`
- Q3: `question_author_opinion`

**Combo 3** (dual marker):
- Q1: `question_reference` (①)
- Q2: `question_reference` (②) / `question_meaning_interpretation` (②)
- Q3: `question_author_opinion`

**Combo 4** (alternative cuối):
- Q1: `question_reference` (①)
- Q2: `question_reason_explanation`
- Q3: `question_content_match` (tổng thể)

### N2 (3 câu/bài) — spec identical với N1

**Combo 1** (phổ biến nhất):
- Q1: `question_reference` (marker ①)
- Q2: `question_reason_explanation`
- Q3: **`question_author_opinion`**

**Combo 2** (reference heavy):
- Q1: `question_reference` (①)
- Q2: `question_reference` (②)
- Q3: `question_author_opinion`

**Combo 3** (meaning focused):
- Q1: `question_meaning_interpretation` (①)
- Q2: `question_reason_explanation`
- Q3: `question_author_opinion`

**Combo 4** (alternative cuối):
- Q1: `question_reference` (①)
- Q2: `question_reason_explanation`
- Q3: `question_content_match` (tổng thể)

### Rule cứng câu cuối

Cả 2 level: **Câu 3 PHẢI là `question_author_opinion` hoặc `question_content_match`**. CẤM câu cuối là `question_reference`, `question_reason_explanation`, `question_meaning_interpretation`.

## 5. Topic Distribution Theo Data

### N1 topic phổ biến (tự phân nhóm):

| Nhóm | Tỷ lệ | Ví dụ |
|------|-------|-------|
| Triết học / ngôn ngữ / bản chất con người | ~30% | "言葉と思考", "個の意味" |
| Phê bình văn hóa / văn học | ~25% | phê bình văn học, xã hội |
| Xã luận chính sách / kinh tế | ~20% | giáo dục, môi trường, kinh tế |
| Khoa học nhận thức / phân tâm học | ~15% | tâm lý học, cognitive |
| Phê bình công nghệ | ~10% | AI, digital society |

### N2 topic phổ biến:

| Nhóm | Tỷ lệ | Ví dụ |
|------|-------|-------|
| Văn hóa đời sống / lối sống | ~35% | gia đình, thế hệ trẻ, ăn uống |
| Xã luận công nghệ / AI | ~20% | scả lợi-hại |
| Phê bình giáo dục | ~15% | cải cách, học tập |
| Ngôn ngữ và xã hội | ~15% | media, commu |
| Môi trường / sức khỏe | ~15% | nature, health |

N1 thiên về abstract / philosophical; N2 gần gũi đời sống hơn nhưng vẫn là editorial.

## 6. Style Cheatsheet Cho Gen Agent

```
N1 cheatsheet (25 samples):
  - Char target: 1000-1200 (P25-P75: 1061-1169)
  - Paragraph: 6-10 (dài, chặt chẽ)
  - 3 câu, câu cuối = author_opinion (ưu tiên mạnh)
  - Pattern HTML:
    * <u> underline: 88%+ (RẤT NÊN dùng)
    * marker ①②: 76%+ (NÊN dùng 1-2)
    * annotation 注: 60%+ (NÊN có 1-2)
    * source line: 64%+ (RẤT NÊN có)
    * (中略): 28% (optional)
    * ruby: 0% (hạn chế)
    * KHÔNG dùng <br>, <table>
  - Văn phong: luận thuyết cao cấp, keigo văn viết,
    grammar ～にほかならない / ～ざるを得ない / ～というものだ
  - Topic: triết học, phê bình văn hóa sâu, xã luận cao cấp

N2 cheatsheet (41 samples):
  - Char target: 900-1100 (P25-P75: 924-1073)
  - Paragraph: 5-8
  - 3 câu, câu cuối = author_opinion (ưu tiên mạnh)
  - Pattern HTML:
    * <u> underline: 26% (optional)
    * marker ①②: 48% (NÊN dùng 1-2)
    * annotation 注: 51% (NÊN có 1-2)
    * source line: 26% (optional)
    * (中略): 19% (optional)
    * ruby: 9% (tối đa 5 cặp)
    * KHÔNG dùng <br>, <table>
  - Văn phong: formal văn viết trung cấp,
    grammar ～に伴い / ～を踏まえて / ～に限り / ～とはいえ
  - Topic: văn hóa đời sống, xã luận công nghệ vừa,
    phê bình giáo dục, ngôn ngữ xã hội
```

## 7. Key Takeaways

- **Đọc hiểu chủ đề yêu cầu cao** — kết hợp bài dài (900-1200) + văn abstract + distractor tinh vi + BẮT BUỘC câu cuối tổng thể
- **N1 88% dùng `<u>`, 76% dùng marker, 64% dùng source line** — bài N1 rất "structured editorial"
- **`(中略)` là đặc trưng điển hình của dạng này** — dùng để lược 1 khối logic dài, 1 lần/bài
- **68% data N1 có 4 câu** nhưng spec = 3 — luôn follow spec
- **N3/N4/N5 không có kind này** — skill hard-block các level đó
