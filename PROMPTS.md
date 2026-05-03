# Prompt — Gen bài Đọc Hiểu Chủ Đề (JLPT 主張理解)

## Cách dùng

Copy prompt bên dưới, thay `{số}` rồi paste vào Claude hoặc Gemini.
SKILL.md chứa workflow + checklist QC. rules/ chứa chi tiết. Prompt chỉ cần nói **cái gì** và **bao nhiêu**.

**⛔ Scope chỉ 2 level**: **N1** (3 câu/bài, ~1000–1200 chars) và **N2** (3 câu/bài, ~900–1100 chars). N3/N4/N5 KHÔNG có kind này — KHÔNG gen.

**Đặc thù**: bài là **editorial / xã luận / phê bình** có thesis rõ ràng, KHÔNG phải tùy bút kể chuyện. Câu cuối BẮT BUỘC test thesis tổng thể.

---

## Prompt ngắn (khuyên dùng)

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md rồi gen bài đọc hiểu chủ đề:
- N2: {số} bài (3 câu/bài, ~900–1100 chars)
- N1: {số} bài (3 câu/bài, ~1000–1200 chars)

⛔ CHỈ N1 và N2. KHÔNG gen N3/N4/N5.

Lưu CSV vào sheets/samples_v1.csv. HTML lưu vào assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html.
Làm đúng theo SKILL.md — từng bài một, đọc rules/ trước khi gen.

⛔ Q COUNT BẮT BUỘC: cả N1 và N2 = 3 câu (fill question_{1,2,3}, slot 4–5 empty).

⛔ TAIL RULE — câu cuối (Q3) BẮT BUỘC là `question_author_opinion` HOẶC `question_content_match`:
- Câu cuối test THESIS TỔNG THỂ, KHÔNG có marker
- CẤM câu cuối = reference / reason / meaning (test cục bộ 1 đoạn)

⛔ COVERAGE RULE: Q1 + Q2 test 2 đoạn KHÁC NHAU (có thể có marker ①②). Q3 test thesis tổng thể.

⛔ FORMAT BẮT BUỘC: bài là **editorial / xã luận / phê bình** có:
- Thesis rõ ràng (tóm tắt được trong 1-2 câu)
- 6-10 paragraph (N1) / 5-8 paragraph (N2), mỗi <p> = 1 bước logic
- KHÔNG phải tùy bút kể chuyện thuần

⛔ ĐA DẠNG — BẮT BUỘC:
1. Đọc rules/rule_doc_hieu.md (rule giáo viên — section 3-5 áp dụng trực tiếp) + rules/content.md (chủ đề + char range + format) + rules/questions.md (label combo).
2. Scan sheets/samples_v1.csv xem topic + label combo đã dùng.
3. Trong cùng level: KHÔNG trùng topic; mỗi bài dùng ≥ 2 question_label khác nhau (lý tưởng ≥ 3).
4. Tag **tiếng Anh** từ cột `en` của `rules/topic.json` (vd: philosophy, cultural criticism, journalism). TUYỆT ĐỐI không tiếng Việt/Nhật.

⛔ FURIGANA — chỉ cho từ VƯỢT level. Cấm dạng "Ab". Tra rules/kanji_simplified.csv. Data thực tế: N1 = 0%, N2 = 9% ruby — ưu tiên ÍT ruby.

⛔ SOURCE LINE: N1 RẤT NÊN có (data 64%), N2 optional. Tên tác giả/báo TỰ CHẾ (KHÔNG dùng tên thật như 朝日/読売/村上春樹/夏目漱石).

⛔ ANNOTATION (注): N1 nên có 1-2 chú thích (data 60%), N2 optional (51%). Giải thích bằng tiếng Nhật đơn giản.

⛔ (中略): tối đa 1 lần/bài, ở giữa bài (không đầu/cuối). Optional.

