# Rules: Nội dung, Layout, Format & Visual (R1, R2, R7, R8)

> **Scope**: Đọc hiểu chủ đề (主張理解 / thematic) — văn abstract/editorial/critique Nhật 900–1200 ký tự với **3 câu hỏi trắc nghiệm** per bài, focus **thesis / main argument** của tác giả. **CHỈ áp dụng cho N1 và N2** — N3/N4/N5 không có dạng này per `rules/question_format.json`.

## R1. Chủ đề & Văn phong theo level

> **NGUYÊN TẮC**: Đọc hiểu chủ đề là **văn luận thuyết thuần** (editorial / critique / tiểu luận trừu tượng) — test khả năng **nắm thesis tổng thể và chuỗi luận điểm** qua 3 câu hỏi, câu cuối **BẮT BUỘC** kiểm tra ý tác giả ở mức toàn bài.

| Level | Chủ đề | Văn phong | Cấu trúc câu |
|-------|--------|-----------|--------------|
| **N2** | Xã luận báo chí về công nghệ/xã hội, bình luận văn hóa trung cấp, phê bình đời sống, tiểu luận cá nhân có luận điểm rõ, phê bình giáo dục nhẹ | Formal, văn viết trung cấp | ～に伴い, ～に基づき, ～を踏まえて, ～に限り, ～とはいえ, ～からこそ |
| **N1** | Xã luận báo chí cao cấp, phê bình triết học, tiểu luận trừu tượng, bình luận chính sách/kinh tế/văn hóa sâu, triết học ngôn ngữ, phân tâm học, bản chất con người | Rất formal, văn bản luận thuyết cao cấp, keigo văn viết | ～いかんによらず, ～をもって, ～に先立ち, ～にほかならない, ～というものだ, ～ざるを得ない, ～に足る |

### Topic tag — BẮT BUỘC

Tag PHẢI bằng **tiếng Anh** — chọn từ cột `en` của `rules/topic.json` (catalog 287 topics, 13 category). Tham khảo `rules/rule_doc_hieu.md` (rule chung của giáo viên cho TOÀN BỘ phần đọc hiểu) để chọn topic phù hợp level. Category gợi ý theo level:

| Category | Ví dụ tag (en) | Phù hợp level |
|----------|----------------|---------------|
| Editorial / social criticism | `journalism`, `social criticism`, `cultural criticism`, `literary criticism` | **N1** (phổ biến), N2 (nhẹ hơn) |
| Science & Technology | `technology`, `digital society`, `artificial intelligence`, `popular science` | N1, N2 |
| Education & Language | `education`, `language`, `educational reform`, `language and society` | N1, N2 |
| Economics & Policy | `economics`, `consumption`, `policy`, `environment` | **N1** |
| Culture & Daily Life | `culture`, `lifestyle`, `family`, `youth` | **N2** (phổ biến) |
| Philosophy & Ethics | `philosophy`, `ethics`, `human nature`, `freedom` | **N1** |
| Psychology & Cognition | `psychology`, `cognition`, `mindset`, `perception` | **N1** |

> **⚠️ KHÔNG dùng tag tiếng Việt hoặc tiếng Nhật. TUYỆT ĐỐI tiếng Anh.**
> Phải dùng tiếng Anh slug đúng cột `en` của `rules/topic.json` (✅ `journalism`, `technology`, `philosophy`).

Trong batch ≥ 3 bài, chọn topic từ ≥ 2 category khác nhau để đa dạng.

---

## R2. Format văn bản & Độ dài

### Target character count (BẮT BUỘC)

Đo bằng `count_body_chars()` — đếm **ký tự visible trong body**, bỏ whitespace, bỏ `<rt>` furigana.

Dữ liệu tham khảo từ sample JSON `data/doc_hieu_chu_de_n{1,2}_clean.json`:

| Level | Samples | Min  | P25  | P50  | P75  | Avg  | Max  |
|-------|---------|------|------|------|------|------|------|
| N1    | 25      | 1030 | 1061 | 1101 | 1169 | 1126 | 1353 |
| N2    | 41      |  901 |  924 |  982 | 1073 | 1034 | 1564 |

Target range khuyến nghị:

| Level | Target Range | Hard Reject (< Min) |
|-------|--------------|---------------------|
| **N1**    | **1000–1200** | < 950 → gen lại    |
| **N2**    | **900–1100**  | < 850 → gen lại    |

