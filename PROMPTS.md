# PROMPTS.md — Đọc Hiểu Chủ Đề

Prompt templates để gọi LLM gen content cho skill `jlpt-reading-thematic` (主張理解 / đọc hiểu chủ đề).

**Scope chỉ 2 level**: N1 (3 câu/bài, ~1000-1200 ký tự) và N2 (3 câu/bài, ~900-1100 ký tự). N3/N4/N5 KHÔNG có kind này — đừng gen.

**Workload cao nhất của series** (bài dài abstract + distractor tinh vi nhất). Batch size khuyến nghị: **3-4 bài/lần**.

Cách dùng: copy prompt theo level, thay các `{PLACEHOLDER}` bằng giá trị thực tế, feed vào Claude/Gemini.

## 0. Common System Prompt (cả N1 và N2)

```
Bạn là trợ lý chuyên gen dữ liệu JLPT 主張理解 (đọc hiểu chủ đề).

Rule BẤT BIẾN:
1. Gen đoạn văn tiếng Nhật đúng Target Range:
   - N1: 1000-1200 ký tự
   - N2:  900-1100 ký tự
   (Đếm không whitespace, không tính <rt>, <style>, <script>.)
2. CHỈ gen cho N1 hoặc N2. N3/N4/N5 không có kind này.
3. Bài PHẢI là editorial / phê bình / luận thuyết — có thesis (主張) rõ ràng.
   KHÔNG gen bài kể chuyện / hồi ký / thư cá nhân / narrative thuần.
4. HTML template: <!DOCTYPE html>, Noto Sans JP qua Google Fonts,
   <div class="passage"> max-width 800px (rộng nhất 4 phase), chứa <p> với
   text-indent 1em. KHÔNG dùng <br> giữa câu. Dùng <p> thuần.
5. Furigana RẤT HIẾM:
   - N1: tối đa 3 cặp <ruby>/<rt> (data 0%)
   - N2: tối đa 5 cặp (data 9%)
   Chỉ cho từ vượt level. Cấm dạng "Ab" (nửa kanji nửa hiragana).
6. Mỗi bài có SỐ CÂU HỎI CHÍNH XÁC: 3 câu (cho cả N1 và N2).
7. Trong 1 bài, ≥ 2 question_label khác nhau.
8. Các câu hỏi trong 1 bài test các ĐOẠN/Ý KHÁC NHAU của bài.
9. CÂU CUỐI (câu 3) BẮT BUỘC:
   - Label phải là `question_author_opinion` hoặc `question_content_match`
   - Test **thesis / main idea tổng thể**, KHÔNG test đoạn riêng lẻ
   - Ưu tiên mạnh `question_author_opinion`
10. Nếu dùng marker ①②③ cho câu reference, MARKER phải xuất hiện trong HTML
    ngay trước cụm từ được hỏi, và câu hỏi dẫn bằng「①cụm từ」とあるが.
11. `(中略)` optional — có thể dùng 1 lần/bài giữa 2 khối logic lớn.
    Format: <p class="ellipsis">（中略）</p>
12. Distractor TINH VI NHẤT series: sai nuance, sai mức độ, trộn 2 luận điểm,
    paraphrase sai, polarity đảo. KHÔNG đáp án sai kiểu ngô nghê.
13. Giải thích VN + EN cho TỪNG CÂU (tại sao đáp án đúng + tại sao 3 đáp án
    kia sai, chỉ rõ line/paragraph support).
14. Tên tác giả trong source line PHẢI tự chế, KHÔNG dùng tác giả có thật.
    KHÔNG dùng tên báo có thật (朝日/読売/毎日).
15. Paragraph count:
    - N1: 6-10 paragraph
    - N2: 5-8 paragraph

Output format: JSON với các field:
{
  "id": "{LEVEL}_{uuid32hex}",
  "level": "N1" hoặc "N2",
  "tag": "triết học ngôn ngữ",
  "html": "<!DOCTYPE html>...",
  "questions": [
    {
      "label": "question_reference",
      "question": "①「...」とあるが、何を指すか。",
      "answers": ["A option", "B option", "C option", "D option"],
      "correct": 2,
      "explain_vn": "...",
      "explain_en": "..."
    },
    ...TỔNG CỘNG 3 phần tử, phần tử cuối label = author_opinion hoặc content_match...
  ]
}
```

## 1. Prompt N1 — Xã luận / phê bình cao cấp, 3 câu, câu cuối = author_opinion

