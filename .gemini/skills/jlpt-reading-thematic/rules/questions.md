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

### R5.7 Văn phong câu hỏi (thể động từ) theo level — BẮT BUỘC

Câu hỏi (`question_X`) và 4 lựa chọn (`answer_X`) phải dùng đúng **thể động từ** theo level:

| Level | Thể bắt buộc | Đặc trưng kết câu |
|-------|--------------|-------------------|
| **N1, N2, N3** | **Thể thường** (普通体 / だ・である調) | `〜か。` / `〜のはどれか。` / `〜と考えられるか。` (KHÔNG dùng です/ます) |
| **N4, N5** | **Thể ます** (です・ます調) | `〜ですか。` / `〜のはどれですか。` / `〜と思いますか。` |

**Quy tắc cứng:**
- Đọc hiểu chủ đề CHỈ có **N1 và N2** → cả 2 level đều dùng **thể thường**, KHÔNG được dùng です/ます
- Câu hỏi và **cả 4 đáp án** phải nhất quán cùng thể (không trộn lẫn)

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

### ⛔ Phân loại bẫy đáp án — 7 loại tổng (5 chuẩn + bẫy có điều kiện)

> **Nguồn**: rule_doc_hieu.md Phần 5 (5.1–5.7). Áp dụng cho dạng này: **N1 + N2**.
>
> **Quy tắc:** Trong 4 đáp án (1 đúng + 3 sai), 3 distractor PHẢI dùng **≥ 3 loại bẫy khác nhau** từ bảng dưới. Mỗi distractor phải dùng info/ý THẬT từ bài (trừ Fabrication có thể bịa cận-context).

| Loại bẫy | Mô tả | Ví dụ |
|----------|-------|-------|
| **① Reversal** ❌ | Đảo ngược ý nghĩa, kết luận, quan hệ nhân-quả từ bài | Bài: 「Aによって元気になった」 → Bẫy: 「Aの後で体が重くなった」 (đảo ngược) |
| **② Detail Swap** 🔄 | Dùng thông tin đúng nhưng gán sai ngữ cảnh (sai đối tượng/thời điểm/địa điểm) | Bài: 「Aは嵐山, Bは金閣寺」 → Bẫy: 「Aは金閣寺」 (đúng chi tiết, sai ngữ cảnh) |
| **③ Fabrication** 🎭 | Thêm thông tin hoàn toàn KHÔNG CÓ trong bài | Bài không nói X → Bẫy: 「XだからY」 — không kiểm chứng được |
| **④ Scope** 📐 | Đáp án quá RỘNG (over-generalization) hoặc quá HẸP so với ý bài | Bài: 「金閣寺で写真」 → Bẫy rộng: 「京都で写真」 / Bẫy hẹp: 「池のそばで写真」 |
| **⑤ Mixing** 🧩 | Kết hợp 2 thông tin đúng riêng lẻ thành ý sai (không tồn tại trong bài) | A đúng + B đúng nhưng không liên quan → Bẫy: 「AだからB」 |
| **⑦ Peripheral Source** 📎 | Đáp án lấy nội dung từ **chú thích 注 hoặc trích dẫn (による)** thay vì luận điểm chính của tác giả | Bài có 注 giải thích khái niệm triết học; Bẫy dùng định nghĩa đó làm câu trả lời cho câu thesis. Phân biệt với Fabrication: thông tin có trong bài (từ 注), nhưng KHÔNG phải lập luận tác giả. |

**📊 Phân bổ thực tế per level (từ data đề thi):**
- **N5–N4**: Reversal (cảm xúc/hành động) + Detail Swap đơn giản + Fabrication thông tin ngoài bài
- **N3**: Detail Swap (hoán đổi nhân vật/thời điểm) + Mixing (trộn lý do) + Fabrication tinh tế hơn
- **N2**: Scope (quá rộng/hẹp) + Reversal logic (concede trap: ý nhượng bộ vs ý chính) + Mixing (evidence + opinion)
- **N1**: Peripheral Source (nếu 注 dài) + Reversal sâu (premise vs conclusion) + Scope cực tinh tế (1 từ điều kiện) + Mixing phức tạp (2+ bước lập luận)

