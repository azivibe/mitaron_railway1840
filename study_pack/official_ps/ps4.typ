#pagebreak()
= PS4 · 평균–분산 분석과 효율적 프런티어

#key([
  교수님이 수업에서 강조한 정석 5단계:
  *① 각 자산의 기대수익률·표준편차·공분산 → ② 상관계수 → ③ 포트폴리오 평균·분산 → ④ 가중치 제거 → ⑤ $(sigma_p,r_p)$ 평면에 표시*.
  Exercise 2–7은 이 순서로 풀고, Exercise 1만 두 자산의 평균이 같아 ④가 불가능한 예외형이다.
])

#formula([
  $ r_p=w r_A+(1-w)r_B $
])
#formula([
  $ sigma_p^2=w^2sigma_A^2+(1-w)^2sigma_B^2
    +2w(1-w)rho_(A B)sigma_A sigma_B $
])

== Exercise 1
#problem("공식 PS4 Exercise 1", [
  세 상태가 각각 확률 $1/3$로 발생한다. 무위험수익률은 $r_f=1$이다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [1], [2], [3],
    [자산 B], [3], [0], [3],
  )

  (a) A와 B만 가능하고 공매도가 금지될 때 효율적 프런티어를 구하라.
  (b) 무위험자산을 포함하고 차입·대출이 가능할 때 효율적 프런티어와 자산배분을 설명하라.
  (c) “더 위험회피적인 투자자는 B의 비중이 높고 A의 비중이 낮다”는 참·거짓·판단불가 중 무엇인가?
  (d) “금리 인하는 Sharpe ratio를 높이므로 모든 투자자가 환영한다”는 참·거짓·판단불가 중 무엇인가?
])

#maybe-solution("Exercise 1", [
  === (a) 평균이 같은 예외형
  각 자산의 평균은
  #formula([
    $ r_A=frac(1+2+3,3)=2, quad r_B=frac(3+0+3,3)=2 $
  ])
  분산과 공분산은
  #formula([
    $ sigma_A^2=frac((-1)^2+0^2+1^2,3)=frac(2,3) $
  ])
  #formula([
    $ sigma_B^2=frac(1^2+(-2)^2+1^2,3)=2 $
  ])
  #formula([
    $ sigma_(A B)=frac((-1)(1)+0(-2)+(1)(1),3)=0 $
  ])
  이다. 따라서 $rho_(A B)=0$이다.

  A의 비중을 $w$라 하면
  #formula([
    $ r_p=2w+2(1-w)=2 $
  ])
  모든 포트폴리오의 기대수익률이 2로 같다. 그래서 평균식에서 $w$를 풀려고 하면 분모 $r_A-r_B=0$이 되어 일반적인 STEP 4를 사용할 수 없다.

  분산을 직접 최소화한다.
  #formula([
    $ sigma_p^2=frac(2,3)w^2+2(1-w)^2 $
  ])
  미분하면
  #formula([
    $ frac(d sigma_p^2,dw)=frac(4,3)w-4(1-w)=0
      => w_(MVP)=frac(3,4) $
  ])
  따라서 B의 비중은 $1/4$이고
  #formula([
    $ sigma_(MVP)^2=frac(1,2), quad sigma_(MVP)=frac(1,sqrt(2)) $
  ])

  기대수익률은 전부 2이므로 MVP 이외의 포트폴리오는 같은 수익률에 더 큰 위험을 가진다.
  #answer([
    A:B=$3:1$인 MVP 한 점 $(sigma_p,r_p)=(1/sqrt(2),2)$만 효율적 프런티어다.
  ])

  === (b) 무위험자산 포함
  위험자산 중 평균이 모두 2이므로 위험 1단위당 초과수익을 가장 크게 하는 자산은 위험이 가장 작은 MVP이다. 즉, MVP가 접점포트폴리오 $T$가 된다.
  #formula([
    $ upright("Sharpe")(T)=frac(2-1,1/sqrt(2))=sqrt(2) $
  ])
  따라서 자본배분선은
  #formula([
    $ r_p=1+sqrt(2)sigma_p $
  ])

  모든 투자자는 위험자산 묶음 내부에서는 A:B=$3:1$을 유지한다. 위험회피도가 높은 사람은 무위험자산 비중을 높이고, 덜 위험회피적인 사람은 $T$ 비중을 높인다. $T$보다 오른쪽을 고르면 무위험자산을 음수로 보유, 즉 차입하여 레버리지를 쓴다.

  === (c) 거짓
  두 기금 분리정리에 따라 투자자마다 달라지는 것은 *무위험자산과 $T$ 사이의 비중*이다. $T$ 내부의 A:B=$3:1$ 비율은 모든 투자자에게 같다.

  === (d) 판단불가
  금리 인하로 자본배분선의 기울기, 즉 Sharpe ratio가 커질 수는 있다. 그러나 기존 순대출자는 안전자산 수익률 하락으로 불리하고, 순차입자는 차입비용 하락으로 유리하다. $T$만 보유한 투자자는 직접 효과가 없을 수 있다.

  #answer([
    (c) False. (d) Can’t tell. “Sharpe ratio 상승”만으로 모든 투자자의 후생을 판정할 수 없다.
  ])
])

