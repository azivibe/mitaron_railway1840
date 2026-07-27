#pagebreak()
= PS3 · 포트폴리오 선택과 균형자산가격

#key([
  PS3의 기본 골격은 *최종부 작성 → 기대값·분산 → 효용 또는 확실성등가 → FOC로 개인수요 → 시장청산으로 가격*이다.
  숫자를 바로 넣기보다 일반식으로 해를 구한 뒤 마지막에 수치를 대입하면 비교정태와 경제적 의미가 보인다.
])

== Exercise 1
#problem("공식 PS3 Exercise 1", [
  펀드매니저가 Adidas 주식, Boeing 주식, 무위험채권에 투자한다.

  - Adidas: 기대수익률 20%, 표준편차 4%
  - Boeing: 기대수익률 10%, 표준편차 1.5%
  - 무위험수익률 2%
  - 두 주식의 상관계수 0.2
  - 고객의 초기부 100,000달러, 기대효용 $E[W]-0.0025upright("Var")(W)$

  (a) Adidas와 채권만 가능할 때 최적 포트폴리오를 구하라.
  (b) 세 자산 모두 가능할 때 최적 포트폴리오를 구하라.
  (c) 상관계수가 0.2에서 $-0.2$로 떨어지면 포트폴리오를 어떻게 바꾸는가? 직관을 설명하라.
])

#maybe-solution("Exercise 1", [
  Adidas 투자액을 $A$, Boeing 투자액을 $B$라 하자. 채권 투자액은 $100,000-A-B$이다.

  === (a) Adidas와 채권
  최종부는
  #formula([
    $ W=(1+r_A)A+1.02(100,000-A) $
  ])
  이다. 기대값과 분산은
  #formula([
    $ E[W]=102,000+0.18A, quad upright("Var")(W)=0.04^2 A^2=0.0016A^2 $
  ])
  따라서 목적함수는
  #formula([
    $ 102,000+0.18A-0.0025(0.0016A^2) $
  ])
  이다. FOC:
  #formula([
    $ 0.18-2(0.0025)(0.0016)A=0
      => A^*=22,500 $
  ])
  나머지 $77,500$달러를 채권에 둔다.

  #answer([Adidas 22,500달러, 무위험채권 77,500달러.])

  === (b) 세 자산
  공분산은
  #formula([
    $ sigma_(A B)=rho_(A B)sigma_A sigma_B
      =0.2(0.04)(0.015)=0.00012 $
  ])
  최종부의 기대값과 분산은
  #formula([
    $ E[W]=102,000+0.18A+0.08B $
  ])
  #formula([
    $ upright("Var")(W)=0.0016A^2+0.000225B^2+2(0.00012)AB $
  ])
  목적함수를 $A,B$로 미분하면
  #formula([
    $ 0.0016A+0.00012B=36 $
  ])
  #formula([
    $ 0.00012A+0.000225B=16 $
  ])
  의 연립방정식이 나온다. 이를 풀면
  #formula([
    $ A^*=17,881.94, quad B^*=61,574.07 $
  ])
  채권은
  #formula([
    $ 100,000-A^*-B^*=20,543.98 $
  ])
  이다.

  #answer([
    Adidas 약 17,882달러, Boeing 약 61,574달러, 채권 약 20,544달러.
  ])

  === (c) 상관계수 $-0.2$
  공분산이 $-0.00012$로 바뀐다. FOC는
  #formula([
    $ 0.0016A-0.00012B=36, quad
      -0.00012A+0.000225B=16 $
  ])
  이고 해는
  #formula([
    $ A^*=28,993.06, quad B^*=86,574.07 $
  ])
  이다. 채권투자는
  #formula([
    $ 100,000-A^*-B^*=-15,567.13 $
  ])
  으로 음수다. 즉, 약 15,567달러를 무위험이자율로 빌려 두 주식을 더 산다.

  #answer([
    음의 상관관계가 강해지면 두 주식이 서로의 변동을 상쇄하므로 위험자산 보유를 모두 늘리고, 이 문제의 수치에서는 채권을 공매도해 레버리지를 사용한다.
  ])

  #key([
    분산식에서 $2ABupright("Cov")(r_A,r_B)$를 빠뜨리면 (b)와 (c)의 핵심인 분산효과가 사라진다.
  ])
])