> **Áp dụng:** 5 loại chuẩn áp dụng cho cả N1 và N2. Peripheral Source ĐẶC BIỆT phổ biến ở N1 主張 (data 75–80% bài có 注 dài).

> **🔍 Peripheral Source — RẤT phổ biến ở N1 主張**: Data N1 主張 có 注 ở 75–80% bài, thường dài và chi tiết về thuật ngữ triết học. Distractor có thể lấy định nghĩa từ 注 làm câu trả lời cho câu hỏi về thesis. BẮT BUỘC self-check: distractor có lấy info từ 注 không? Nếu có và câu hỏi không phải về 注, đó là Peripheral Source — KHÔNG phải đáp án đúng.


### R6.3 Explanation format — 3 phần BẮT BUỘC (VN + EN)

> **Explanation không chỉ "có nội dung" — nó phải CHỨNG MINH câu hỏi + đáp án đúng có logic.**
> Đọc hiểu chủ đề là **editorial/critique 6-10 paragraph** với thesis rõ ràng. Explanation PHẢI **chỉ rõ paragraph**, trích cụ thể từ bài, đặc biệt cho câu cuối (thesis).

#### Phần 1 — Đáp án đúng (BẮT BUỘC trích bài + paragraph)
- Nêu rõ "Đáp án đúng: (X)" + nội dung paraphrase
- **Trích dẫn câu/đoạn cụ thể** trong bài (vd: "Paragraph 4 viết: `「...」`", "Câu cuối paragraph 7: `「...」`")
- **Bắt buộc chỉ rõ paragraph số mấy** — bài dài 6-10 paragraph, không đủ để nói "trong bài"
- Cho câu cuối (author_opinion / content_match): **trích thesis statement** từ paragraph mở đầu / kết / chuyển ý
- Cho câu reference/meaning (có marker ①②): **trích cả câu chứa marker** + 1-2 câu trước/sau làm context
- Nêu paraphrase: đáp án dùng từ đồng nghĩa nào với bài

#### Phần 2 — Đáp án sai (TỪNG đáp án + loại bẫy)
- Đi qua **TẤT CẢ 3 đáp án sai** (1 đáp án 1 dòng), không bỏ sót
- Mỗi đáp án sai phải nêu:
  1. **Loại bẫy** (Reversal / Detail swap / Scope / Misinterpretation / Part of truth / Mixing / Over-generalization)
  2. **Trích cụ thể** từ bài chứng minh sai + **chỉ rõ paragraph** (vd: "Paragraph 2 phê phán X nhưng đáp án 3 nói X tốt → đảo ngược")
- Câu cuối: distractor đặc thù **Scope** (hẹp hơn thesis) / **Mixing** (trộn 2 luận điểm) / **Misinterpretation** (sai nuance) — phải nêu rõ thesis chuẩn vs distractor sai ở đâu
- KHÔNG dùng câu chung chung — phải chỉ rõ paragraph, ý nào trong bài đủ để bác bỏ

#### Phần 3 — Tóm tắt chiến lược
- 1-2 câu: chiến lược giải dạng câu hỏi này (vd: "Câu cuối → trích thesis ở paragraph kết, loại trừ đáp án trái thesis / hẹp hơn / trộn ý")

### R6.4 Ví dụ explain VN cho câu cuối (thesis) — BÀI N1 mẫu (8 paragraph)

**Bài N1** (giả tưởng — 8 paragraph): Tác giả phê bình quan điểm "ngôn ngữ là vách giới hạn tư duy" (paragraph 1-2), phân tích cơ chế ngôn ngữ mở rộng qua phép ẩn dụ (paragraph 3-4), tái định nghĩa (paragraph 5), tiếp xúc đa văn hóa (paragraph 6-7), và kết luận (paragraph 8) rằng ngôn ngữ là "frontier" được mở rộng liên tục.

**Question 3** (`question_author_opinion` — câu cuối):
> この文章で筆者が最も主張したいことは何か。

