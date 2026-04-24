# Rules: Từ vựng, Ngữ pháp & Furigana (R3, R4)

> **Scope**: Đọc hiểu chủ đề (主張理解 / thematic) — **CHỈ N1 & N2**.

## R3. Trình độ kiến thức (Kanji, Từ vựng, Ngữ pháp)

### Nguyên tắc tổng quát

| Level | Kanji/Từ vựng cốt lõi | Ngữ pháp cốt lõi |
|-------|----------------------|-------------------|
| **N2** | ~1000 kanji + ~6000 từ | ～に伴い, ～に基づき, ～を踏まえて, ～に限り, ～とはいえ, ～からこそ, ～かねる, ～ずにはいられない |
| **N1** | ~2000 kanji + ~10000 từ | ～いかんによらず, ～をもって, ～に先立ち, ～にほかならない, ～というものだ, ～ざるを得ない, ～に足る, keigo văn viết cao |

### Golden principle — "THAY TỪ, KHÔNG RẮC FURIGANA"

Nếu bài N2 dùng quá nhiều kanji N1 → **viết lại bằng từ N2**, không phải rắc furigana bừa bãi cho từ N1.

**Furigana dùng khi không có cách nào thay thế khác** — ví dụ thuật ngữ triết học / phê bình cao cấp không có từ N2 tương đương (`実存`, `媒体`, `疎外` ở N2).

### Phân loại từ trong bài

1. **Từ khóa của bài** (key terms): từ trung tâm mà thesis xoay quanh — **BẮT BUỘC** ở đúng level bài, KHÔNG cần furigana.
   VD: Trong bài N2 về 言葉 (ngôn ngữ) → chính từ 言葉 phải là N2, không rắc furigana.

2. **Từ ngữ cảnh** (context words): từ phụ hỗ trợ, hay xuất hiện (社会, 問題, 考える, 生活) → giữ đúng level.

3. **Từ chuyên môn / thuật ngữ** (jargon): từ không thể thay thế, vượt level → **có thể thêm furigana** hoặc **thêm 注 annotation** giải thích.

### Văn phong luận thuyết (BẮT BUỘC)

Đọc hiểu chủ đề = văn luận thuyết, nên **văn phong formal** (editorial/critique):

- **N1**: dùng nhiều keigo văn viết (`～であろう`, `～にほかならない`, `～ざるを得ない`, `～というものだ`). Câu dài, mệnh đề phụ nhiều.
- **N2**: formal trung cấp (`～に伴い`, `～を踏まえて`, `～とはいえ`, `～からこそ`). Câu vừa phải, có dùng `である` thay `だ`.

### Ruby count density per level (đọc hiểu chủ đề)

| Level | Above-level words | Ruby `<ruby>` expected |
|-------|-------------------|------------------------|
| **N2** | 0–5               | 0–8                    |
| **N1** | 0–3               | 0–5                    |

> **Lưu ý đặc thù**: Data gốc **N1 ruby = 0%**, **N2 ruby = 9%** — đề thi thực tế gần như KHÔNG dùng furigana. Skill vẫn cho phép furigana cho từ vượt level, NHƯNG **khuyến nghị giữ ít (0-3 cặp)**, ưu tiên 0.

> **Nguyên tắc**: ≥ 80% từ vựng/ngữ pháp phải ở đúng level. Ruby chỉ cho phần vượt level không thể tránh.

---

## R4. Furigana — Quy tắc & Kanji lookup

### R4.1 Compound Word Rule — CẤM dạng "Ab"

**LUÔN viết nguyên bộ kanji** rồi đặt furigana bao toàn bộ. **TUYỆT ĐỐI KHÔNG** tách nửa kanji nửa hiragana.

Chỉ chọn 1 trong 2:

1. **Full kanji + furigana**: `<ruby>媒体<rt>ばいたい</rt></ruby>`
2. **Full hiragana** (khi ở level thấp): `ばいたい`