Sau khi gen xong mỗi bài, tự QC checklist 33 mục trong SKILL.md (HTML + CSV + multi-question coverage + thesis check → log PASS/FAIL). 1 FAIL = sửa → QC lại. Tất cả PASS mới sang bài tiếp.
Điền Q&A bằng scripts/fill_qa.py (KHÔNG sửa CSV bằng tay).
Sửa HTML = chạy lại process_html.py --refresh.
Verify cuối: python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py --validate --html-dir assets/html/doc_hieu_chu_de
```

---

## Prompt có thêm ràng buộc (khi cần kiểm soát chất lượng)

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md rồi gen bài đọc hiểu chủ đề:
- N2: {số} bài | N1: {số} bài

⛔ CHỈ N1 và N2. KHÔNG gen N3/N4/N5.

Lưu CSV vào sheets/samples_v1.csv. HTML lưu vào assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html.
Trước khi gen:
1. Đọc rules/rule_doc_hieu.md (rule giáo viên — source-of-truth cho vocab/grammar/distractor)
2. Đọc rules/content.md + rules/vocabulary.md + rules/technical.md + rules/questions.md
3. Đọc rules/kanji_simplified.csv để tra level kanji
4. Đọc 1-2 sample: scripts/load_references.py --level {LEVEL} --count 2
5. Scan sheets/samples_v1.csv xem topic + label combo nào đã dùng

⛔ Q COUNT: cả N1 và N2 = 3 câu. Slot 4-5 empty.

⛔ TAIL RULE — câu 3 PHẢI là `question_author_opinion` hoặc `question_content_match` (test thesis tổng thể, KHÔNG marker). CẤM câu 3 = reference/reason/meaning.

⛔ MULTI-QUESTION COVERAGE:
- Q1 + Q2 test 2 đoạn KHÁC NHAU (có thể có marker ①②)
- Q3 test THESIS TỔNG THỂ (không marker, không cục bộ 1 đoạn)
- Marker trong HTML khớp câu hỏi reference/meaning. Không marker dư

⛔ FORMAT EDITORIAL — BẮT BUỘC:
- Bài có thesis rõ ràng (tóm tắt được trong 1-2 câu)
- Editorial / phê bình / xã luận có chuỗi luận điểm. KHÔNG tùy bút kể chuyện
- Paragraph: N1 6–10 đoạn, N2 5–8 đoạn (mỗi <p> = 1 bước logic)
- Container 800px, line-height 2.0, word-break keep-all, padding 56px 64px

⛔ ĐA DẠNG CHỦ ĐỀ + LABEL:
- Trong cùng level: KHÔNG trùng topic; mỗi bài ≥ 2 question_label khác nhau
- Cross-level: ưu tiên topic chưa xuất hiện
- Tag **tiếng Anh** từ cột `en` của `rules/topic.json` (philosophy, cultural criticism, journalism, etc.) — TUYỆT ĐỐI không tiếng Việt/Nhật

⛔ FURIGANA ZERO-TOLERANCE:
- Kanji vượt level PHẢI có <ruby><rt>
- Cấm dạng "Ab". Chọn 1 trong 2: full kanji + furigana HOẶC full hiragana
- Ưu tiên ÍT ruby — N1 ≤ 5, N2 ≤ 8

⛔ SOURCE LINE — N1 rất nên có, N2 optional:
- Tự chế tên tác giả/báo (KHÔNG dùng 朝日/読売/毎日/日経/村上春樹/夏目漱石)
- Format: （著者名「タイトル」による） hoặc tương tự

⛔ ANNOTATION (注): N1 nên có 1-2, N2 optional. Tiếng Nhật đơn giản, KHÔNG tiếng Anh/Việt.

⛔ (中略): optional, tối đa 1 lần/bài, ở giữa bài.

⛔ ĐÁP ÁN — 4 options newline-separated, KHÔNG prefix "1.", "①", "1)".

Yêu cầu chất lượng câu hỏi (đọc hiểu chủ đề distractor TINH VI nhất):
- Question_label dùng prefix `question_`. ≥ 2 unique labels per bài (lý tưởng ≥ 3)
- Distractor đa dạng ≥ 3 loại bẫy (Reversal / Detail swap / Scope / Misinterpretation / Part of truth / Mixing)
- Mỗi distractor PHẢI dùng info thật từ bài, KHÔNG bịa
- Paraphrase: đáp án đúng KHÔNG copy nguyên văn ≥ 4 từ liên tiếp (N1) / 5 từ (N2)
- Self-solve verify: tự giải từng câu, KHỚP correct_answer_i
- Explanation 3 phần (VN + EN)
- Câu 3 (thesis): distractor thường dùng Scope / Mixing / Misinterpretation

Sau khi gen xong mỗi bài, BẮT BUỘC tự QC theo 33 mục checklist trong SKILL.md:
- Phần A HTML (12) + B Content (6) + C Q&A (11) + D Coverage (4) + Thesis check
- 1 FAIL = sửa → refresh CSV (nếu sửa HTML) → QC lại

Lưu ý kỹ thuật:
- Điền Q&A bằng scripts/fill_qa.py (KHÔNG edit CSV tay; tail rule auto-validate)
- Refresh CSV sau sửa HTML: process_html.py --refresh
- Verify cuối: process_html.py --validate --html-dir assets/html/doc_hieu_chu_de
```