== Exercise 2
#problem("공식 PS3 Exercise 2", [
  두 시점 $t=0,1$, 무위험 순수익률 $r_f$, 위험자산의 1주당 현금흐름 $delta$가 평균 $mu$, 분산 $sigma_delta^2$인 정규분포를 따른다. 현재가격은 $P$, 총공급은 $S$, 동일한 투자자는 $N$명이며 초기부는 $Y_0$이다. 각 투자자는 CARA 효용 $-exp(-nu Y_1)$을 극대화한다.

  (a) 투자자 문제를 설정하라. (b) 수요함수 $X(P)$를 구하라. (c) 시장청산으로 균형가격을 구하라. (d) $sigma_delta^2$가 증가하면 가격은 어떻게 되는가?
])

#maybe-solution("Exercise 2", [
  === (a) 최종부와 최적화 문제
  위험자산 $X$주를 사면 매입비용은 $PX$, 나머지는 무위험자산에 둔다.
  #formula([
    $ Y_1=delta X+(1+r_f)(Y_0-PX) $
  ])
  따라서
  #formula([
    $ max_X E[-exp(-nu Y_1)] $
  ])
  이 투자자의 문제다.

  === (b) CARA–normal 변환
  정규확률변수 $z$에 대해
  #formula([$ E[exp(z)]=exp(E[z]+upright("Var")(z)/2) $])
  이다. $-nu Y_1$도 정규분포이므로 기대효용 극대화는 다음 확실성등가 극대화와 동치다.
  #formula([
    $ max_X mu X+(1+r_f)(Y_0-PX)-frac(nu,2)sigma_delta^2 X^2 $
  ])
  FOC는
  #formula([
    $ mu-(1+r_f)P-nu sigma_delta^2 X=0 $
  ])
  따라서
  #formula([
    $ X(P)=frac(mu-(1+r_f)P,nu sigma_delta^2) $
  ])

  === (c) 시장청산
  #formula([
    $ NX(P)=S $
  ])
  를 대입하면
  #formula([
    $ P^*=frac(mu-nu sigma_delta^2(S/N),1+r_f) $
  ])

  #answer([
    균형가격은 “기대현금흐름에서 투자자 1인당 공급에 대한 위험프리미엄을 뺀 뒤 무위험수익률로 할인한 값”이다.
  ])

  === (d) 위험 증가
  #formula([
    $ frac(partial P^*,partial sigma_delta^2)
      =-frac(nu(S/N),1+r_f)<0 $
  ])
  현금흐름의 변동성이 커지면 위험회피 투자자는 더 큰 보상을 요구한다. 기대수익률이 올라가려면 현재가격은 낮아져야 한다.
])

== Exercise 3
#problem("공식 PS3 Exercise 3", [
  Exercise 2를 수정한다. 투자자의 비율 $alpha$는 낙관형 H로 평균 현금흐름을 $mu_H$라고 믿고, 나머지는 비관형 L로 $mu_L<mu_H$라고 믿는다. 분산 $sigma^2$과 CARA 계수 $nu$는 같다. 시장 개장 전 각 투자자는 $S/N$주씩 보유한다.

  (a) $X_H,X_L,P$를 구하라. (b) 거래량과 누가 얼마나 사고파는지 구하고, 거래량이 언제 큰지 설명하라.
])

