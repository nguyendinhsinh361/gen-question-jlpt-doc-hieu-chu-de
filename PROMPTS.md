# Prompt — Gen bài Đọc Hiểu Chủ Đề (JLPT 主張理解)

## Cách dùng

Copy prompt bên dưới, thay `{số}` rồi paste vào Claude hoặc Gemini.

**⛔ Scope chỉ 2 level**: **N1** (3 câu, ~1000–1200 chars) và **N2** (3 câu, ~900–1100 chars). Bài là **editorial / xã luận / phê bình** có thesis rõ ràng. Câu cuối BẮT BUỘC test thesis tổng thể.

> **🚨 ZERO-TOLERANCE WORKFLOW**: SKILL.md có **5 GATE bắt buộc** (0→1, 1→2, 2→3, 3→4, 4→5). Mỗi gate phải log `GATE X→Y PASSED`. **1 mục FAIL = sửa/gen lại → QC TỪ ĐẦU**, đến khi 33/33 PASS mới hoàn thành.

---

## Prompt

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md rồi gen bài đọc hiểu chủ đề:
- N2: {số} bài (3 câu, ~900–1100 chars)
- N1: {số} bài (3 câu, ~1000–1200 chars)

⛔ CHỈ N1 và N2. Lưu CSV: sheets/samples_v1.csv. HTML: assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html.

🔒 5 GATE bắt buộc — KHÔNG QUA = KHÔNG SANG BƯỚC TIẾP. Log explicit GATE X→Y PASSED.

═══ BƯỚC 0 — CHUẨN BỊ (1 lần) → GATE 0→1 ═══
Đọc đầy đủ:
- rules/rule_doc_hieu.md (Phần 2.4 thể chia toàn 普通形, Phần 5 — 7 loại bẫy + **Peripheral Source RẤT phổ biến cho N1 主張 với 注 dài (75-80% bài)**, Phần 9.4 N2 主張 + Phần 10.5 N1 主張)
- rules/{content,vocabulary,technical,questions}.md + rules/kanji_jlpt_sensei.csv
- Load 2 sample/level: scripts/load_references.py --level {LEVEL} --count 2
- Scan sheets/samples_v1.csv
GATE 0→1: tick 6/6 → log "GATE 0→1 PASSED".

═══ BƯỚC 1 — GEN HTML + 3 Q+A → GATE 1→2 ═══
1. _id = {LEVEL}_{uuid32}
2. Tag = **tiếng Anh** từ rules/topic.json (philosophy, cultural criticism...)
3. Gen HTML editorial: container 800px, line-height 2.0, padding 56px 64px, <p> thuần (mỗi <p> = 1 bước logic)
   - N1: 6–10 paragraph; N2: 5–8 paragraph. Có thesis rõ ràng (tóm tắt được trong 1-2 câu)
   - **Toàn 普通形 (Phần 2.4)**. Furigana chỉ vượt level (cấm "Ab"); ưu tiên ÍT ruby (data N1=0%, N2=9%)
   - Source line: N1 RẤT NÊN có (data 64%, tự chế tên — CẤM 朝日/読売/村上春樹). N2 optional
   - Annotation 注: N1 nên có 1-2 (data 60%), N2 optional (51%) — tiếng Nhật đơn giản
4. Gen 3 Q + 4 đáp án (newline \n, KHÔNG prefix):
   - **Q3 BẮT BUỘC = author_opinion HOẶC content_match** test thesis tổng thể (KHÔNG marker). CẤM Q3 = reference/reason/meaning
   - Q1 + Q2 test 2 đoạn KHÁC NHAU (có marker ①②). Marker khớp Q, không marker dư
   - Distractor ≥ 3 loại bẫy + **Peripheral Source self-check cho N1**: distractor có lấy info từ 注 không?
5. Tạo CSV bằng process_html.py + fill_qa.py (tail rule auto-validate)
GATE 1→2: tick 5/5 → log "GATE 1→2 PASSED".

═══ BƯỚC 2-3 — QC 33 MỤC → GATE 2→3 + GATE 3→4 ═══
GATE 2→3: cam kết check ĐẦY ĐỦ 33 mục → log "GATE 2→3 PASSED".
Đánh giá 33 mục: A. HTML 12 + B. Content 6 + C. Q&A 11 (paraphrase ≥4 từ N1 / ≥5 N2, explain VN+EN, self-solve khớp) + D. Coverage 4 + Thesis check.
**Peripheral Source check N1**: nếu distractor lấy định nghĩa từ 注 cho Q về thesis → REJECT.
GATE 3→4: liệt kê FAIL + diagnosis → log "GATE 3→4 PASSED".

═══ BƯỚC 4-5 — SỬA + LẶP → GATE 4→5 ═══
- Fix HTML → `--refresh`. Fix Q&A → fill_qa.py
- ≥ 50% FAIL / self-solve FAIL / Q3 không phải author_opinion-content_match / char Hard Reject → **GEN LẠI** (giữ _id)
- Quay lại GATE 2→3 → QC 33/33 TỪ ĐẦU
- Tối đa 5 vòng → báo user
GATE 4→5: 33/33 PASS + --validate clean → log "🎉 ALL PASSED (33/33) + GATE 4→5 PASSED" → bài tiếp.

═══ HARD REJECT (gen lại ngay) ═══
- Q count khác 3 (slot 4-5 phải empty); Q3 không phải author_opinion/content_match HOẶC test cục bộ 1 đoạn
- Char range ngoài: N1 1000–1200 | N2 900–1100
- Bài là tùy bút kể chuyện (không có thesis luận điểm rõ ràng)
- <ruby> thiếu <rt>; furigana "Ab"; thể chia có です・ます
- Source dùng tên thật; 注 giải thích bằng Anh/Việt
- Tag tiếng Việt/Nhật; trùng topic; <2 unique label per bài

═══ CUỐI BATCH ═══
python3 .claude/skills/jlpt-reading-thematic/scripts/process_html.py --validate --html-dir assets/html/doc_hieu_chu_de --csv sheets/samples_v1.csv
```
