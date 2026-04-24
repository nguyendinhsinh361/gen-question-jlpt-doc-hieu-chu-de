# Rules: Câu hỏi, Đáp án & Explain (R5, R6)

> **Scope**: Đọc hiểu chủ đề (主張理解 / thematic) — **CHỈ N1 & N2**, mỗi bài **đúng 3 câu**.

## R5. Câu hỏi — Labels & Combos

### R5.1 Catalog 7 labels

Tất cả label **BẮT BUỘC** có prefix `question_` (snake_case). Dùng lại 7 labels chuẩn của skill đọc hiểu:

| Label | Khi nào dùng | Phù hợp |
|-------|--------------|---------|
| `question_author_opinion` | Hỏi luận điểm tổng thể, 筆者の主張 | **BẮT BUỘC câu cuối cả N1 và N2** (ưu tiên) |
| `question_content_match` | Chọn câu phù hợp nội dung tổng thể | **Câu cuối N1/N2** (alternative cho author_opinion) |
| `question_reason_explanation` | Hỏi nguyên nhân/lý do cụ thể | N1/N2 (rất phổ biến cho câu giữa) |
| `question_reference` | Hỏi đại từ/cụm từ chỉ định (với marker ①②) | N1/N2 (câu 1 hoặc câu 2) |
| `question_meaning_interpretation` | Hỏi nghĩa câu/cụm cụ thể | N1/N2 (câu 1 hoặc câu 2) |
| `question_content_mismatch` | Chọn câu KHÔNG phù hợp | Ít dùng — dễ gây nhầm, cân nhắc kỹ |
| `question_fill_in_the_blank` | Điền từ vào ô trống | **HIẾM** ở đọc hiểu chủ đề (data N1=8%, N2=4%) — không khuyến khích |

> **⛔ QUAN TRỌNG**: Label phải có **prefix `question_`**. Sai prefix (dùng `reference` thay `question_reference`) → invalid CSV.

### R5.2 Rule cứng CÂU CUỐI (BẮT BUỘC cả N1 và N2)

Cả 2 level: **Câu 3 PHẢI là `question_author_opinion` hoặc `question_content_match`** (kiểm tra thesis tổng thể).

**CẤM** câu cuối là:
- `question_reference` (test 1 đoạn → sai tinh thần thesis)
- `question_reason_explanation` (test logic cục bộ)
- `question_meaning_interpretation` (test 1 cụm)
- `question_fill_in_the_blank`
- `question_content_mismatch`

**Khuyến nghị mạnh**: Ưu tiên `question_author_opinion` cho câu cuối vì spec JLPT nhấn "overall intended points and ideas" (thesis / main argument).

### R5.3 Distribution combo 3 câu per level

Cả N1 và N2 đều **3 câu/bài** với cùng spec focus. Các combo gợi ý:

#### N1 (3 câu) — spec focus "overall intended points and ideas"

| # | Combo | Q1 | Q2 | Q3 (cuối) |
|---|-------|----|----|-----------|
| 1 | **phổ biến nhất** | `question_reference` (marker ①) | `question_reason_explanation` | **`question_author_opinion`** |
| 2 | essay analytic | `question_meaning_interpretation` (①) | `question_reason_explanation` | **`question_author_opinion`** |
| 3 | dual marker | `question_reference` (①) | `question_reference` (②) | **`question_author_opinion`** |
| 4 | alternative cuối | `question_reference` (①) | `question_reason_explanation` | `question_content_match` |

#### N2 (3 câu) — spec identical với N1

| # | Combo | Q1 | Q2 | Q3 (cuối) |
|---|-------|----|----|-----------|
| 1 | **phổ biến nhất** | `question_reference` (marker ①) | `question_reason_explanation` | **`question_author_opinion`** |
| 2 | reference heavy | `question_reference` (①) | `question_reference` (②) | **`question_author_opinion`** |
| 3 | meaning focused | `question_meaning_interpretation` (①) | `question_reason_explanation` | **`question_author_opinion`** |
| 4 | alternative cuối | `question_reference` (①) | `question_reason_explanation` | `question_content_match` |

