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
