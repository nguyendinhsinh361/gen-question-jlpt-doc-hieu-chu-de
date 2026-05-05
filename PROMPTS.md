# Prompt — Gen bài Đọc Hiểu Chủ Đề (JLPT 主張理解)

## Cách dùng

Copy prompt bên dưới, thay `{số}` rồi paste vào Claude hoặc Gemini.

**⛔ Scope chỉ 2 level**: **N1** (3 câu/bài, ~1000–1200 chars) và **N2** (3 câu/bài, ~900–1100 chars). N3/N4/N5 KHÔNG có kind này — KHÔNG gen.

**Đặc thù**: bài là **editorial / xã luận / phê bình** có thesis rõ ràng, KHÔNG phải tùy bút kể chuyện. Câu cuối BẮT BUỘC test thesis tổng thể.

> **🚨 ZERO-TOLERANCE QC**: Chỉ cần **1 tiêu chí FAIL** trong checklist 33 mục QC của SKILL.md → **fix ngay hoặc gen lại** trước khi sang bài tiếp.

---

## Prompt

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md rồi gen bài đọc hiểu chủ đề:
- N2: {số} bài (3 câu/bài, ~900–1100 chars)
- N1: {số} bài (3 câu/bài, ~1000–1200 chars)

⛔ CHỈ N1 và N2. Không gen N3/N4/N5.

Lưu CSV: sheets/samples_v1.csv. HTML: assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html.

═══ BƯỚC 0 — CHUẨN BỊ (1 lần) ═══
1. Đọc rules/rule_doc_hieu.md (rule giáo viên — source-of-truth, 11 phần). Áp dụng đặc biệt:
   - Phần 2.4 (Thể chia 文体の統一): N1/N2 → 普通形 (だ・である). Văn bản editorial + câu hỏi + 4 đáp án (mọi câu) thống nhất 普通形 toàn bộ.
   - Phần 3 (Furigana), Phần 4 (8 loại Q — đặc biệt author_opinion câu cuối), Phần 5 (5 loại bẫy chuẩn — đặc biệt Reversal/Scope/Mixing cho câu thesis).
2. Đọc rules/content.md + vocabulary.md + technical.md + questions.md.
3. Đọc rules/kanji_jlpt_sensei.csv (2495 kanji) để tra furigana.
4. Load 2 sample/level: scripts/load_references.py --level {LEVEL} --count 2.
5. Scan sheets/samples_v1.csv xem topic + label combo đã dùng.

═══ BƯỚC 1→5 — LẶP CHO TỪNG BÀI ═══
1. Gen _id = {LEVEL}_{uuid32}; chọn topic + label combo chưa/ít dùng (≥ 2 unique label per bài, lý tưởng ≥ 3).
2. Tag = **tiếng Anh** từ cột `en` của rules/topic.json (philosophy, cultural criticism, journalism...). TUYỆT ĐỐI không tiếng Việt/Nhật.
3. Gen HTML editorial: container 800px, line-height 2.0, word-break keep-all, padding 56px 64px, <p> thuần (mỗi <p> = 1 bước logic).
   - N1: 6–10 paragraph; N2: 5–8 paragraph. Có thesis rõ ràng (tóm tắt được trong 1-2 câu).
   - **Toàn bộ 普通形 (Phần 2.4)**. Furigana chỉ cho từ vượt level (cấm "Ab"); ưu tiên ÍT ruby (data N1=0%, N2=9%).
   - Source line: N1 RẤT NÊN có (data 64%) tự chế tên; N2 optional. CẤM tên thật (朝日/読売/村上春樹/夏目漱石).
   - Annotation 注: N1 nên có 1-2 (data 60%), N2 optional (51%) — giải thích bằng tiếng Nhật đơn giản.
   - (中略): tối đa 1 lần/bài, ở giữa, optional.
4. Gen 3 câu Q + 4 đáp án (newline \n, KHÔNG prefix):
   - **Q3 (câu cuối) BẮT BUỘC = question_author_opinion HOẶC question_content_match** test thesis tổng thể (KHÔNG marker). CẤM Q3 = reference/reason/meaning.
   - Q1 + Q2 test 2 đoạn KHÁC NHAU (có thể có marker ①②). Marker khớp Q reference, không marker dư.
   - Distractor ≥ 3 loại bẫy (Reversal/Detail swap/Scope/Misinterpretation/Part of truth/Mixing) dùng info THẬT từ bài.
5. Tạo CSV row bằng scripts/process_html.py. Fill Q&A bằng scripts/fill_qa.py (KHÔNG sửa CSV tay; tail rule auto-validate).

═══ BƯỚC 2 — QC ZERO-TOLERANCE (BẮT BUỘC) ═══
Tự đánh giá 33 mục checklist trong SKILL.md, log PASS/FAIL:
- A. HTML (12) + B. Content (6 — chủ đề editorial, từ vựng level, **toàn bộ 普通形**) + C. Q&A (11 — label, đáp án, paraphrase ≥4 từ N1 / ≥5 từ N2, explain VN+EN, self-solve khớp correct) + D. Coverage (4) + Thesis check
- **1 FAIL = fix ngay hoặc gen lại → refresh CSV (nếu sửa HTML) → QC lại từ đầu**. CẤM bỏ qua.

═══ HARD REJECT (gen lại ngay) ═══
- Q count khác 3 (slot 4-5 phải empty)
- Q3 KHÔNG phải author_opinion/content_match, hoặc Q3 test cục bộ 1 đoạn (không thesis)
- Char range ngoài: N1 1000–1200 | N2 900–1100
- Bài là tùy bút kể chuyện (không có thesis luận điểm)
- <ruby> thiếu <rt> hoặc <rt> rỗng; furigana dạng "Ab"
- Thể chia trộn lẫn (xuất hiện です・ます trong bài)
- Source dùng tên thật; 注 giải thích bằng Anh/Việt
- Tag tiếng Việt/Nhật; trong cùng level: trùng topic hoặc <2 unique label per bài

═══ CUỐI BATCH ═══
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py --validate --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv
```