```
Gen 1 bài JLPT N1 đọc hiểu chủ đề về chủ đề {TOPIC} (ví dụ: triết học ngôn ngữ,
phê bình văn hóa sâu, xã luận chính sách/kinh tế, luận về bản chất con người,
phân tích hệ thống giáo dục, khoa học nhận thức, phê bình công nghệ cao cấp).

Yêu cầu cụ thể:
- Độ dài: 1000-1200 ký tự (count không whitespace, không <rt>)
- Thể loại: xã luận / tiểu luận / phê bình — CÓ thesis (主張) rõ, KHÔNG kể chuyện
- Văn phong: rất formal, luận thuyết cao cấp
  (～いかんによらず, ～をもって, ～に先立ち, ～をものともせず, ～にほかならない,
   ～というものだ, ～ざるを得ない, ～に足る, ～にたえない, ～というほかない)
- Cấu trúc: 6-10 paragraph (KHÔNG dùng <br>)
- Furigana: tối đa 3 cặp <ruby>/<rt>, chỉ cho từ vượt N1
- Annotation 注 khuyến nghị (data 60%): 1-2 chú thích dưới <div class="annotations">
- Source line RẤT NÊN có (data 64%): `（{tên tác giả tự chế}「{tên sách/bài}」による）`
  hoặc `（{tác giả}「{title}」○○新聞による）` (nếu là xã luận báo)
- Underline <u> NHIỀU (data 88%) — dùng cho MỌI cụm từ được hỏi
- Marker ①② (data 76%) — dùng cho 1-2 câu reference
- `(中略)` optional (data 28%) — có thể dùng để lược đoạn giữa bài

BẮT BUỘC: Đúng 3 câu hỏi với ≥ 2 labels khác nhau.

Combo câu hỏi đề xuất (chọn 1):
  A. (phổ biến nhất)
     Q1: question_reference (marker ①) — test 1 đoạn/cụm cụ thể
     Q2: question_reason_explanation — test logic chain
     Q3: question_author_opinion — **BẮT BUỘC** tổng kết thesis
  B. (essay analytic)
     Q1: question_meaning_interpretation (①) — test hiểu nuance
     Q2: question_reason_explanation
     Q3: question_author_opinion
  C. (dual marker)
     Q1: question_reference (①)
     Q2: question_reference (②)
     Q3: question_author_opinion
  D. (alternative)
     Q1: question_reference (①)
     Q2: question_reason_explanation
     Q3: question_content_match (tổng thể)

**Rule cứng**: câu 3 cuối cùng LUÔN là question_author_opinion (ưu tiên mạnh)
hoặc question_content_match. CẤM question_reference / question_reason ở câu cuối.
N1 focus "overall intended points and ideas" — phải có 1 câu tổng thể.

Reference with marker pattern:
  HTML: <p>...<span class="marker">①</span><u>この柔軟性</u>...</p>
  Question: 「①この柔軟性」とあるが、どのような柔軟性か。
  (label = question_reference hoặc question_meaning_interpretation)

Reason pattern (test lý do cụ thể):
  Question: 筆者が...と考えているのはなぜか。
  Question: 筆者が...を問題視するのはなぜか。

Author opinion pattern (câu cuối tổng thể):
  Question: 筆者が最も言いたいことはどれか。
  Question: この文章で筆者が最も訴えたいことはどれか。
  Question: 筆者の主張と一致するものはどれか。
  Question: この文章全体のテーマとして最も適切なものはどれか。

4 đáp án bắt buộc TINH VI — N1 distractor:
  - Paraphrase sai ở 1 keyword
  - Đúng nội dung nhưng chệch mức độ (絶対/しばしば, すべて/多く)
  - Trộn 2 luận điểm của bài thành 1 ý sai
  - Ngược polarity (肯定↔否定)
  - Cắt xén điều kiện/phạm vi
  - Generalize sai (bài nói 1 trường hợp, distractor → "luôn luôn")

**Thesis placement**: Phát biểu thesis rõ ở ít nhất 1 trong 3 vị trí:
  - Đầu bài (hook + thesis statement ngay para 1-2)
  - Cuối bài (build-up + thesis ở para cuối)
  - Khung "common view → phản đề → thesis" (phản biện lý luận)

Output JSON theo Common System Prompt, mảng "questions" có ĐÚNG 3 phần tử,
questions[2].label ∈ {"question_author_opinion", "question_content_match"}
(ưu tiên author_opinion).
```