**Answers** (4 options, no prefix):
```
言語が思考を完全に決定するため、語彙の限界がそのまま思考の限界となる
言語の限界は固定された壁ではなく、絶えず押し広げられていくものである
語彙が新しく作られなければ、人間の思考は前進することができない
言語は感情を伝える手段であり、文化的な背景に強く依存する
```

**correct_answer**: 2

**explain_vn**:
```
ĐÁP ÁN ĐÚNG (2): 言語の限界は固定された壁ではなく、絶えず押し広げられていくものである (Giới hạn ngôn ngữ không phải vách cố định mà là cái được mở rộng liên tục).
Paragraph 8 (kết) viết: 「言語の限界とは、克服されるべき壁ではなく、絶えず押し広げられてゆくフロンティアなのである」 — thesis tác giả: ngôn ngữ là "frontier" được mở rộng, không phải vách giới hạn. Paragraph 3-7 đã xây dựng các cơ chế mở rộng (ẩn dụ, tái định nghĩa, đa văn hóa). Đáp án 2 paraphrase đúng thesis tổng thể.

ĐÁP ÁN SAI:
(1) 言語が思考を完全に決定する... — Reversal: Paragraph 2 viết 「言語決定論は素朴すぎる見解にすぎない」 — tác giả phản đối determinism này ngay từ đầu. Đáp án 1 đảo ngược thesis hoàn toàn.
(3) 語彙が新しく作られなければ... — Scope (too narrow): Paragraph 5 có nói về "tạo từ mới" nhưng thesis bao quát hơn — gồm ẩn dụ (P3-4), tái định nghĩa (P5), đa văn hóa (P6-7). Đáp án 3 thu hẹp về 1 cơ chế.
(4) 言語は感情を伝える手段... — Mixing/Scope: Paragraph 1 nhắc "ngôn ngữ là phương tiện giao tiếp" như giả thuyết khởi đầu, nhưng tác giả KHÔNG luận về "biểu đạt cảm xúc" hay "phụ thuộc văn hoá" trong bài. Trộn ý ngoài + bịa phạm vi.

Tóm tắt: Câu cuối (author_opinion) → trích thesis paragraph kết (P8), so với options. Loại trừ: (a) đảo ngược thesis, (b) thu hẹp 1 cơ chế trong nhiều cơ chế, (c) trộn ý phụ + bịa phạm vi ngoài bài.
```

**explain_en**:
```
CORRECT ANSWER (2): 言語の限界は固定された壁ではなく、絶えず押し広げられていくものである (Language's limits are not a fixed wall but something continuously expanded).
Paragraph 8 (conclusion) states: 「言語の限界とは、克服されるべき壁ではなく、絶えず押し広げられてゆくフロンティアなのである」 — author's thesis: language is a "frontier" that expands, not a fixed wall. Paragraphs 3-7 build the expansion mechanisms (metaphor, redefinition, multicultural contact). Option 2 correctly paraphrases the overall thesis.

WRONG ANSWERS:
(1) 言語が思考を完全に決定する... — Reversal: Paragraph 2 states 「言語決定論は素朴すぎる見解にすぎない」 — the author rejects determinism from the start. Option 1 fully reverses the thesis.
(3) 語彙が新しく作られなければ... — Scope (too narrow): Paragraph 5 mentions "new word creation" but the thesis is broader — including metaphor (P3-4), redefinition (P5), multicultural contact (P6-7). Option 3 narrows to one mechanism.
(4) 言語は感情を伝える手段... — Mixing/Scope: Paragraph 1 mentions "language as communication tool" as initial premise, but the author does NOT discuss "expressing emotion" or "cultural dependence" anywhere. Mixes a secondary premise with fabricated scope.

Summary: Final author_opinion → quote thesis from closing paragraph (P8), compare to options. Eliminate (a) reversed thesis, (b) narrowed to one mechanism among many, (c) mixed secondary premise + fabricated scope.
```

**Explanation phải bằng cả 2 ngôn ngữ (VN + EN)** với cùng nội dung logic — không phải dịch máy.

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
