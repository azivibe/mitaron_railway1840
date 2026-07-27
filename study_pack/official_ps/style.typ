#let navy = rgb("#173B57")
#let blue = rgb("#2E678D")
#let pale = rgb("#F3F8FC")
#let pale2 = rgb("#F8F5EC")
#let green = rgb("#2F6B57")
#let red = rgb("#9B3E36")
#let gray = rgb("#5E6972")

#set page(
  paper: "a4",
  margin: (top: 18mm, bottom: 18mm, left: 19mm, right: 19mm),
  numbering: "1",
  number-align: center,
)
#set text(
  font: ("Noto Sans CJK KR", "Noto Sans CJK JP", "Noto Sans"),
  size: 9.6pt,
  lang: "ko",
)
#set par(justify: true, leading: 0.72em)
#set heading(numbering: "1.1")
#set list(indent: 1.2em, body-indent: 0.55em, spacing: 0.35em)
#set enum(indent: 1.2em, body-indent: 0.55em, spacing: 0.35em)
#set table(stroke: 0.45pt + rgb("#BCC8D0"), inset: 5pt)

#show heading.where(level: 1): it => block(
  above: 10pt,
  below: 7pt,
  breakable: false,
)[
  #text(size: 17pt, weight: 700, fill: navy)[#it.body]
  #line(length: 100%, stroke: 1.2pt + blue)
]

#show heading.where(level: 2): it => block(
  above: 9pt,
  below: 5pt,
  breakable: false,
)[#text(size: 13pt, weight: 700, fill: blue)[#it.body]]

#show heading.where(level: 3): it => block(
  above: 7pt,
  below: 3pt,
  breakable: false,
)[#text(size: 10.8pt, weight: 700, fill: green)[#it.body]]

#let problem(title, body) = block(
  width: 100%,
  fill: pale,
  stroke: 0.7pt + blue,
  radius: 5pt,
  inset: 10pt,
  breakable: true,
)[
  #text(weight: 700, fill: navy)[공식 문제 · #title]
  #v(4pt)
  #body
]

#let solution(title, body) = block(
  width: 100%,
  fill: white,
  stroke: 0.8pt + green,
  radius: 5pt,
  inset: 10pt,
  breakable: true,
)[
  #text(weight: 700, fill: green)[상세 풀이 · #title]
  #v(4pt)
  #body
]

#let key(body) = block(
  width: 100%,
  fill: pale2,
  stroke: 0.7pt + rgb("#C7A85A"),
  radius: 4pt,
  inset: 8pt,
  breakable: true,
)[
  #text(weight: 700, fill: rgb("#765A17"))[시험 포인트]
  #h(4pt)
  #body
]

#let caution(body) = block(
  width: 100%,
  fill: rgb("#FFF4F2"),
  stroke: 0.7pt + red,
  radius: 4pt,
  inset: 8pt,
  breakable: true,
)[
  #text(weight: 700, fill: red)[주의]
  #h(4pt)
  #body
]

#let formula(body) = block(
  width: 100%,
  fill: rgb("#FAFCFD"),
  stroke: 0.55pt + rgb("#AABAC5"),
  radius: 4pt,
  inset: (x: 10pt, y: 7pt),
  breakable: true,
)[#align(center)[#body]]

#let step(n, title, body) = block(
  width: 100%,
  above: 3pt,
  below: 3pt,
  breakable: true,
)[
  #text(weight: 700, fill: navy)[STEP #n · #title]
  #h(5pt)
  #body
]

#let answer(body) = block(
  width: 100%,
  fill: rgb("#EEF8F3"),
  stroke: 0.8pt + green,
  radius: 4pt,
  inset: 8pt,
  breakable: true,
)[
  #text(weight: 700, fill: green)[최종 답]
  #h(4pt)
  #body
]

#let smallnote(body) = text(size: 8.3pt, fill: gray)[#body]