== Exercise 2
#problem("공식 PS4 Exercise 2", [
  두 상태가 각각 확률 $1/2$로 발생하고 무위험자산은 없다. A와 B 모두 공매도가 허용된다.

  #table(
    columns: (1.2fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2]),
    [자산 A], [0], [0.2],
    [자산 B], [0.8], [0],
  )

  (a) 효율적 프런티어를 구하라.
  (b) 초기부 1, 기대효용 $E[Y_1]-(1/2)upright("Var")(Y_1)$인 투자자의 최적 비중을 구하라.
  (c) 공매도를 금지하면 프런티어와 투자자 후생은 어떻게 변하는가?
])

#maybe-solution("Exercise 2", [
  === (a) 완전 음의 상관
  #formula([
    $ r_A=0.1, quad r_B=0.4, quad sigma_A=0.1, quad sigma_B=0.4 $
  ])
  #formula([
    $ sigma_(A B)=frac((-0.1)(0.4)+(0.1)(-0.4),2)=-0.04 $
  ])
  따라서
  #formula([$ rho_(A B)=frac(-0.04,(0.1)(0.4))=-1 $])

  A의 비중을 $alpha$라 하면
  #formula([
    $ r_p=0.1alpha+0.4(1-alpha) $
  ])
  완전 음의 상관이므로
  #formula([
    $ sigma_p^2=[0.1alpha-0.4(1-alpha)]^2 $
  ])
  따라서
  #formula([
    $ alpha=frac(±sigma_p+0.4,0.5) $
  ])
  이를 평균식에 넣으면 전체 궤적은
  #formula([
    $ r_p=±frac(3,5)sigma_p+frac(4,25) $
  ])
  이다. 같은 위험에서 더 높은 수익률을 주는 위쪽 가지가 효율적이다.
  #answer([$ r_p=frac(3,5)sigma_p+frac(4,25) $.])

  === (b) 최적 비중
  $Y_0=1$이므로 $Y_1=1+r_p$이고 $upright("Var")(Y_1)=sigma_p^2$이다.
  #formula([
    $ max_alpha 1+0.1alpha+0.4(1-alpha)
      -frac(1,2)[0.1alpha-0.4(1-alpha)]^2 $
  ])
  FOC를 풀면
  #formula([
    $ alpha^*=-frac(2,5), quad 1-alpha^*=frac(7,5) $
  ])
  즉 A를 40% 공매도하고 B를 140% 보유한다.

  === (c) 공매도 금지
  제약은 $0<=alpha<=1$이다. (b)의 내부 최적해 $alpha^*=-2/5$가 허용되지 않으므로 경계 $alpha=0$, 즉 B 100%가 최적이다.
  프런티어에서는 B를 넘어 북동쪽으로 뻗는 $alpha<0$ 구간이 삭제된다.

  #answer([
    공매도 허용 시보다 선택집합이 줄고 원래 최적점이 사라지므로 이 투자자는 더 나빠진다.
  ])
])