#maybe-solution("Exercise 3", [
  === (a) 유형별 수요와 균형가격
  Exercise 2의 수요식을 유형별 평균으로 바꾸면
  #formula([
    $ X_H(P)=frac(mu_H-(1+r_f)P,nu sigma^2), quad
      X_L(P)=frac(mu_L-(1+r_f)P,nu sigma^2) $
  ])
  시장청산은
  #formula([
    $ alpha N X_H+(1-alpha)N X_L=S $
  ])
  이다. 정리하면
  #formula([
    $ P^*=frac(alpha mu_H+(1-alpha)mu_L-nu sigma^2(S/N),1+r_f) $
  ])
  가격을 수요함수에 다시 넣으면
  #formula([
    $ X_H^*=frac(S,N)+frac((1-alpha)(mu_H-mu_L),nu sigma^2) $
  ])
  #formula([
    $ X_L^*=frac(S,N)-frac(alpha(mu_H-mu_L),nu sigma^2) $
  ])

  === (b) 거래량
  낙관형 한 명의 순매수는
  #formula([$ X_H^*-frac(S,N)=frac((1-alpha)(mu_H-mu_L),nu sigma^2) $])
  비관형 한 명의 순매도 절댓값은
  #formula([$ frac(S,N)-X_L^*=frac(alpha(mu_H-mu_L),nu sigma^2) $])
  이다. 전체 매수량과 전체 매도량은 같으며 시장 전체 거래량은
  #formula([
    $ V=frac(N alpha(1-alpha)(mu_H-mu_L),nu sigma^2) $
  ])

  #answer([
    거래량은 $alpha$에 대해 역 U자형이며 $alpha=1/2$에서 최대다. 의견차 $mu_H-mu_L$가 크고, 위험회피 $nu$와 불확실성 $sigma^2$가 작을수록 크다.
  ])
])

== Exercise 4
#problem("공식 PS3 Exercise 4", [
  Exercise 2의 $N$명 가격수용자 외에 가격영향을 이해하는 대형투자자가 있다. 그는 위험중립이고 위험자산 현금흐름의 평균을 $mu_B$라고 믿는다. 대형투자자의 보유량을 $Z$라 하자.

  (a) $X,Z,P$를 포함한 경쟁균형을 구하라. (b) $partial Z/partial sigma<0$임을 보이고, 위험중립 투자자가 왜 위험이 커질 때 보유량을 줄이는지 설명하라.
])

#maybe-solution("Exercise 4", [
  === (a) 대형투자자의 가격영향
  소형 투자자 한 명의 수요는
  #formula([$ X(P)=frac(mu-(1+r)P,nu sigma^2) $])
  이다. 대형투자자가 $Z$주를 보유하면 소형투자자 전체가 흡수해야 하는 공급은 $S-Z$이다.
  #formula([
    $ NX(P)+Z=S $
  ])
  에서 가격을 $Z$의 함수로 풀면
  #formula([
    $ P(Z)=frac(mu-(nu sigma^2/N)(S-Z),1+r) $
  ])

  대형투자자는 위험중립이지만 자신이 $Z$를 늘리면 가격이 상승한다는 점을 안다.
  #formula([
    $ max_Z mu_B Z+(1+r)(Y_0-P(Z)Z) $
  ])
  이 목적함수를 미분하면
  #formula([
    $ Z^*=frac(S,2)+frac(N(mu_B-mu),2nu sigma^2) $
  ])
  이다. 이를 가격식과 소형투자자 수요에 넣으면
  #formula([
    $ P^*=frac((mu+mu_B)/2-(nu sigma^2 S)/(2N),1+r) $
  ])
  #formula([
    $ X^*=frac(S,2N)-frac(mu_B-mu,2nu sigma^2) $
  ])

  === (b) 왜 위험중립자도 $Z$를 줄이는가
  #formula([
    $ frac(partial Z^*,partial sigma^2)
      =-frac(N(mu_B-mu),2nu sigma^4) $
  ])
  특히 $mu_B>mu$이면 음수다. 이유는 대형투자자가 위험 자체를 싫어해서가 아니다.
  $sigma$가 커지면 소형 위험회피 투자자의 수요곡선이 더 가팔라지고, 대형투자자가 공급을 흡수할 때 가격이 더 크게 오른다. 높은 매입가격은 대형투자자의 이익을 줄이므로 최적 $Z$가 작아진다.

  #key([
    이 문제의 핵심은 *risk exposure*가 아니라 *price impact*. 위험중립이라는 말은 현금흐름 위험을 싫어하지 않는다는 뜻이지, 자신이 올려 놓은 비싼 가격을 무시한다는 뜻이 아니다.
  ])
])

