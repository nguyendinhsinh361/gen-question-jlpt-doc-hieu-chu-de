# Prompt — Gen bài Đọc Hiểu Chủ Đề (JLPT 主張理解)

Copy prompt bên dưới, thay `{số}` rồi paste vào Claude hoặc Gemini.

CHỈ N1 (3 câu, ~1000–1200 chars) và N2 (3 câu, ~900–1100 chars). Bài là editorial / xã luận / phê bình có thesis rõ ràng.

## Prompt

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md và tuân thủ đầy đủ workflow + 5 GATE.

Gen bài đọc hiểu chủ đề (CHỈ N1 và N2):
- N2: {số} bài (3 câu)
- N1: {số} bài (3 câu)

Lưu CSV: sheets/samples_v1.csv
Lưu HTML: assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html
```

---

## Prompt QC hậu kỳ

Chạy QC trên CSV đã gen — auto-check scripts + LLM review + auto-fix tối đa 3 vòng.

```
Đọc .claude/skills/jlpt-reading-thematic-post-qc/SKILL.md và chạy QC đầy đủ theo workflow.

CSV cần QC: sheets/samples_v1.csv

Phạm vi (chọn 1):
- ALL: toàn bộ CSV (CHỈ N1 và N2)
- LEVEL: chỉ rows có level = {N1|N2}
- ID: chỉ row có _id = {LEVEL}_{uuid}

Quy trình BẮT BUỘC:
1. BƯỚC 1 — Auto-check: chạy post_qc.py + check_furigana + check_spacing + check_csv_fields + check_answer_punctuation
2. BƯỚC 2 — LLM review: L1-L16 (đặc thù 主張: L10 stem 「最も」, L11 cấu trúc 5 phần luận thuyết, L12 bẫy Evidence-as-claim/Concede/Criticized-view, L13 N1 fill_in HIẾM ~10-15%)
3. BƯỚC 3 — Cross-batch: B1-B5 (đặc biệt B5 (中略) rate N1 ~40-45%, N2 ~28-35%)
4. BƯỚC 4 — Auto-fix: row FAIL → sửa tối thiểu phần lỗi (KHÔNG gen lại toàn bộ), lặp tối đa 3 vòng. Q3 BẮT BUỘC test thesis (author_opinion/content_match), nếu sai → bắt buộc sửa câu cuối.

Báo cáo theo format trong SKILL.md.
```

---

## Prompt với topic chỉ định

Chỉ định topic cho từng level (CHỈ N1 và N2). Topic dùng tiếng Anh từ cột `en` của `rules/topic.json`. Đặc thù 主張: bài là editorial / xã luận / phê bình có thesis rõ ràng — topic nên thuộc nhóm `philosophy`, `cultural criticism`, `journalism`, `social commentary`, `aesthetics`, `ethics`.

```
Đọc .claude/skills/jlpt-reading-thematic/SKILL.md và tuân thủ đầy đủ workflow + 5 GATE.

Gen bài đọc hiểu chủ đề với số bài + topic chỉ định cho từng level (CHỈ N1 và N2, mỗi bài 3 câu):
- N2: 2 bài | topic: cultural criticism
- N1: 3 bài | topic: philosophy

Quy tắc:
- Topic PHẢI có trong cột `en` của `rules/topic.json` — kiểm tra trước, không có → DỪNG báo user.
- Topic PHẢI cho phép viết editorial có thesis (tránh topic thuần kể chuyện như "travel diary", "food review").
- CSV field `tag` của mỗi row = topic của level đó.
- Nhiều bài cùng level → giữ chung topic NHƯNG mỗi bài có thesis KHÁC NHAU (khía cạnh khác).
- Q3 BẮT BUỘC test thesis tổng thể (author_opinion/content_match).

Lưu CSV: sheets/samples_v1.csv
Lưu HTML: assets/html/doc_hieu_chu_de/{LEVEL}_{uuid}.html
```