== Exercise 3
#problem("공식 PS4 Exercise 3", [
  세 상태가 각각 확률 $1/3$, 무위험자산은 없고 두 자산 모두 공매도가 가능하다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [1], [2], [0],
    [자산 B], [0], [3], [3],
  )

  (a) 평균–분산 지배가 존재하는가?
  (b) 최소분산 프런티어를 구하고 MVP의 평균과 표준편차도 구하라.
  (c) 초기부 1, 기대효용 $E[Y_1]-(1/6)upright("Var")(Y_1)$인 투자자의 최적비중과 무차별곡선을 구하라.
])

#maybe-solution("Exercise 3", [
  기초통계량은
  #formula([
    $ r_A=1, quad r_B=2, quad sigma_A^2=frac(2,3), quad sigma_B^2=2, quad sigma_(A B)=0 $
  ])

  === (a) 지배 없음
  B는 평균이 높지만 분산도 높다. A는 위험이 작지만 평균도 작다. 따라서 어느 자산도 다른 자산을 평균–분산 지배하지 않는다.

  === (b) 최소분산 프런티어
  A의 비중을 $alpha$라 하면
  #formula([
    $ r_p=alpha+2(1-alpha)=2-alpha $
  ])
  #formula([
    $ sigma_p^2=frac(2,3)alpha^2+2(1-alpha)^2 $
  ])
  평균식에서 $alpha=2-r_p$이므로
  #formula([
    $ sigma_p^2=frac(2,3)(2-r_p)^2+2(r_p-1)^2 $
  ])
  전개·완전제곱하면
  #formula([
    $ sigma_p^2=frac(1,2)+frac(8,3)(r_p-frac(5,4))^2 $
  ])
  이 전체가 최소분산 프런티어이고, $r_p>=5/4$인 위쪽 부분이 효율적 프런티어다.

  분산을 $alpha$로 최소화하면
  #formula([
    $ alpha_(MVP)=frac(sigma_B^2,sigma_A^2+sigma_B^2)=frac(3,4) $
  ])
  #formula([
    $ r_(MVP)=frac(5,4), quad sigma_(MVP)^2=frac(1,2), quad sigma_(MVP)=frac(1,sqrt(2)) $
  ])

  === (c) 투자자의 최적점
  #formula([
    $ max_alpha 1+(2-alpha)-frac(1,6)[frac(2,3)alpha^2+2(1-alpha)^2] $
  ])
  분산의 미분은 $(16/3)alpha-4$이므로
  #formula([
    $ -1-frac(1,6)(frac(16,3)alpha-4)=0
      => alpha^*=-frac(3,8) $
  ])
  따라서 B의 비중은 $11/8$이다.
  #formula([
    $ r_p^*=frac(19,8), quad sigma_p^{2*}=frac(31,8), quad sigma_p^*=sqrt(frac(31,8)) $
  ])

  효용수준을 $u$로 고정하면 무차별곡선은
  #formula([
    $ r_p=u-1+frac(1,6)sigma_p^2 $
  ])
  이다. $(sigma_p,r_p)$ 평면에서 오른쪽으로 갈수록 기울기가 커지는 위로 볼록한 곡선이며, 최적점에서 효율적 프런티어와 접한다.

  #answer([
    A 비중 $-3/8$, B 비중 $11/8$. 즉 A를 공매도해 B를 레버리지 보유한다.
  ])
])

== Exercise 4
#problem("공식 PS4 Exercise 4", [
  세 상태가 각각 확률 $1/3$, 무위험수익률 $r_f=5.5$, A와 B의 공매도는 금지된다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [8], [6], [4],
    [자산 B], [11], [7], [3],
  )

  (a) 평균–분산 지배가 있는가? (b) Sharpe ratio로 A와 B를 순위매겨라.
  (c) A와 B만 있을 때 효율적 프런티어를 구하라.
  (d) 무위험자산을 포함하면 어떻게 배분하는가?
  (e) $r_f$가 4.5로 하락하면 선택과 후생이 어떻게 바뀌는가?
])