## 2. Prompt N2 — Xã luận / phê bình trung cấp, 3 câu, câu cuối = author_opinion

```
Gen 1 bài JLPT N2 đọc hiểu chủ đề về chủ đề {TOPIC} (ví dụ: xã luận công nghệ,
văn hóa đời sống hiện đại, phê bình giáo dục, ngôn ngữ và xã hội, lối sống thế hệ
trẻ, gia đình hiện đại, môi trường, AI và xã hội, khoa học đại chúng).

Yêu cầu cụ thể:
- Độ dài: 900-1100 ký tự
- Thể loại: xã luận vừa / tiểu luận có luận điểm — CÓ thesis, KHÔNG kể chuyện thuần
- Văn phong: formal văn viết trung cấp
  (～に伴い, ～に基づき, ～を踏まえて, ～に限り, ～とはいえ, ～からこそ, ～わけで,
   ～ないではいられない, ～ずにはいられない, ～に応じて, ～において)
- Cấu trúc: 5-8 paragraph (KHÔNG <br>; dùng <p> thuần)
- Furigana: tối đa 5 cặp, cho từ N1 rare
- Annotation 注 khuyến nghị (data 51%): 1-2 chú thích
- Source line optional (data 26%) — có thể thêm nếu topic là xã luận báo
- Underline <u> trung bình (data 26%) — dùng cho cụm từ được hỏi
- Marker ①② (data 48%) — dùng cho 1-2 câu reference
- `(中略)` optional (data 19%) — có thể dùng để lược đoạn

BẮT BUỘC: Đúng 3 câu hỏi với ≥ 2 labels khác nhau.

Combo câu hỏi đề xuất (chọn 1):
  A. (phổ biến nhất)
     Q1: question_reference (marker ①) — test 1 đoạn cụ thể
     Q2: question_reason_explanation — test lý do
     Q3: question_author_opinion — **BẮT BUỘC** tổng kết thesis
  B. (reference heavy)
     Q1: question_reference (①)
     Q2: question_reference (②)
     Q3: question_author_opinion
  C. (meaning focused)
     Q1: question_meaning_interpretation (①)
     Q2: question_reason_explanation
     Q3: question_author_opinion
  D. (alternative cuối)
     Q1: question_reference (①)
     Q2: question_reason_explanation
     Q3: question_content_match (tổng thể)

**Rule cứng**: câu 3 LUÔN là question_author_opinion (ưu tiên) hoặc
question_content_match. CẤM question_reference / question_reason ở câu cuối.

Reference pattern:
  HTML: <p>...<span class="marker">①</span><u>こうした変化</u>...</p>
  Question: ①「こうした変化」とあるが、どのような変化か。

Reason pattern:
  Question: 筆者は、なぜ...と考えているのか。
  Question: ...のはどうしてか。

Author opinion pattern (câu cuối):
  Question: この文章で筆者が最も言いたいことはどれか。
  Question: 筆者の考えと合っているものはどれか。
  Question: 筆者の主張として最も適切なものはどれか。

Ví dụ câu hỏi N2 phổ biến (theo data):
  - ①「...」とあるが、どのようなことか。
  - ②「...」とあるが、何を指しているか。
  - 筆者は...についてどう考えているか。
  - 本文の内容と合うものはどれか。(alternative cho câu cuối)

4 đáp án N2 distractor sai ở:
  - Paraphrase sai 1 nuance
  - Đảo nhân-quả (A→B ↔ B→A)
  - Tuyệt đối hoá (すべて/常に vs thường/多く)
  - Trộn 2 ý thành 1
  - Cắt xén điều kiện

**Thesis placement**: N2 thesis thường rõ hơn N1, phát biểu ở:
  - Para 1-2 (hook + thesis)
  - Para cuối (build-up + khẳng định thesis)

Output JSON theo Common System Prompt, mảng "questions" có ĐÚNG 3 phần tử,
questions[2].label ∈ {"question_author_opinion", "question_content_match"}
(ưu tiên author_opinion).
```

## 3. Batch Prompt — Gen nhiều bài 1 lần