> **Diversity rule**: Trong 1 bài phải có ≥ 2 label khác nhau. Không được dùng 3 label giống nhau (vd 3 câu đều là `question_reference`).

### R5.4 Câu cuối = thesis author

Câu 3 kiểm tra khả năng **tổng hợp toàn bài**, không phải 1 đoạn. Đáp án đúng phải phản ánh thesis tác giả.

**Ví dụ câu hỏi cuối phổ biến (Nhật)**:
- `筆者の主張と一致するものはどれか。`
- `この文章で筆者が最も言いたいことはどれか。`
- `筆者の考えと合っているものはどれか。`
- `この文章全体のテーマとして最も適切なものはどれか。`
- `筆者が最も訴えたいことは何か。`

Câu cuối **KHÔNG** được tham chiếu marker ①② (vì test tổng thể).

### R5.5 Question quality rules

1. Câu hỏi answer được **trong bài**, không kiến thức nền
2. Mỗi câu có **4 đáp án plausible**, 1 đúng
3. **Các câu hỏi trong 1 bài test 3 ĐOẠN/Ý KHÁC NHAU** — Q1/Q2 test 2 đoạn giữa, Q3 test tổng thể
4. Marker `①②` trong HTML **phải match** câu hỏi reference (nếu Q1 hỏi `①...` thì bài phải có `<span class="marker">①</span>`)
5. `question_image_X` **luôn empty** (đọc hiểu chủ đề là văn thuần)
6. Câu cuối **KHÔNG** có marker (test tổng thể)

### R5.6 Paraphrasing rule

Distractor **không được copy nguyên đoạn từ bài**:

| Level | Max chuỗi copy liên tục |
|-------|-------------------------|
| **N1** | 4 từ |
| **N2** | 5 từ |

Quá giới hạn → distractor quá dễ hoặc đáp án đúng bị lộ vì copy.

---

## R6. Định dạng câu trả lời & Explanation

### R6.1 Answer format — NO prefix

**4 options** tách nhau bằng `\n` (newline), **KHÔNG** có prefix `1.`, `2.`, `①`, `1)`:

**✅ ĐÚNG:**
```
言語は思考を単純に決定するという立場
言語は思考の柔軟な足場を与えるという立場
言語は思考を完全に拘束するという立場
言語と思考は無関係であるという立場
```

**❌ SAI → REJECT:**
```
1. 言語は思考を単純に決定するという立場
2. 言語は思考の柔軟な足場を与えるという立場
...
```

Khi lưu vào CSV column `answer_X`, option tách nhau bằng `\n`:
```
answer_1 = "言語は思考を単純に決定するという立場\n言語は思考の柔軟な足場を与えるという立場\n言語は思考を完全に拘束するという立場\n言語と思考は無関係であるという立場"
```

**Column `correct_answer_X`** = chuỗi `"1"`, `"2"`, `"3"`, `"4"` (1-based, match vị trí trong `answer_X`).

> **CHÚ Ý**: Data gốc JSON dùng `correctAnswer` 0-based. Khi convert sang CSV phải **+1** để thành 1-based.

### R6.2 Distractor trap types

Đọc hiểu chủ đề yêu cầu distractor **tinh vi nhất** trong series vì văn abstract. 6 trap type:

1. **Reversal** — đáp án ngược với thesis/luận điểm bài
2. **Detail swap** — đổi chủ ngữ/đối tượng/quan hệ giữa các luận điểm
3. **Scope** — mở rộng (over-generalization) hoặc thu hẹp (too-narrow) so với thesis
4. **Misinterpretation** — hiểu sai sắc thái mệnh đề phụ (vd `としても` → `だから`)
5. **Part of truth** — chỉ đúng 1 bước luận điểm, không đúng toàn bài / thesis
6. **Mixing** — trộn 2 luận điểm thành 1 ý sai (đặc trưng thematic vì bài nhiều luận điểm)