#maybe-solution("Exercise 4", [
  통계량은
  #formula([
    $ r_A=6, quad r_B=7, quad sigma_A^2=frac(8,3), quad sigma_B^2=frac(32,3) $
  ])
  #formula([
    $ sigma_(A B)=frac(16,3), quad rho_(A B)=1 $
  ])

  === (a) 지배 없음
  B는 평균이 더 높지만 위험도 더 크므로 지배관계가 없다.

  === (b) Sharpe ratio
  #formula([
    $ SR_A=frac(6-5.5,sqrt(8/3)), quad
      SR_B=frac(7-5.5,sqrt(32/3)) $
  ])
  계산하면 $SR_B>SR_A$이다.

  === (c) 완전 양의 상관 프런티어
  A의 비중을 $w$라 하면 $0<=w<=1$이고
  #formula([
    $ sigma_p=w sigma_A+(1-w)sigma_B $
  ])
  평균식과 함께 $w$를 제거하면
  #formula([
    $ r_p=sqrt(frac(3,8))sigma_p+5 $
  ])
  단, $sigma_p$는 $sigma_A$와 $sigma_B$ 사이이다. 그래프는 A와 B를 잇는 직선구간이다.

  === (d) 무위험자산 포함
  $r_f=5.5$에서는 B의 Sharpe ratio가 더 높으므로 접점포트폴리오는 B 한 자산이다. 모든 투자자는 B와 무위험자산만 조합하고 A는 보유하지 않는다. 위험회피도에 따라 B와 무위험자산의 비중만 달라진다.

  === (e) 금리 4.5
  새 Sharpe ratio는
  #formula([
    $ SR_A'=frac(6-4.5,sqrt(8/3)), quad
      SR_B'=frac(7-4.5,sqrt(32/3)) $
  ])
  이며 이번에는 $SR_A'>SR_B'$이다. 따라서 접점 위험자산이 B에서 A로 바뀌고, 투자자들은 A와 무위험자산을 조합한다.

  그러나 후생효과는 투자자마다 다르다. 새 무위험수익률 자체는 낮아져 순대출자에게 불리하지만, 자본배분선의 기울기는 커져 충분히 위험을 지거나 차입하는 투자자에게 유리할 수 있다.

  #answer([
    금리 하락 후 접점자산은 A. 후생은 일률적으로 판단할 수 없으며 저위험 대출자는 나빠지고 고위험·차입자는 좋아질 수 있다.
  ])
])

== Exercise 5
#problem("공식 PS4 Exercise 5", [
  세 상태가 각각 확률 $1/3$, 무위험자산은 없다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [6], [8], [4],
    [자산 B], [7], [3], [11],
  )

  (a) 평균–분산 지배가 있는가?
  (b) 두 자산 모두 공매도 금지일 때 효율적 프런티어를 구하라.
  (c) B만 공매도할 수 있으면 프런티어와 후생은 어떻게 되는가?
  (d) 두 자산 모두 공매도할 수 있으면 어떻게 달라지는가?
])