== Exercise 5
#problem("공식 PS3 Exercise 5", [
  위험자산의 1주당 현금흐름은 확률 $pi$로 $A>0$, 확률 $1-pi$로 0이다. 가격은 $P$, 공급은 $S$, 투자자는 $N$명이고 무위험 순수익률은 $r$이다. 기대효용은
  $E[Y_1]-(theta/2)upright("Var")(Y_1)$이다.

  (a) 수요 $X(P)$와 균형가격을 구하라. (b) $theta$가 증가하면 가격은 어떻게 되는가? (c) $A$가 증가하면 가격은 어떻게 되는가?
])

#maybe-solution("Exercise 5", [
  현금흐름의 평균과 분산은
  #formula([
    $ E[delta]=pi A, quad upright("Var")(delta)=pi(1-pi)A^2 $
  ])
  이다. 최종부는 $Y_1=delta X+(1+r)(Y_0-PX)$이므로 목적함수에서 $X$와 관련된 부분은
  #formula([
    $ [pi A-(1+r)P]X-frac(theta,2)pi(1-pi)A^2X^2 $
  ])
  이다.

  FOC로부터
  #formula([
    $ X(P)=frac(pi A-(1+r)P,theta pi(1-pi)A^2) $
  ])
  시장청산 $NX=S$를 적용하면
  #formula([
    $ P^*=frac(pi A-theta pi(1-pi)A^2(S/N),1+r) $
  ])

  === (b) 위험회피도 증가
  #formula([
    $ frac(partial P^*,partial theta)
      =-frac(pi(1-pi)A^2(S/N),1+r)<0 $
  ])
  더 위험회피적이면 같은 공급을 보유시키기 위해 더 낮은 가격이 필요하다.

  === (c) 성공 시 지급액 증가
  #formula([
    $ frac(partial P^*,partial A)
      =frac(pi,1+r)[1-2theta(1-pi)A(S/N)] $
  ])
  따라서 효과는 항상 한 방향이 아니다. $A$가 작을 때는 기대현금흐름 증가가 우세해 가격이 오르지만,
  #formula([$ A>frac(N,2theta(1-pi)S) $])
  이면 분산이 $A^2$로 커지는 위험효과가 우세해 가격이 내려간다.

  #answer([
    $P$는 $A$에 대해 역 U자형일 수 있다. “좋은 상태의 지급액이 커지면 무조건 가격이 오른다”라고 쓰면 위험프리미엄 효과를 놓친다.
  ])
])

== Exercise 6
#problem("공식 PS3 Exercise 6", [
  위험자산 현금흐름은 확률 $1/2$로 $delta_H$, 확률 $1/2$로 $delta_L$이며 $delta_H>delta_L$이다. 가격 $P$, 공급 $S$, 무위험 순수익률 $r$, 동일한 CARA 투자자 $N$명, 효용 $-exp(-nu Y_1)$이다.

  (a) 투자문제를 설정하라. (b) 수요함수를 구하라. (c) 균형가격을 구하라. (d) $N to infinity$일 때 가격을 구하고 직관을 설명하라.
])