> **🚫 HARD REJECT**: Nếu `count_body_chars()` **thấp hơn Hard Reject threshold**, bài **PHẢI gen lại từ đầu**. Không chấp nhận, không chỉnh sửa nhỏ — gen lại hoàn toàn.
> **⚠️ UNDER TARGET**: Dưới Target Range nhưng ≥ Hard Reject → bổ sung 1-2 câu văn hoặc thêm 1 đoạn elaboration / 1 `注` annotation.
> **⚠️ OVER TARGET**: Cho phép dài hơn tới +100 chars (bài abstract cho phép chênh lệch); quá nữa (> 1300 N1 / > 1200 N2) thì cảnh báo.

**Lưu ý**: Max N1=1353, N2=1564 là outlier (bài đặc biệt dài). Spec JLPT thực tế ~1000-1100, nên skill giữ 1000-1200 (N1) / 900-1100 (N2) để sát spec.

### Số câu hỏi per bài (BẮT BUỘC)

Dựa trên `rules/question_format.json` (spec JLPT chính thức):

| Level | Q Count | Focus spec |
|-------|---------|------------|
| **N1** | **3**   | overall intended points and ideas |
| **N2** | **3**   | overall intended points and ideas |

- N3, N4, N5 **KHÔNG CÓ** dạng đọc hiểu chủ đề — skill này chỉ apply N1/N2.
- CSV columns `question_1..question_3` populate đủ. `question_4`, `question_5` (+ related cols) = "" (empty string).
- **Data gốc có noise** — N1 data phần lớn có 4 câu (68%), N2 khớp spec (95% có 3 câu). Skill luôn follow spec (N1=3, N2=3), không bắt chước data N1 noise.

### Paragraph count (BẮT BUỘC)

| Level | Paragraph count | Lý do |
|-------|-----------------|-------|
| **N1** | **6–10** | Bài 1000-1200 chars, essay logic chặt chẽ với nhiều bước lập luận |
| **N2** | **5–8**  | Bài 900-1100 chars, editorial trung cấp |

> **⛔** Bài chỉ 3-4 paragraph ở 1000+ chars → quá đặc, khó đọc → REJECT. Chia nhỏ theo đoạn ý tưởng (hook → common view → luận điểm → nuance → counter → conclusion).
> **⛔** Quá > 10 paragraph → fragmentation, mỗi đoạn quá ngắn → REJECT.

### Flow text (KHÔNG `<br>` giữa câu)

> **⛔ LỖI PHỔ BIẾN**: Data gốc có 28-31% dùng `<br>` để chèn xuống dòng.
> **Output KHÔNG dùng `<br>` giữa câu** — dùng `<p>` thuần, text flow liên tục.

**Quy tắc:**
- **ĐÚNG**: `<p>Câu 1。Câu 2。Câu 3。</p>` — 1 paragraph 1 `<p>`
- **SAI → REJECT**: `<p>Câu 1。<br>Câu 2。</p>`
- **Ngắt paragraph** chỉ khi chuyển ý hoàn toàn khác (mỗi `<p>` = 1 bước logic)
- **Xuống hàng trong source code** chỉ để dễ đọc; HTML parser sẽ collapse whitespace

Đọc hiểu chủ đề **KHÔNG có exception `<br>`** nào — luôn dùng `<p>` thuần.

### CSS layout bắt buộc

- **Container**: `max-width: 800px`, `margin: 0 auto`, `padding: 56px 64px`, white background trên light gray body `#f9fafb`
- **Body**: `word-break: keep-all`, `line-break: strict`, `overflow-wrap: break-word`, `line-height: 2.0`
  (`keep-all` đảm bảo xuống dòng ở ranh giới từ, tránh cắt kanji compound)
- **Paragraph**: `<p>` với `text-indent: 1em` (chuẩn văn Nhật)
- **Font**: Noto Sans JP qua Google Fonts (KHÔNG dùng Tailwind CDN)

Template chi tiết xem `rules/technical.md` R9.

### Test mơ hồ (BẮT BUỘC)

> **Mỗi đoạn văn phải có DUY NHẤT 1 cách hiểu hợp lý cho mỗi câu hỏi.**
> Sau khi viết xong, đọc lại: "Câu hỏi này có thể hiểu theo cách thứ 2 không?" Nếu có → sửa lại.
> **Đặc biệt quan trọng với 3 câu multi-question**: các câu hỏi KHÔNG được test cùng 1 đoạn/ý. Câu 3 phải test tổng thể (thesis), không 1 đoạn riêng lẻ.

### Thesis rõ ràng (BẮT BUỘC)