#maybe-solution("Exercise 5", [
  #formula([
    $ r_A=6, quad r_B=7, quad sigma_A^2=frac(8,3), quad sigma_B^2=frac(32,3) $
  ])
  #formula([
    $ sigma_(A B)=-frac(16,3), quad rho_(A B)=-1 $
  ])

  === (a) 지배 없음
  B의 평균이 더 높지만 분산도 더 높으므로 지배관계가 없다.

  === (b) 공매도 금지
  A 비중을 $alpha$라 하자. $0<=alpha<=1$이며
  #formula([
    $ r_p=6alpha+7(1-alpha)=7-alpha $
  ])
  $sigma_A=sqrt(8/3)$, $sigma_B=2sigma_A$이므로
  #formula([
    $ sigma_p=sigma_A|3alpha-2| $
  ])
  평균식의 $alpha=7-r_p$를 대입하면
  #formula([
    $ r_p=frac(19,3)±frac(sigma_p,2sqrt(6)) $
  ])

  $alpha=2/3$에서는 위험이 0이고 기대수익률은 $19/3$이다.
  공매도 금지 구간에서 효율적 프런티어는 이 무위험점과 B를 잇는 위쪽 가지이다.
  #formula([
    $ r_p=frac(19,3)+frac(sigma_p,2sqrt(6)), quad
      0<=sigma_p<=sqrt(frac(32,3)) $
  ])

  === (c) B만 공매도 허용
  B의 비중 $1-alpha<0$이면 $alpha>1$이다. 이는 A점에서 더 낮은 기대수익률·더 높은 위험 쪽으로 아래 가지를 연장할 뿐이다. 새로 생기는 모든 포트폴리오는 기존 효율적 포트폴리오에 지배된다.

  #answer([효율적 프런티어는 변하지 않고, 평균–분산 투자자의 후생도 달라지지 않는다.])

  === (d) 두 자산 모두 공매도 허용
  이제 $alpha<0$, 즉 A를 공매도하고 B를 100% 이상 보유하는 포트폴리오도 가능하다. 이는 B를 넘어 위쪽 효율적 가지를 북동쪽으로 연장한다.

  #answer([
    효율적 프런티어가 B 바깥까지 확장된다. 높은 위험을 감수하려는 투자자는 더 좋아질 수 있고, 기존 선택을 유지할 수 있는 투자자는 나빠지지 않는다.
  ])
])

== Exercise 6
#problem("공식 PS4 Exercise 6", [
  세 상태가 각각 확률 $1/3$, 무위험자산이 없고 공매도가 금지된다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [2], [4], [0],
    [자산 B], [4], [0], [8],
  )

  (a) 효율적 프런티어를 구하라.
  (b) “극도로 위험회피적인 투자자는 B보다 변동성이 낮은 A에 70%보다 많이 투자할 수 있다”는 참·거짓·판단불가 중 무엇인가?
  (c) B를 상태별로 지배하는 C=(4,6,8)로 교체한다. 투자자가 좋아질 수도 나빠질 수도 있음을 평균–분산 그림으로 설명하고, 왜 이런 역설이 생기는지 설명하라.
])

#maybe-solution("Exercise 6", [
  #formula([
    $ r_A=2, quad r_B=4, quad sigma_A^2=frac(8,3), quad sigma_B^2=frac(32,3), quad rho_(A B)=-1 $
  ])

  === (a) 효율적 프런티어
  A 비중을 $alpha$라 하면
  #formula([
    $ r_p=2alpha+4(1-alpha)=4-2alpha $
  ])
  #formula([
    $ sigma_p=sigma_A|3alpha-2| $
  ])
  $alpha=(4-r_p)/2$를 넣으면 전체 궤적은
  #formula([
    $ r_p=frac(8,3)±frac(sigma_p,sqrt(6)) $
  ])
  이다. $alpha=2/3$에서 $sigma_p=0$, $r_p=8/3$이다.
  공매도 금지하의 효율적 프런티어는 무위험점과 B 사이의 위쪽 가지:
  #formula([
    $ r_p=frac(8,3)+frac(sigma_p,sqrt(6)), quad
      0<=sigma_p<=sqrt(frac(32,3)) $
  ])

  === (b) False
  효율적 프런티어에서 A의 최대비중은 MVP의 $alpha=2/3$, 즉 66.7%이다.
  그보다 A 비중을 높이면 기대수익률이 더 낮아지면서 위험은 다시 커져 지배되는 아래 가지로 들어간다.
  #answer([70%를 넘는 A 비중은 평균–분산 투자자의 최적 선택이 될 수 없으므로 거짓이다.])

  === (c) B를 C로 교체
  C의 평균과 분산은
  #formula([
    $ r_C=6, quad sigma_C^2=frac(8,3) $
  ])
  이고 A와 C의 공분산은 $-4/3$, 상관계수는 $-1/2$이다.
  새 조합은 기대수익률을 크게 높일 수 있지만 완전 음의 상관이 아니므로 더 이상 위험 0을 만들 수 없다. 실제로 A와 C의 분산이 같아 MVP는 50–50이고 그 분산은 $2/3>0$이다.

  높은 기대수익률을 중시하는 투자자는 C 도입 후 더 높은 무차별곡선으로 갈 수 있다. 반대로 위험을 거의 허용하지 않는 투자자는 기존 A–B 조합의 무위험 포트폴리오를 잃어 더 나빠질 수 있다.

  이 결과는 현실에서 C가 나쁜 자산이라서가 아니라 평균–분산 모형의 한계다. C는 모든 상태에서 B보다 같거나 높은 지급을 주므로 완전한 분포 기준으로는 B보다 낫다. 그러나 평균과 분산 두 숫자만 보는 MPT는 상태별 지배를 완전히 반영하지 못한다.
])