```
Gen {N} bài JLPT {LEVEL} đọc hiểu chủ đề. Yêu cầu đa dạng:

1. Topic: chọn từ {N_TOPIC} nhóm khác nhau:
   N1:
   - Triết học ngôn ngữ / bản chất con người
   - Phê bình văn hóa / văn học
   - Xã luận chính sách / kinh tế
   - Phân tích hệ thống giáo dục cao cấp
   - Khoa học nhận thức / tâm lý học
   - Phê bình công nghệ / AI cao cấp
   - Xã hội học / đạo đức học
   N2:
   - Xã luận công nghệ / AI và đời sống
   - Văn hóa đời sống / gia đình hiện đại
   - Phê bình giáo dục (trung cấp)
   - Ngôn ngữ và xã hội
   - Lối sống thế hệ trẻ
   - Môi trường / sức khỏe
   - Khoa học đại chúng

2. Số câu hỏi per bài: BẮT BUỘC ĐÚNG 3 câu cho cả N1 và N2

3. question_label:
   - Mỗi bài ≥ 2 labels khác nhau
   - **Câu cuối BẮT BUỘC = question_author_opinion (ưu tiên) hoặc question_content_match**
   - Batch-level: ≥ 3 labels khác nhau trong cả batch

4. Mỗi bài có _id riêng: {LEVEL}_{uuid32hex}.

5. Độ dài nằm trong Target Range:
   - N1: 1000-1200
   - N2:  900-1100

6. Các câu hỏi trong cùng bài phải test các ĐOẠN/Ý khác nhau.

7. Visual elements:
   - N1: underline 88%+, marker 76%+, annotation 1-2, source line 64%+
   - N2: marker 48%+, annotation 1-2, source line optional

8. Mỗi bài phải có thesis rõ ràng (tóm tắt được trong 1-2 câu).

Batch size khuyến nghị: **3-4 bài/lần** (workload cao nhất của series).

Output: array của {N} JSON objects theo Common System Prompt.
```

## 4. Fix Prompt — Khi bài fail validate

### Case: UNDER_TARGET (trên HARD_REJECT nhưng dưới TARGET)

```
Bài {ID} có {CHARS} ký tự, dưới Target Range của {LEVEL} ({LO}-{HI}).

Bổ sung thêm {NEEDED} ký tự bằng một trong các cách (theo thứ tự ưu tiên):
1. Thêm 1-2 câu văn vào paragraph giữa (mở rộng luận điểm, KHÔNG đưa ý mới trái)
2. Thêm 1 paragraph nuance / counter-argument addressed (nối flow logic)
3. Thêm ví dụ cụ thể cho 1 luận điểm đã có
4. Thêm 1 chú thích 注1/注2 ở <div class="annotations">

KHÔNG thêm paragraph có ý trái ngược thesis — phải flow nối tiếp.
Giữ nguyên: _id, tất cả questions, đáp án đúng, thesis.
Marker ①②③ đã dùng phải giữ nguyên vị trí (nếu không sẽ break câu hỏi reference).

Output: JSON object mới (cùng schema, cùng _id, cùng questions), đã chỉnh độ dài.
```

### Case: OVER_TARGET (> HI + 100)

```
Bài {ID} có {CHARS} ký tự, vượt xa Target Range của {LEVEL} ({LO}-{HI}).

Rút ngắn còn {LO}-{HI} ký tự bằng cách:
1. Loại bỏ 1 paragraph có nội dung tangential (không liên quan trực tiếp đến 3 câu hỏi)
2. Rút gọn câu dài thành 1-2 câu ngắn
3. Bỏ annotation/source line thừa
4. Thêm `(中略)` thay cho 1 khối paragraph dài mà ý đã rõ

KHÔNG được xoá đoạn chứa marker ①②③ nếu câu hỏi đang reference marker đó.
KHÔNG xoá paragraph có thesis.

Giữ nguyên: _id, tất cả questions, đáp án đúng.

Output: JSON object mới (cùng schema, cùng _id, cùng questions).
```

### Case: HARD_REJECT

```
Bài {ID} có {CHARS} ký tự, DƯỚI Hard Reject của {LEVEL} ({THRESHOLD}).
KHÔNG chỉnh sửa — GEN LẠI TỪ ĐẦU.

Yêu cầu:
  {LEVEL} Target Range {LO}-{HI} ký tự.
  Số câu: 3 (spec).
  Paragraph count: {PARAGRAPH_RANGE}.
  Topic: {TOPIC}.
  Labels đề xuất: {LABEL_COMBO}.
  Câu cuối: question_author_opinion (ưu tiên) hoặc question_content_match.
  Thesis: phải rõ ràng, tóm tắt được trong 1-2 câu.

Output: JSON object mới hoàn toàn.
```

### Case: UNSUPPORTED_LEVEL

