
# coding: utf-8

# # 상관분석

# In[1]:

from __future__ import print_function, division


# #### 안내사항
# 
# 지난 시간에 다룬 21장과 22장 내용을 활용하고자 한다.
# 따라서 아래와 같이 21장과 21장 내용을 모듈로 담고 있는 파이썬 파일을 임포트 해야 한다.
# 
# **주의:** 아래 두 개의 파일이 동일한 디렉토리에 위치해야 한다.
# * GongSu21_Statistics_Averages.py 
# * GongSu22_Statistics_Population_Variance.py 

# In[2]:

from GongSu22_Statistics_Population_Variance import *


# #### 주의
# 
# 위 모듈을 임포트하면 아래 모듈 또한 자동으로 임포트 된다.
# 
# * GongSu21_Statistics_Averages.py

# ## 주요 내용

# * 상관분석
# * 공분산
# * 상관관계와 인과관계

# ## 주요 예제

# 21장에서 다룬 미국의 51개 주에서 거래되는 담배(식물)의 도매가격 데이터를 보다 상세히 분석한다. 
# 
# 특히, 캘리포니아 주에서 거래된 담배(식물) 도매가와 뉴욕 주에서 거래된 담배(식물) 도매가의 상관관계를 다룬다.

# ## 오늘 사용할 데이터
# 
# * 주별 담배(식물) 도매가격 및 판매일자: Weed_price.csv
# 
# 아래 그림은 미국의 주별 담배(식물) 판매 데이터를 담은 Weed_Price.csv 파일를 엑셀로 읽었을 때의 일부를 보여준다.
# 
# <p>
# <table cellspacing="20">
# <tr>
# <td>
# <img src="img/weed_price.png", width=600>
# </td>
# </tr>
# </table>
# </p>

# **주의:** 언급된 파일이 GongSu21_Statistics_Averages 모듈에서 prices_pd 라는 변수에 저장되었음. 
# 또한 주(State)별, 거래날짜별(date) 기준으로 이미 정렬되어 있음. 
# 
# 따라서 아래에서 볼 수 있듯이 예를 들어, prices_pd의 첫 다섯 줄의 내용은 알파벳순으로 가장 빠른 이름을 가진 알라바마(Alabama) 주에서 거래된 데이터 중에서 가정 먼저 거래된 5개의 거래내용을 담고 있다.

# In[3]:

prices_pd.head()


# ## 상관분석 설명
# 
# 상관분석은 두 데이터 집단이 어떤 관계를 갖고 있는 지를 분석하는 방법이다. 
# 두 데이터 집단이 서로 관계가 있을 때 상관관계를 계산할 수도 있으며, 상관관계의 정도를 파악하기 위해서 대표적으로 피어슨 상관계수가 사용된다. 또한 상관계수를 계산하기 위해 공분산을 먼저 구해야 한다.

# ## 공분산(Covariance)
# 
# 공분산은 두 종류의 데이터 집단 x와 y가 주어졌을 때 한쪽에서의 데이터의 변화와 
# 다른쪽에서의 데이터의 변화가 서로 어떤 관계에 있는지를 설명해주는 개념이다. 
# 공분산은 아래 공식에 따라 계산한다.
# 
# $$Cov(x, y) = \frac{\Sigma_{i=1}^{n} (x_i - \bar x)(y_i - \bar y)}{n-1}$$

# ###  캘리포니아 주와 뉴욕 주에서 거래된 상품(HighQ) 담배(식물) 도매가의 공분산

# #### 준비 작업: 뉴욕 주 데이터 정리하기

# 먼저 뉴욕 주에서 거래된 담배(식물) 도매가의 정보를 따로 떼서 `ny_pd` 변수에 저장하자.
# 방식은 california_pd를 구할 때와 동일하게 마스크 인덱싱을 사용한다.

# In[4]:

ny_pd = prices_pd[prices_pd['State'] == 'New York'].copy(True)
ny_pd.head(10)


# 이제 정수 인덱싱을 사용하여 상품(HighQ)에 대한 정보만을 가져오도록 하자.

# In[5]:

ny_pd_HighQ = ny_pd.iloc[:, [1, 7]]


# 위 코드에 사용된 정수 인덱싱은 다음과 같다.
# 
#     [:, [1, 7]]
#     
# * ':' 부분 설명: 행 전체를 대상으로 한다.
# * '[1, 7]' 부분 설명: 1번 열과 7번 열을 대상으로 한다.
# 
# 결과적으로 1번 열과 7번 열 전체만을 추출하는 슬라이싱을 의미한다.
# 
# 이제 각 열의 이름을 새로 지정하고자 한다. 뉴욕 주에서 거래된 상품(HighQ) 이기에 NY_HighQ라 명명한다.