== Exercise 7
#problem("공식 PS4 Exercise 7", [
  세 상태가 각각 확률 $1/3$, 무위험자산은 없고 공매도가 허용된다.

  #table(
    columns: (1.2fr, 1fr, 1fr, 1fr),
    table.header([*수익률*], [상태 1], [상태 2], [상태 3]),
    [자산 A], [2], [5], [2],
    [자산 B], [0], [6], [0],
  )

  투자자의 초기부는 $Y_0$이고 효용은 $ln Y_1$. A 비중을 $w$, B 비중을 $1-w$라 한다.
  (a) 효율적 프런티어를 구하라. (b) MVP를 구하라.
  (c) 로그효용 투자자의 최적비중, 기대수익률, 표준편차를 구하라.
])

#maybe-solution("Exercise 7", [
  기초통계량은
  #formula([
    $ r_A=3, quad r_B=2, quad sigma_A^2=2, quad sigma_B^2=8, quad sigma_(A B)=4 $
  ])
  따라서 $rho_(A B)=1$이다.

  === (a) 효율적 프런티어
  #formula([
    $ r_p=3w+2(1-w)=2+w $
  ])
  완전 양의 상관이므로
  #formula([
    $ sigma_p=sqrt(2)|2-w| $
  ])
  $w=r_p-2$를 대입하면
  #formula([
    $ r_p=4±frac(sigma_p,sqrt(2)) $
  ])
  같은 위험에서 수익률이 높은 위쪽 가지가 효율적이다.
  #answer([$ r_p=4+sigma_p/sqrt(2) $.])

  === (b) MVP
  위험이 0이 되려면
  #formula([
    $ 2-w=0 => w_(MVP)=2 $
  ])
  이다. 따라서 A 200%, B $-100%$이며
  #formula([
    $ r_(MVP)=4, quad sigma_(MVP)=0 $
  ])
  이다. A와 B가 완전 양의 상관이어도 서로 다른 변동폭을 이용한 long–short 조합으로 확정수익을 만들 수 있다.

  === (c) 로그효용 최적화
  상태 1과 3에서 포트폴리오 수익률은 $2w$, 상태 2에서는 $6-w$이다. 따라서 gross wealth는
  #formula([
    $ Y_1=Y_0(1+2w) quad "with probability" quad frac(2,3) $
  ])
  #formula([
    $ Y_1=Y_0(7-w) quad "with probability" quad frac(1,3) $
  ])
  이다. $ln Y_0$는 선택과 무관하므로
  #formula([
    $ max_w frac(2,3)ln(1+2w)+frac(1,3)ln(7-w) $
  ])
  FOC는
  #formula([
    $ frac(4,3(1+2w))-frac(1,3(7-w))=0 $
  ])
  즉
  #formula([
    $ 4(7-w)=1+2w => w^*=frac(9,2) $
  ])
  이다. B 비중은 $1-w^*=-7/2$이다.

  #formula([
    $ r_p^*=2+frac(9,2)=frac(13,2) $
  ])
  #formula([
    $ sigma_p^*=sqrt(2)|2-frac(9,2)|=frac(5sqrt(2),2) $
  ])

  #answer([
    A 450%, B $-350%$; 기대수익률 $13/2$, 표준편차 $5sqrt(2)/2$.
  ])

  #caution([
    로그효용에서는 모든 상태의 최종부가 양수여야 한다. 여기서는 $1+2w>0$과 $7-w>0$이 필요하며 $w=9/2$는 두 조건을 만족한다.
  ])
])