**❌ CẤM**: `媒たい`, `友だち`, `拠てん`, `経けん`

**✅ Ngoại lệ Okurigana**: `<ruby>届<rt>とど</rt></ruby>く` — furigana chỉ phủ kanji, okurigana đứng riêng ngoài ruby.

### R4.2 Furigana Lookup Procedure

Bước 1: **Xác định level kanji** bằng `rules/jlpt_kanji.csv` (2150 kanji, mapped từ N5→N1).

Bước 2: **Nếu kanji > level bài** → thêm furigana:

```html
<ruby>媒体<rt>ばいたい</rt></ruby>
```

Bước 3: **Nếu kanji ≤ level bài** → KHÔNG thêm furigana.

### R4.3 Ví dụ áp dụng

| Từ | Level kanji | Bài N2 | Bài N1 |
|----|-------------|--------|--------|
| 媒体 (ばいたい) | N1 | `<ruby>媒体<rt>ばいたい</rt></ruby>` | 媒体 (không furigana) |
| 普遍的 (ふへんてき) | N2 | 普遍的 (không furigana) | 普遍的 (không furigana) |
| 実存 (じつぞん) | N1 | `<ruby>実存<rt>じつぞん</rt></ruby>` | 実存 (không furigana) |
| 経験 (けいけん) | N3 | 経験 (không furigana) | 経験 (không furigana) |
| 社会 (しゃかい) | N4 | 社会 (không furigana) | 社会 (không furigana) |

### R4.4 Furigana cho name riêng

Tên người/địa danh trong source line → **thêm furigana** nếu kanji có thể đọc nhiều cách:

- `<ruby>山口和彦<rt>やまぐちかずひこ</rt></ruby>`
- `<ruby>田中由美<rt>たなかゆみ</rt></ruby>`

Ở N2, tên đọc phổ biến có thể không cần furigana (`山田`, `佐藤`, `鈴木`).

### R4.5 Số lượng ruby cho đọc hiểu chủ đề

Bài dài 900-1200 chars, nhưng data thực tế **N1 ruby = 0%**, **N2 ruby = 9%** — skill giữ ruby ít nhất có thể.

**Dấu hiệu rắc furigana sai**:
- Bài N1 có > 5 ruby tag → chắc chắn sai level bài (bài N1 nên đã dùng kanji cao cấp)
- Bài N2 có > 8 ruby tag → chắc chắn sai level bài (viết lại bằng từ N2 thay vì rắc ruby)
- Có ruby cho từ cơ bản như `社会`, `問題`, `考える`, `人間` ở bài N2 → thừa
- Ruby tag kéo dài hơn 6 ký tự hiragana → từ quá vượt level, nên thay từ khác

### R4.6 Annotation `注` vs Furigana

Chọn một:

- **Furigana** cho từ có reading khó nhưng nghĩa dễ đoán từ ngữ cảnh
- **注 annotation** cho từ chuyên môn cần giải thích nghĩa

Ví dụ:
- `<ruby>憧れ<rt>あこがれ</rt></ruby>` → furigana OK (nghĩa dễ đoán)
- `決定論` N1 term trong bài N2 → thêm `注1 決定論：原因によって結果が一意に定まるという考え方` → không cần furigana

Cả hai cùng lúc OK nếu cần:
```html
<ruby>決定論<rt>けっていろん</rt></ruby>（注1）
...
<div class="annotations">
    <p>注1　決定論：原因によって結果が一意に定まるという考え方。</p>
</div>
```

> **Lưu ý đọc hiểu chủ đề**: Bài editorial/critique nhiều thuật ngữ → **khuyến nghị dùng `注` hơn furigana**. Data N1 annotation=60%, N2=51% (rất cao) vs ruby=0-9% (rất thấp). Viết thuật ngữ ở kanji full + thêm 注 giải thích nghĩa thay vì rắc furigana cho reading.