# In[6]:

ny_pd_HighQ.columns = ['NY_HighQ', 'date']
ny_pd_HighQ.head()


# #### 준비 작업: 캘리포니아 주 데이터 정리하기

# 비슷한 일을 캘리포니아 주에서 거래된 상품(HighQ) 담배(식물) 도매가에 대해서 실행한다.

# In[7]:

ca_pd_HighQ = california_pd.iloc[:, [1, 7]]
ca_pd_HighQ.head()


# #### 준비 작업: 정리된 두 데이터 합치기

# 이제 두 개의 테이블을 date를 축으로 하여, 즉 기준으로 삼아 합친다.

# In[8]:

ca_ny_pd = pd.merge(ca_pd_HighQ, ny_pd_HighQ, on="date")
ca_ny_pd.head()


# 캘리포니아 주의 HighQ 열의 이름을 CA_HighQ로 변경한다.

# In[9]:

ca_ny_pd.rename(columns={"HighQ": "CA_HighQ"}, inplace=True)
ca_ny_pd.head()


# #### 준비 작업: 합친 데이터를 이용하여 공분산 계산 준비하기

# 먼저 뉴욕 주에서 거래된 상품(HighQ) 담배(식물) 도매가의 평균값을 계산한다.

# In[10]:

ny_mean = ca_ny_pd.NY_HighQ.mean()
ny_mean


# 이제 ca_ny_pd 테이블에 새로운 열(column)을 추가한다. 추가되는 열의 이름은 `ca_dev`와 `ny_dev`이다.
# 
# * `ca_dev`: 공분산 계산과 관련된 캘리포니아 주의 데이터 연산 중간 결과값
# * `ny_dev`: 공분산 계산과 관련된 뉴욕 주의 데이터 연산 중간 결과값
# 
# 즉, 아래 공식에서의 분자에 사용된 값들의 리스트를 계산하는 과정임.
# 
# $$Cov(x, y) = \frac{\Sigma_{i=1}^{n} (x_i - \bar x)(y_i - \bar y)}{n-1}$$

# In[11]:

ca_ny_pd['ca_dev'] = ca_ny_pd['CA_HighQ'] - ca_mean
ca_ny_pd.head()


# In[12]:

ca_ny_pd['ny_dev'] = ca_ny_pd['NY_HighQ'] - ny_mean
ca_ny_pd.head()


# #### 캘리포니아 주와 뉴욕 주에서 거래된 상품(HighQ) 담배(식물) 도매가의 공분산
# 
# 이제 공분산을 쉽게 계산할 수 있다.
# 
# **주의:** 
# * DataFrame 자료형의 연산은 넘파이 어레이의 연산처럼 항목별로 실행된다.
# * sum 메소드의 활용을 기억한다.

# In[13]:

ca_ny_cov = (ca_ny_pd['ca_dev'] * ca_ny_pd['ny_dev']).sum() / (ca_count - 1)
ca_ny_cov


# ## 피어슨 상관계수
# 
# 피어슨 상관계수(Pearson correlation coefficient)는 두 변수간의 관련성 정도를 나타낸다. 
# 
#     두 변수 x와 y의 상관계수(r) = x와 y가 함께 변하는 정도와 x와 y가 따로 변하는 정도 사이의 비율
# 
# 즉, $$r = \frac{Cov(X, Y)}{s_x\cdot s_y}$$
# 
# * 의미: 
#     * r = 1: X와 Y 가 완전히 동일하다.
#     * r = 0: X와 Y가 아무 연관이 없다
#     * r = -1: X와 Y가 반대방향으로 완전히 동일 하다.
# 
# 
# * 선형관계 설명에도 사용된다.    
#     * -1.0 <= r < -0.7: 강한 음적 선형관계
#     * -0.7 <= r < -0.3: 뚜렷한 음적 선형관계
#     * -0.3 <= r < -0.1: 약한 음적 선형관계
#     * -0.1 <= r <= 0.1: 거의 무시될 수 있는 관계
#     * 0.1 < r <= +0.3: 약한 양적 선형관계
#     * 0.3 < r <= 0.7: 뚜렷한 양적 선형관계
#     * 0.7 < r <= 1.0: 강한 양적 선형관계