```
Bài {ID} có level {LEVEL} nhưng kind "đọc hiểu chủ đề" CHỈ dành cho N1 và N2.

Xử lý:
1. Nếu nội dung phù hợp N1/N2 → sửa _id thành {N1|N2}_{uuid_mới},
   điều chỉnh độ dài + văn phong theo level mới.
2. Nếu nội dung không phù hợp (ví dụ là essay/thư dài N3) →
   chuyển sang skill khác (jlpt-reading-long-passage cho N3 đoạn văn dài).

Không commit vào CSV của đọc hiểu chủ đề cho đến khi level đã chuẩn hoá.
```

### Case: Sai số câu hỏi (warning)

```
Bài {ID} đang có {ACTUAL_Q} câu hỏi, nhưng đọc hiểu chủ đề yêu cầu ĐÚNG 3 câu.

Fix:
- Nếu dư câu (≥ 4): giữ 2 câu test đoạn cụ thể nhất + 1 câu author_opinion tổng thể.
  Bỏ câu lặp ý hoặc test cùng đoạn với câu khác.
- Nếu thiếu câu (≤ 2): thêm câu test đoạn CHƯA được hỏi.
  Nếu thiếu câu tổng thể → thêm question_author_opinion.

Giữ nguyên: _id, HTML, đáp án các câu còn lại.

Output: JSON object mới, "questions" có ĐÚNG 3 phần tử.
```

### Case: Câu cuối không phải author_opinion/content_match (warning)

```
Bài {ID} là {LEVEL} đọc hiểu chủ đề, nhưng câu cuối (câu 3) có label = {ACTUAL_LABEL}
thay vì question_author_opinion/question_content_match.

**Đây là vi phạm NGUYÊN TẮC BẤT BIẾN** — câu cuối của đọc hiểu chủ đề PHẢI
test thesis tổng thể, không được test đoạn riêng lẻ.

Fix (giữ 2 câu đầu nguyên vẹn):
1. Chuyển câu 3 thành question_author_opinion:
   - Template: 筆者が最も言いたいことはどれか。
   - Template: 筆者の主張と一致するものはどれか。
   - Template: この文章全体のテーマとして最も適切なものはどれか。
2. HOẶC chuyển thành question_content_match:
   - Template: この文章の内容と合っているものはどれか。
   - Template: 本文の内容に合うものはどれか。

4 đáp án plausible phải bao phủ thesis bài. Đáp án đúng = thesis paraphrase.
Distractor = luận điểm phụ hoặc paraphrase sai của thesis.

Giữ nguyên: _id, HTML, câu 1-2.

Output: JSON object mới.
```

### Case: Các câu hỏi cùng test 1 đoạn (warning)

```
Bài {ID} có câu {Q_A} và câu {Q_B} cùng test 1 đoạn/luận điểm trong bài.

Fix: chuyển 1 trong 2 câu sang test đoạn/luận điểm KHÁC.
Ưu tiên:
- Câu reference → chuyển sang đoạn chưa hỏi có marker ②
- Câu reason → chuyển sang lý do cho luận điểm khác

Giữ nguyên câu 3 (author_opinion/content_match), _id, HTML.
Nếu cần thêm marker ② vào HTML → update HTML cho khớp.

Output: JSON object mới.
```

### Case: Dạng "Ab"

```
Bài {ID} có dạng "Ab" (nửa kanji nửa hiragana) sai quy tắc furigana.

Cụm vi phạm: "{VIOLATION}" (ví dụ: 週かん, 友だち)

Fix: chọn 1 trong 2 cách:
1. Full kanji + <ruby>: <ruby>週間<rt>しゅうかん</rt></ruby>
2. Full hiragana: しゅうかん

Giữ nguyên phần còn lại, chỉ sửa cụm vi phạm.

Output: JSON object mới (cùng _id, cùng questions, HTML đã fix).
```

### Case: Marker không match câu hỏi

```
Bài {ID} có câu hỏi「{Q_NUM}」tham chiếu marker {MARKER} nhưng HTML không có marker đó.

Fix: thêm marker vào HTML:
  <span class="marker">{MARKER}</span><u>{PHRASE}</u>
ngay trước hoặc bao quanh cụm từ được hỏi.

Hoặc: đổi câu hỏi không dùng marker, chỉ quote cụm từ:
  「{PHRASE}」とあるが、〜

Giữ nguyên các phần còn lại.

Output: JSON object mới.
```