> Đọc hiểu chủ đề = editorial/critique → bài **PHẢI có thesis rõ ràng** (主張) có thể tóm tắt trong 1-2 câu.
> Thesis có thể đặt: (a) đầu bài + khai triển, (b) giữa bài + khẳng định lại cuối, (c) cuối bài sau chuỗi lập luận, hoặc (d) ẩn nhưng có thể rút ra từ cách chọn luận cứ.
> **KHÔNG được** viết bài thuần kể chuyện / thuật sự không có luận điểm — đọc hiểu chủ đề yêu cầu văn luận thuyết có thesis.

---

## R7. Các dạng bài (document formats)

Đọc hiểu chủ đề có 4 dạng chính:

| # | Format | Level | Đặc điểm | Ví dụ chủ đề |
|---|--------|-------|----------|--------------|
| 1 | **Xã luận / phê bình cao cấp** | **N1** | 6-10 paragraph luận thuyết sâu, thesis + counter + kết luận, source line ≥ 64% | 言葉と思考, 現代社会のゆくえ, AIと人間 |
| 2 | **Tiểu luận triết học / văn hóa** | **N1** | 6-10 paragraph trừu tượng, đào sâu 1 khái niệm, annotation 1-2 | 存在と時間, 文化相対主義, 倫理学 |
| 3 | **Xã luận trung cấp (báo chí)** | **N2** | 5-8 paragraph editorial thực tế gần gũi, media-style | デジタル社会, 働き方改革, 食と健康 |
| 4 | **Tiểu luận cá nhân có luận điểm** | **N2** | 5-8 paragraph observation + reflection + thesis | 家族の変化, 現代の若者, 学校教育 |

Mỗi bài phải có đủ nội dung để:
- Gen 2 câu reference/meaning bám vào 2 đoạn khác nhau (có marker ①②)
- Gen 1 câu author_opinion/content_match kiểm tra thesis tổng thể

→ Do đó **minimum 5 paragraph** (N2) hoặc **6 paragraph** (N1).

### Source line convention

Format: `（[fake author]「[fake title]」による）` hoặc với media:

- `（[author]「[title]」○○新聞による）` (xã luận báo chí)
- `（[author]「[title]」による）` (tiểu luận độc lập)
- `（[author]「[title]」による。一部改変）` (có "一部改変")

**Ví dụ:**
- `（山口和彦「言葉と思考の未来」による）`
- `（田中由美「毎日の小さな選択」による）`
- `（佐藤健一「現代人の思考様式」朝陽新聞による）`

**Rule:**
- Author: tên Nhật tự chế (2-4 chữ, họ + tên)
- **⛔ TUYỆT ĐỐI KHÔNG** dùng tên tác giả thật (`村上春樹`, `夏目漱石`, `芥川龍之介`, `太宰治`, `吉本ばなな`...)
- Media: `朝○新聞`, `○○新聞`, `月刊○○` — tên fake, **KHÔNG** dùng tên báo có thật (`朝日`, `読売`, `毎日`, `日経`...)
- Title Nhật tự chế ngắn gọn phù hợp nội dung

### Tần suất source line theo data (khuyến nghị)

| Level | Tần suất thực tế | Có nên thêm? |
|-------|------------------|--------------|
| **N1** | **64%**         | **RẤT NÊN** — đặc trưng xã luận/phê bình cao cấp |
| **N2** | 26%             | Optional — thêm khi bài là xã luận báo chí |

### `(中略)` ellipsis — đặc trưng của đọc hiểu chủ đề

**Tần suất data**: N1=28%, N2=19%. Đây là visual element điển hình của dạng đọc hiểu chủ đề — dùng để mô phỏng việc lược bớt đoạn từ bản gốc editorial dài hơn.

Dùng để mô phỏng việc **lược bỏ 1 đoạn từ bản gốc** → tăng authenticity. Vị trí:
- **Giữa 2 đoạn logic chính** (sau "luận điểm" trước "kết luận")
- **KHÔNG** đặt ở đầu hoặc cuối bài
- **KHÔNG** quá 1 lần per bài (data hầu hết 0-1 lần)

Format HTML:
```html
<p class="ellipsis">（中略）</p>
```

Char counting: `（中略）` đếm ~3 chars sau strip whitespace.

---

## R8. Visual elements cho 3 câu hỏi

### Marker ①②③

**Tần suất data**: **N1=76%**, N2=48%.

Với 3 câu hỏi, **câu 3 cuối bài là author_opinion (tổng thể) → KHÔNG marker**. 2 câu đầu thường dùng marker ① và ②.