# #### 주의
# 
# 위 선형관계 설명은 일반적으로 통용되지만 예외가 존재할 수도 있다.
# 예를 들어, 아래 네 개의 그래프는 모두 피어슨 상관계수가 0.816이지만, 전혀 다른 상관관계를 보여주고 있다.
# (출처: https://en.wikipedia.org/wiki/Correlation_and_dependence)
# <p>
# <table cellspacing="20">
# <tr>
# <td>
# <img src="img/pearson_relation.png", width=600>
# </td>
# </tr>
# </table>
# </p>

# ### 캘리포니아 주와 뉴욕 주에서 거래된 상품(HighQ) 담배(식물) 도매가의 상관계수 계산하기

# In[14]:

ca_highq_std = ca_ny_pd.CA_HighQ.std()
ny_highq_std = ca_ny_pd.NY_HighQ.std()

ca_ny_corr = ca_ny_cov / (ca_highq_std * ny_highq_std)
ca_ny_corr


# ## 상관관계(Correlation)와 인과관계(Causation)
# 
# * 상관관계: 두 변수 사이의 상관성을 보여주는 관계. 즉, 두 변수 사이에 존재하는 모종의 관련성을 의미함.
#     * 예를 들어, 캘리포니아 주의 상품 담배(식물) 도매가와 뉴육 주의 상품 담배(식물) 도매가 사이에는 모종의 관계가 있어 보임. 
#         캘리포니아 주에서의 가격이 오르면 뉴욕 주에서의 가격도 비슷하게 오른다. 상관정도는 0.979 정도로 매우 강한 양적 선형관계를 보인다.
# 
# 
# * 인과관계: 두 변수 사이에 서로 영향을 주거나 실제로 연관되어 있음을 보여주는 관계.
# 
# **주의:** 두 변수 사이에 상관관계가 있다고 해서 그것이 반드시 어느 변수가 다른 변수에 영향을 준다든지, 아니면 실제로 연관되어 있음을 뜻하지는 않는다. 
# 
# 예를 들어, 캘리포니아 주의 담배(식물) 도매가와 뉴욕 주의 담배(식물) 도매가 사이에 모종의 관계가 있는 것은 사실이지만, 그렇다고 해서 한 쪽에서의 가격 변동이 다른 쪽에서의 가격변동에 영향을 준다는 근거는 정확하게 알 수 없다. 

# ## 연습문제

# ### 연습
# 
# 모집단의 분산과 표준편차에 대한 점추정 값을 계산하는 기능이 이미 Pandas 모듈의 DataFrame 자료형의 메소드로 구현되어 있다.
# 
# `describe()` 메소드를 캘리포니아 주에서 거래된 담배(식물)의 도매가 표본을 담고 있는 `california_pd`에서 실행하면 아래와 같은 결과를 보여준다.
# 
# * count: 총 빈도수, 즉 표본의 크기
# * mean: 평균값
# * std: 모집단 표준편차 점추정 값
# * min: 표본의 최소값
# * 25%: 하한 사분위수 (하위 4분의 1을 구분하는 위치에 자리하는 수)
# * 50%: 중앙값
# * 75%: 상한 사분위수 (상위 4분의 1을 구분하는 위치에 자리하는 수)
# * max: 최대값

# In[15]:

california_pd.describe()


# ### 연습

# 공분산에 대한 점추정 값을 계산하는 기능이 이미 Pandas 모듈의 DataFrame 자료형의 메소드로 구현되어 있다.
# 
# cov() 메소드를 캘리포니아 주와 뉴욕 주에서 거래된 담배(식물)의 도매가 표본을 담고 있는 ca_ny_pd에서 실행하면 아래와 같은 결과를 보여준다.

# In[16]:

ca_ny_pd.cov()


# 위 테이블에서 CA_HighQ와 NY_HighQ가 만나는 부분의 값을 보면 앞서 계산한 공분산 값과 일치함을 확인할 수 있다.

# ### 연습

# 상관계수에 대한 점추정 값을 계산하는 기능이 이미 Pandas 모듈의 DataFrame 자료형의 메소드로 구현되어 있다.
# 
# corr() 메소드를 캘리포니아 주와 뉴욕 주에서 거래된 담배(식물)의 도매가 표본을 담고 있는 ca_ny_pd에서 실행하면 아래와 같은 결과를 보여준다.

# In[17]:

ca_ny_pd.corr()


# 위 테이블에서 CA_HighQ와 NY_HighQ가 만나는 부분의 값을 보면 앞서 계산한 상관계수 값과 일치함을 확인할 수 있다.