### Case: Bài là narrative / kể chuyện (không có thesis)

```
Bài {ID} là narrative / câu chuyện / thư cá nhân — không có thesis rõ ràng.
Đọc hiểu chủ đề BẮT BUỘC là editorial / luận thuyết / phê bình có thesis.

Fix: GEN LẠI từ đầu với cấu trúc editorial:
  - Para 1-2: Hook + common view
  - Para 3-5: Luận điểm + evidence + counter
  - Para cuối: Thesis khẳng định

Topic giữ nguyên nếu phù hợp, hoặc chuyển sang topic editorial rõ hơn.

Output: JSON object mới hoàn toàn.
```

## 5. Quality Check Prompt (gọi sau batch)

```
Kiểm tra chất lượng batch {N} bài JLPT {LEVEL} đọc hiểu chủ đề. Cho mỗi bài:

1. Level = N1 hoặc N2:                           PASS / FAIL
2. Độ dài (target {LO}-{HI}):                    PASS / FAIL ({CHARS} chars)
3. Số câu hỏi = 3:                               PASS / FAIL ({ACTUAL_Q})
4. Paragraph count ({PARAGRAPH_RANGE}):          PASS / FAIL
5. ≥ 2 labels khác nhau trong bài:               PASS / FAIL
6. Câu 3 = author_opinion/content_match:         PASS / FAIL (actual: {LAST_LABEL})
7. Các câu hỏi test đoạn KHÁC NHAU:              PASS / FAIL
8. Marker ①② match câu hỏi (nếu có):             PASS / FAIL
9. Bài có thesis rõ ràng (tóm tắt được):         PASS / FAIL
10. Thể loại = editorial/critique (KHÔNG kể):    PASS / FAIL
11. Furigana đúng quy tắc (không "Ab"):          PASS / FAIL
12. Mỗi câu chỉ 1 đáp án đúng:                   PASS / FAIL
13. Distractor tinh vi level-phù hợp:            PASS / FAIL
14. Câu hỏi answer được từ trong bài:            PASS / FAIL
15. explain_vn + explain_en non-empty:           PASS / FAIL
16. Source line (nếu có) dùng tên fake:          PASS / FAIL
17. Source line ở N1 khuyến nghị (64%):          PASS / WARN
18. Annotation 注 khuyến nghị (60%+):            PASS / WARN

Batch-level:
- ≥ 3 question_label khác nhau trong batch?     YES / NO
- ≥ 2 tag (topic) khác nhau?                    YES / NO
- Tất cả _id unique?                            YES / NO
- {N} bài × 3 = {TOTAL_Q} câu hỏi — đúng?       YES / NO
- 100% câu cuối là author_opinion/content_match? YES / NO

Output: bảng markdown 1 row per bài + summary batch-level.
```

## 6. Variables reference

| Placeholder | Giá trị mẫu |
|-------------|-------------|
| `{LEVEL}`   | N1 hoặc N2 (CHỈ 2 level) |
| `{TOPIC}`   | triết học ngôn ngữ, xã luận công nghệ, phê bình văn hóa... |
| `{N}`       | Số bài (khuyến nghị 3-4) |
| `{N_TOPIC}` | Số nhóm topic (thường 2-3) |
| `{LO}, {HI}` | Target Range (N1: 1000-1200, N2: 900-1100) |
| `{THRESHOLD}` | Hard Reject (N1: 950, N2: 850) |
| `{CHARS}`   | Char count thực tế |
| `{NEEDED}`  | Số ký tự cần bổ sung |
| `{ID}`      | `{LEVEL}_{uuid32hex}` |
| `{VIOLATION}` | Cụm vi phạm rule furigana |
| `{ACTUAL_Q}` | Số câu thực tế (spec luôn 3) |
| `{ACTUAL_LABEL}` | Label thực tế của câu cuối |
| `{LAST_LABEL}` | Label câu cuối cùng của bài |
| `{LABEL_COMBO}` | Combo labels đề xuất (xem section level) |
| `{PARAGRAPH_RANGE}` | N1: 6-10, N2: 5-8 |
| `{Q_NUM}` / `{Q_A}` / `{Q_B}` | 1, 2, 3 (số thứ tự câu hỏi) |
| `{MARKER}` | ①, ②, ③ |
| `{PHRASE}` | Cụm từ được gạch chân |
| `{TOTAL_Q}` | Tổng câu hỏi kỳ vọng cả batch (N × 3) |
