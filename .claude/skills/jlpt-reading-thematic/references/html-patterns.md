# HTML Patterns — Đọc Hiểu Chủ Đề

Cụ thể hoá template HTML cho N1 (xã luận / phê bình cao cấp) và N2 (xã luận / phê bình trung cấp). Đặc trưng dạng này: container **800px**, paragraph 6-10 (N1) hoặc 5-8 (N2), thường dùng `(中略)` lược đoạn, câu cuối BẮT BUỘC là author_opinion/content_match.

## 1. Base HTML Template (áp dụng cả N1 & N2)

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Japanese title ngắn]</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: #f9fafb;
            color: #111827;
            line-height: 2.0;
            word-break: keep-all;
            line-break: strict;
            overflow-wrap: break-word;
            margin: 0;
            padding: 40px 20px;
        }
        .passage {
            max-width: 800px;          /* container rộng cho văn luận thuyết nhiều đoạn */
            margin: 0 auto;
            background: white;
            padding: 56px 64px;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            font-size: 16px;
        }
        .passage p { margin: 0 0 1em 0; text-indent: 1em; }
        .passage .no-indent { text-indent: 0; }
        .ellipsis {
            text-align: center;
            font-size: 0.9em;
            color: #6b7280;
            margin: 0.8em 0;
            text-indent: 0;
        }
        .marker { font-weight: bold; color: #1e40af; }
        .annotations {
            margin-top: 2em;
            padding-top: 1em;
            border-top: 1px dashed #d1d5db;
            font-size: 0.9em;
            color: #374151;
            line-height: 1.7;
        }
        .annotations p { margin: 0.3em 0; text-indent: 0; }
        .source {
            margin-top: 1.2em;
            text-align: right;
            font-size: 0.88em;
            color: #4b5563;
            text-indent: 0;
        }
        ruby { ruby-align: center; ruby-position: over; vertical-align: baseline; }
        ruby rt { font-size: 0.55em; color: #374151; letter-spacing: 0.02em; line-height: 1; vertical-align: top; }
        u { text-decoration: underline; text-decoration-thickness: 1.5px; }
    </style>
</head>
<body>
<div class="passage">
    <!-- content here -->
</div>
</body>
</html>
```

## 2. N1 Template — Xã luận / phê bình cao cấp (6-10 paragraph, 1000-1200 chars)

Cấu trúc essay luận thuyết chuẩn:

```
<p>① Hook / context — nêu vấn đề hoặc common view</p>
<p>② Tác giả bác bỏ / phản đề — đặt thesis ban đầu</p>
<p>③ Supporting argument 1 — có thể chứa marker ① cho Q1 reference</p>
<p>④ Supporting argument 2 — logic chain</p>
<p class="ellipsis">（中略）</p>                   <!-- optional, 28% data có -->
<p>⑤ Counter-argument / nuance — có thể chứa marker ② cho Q2</p>
<p>⑥ Synthesis / implication</p>
<p>⑦ Conclusion — tác giả chốt thesis (Q3 author_opinion test ở đây — KHÔNG marker)</p>
<div class="annotations"><p>注1 ...</p></div>  <!-- 60% data có - khuyến nghị -->
<p class="source">（[fake author]「[fake title]」による）</p>  <!-- 64% data có - khuyến nghị -->
```

Ví dụ cụ thể N1 — xã luận phê bình ngôn ngữ:

```html
<div class="passage">
    <p>言葉は単なる意思伝達の道具ではなく、人間の思考そのものを形づくる装置である。ある言語を習得するとは、その言語が備える概念の枠組みを内面化することであり、世界の見え方が特定の方向に色づけられることを意味する。</p>
    <p>しかし、言語と思考の関係を単純な決定論として語ることには慎重でなければならない。言語は思考を拘束するのではなく、むしろ思考のための足場を与えるものだと考えるほうが実態に近い。話し手は、手持ちの語彙を組み替えたり、新しい比喩を生み出したりすることで、既存の枠組みを超えていくことができるからである。</p>
    <p><span class="marker">①</span><u>この柔軟性</u>こそが、言語を単なる閉じた体系から、絶え間なく更新される生きた媒体へと変えているといえる。文学や哲学における新語の発明や、科学における用語の再定義は、すべてこの柔軟性に依拠している。</p>
    <p>もちろん、柔軟性にも限界はある。ある概念をそれにふさわしい語で表現できない場合、話し手はしばしば曖昧な言い換えでその概念を示すほかない。<span class="marker">②</span><u>このような言語的不自由</u>は、個人の思考に思わぬ制約を課すことがある。</p>
    <p class="ellipsis">（中略）</p>
    <p>それでも筆者は、言語を通じた思考の豊かさを悲観する必要はないと考えている。新しい概念に対して新しい語を編み出す営みは、文化の発展とともに絶え間なく続けられてきた。言語の限界とは、克服されるべき壁ではなく、絶えず押し広げられてゆくフロンティアなのである。</p>
    <p>また、異文化との接触も言語の拡張に大きな役割を果たしてきた。翻訳という営みは、単なる置き換えではなく、二つの思考枠組みを突き合わせて新しい理解を生む過程でもある。</p>
    <p>重要なのは、自分の使う言葉に対して敏感であることだ。ある語を選ぶとき、同時に他の語を捨てていることに気づき、なぜその語でなければならないのかを問う姿勢こそが、思考を深める糸口となる。</p>
    <div class="annotations">
        <p>注1　決定論：原因によって結果が一意に定まるという考え方。</p>
    </div>
    <p class="source">（山口和彦「言葉と思考の未来」による）</p>
</div>
```

→ Q1 (reference, marker ①): `①「この柔軟性」とあるが、どのような柔軟性か。`
→ Q2 (reason_explanation): `筆者が言語を通じた思考の豊かさについて悲観する必要はないと考えているのはなぜか。`
→ Q3 (author_opinion): `この文章で筆者が最も言いたいことはどれか。`

## 3. N2 Template — Xã luận / phê bình trung cấp (5-8 paragraph, 900-1100 chars)

Cấu trúc editorial vừa:

```
<p>① Hook / vấn đề xã hội (thường thực tế, gần gũi hơn N1)</p>
<p>② Common view → tác giả nhận xét</p>
<p>③ Luận điểm + evidence (có thể marker ①)</p>
<p>④ Nuance / counter (có thể marker ② — optional)</p>
<p class="ellipsis">（中略）</p>               <!-- optional, 19% data có -->
<p>⑤ Conclusion — thesis tổng thể (Q3 author_opinion test ở đây)</p>
<div class="annotations"><p>注1 ...</p></div>  <!-- 51% data có - optional -->
<p class="source">（[fake author]「[fake title]」○○新聞による）</p>  <!-- 26% data có - optional -->
```

Ví dụ cụ thể N2 — xã luận công nghệ/xã hội:

```html
<div class="passage">
    <p>最近、スマートフォンを使って食事を注文したり、買い物をしたりする人が増えている。数年前まではレストランや店で直接やり取りするのが当たり前だったが、今では画面をタップするだけで用事が済んでしまう。</p>
    <p>便利さという点から見れば、これは確かに大きな進歩だ。待たされることもなく、自分のペースで選べる。しかし、その一方で、人と人とが直接言葉を交わす機会が少しずつ失われていることにも、私たちは気づかなければならない。</p>
    <p><span class="marker">①</span><u>こうした変化</u>は、単なる生活習慣の問題ではない。相手の表情を見ながら話す、声の調子から気持ちを読み取る——そういった力は、使わなければ衰えていくものである。画面を介したやり取りが増えるほど、実は私たちは、人間関係を築く基礎的な能力を少しずつ手放しているのかもしれない。</p>
    <p>もちろん、技術の進歩そのものを否定するつもりはない。高齢者や忙しい人にとって、こうしたサービスは大きな助けになっている。問題は、便利さに依存しすぎて、人と直接関わる時間そのものを失ってしまうことだ。</p>
    <p class="ellipsis">（中略）</p>
    <p>私たちは、便利な道具をどう使うかを選べる立場にある。すべてを機械任せにするのではなく、意識的に人と顔を合わせる機会を作ることが、これからの社会を生きていくうえで大切になるのではないだろうか。</p>
    <div class="annotations">
        <p>注1　衰える：弱くなる</p>
    </div>
    <p class="source">（田中由美「毎日の小さな選択」による）</p>
</div>
```

→ Q1 (reference, marker ①): `①「こうした変化」とあるが、どのような変化か。`
→ Q2 (reason_explanation): `筆者は、なぜ便利さに依存しすぎるのが問題だと考えているか。`
→ Q3 (author_opinion): `この文章で筆者が最も言いたいことはどれか。`

## 4. Marker Strategy Cho 3 Câu Hỏi (cả N1 & N2)

Với 3 câu, luôn dành câu 3 cho tổng thể (không marker). 2 câu đầu thường bám marker ①②.

### Pattern A — 2 markers + 1 tổng kết (phổ biến nhất)

```html
<p>... <span class="marker">①</span><u>cụm A</u> ...</p>
<p>... <span class="marker">②</span><u>cụm B</u> ...</p>
<p>... [đoạn cuối không marker — Q3 author_opinion/content_match] ...</p>
```

- Q1 = reference / meaning_interpretation (① - bám 1 đoạn giữa bài)
- Q2 = reference / meaning_interpretation (② - bám 1 đoạn khác)
- Q3 = **author_opinion** (tổng thể)

### Pattern B — 1 marker + 1 reason + 1 tổng kết (editorial-style)

```html
<p>... <span class="marker">①</span><u>cụm A</u> ...</p>
<p>... [đoạn lý do cụ thể — Q2 reason_explanation] ...</p>
<p>... [kết luận — Q3 author_opinion] ...</p>
```

- Q1 = reference
- Q2 = reason_explanation
- Q3 = **author_opinion**

### Pattern C — 0 marker + 1 meaning + 1 reason + 1 tổng kết (thuần lý luận)

Ít dùng — dùng khi bài thuần abstract không có cụm cần gạch chân. Q1/Q2 hỏi trực tiếp về luận điểm/đoạn văn:

```
Q1: `筆者は◯◯についてどう述べているか。` (không marker)
Q2: `筆者は△△が□□と異なる点はどこだと考えているか。`
Q3: author_opinion
```

## 5. `(中略)` Ellipsis Rules

Đặc trưng đọc hiểu chủ đề — data N1 có 28%, N2 có 19% bài dùng. Dùng để:

- Mô phỏng việc lược bỏ 1 đoạn từ bản gốc (tăng authenticity)
- Cho phép chuyển cảnh logic nhanh hơn
- **KHÔNG BẮT BUỘC** — chỉ dùng khi hợp flow

Format HTML:
```html
<p class="ellipsis">（中略）</p>
```

Vị trí:
- Giữa 2 đoạn logic chính (sau "luận điểm" trước "kết luận")
- **KHÔNG đặt** ở đầu hoặc cuối bài
- Không quá 1 lần per bài (data hầu hết 0-1 lần)

Char counting: `(中略)` **đếm** (3 chars Kanji + 2 括弧) — khoảng 3 chars sau strip whitespace.

## 6. Source Line Rules

| Level | Data rate | Khuyến nghị |
|-------|-----------|-------------|
| N1    | **64%**   | **RẤT NÊN** thêm (đặc trưng xã luận cao cấp) |
| N2    | 26%       | Optional — thêm khi bài là xã luận báo chí |

Format: `（[fake author]「[fake title]」による）` hoặc với media:

- `（[author]「[title]」○○新聞による）` (xã luận báo chí)
- `（[author]「[title]」による）` (tiểu luận độc lập)
- `（[author]「[title]」による。一部改変）` (có thể có "一部改変")

Examples:
- `（山口和彦「言葉と思考の未来」による）`
- `（田中由美「毎日の小さな選択」による）`
- `（佐藤健一「現代人の思考様式」朝陽新聞による）`

**Rule**: KHÔNG dùng tên tác giả có thật, KHÔNG dùng tên báo có thật (朝日/読売/...). Dùng fake.

## 7. Annotation 注 Rules

| Level | Data rate | Khuyến nghị |
|-------|-----------|-------------|
| N1    | **60%**   | **RẤT NÊN** thêm 1-2 annotation |
| N2    | 51%       | Khuyến nghị 1-2 annotation |

Format — gọn, 1-2 dòng:

```html
<div class="annotations">
    <p>注1　単語（よみ）：意味</p>
    <p>注2　単語：意味</p>
</div>
```

Hoặc inline với marker:
```html
<p>...<u>決定論</u>（注1）の立場に立つと...</p>
...
<div class="annotations">
    <p>注1　決定論：原因によって結果が一意に定まるという考え方。</p>
</div>
```

Từ cần chú thích = từ chuyên môn / từ cũ / từ rare không nằm ngay trong vốn từ của level đó.

## 8. Visual Elements Reference

| Element | N1 rate | N2 rate | Khi nào dùng |
|---------|---------|---------|--------------|
| `<u>` underline | **88%** | 26% | Cụm từ được hỏi (mọi câu reference); N1 dùng rất nhiều |
| `<span class="marker">①</span>` | **76%** | 48% | Đặt trước cụm reference; mỗi bài 1-2 marker |
| `<div class="annotations">` | **60%** | 51% | Khi có thuật ngữ khó — khuyến nghị cả 2 level |
| `<p class="source">` | **64%** | 26% | Cuối bài — rất nên N1, optional N2 |
| `<p class="ellipsis">（中略）</p>` | 28% | 19% | Lược đoạn — optional, tăng authenticity |
| `<br>` | 28% | 31% | **KHÔNG dùng** (skill bắt `<p>` thuần) |
| `<span>` (others) | 8% | 36% | **KHÔNG dùng** trừ `.marker` — N2 data cao là do JSON marker khác |
| `<ruby>/<rt>` | 0% | 9% | Chỉ khi thực sự cần — max 0-5 cặp |
| `[　]` blank | 8% | 4% | Hiếm — không khuyến khích |
| `<table>` | 0% | 4% | **KHÔNG dùng** |

## 9. Paragraph Count Guidelines

| Level | Paragraph count | Lý do |
|-------|----------------|-------|
| N1    | **6–10**        | Bài 1000-1200 chars, essay có nhiều sections logic |
| N2    | **5–8**         | Bài 900-1100 chars, editorial vừa |

Nếu ≤ 4 paragraph ở bài 1000+ chars → quá đặc, khó đọc. Chia theo đoạn ý tưởng (hook → common view → luận điểm → nuance → conclusion).

Không nên > 10 paragraph (fragmentation, mỗi đoạn quá ngắn).

## 10. Thesis Placement Strategy

Thesis (主張) cần rõ ràng. 3 patterns phổ biến:

### Pattern α — Thesis cuối bài (phổ biến nhất)
```
Para 1: Hook (common view)
Para 2-5: Luận điểm và evidence
Para 6: **THESIS — đây là ý tác giả thực sự muốn nói**
```

### Pattern β — Thesis đầu bài + khai triển
```
Para 1: **THESIS** (tuyên bố thẳng)
Para 2-4: Evidence + lập luận bổ sung
Para 5-6: Counter + nuance + khẳng định lại thesis
```

### Pattern γ — Thesis ẩn / rút ra
```
Para 1-5: Mô tả hiện tượng + phân tích
Para 6-7: **Ý tác giả hiện ra qua cách chọn luận cứ** (author_opinion question sẽ dễ nếu thesis ngầm rõ)
```

Khuyến nghị: **Pattern α hoặc β** để người đọc N1/N2 nắm được thesis rõ. Pattern γ chỉ dùng khi tự tin.

## 11. Cheatsheet Cho Gen Agent

```
N1 (3 câu, 1000-1200 chars):
  ✓ 6-10 paragraph
  ✓ 1-2 marker trong HTML (76% data)
  ✓ <u> underline cho cụm reference (88% data)
  ✓ source line (RẤT NÊN — 64%)
  ✓ 1-2 annotation (RẤT NÊN — 60%)
  ✓ `(中略)` optional (28%)
  ✓ Câu cuối = author_opinion (BẮT BUỘC)
  ✗ KHÔNG <br>, KHÔNG <span> ngoài marker
  ✗ KHÔNG ruby nhiều (0-3 cặp)

N2 (3 câu, 900-1100 chars):
  ✓ 5-8 paragraph
  ✓ 1-2 marker trong HTML (48% data)
  ✓ <u> cho cụm reference
  ✓ source line optional (26%)
  ✓ 1-2 annotation (51%)
  ✓ `(中略)` optional (19%)
  ✓ Câu cuối = author_opinion (BẮT BUỘC)
  ✗ KHÔNG <br>, KHÔNG <span> ngoài marker
  ✗ KHÔNG ruby nhiều (0-5 cặp)
```

## 12. Common Mistakes

1. **Bài chỉ 3-4 paragraph** → quá đặc → chia thành 6-10 (N1) hoặc 5-8 (N2) đoạn
2. **Bài kể chuyện / thuật sự** → SAI. Đọc hiểu chủ đề = editorial/critique, phải có thesis và lập luận
3. **Câu cuối là reference/reason** → SAI, PHẢI là author_opinion hoặc content_match
4. **3 câu cùng test 1 đoạn / ý** → SAI, mỗi câu 1 đoạn/ý riêng
5. **Marker ①②③ không có trong HTML** → SAI, phải match câu hỏi reference
6. **Thesis không rõ** → người đọc không biết tác giả muốn nói gì → câu 3 khó gen
7. **Thiếu source line ở N1** → giảm authenticity (data 64% có)
8. **Dùng tên tác giả/báo có thật** → SAI, luôn fake
9. **Dùng `<br>`** → SAI, dùng `<p>` thuần
10. **Abuse `(中略)`** → 1 lần/bài là đủ, không quá 2 lần
11. **Distractor yếu** → đọc hiểu chủ đề yêu cầu distractor tinh vi nhất: sai nuance, sai mệnh đề, sai mức độ, trộn 2 luận điểm
12. **Gen ruby cho mọi kanji** → SAI, chỉ cho từ vượt level (N1 0-3, N2 0-5)