Riêng câu cuối (thesis test), distractor nên dùng **Scope**, **Misinterpretation**, **Mixing** (gần thesis nhưng sai nuance/scope).

### R6.3 Explanation format (3 phần BẮT BUỘC)

Mỗi câu hỏi có 2 cột: `explain_vn_X` (tiếng Việt) và `explain_en_X` (tiếng Anh). Mỗi explain **3 phần** rõ ràng:

#### Phần 1 — Đáp án đúng
- Đáp án số mấy, trích dẫn **đoạn/câu** trong bài để support
- Paraphrase lại ý đáp án nói gì (không copy cả cụm từ đáp án)
- Cho câu cuối: trích **thesis statement** chính

#### Phần 2 — Đáp án sai + bẫy
- Từng đáp án sai (3 options còn lại), nêu rõ:
  - Bẫy gì (Reversal / Scope / Mixing / ...)
  - Vì sao sai (trái thesis / mở rộng sai / trộn 2 luận điểm)

#### Phần 3 — Tóm tắt chiến lược
- 1-2 câu tổng kết: "Phải **tổng hợp toàn bài** / nhận diện **thesis** / loại trừ ý **cục bộ**..."

### R6.4 Ví dụ explain VN cho câu cuối (thesis)

```
Đáp án đúng: 2. Paragraph cuối tác giả kết luận "言語の限界とは、克服されるべき壁ではなく、絶えず押し広げられてゆくフロンティアなのである" — thesis tác giả là ngôn ngữ như 'fronteir' được mở rộng liên tục, không phải vách giới hạn.

Đáp án sai:
- 1. Reversal — đáp án 1 nói "ngôn ngữ quyết định hoàn toàn tư duy", trái thesis (tác giả phản đối determinism này ngay từ paragraph 2).
- 3. Scope (too narrow) — chỉ nói tới "từ mới" nhưng thesis bao quát hơn: cả "phép ẩn dụ" + "tái định nghĩa" + "tiếp xúc đa văn hóa".
- 4. Mixing — trộn ý "ngôn ngữ là công cụ giao tiếp" (paragraph 1) với "thể hiện cảm xúc" (không có trong bài) → trộn sai.

→ Chiến lược: Câu cuối luôn TEST THESIS TỔNG THỂ. Phải trích câu kết luận cuối và loại trừ đáp án (a) trái thesis, (b) hẹp hơn thesis, (c) trộn 2 điểm.
```

### R6.5 Câu hỏi đặc thù đọc hiểu chủ đề

Khi gen câu hỏi, dùng các form Nhật chuẩn JLPT:

- **Reference (①②)**: `「①〇〇」とあるが、何を指すか。` / `「①〇〇」とあるが、どのような〇〇か。`
- **Meaning**: `「①〇〇」とあるが、どういう意味か。` / `筆者が「〇〇」と述べているのは、どのような状況を指しているか。`
- **Reason**: `筆者は、なぜ〇〇と考えているのか。` / `筆者が〇〇について〇〇と述べるのはなぜか。`
- **Author opinion (cuối)**: `この文章で筆者が最も言いたいことはどれか。` / `筆者の主張と一致するものはどれか。`
- **Content match (cuối)**: `この文章全体のテーマとして最も適切なものはどれか。` / `筆者の考えと合っているものはどれか。`

### R6.6 Câu cuối — không test 1 đoạn (CẤM tuyệt đối)

```
❌ SAI: Câu 3 dùng marker ③ test paragraph 5
❌ SAI: Câu 3 hỏi "nguyên nhân của 〇〇" (reason) — đây là test cục bộ
❌ SAI: Câu 3 hỏi "③とあるが、何を指すか" — reference
✅ ĐÚNG: Câu 3 hỏi "この文章で筆者が最も言いたいこと" — tổng thể, không marker
```