**Quy tắc**:
- Mỗi câu `question_reference` hoặc `question_meaning_interpretation` → 1 marker riêng trong bài (`①`, `②`)
- Marker đứng **ngay trước** cụm từ bị hỏi, kèm `<u>...</u>`:
  ```html
  <p>... <span class="marker">①</span><u>この柔軟性</u>こそが ...</p>
  ...
  <p>... <span class="marker">②</span><u>このような言語的不自由</u>は ...</p>
  ...
  <p>... [đoạn cuối không marker — Q3 author_opinion test ở đây] ...</p>
  ```
- Q1: `「①この柔軟性」とあるが、どのような柔軟性か。`
- Q2: `「②このような言語的不自由」とあるが、なぜ生じるのか。`
- Q3: `この文章で筆者が最も言いたいことはどれか。` (KHÔNG marker)

**Marker Strategy Cho 3 Câu Hỏi** (xem `references/html-patterns.md` section 4):
- **Pattern A** (phổ biến): 2 markers (①, ②) + câu cuối tổng kết không marker
- **Pattern B** (editorial): 1 marker (①) + 1 reason + câu cuối tổng kết
- **Pattern C** (ít dùng): 0 marker + 2 câu luận điểm + câu cuối tổng kết

### Underline `<u>`

**Tần suất data**: **N1=88%** (cao nhất series), N2=26%.

Skill dùng `<u>` cho **MỌI** câu hỏi `question_reference` và `question_meaning_interpretation` — cụm từ được hỏi phải được gạch chân và có marker đi kèm.

### Annotation `注`

**Tần suất data**: **N1=60%**, N2=51%. Bài editorial có nhiều thuật ngữ cần giải thích.

**Khuyến nghị**:
- **N1**: **RẤT NÊN** thêm 1-2 `注` (data 60%, nhiều thuật ngữ triết học / văn hóa)
- **N2**: Khuyến nghị 1-2 `注` (data 51%)

Format:
```html
<div class="annotations">
    <p>注1　決定論：原因によって結果が一意に定まるという考え方。</p>
    <p>注2　媒体：何かを伝えるもの。</p>
</div>
```

- Đặt **ngay trước** `<p class="source">` (nếu có)
- Mỗi 注 một `<p>` riêng, dùng full-width `：`
- Số thứ tự `注1`, `注2`
- Giải thích bằng **tiếng Nhật đơn giản** — KHÔNG tiếng Anh/Việt

### Source line

**Tần suất**: N1=64%, N2=26% (xem R7 bên trên).

### `(中略)` ellipsis

**Tần suất**: N1=28%, N2=19% — đặc trưng riêng đọc hiểu chủ đề (xem R7).

### Blank `[ ]` / `( 1 )` — gần như KHÔNG dùng

**Tần suất data**: N1=8%, N2=4%.

Đọc hiểu chủ đề rất hiếm khi dùng blank. Skill **KHÔNG khuyến khích** `question_fill_in_the_blank` cho đọc hiểu chủ đề.

### Cheatsheet — Visual elements per level

| Level | Marker ①② | `<u>` | 注 | Source | `(中略)` | Blank |
|-------|------------|-------|----|--------|---------|-------|
| **N1** | **RẤT CÓ (76%)** | **RẤT CÓ (88%)** | **NÊN (60%)** | **RẤT NÊN (64%)** | Đôi khi (28%) | Không (8%) |
| **N2** | Đôi khi (48%) | Đôi khi (26%) | NÊN (51%) | Optional (26%) | Optional (19%) | Không (4%) |

### Common errors

1. ❌ Có marker `①` trong bài nhưng KHÔNG có câu hỏi reference tương ứng → marker vô nghĩa
2. ❌ Câu hỏi hỏi `①...とあるが` nhưng bài không có marker `①` → câu hỏi không thể trả lời
3. ❌ Câu 3 cuối bài có marker → SAI (câu cuối = tổng thể, không 1 đoạn)
4. ❌ 3 câu hỏi trong 1 bài đều test cùng 1 đoạn → thiếu coverage
5. ❌ Source line dùng tên tác giả thật → vi phạm IP
6. ❌ N1 thiếu source line → giảm authenticity (data 64%)
7. ❌ Thiếu thesis rõ ràng → bài không đủ điều kiện đọc hiểu chủ đề, thành tùy bút
8. ❌ Dùng `<br>` giữa câu → sai, dùng `<p>` thuần
9. ❌ Abuse `(中略)` → ≤ 1 lần per bài
10. ❌ Bài chỉ 3-4 paragraph → quá đặc, chia 6-10 (N1) hoặc 5-8 (N2)