#maybe-solution("Exercise 6", [
  === (a) 문제 설정
  #formula([
    $ max_X E[-exp(-nu Y_1)], quad
      Y_1=delta X+(1+r)(Y_0-PX) $
  ])

  === (b) 두 상태를 직접 미분
  기대효용을 $X$로 미분한 FOC는
  #formula([
    $ [delta_H-(1+r)P]exp(-nu delta_H X)
      =[(1+r)P-delta_L]exp(-nu delta_L X) $
  ])
  이다. 양변의 비율에 로그를 취하면
  #formula([
    $ X(P)=frac(1,nu(delta_H-delta_L))
      ln frac(delta_H-(1+r)P,(1+r)P-delta_L) $
  ])

  === (c) 시장청산
  $X=S/N$을 넣고
  #formula([
    $ q=exp(frac(Snu(delta_H-delta_L),N)) $
  ])
  라 두면
  #formula([
    $ delta_H-(1+r)P=q[(1+r)P-delta_L] $
  ])
  이므로
  #formula([
    $ P^*=frac(1,1+r)frac(delta_H+qdelta_L,1+q) $
  ])

  === (d) 투자자 수가 무한대로 증가
  $N to infinity$이면 $q to 1$이다.
  #formula([
    $ lim_(N to infinity)P^*
      =frac(1,1+r)frac(delta_H+delta_L,2) $
  ])
  투자자 1인당 균형보유량 $S/N$이 0으로 가므로 각자가 부담하는 위험도 사라지고 위험프리미엄이 0으로 수렴한다.
])

== Exercise 7
#problem("공식 PS3 Exercise 7", [
  위험자산의 현금흐름은 확률 $1/2$로 $mu+alpha$, 확률 $1/2$로 $mu-alpha$이며 $mu>alpha>0$이다. 투자자는 로그효용을 가진다. 단순화를 위해 $r=0,S=1,N=1,Y_0=1$이다.

  (a) 투자문제를 설정하라. (b) 수요함수 $X(P)$를 구하라. (c) $P<=mu$인 해에 초점을 맞춰 균형가격을 구하라. (d) $alpha$가 증가하면 가격은 어떻게 되는가?
])

#maybe-solution("Exercise 7", [
  === (a) 상태별 최종부
  #formula([
    $ Y_1=delta X+(1-PX) $
  ])
  이므로
  #formula([
    $ max_X frac(1,2)ln[(mu+alpha)X+1-PX]
      +frac(1,2)ln[(mu-alpha)X+1-PX] $
  ])

  === (b) 수요함수
  FOC는
  #formula([
    $ frac(1,2)frac(mu+alpha-P,(mu+alpha)X+1-PX)
      +frac(1,2)frac(mu-alpha-P,(mu-alpha)X+1-PX)=0 $
  ])
  이다. 정리하면
  #formula([
    $ X(P)=frac(mu-P,[(mu+alpha)-P][P-(mu-alpha)]) $
  ])

  === (c) 균형가격
  공급과 투자자가 각각 1이므로 시장청산은 $X(P)=1$이다.
  #formula([
    $ mu-P=[(mu+alpha)-P][P-(mu-alpha)] $
  ])
  전개하면
  #formula([
    $ P^2-(1+2mu)P+mu+mu^2-alpha^2=0 $
  ])
  따라서 두 근은
  #formula([
    $ P=mu+frac(1,2)(1 plus.minus sqrt(1+4alpha^2)) $
  ])
  이다. 위험회피 투자자가 기대현금흐름보다 높은 가격을 지지하지 않는다는 조건 $P<=mu$에 따라 작은 근을 선택한다.
  #formula([
    $ P^*=mu+frac(1,2)(1-sqrt(1+4alpha^2)) $
  ])
  또는
  #formula([
    $ P^*=mu-frac(1,2)(sqrt(1+4alpha^2)-1) $
  ])
  로 쓰면 기대지급액에서 위험프리미엄을 뺀 구조가 보인다.

  === (d) 변동성 증가
  #formula([
    $ frac(partial P^*,partial alpha)
      =-frac(2alpha,sqrt(1+4alpha^2))<0 $
  ])

  #answer([
    $alpha$는 현금흐름의 표준편차이며, 증가할수록 요구 위험프리미엄이 커져 가격이 하락한다.
  ])
])
