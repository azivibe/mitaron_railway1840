#align(center)[
  #v(18mm)
  #text(size: 26pt, weight: 800, fill: navy)[Money, Banking and Finance A]
  #v(4mm)
  #text(size: 22pt, weight: 750, fill: blue)[PS1–PS4 공식문제 완전정리]
  #v(3mm)
  #if show-solutions [
    #text(size: 15pt, weight: 650, fill: green)[공식 문제 23제 · 단계별 상세풀이 · 시험 답안형 정리]
  ] else [
    #text(size: 15pt, weight: 650, fill: green)[공식 문제 23제 · 문제만 모아풀기]
  ]
  #v(10mm)
  #block(width: 82%, fill: pale, stroke: 0.8pt + blue, radius: 7pt, inset: 13pt)[
    #text(weight: 700, fill: navy)[자료의 범위]
    #v(3pt)
    이 자료의 문제는 전부 Yuki Sato 교수의 공식 Problem Set 1–4에서 가져왔다.
    숫자·가정·소문항을 임의로 바꾼 변형문제는 포함하지 않았다.
    #if show-solutions [
      풀이 부분은 공식 해답과 exercise session 설명을 기준으로, 계산이 생략되지 않도록 한국어로 확장했다.
    ]
  ]
  #v(8mm)
  #text(size: 10pt, fill: gray)[Keio University · Department of Economics]
  #v(2mm)
  #text(size: 9pt, fill: gray)[시험 대비용 개인 학습 편집본]
]

#pagebreak()
= 사용법과 범위

#problem("전체 구성", [
  *PS1 일반균형·Edgeworth Box* 4문제, *PS2 위험태도·기대효용* 5문제,
  *PS3 포트폴리오 선택·균형자산가격* 7문제, *PS4 평균–분산·효율적 프런티어* 7문제를 수록했다.
])

#if show-solutions [
  #key([
    풀이를 읽을 때는 최종 숫자보다 *문제 설정 → 목적함수/예산제약 → 1계조건 → 시장청산 또는 평균·분산 계산 → 경제적 직관*의 순서를 먼저 익힌다.
  ])
]

== 공식문제 체크리스트
#table(
  columns: (1fr, 1fr, 1fr, 1fr),
  table.header(
    [*PS1*], [*PS2*], [*PS3*], [*PS4*],
  ),
  [□ Ex.1], [□ Ex.1], [□ Ex.1], [□ Ex.1],
  [□ Ex.2], [□ Ex.2], [□ Ex.2], [□ Ex.2],
  [□ Ex.3], [□ Ex.3], [□ Ex.3], [□ Ex.3],
  [□ Ex.4], [□ Ex.4], [□ Ex.4], [□ Ex.4],
  [], [□ Ex.5], [□ Ex.5], [□ Ex.5],
  [], [], [□ Ex.6], [□ Ex.6],
  [], [], [□ Ex.7], [□ Ex.7],
)

#outline(title: [목차])

#include "ps1.typ"
#include "ps2.typ"
#include "ps3.typ"
#include "ps4.typ"

#pagebreak()
= 최종 회독표
#table(
  columns: (1.2fr, 3fr),
  table.header([*범위*], [*시험 직전 반드시 가능한 것*]),
  [PS1], [개별 수요함수 도출, 상대가격 결정, 균형배분, 계약곡선과 Pareto 효율 설명],
  [PS2], [ARA·RRA에서 효용함수 식별, 기대효용 비교, 확실성등가·위험프리미엄, CARA/CRRA의 wealth effect],
  [PS3], [최종부 작성, 평균·분산 계산, FOC로 수요함수, 시장청산으로 가격, 위험프리미엄의 비교정태],
  [PS4], [평균·표준편차·공분산·상관계수, 포트폴리오 평균·분산, 가중치 제거, MVP·프런티어·공매도·무위험자산],
)

#v(8pt)
#key([
  교수 설명상 PS4 Exercise 2–7은 같은 5단계 풀이 틀로 반복 연습하는 것이 핵심이고, Exercise 1은 두 위험자산의 기대수익률이 같아 일반적인 가중치 제거가 되지 않는 예외형이다.
])
