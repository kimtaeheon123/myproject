#####!!!!!!!!!!!!!!!!!!!
# 1. SettingCandlePattern 함수로 캔들의 정보를 수치화한다. 총,몸통,윗꼬리,아랫꼬리의 크기 + 윗꼬리,아랫꼬리의 비율
# 2. 이를 토대로 단일캔들패턴을 파악한다. (ex) 샅바형, 장대캔들, 망치, 역망치형)
# 예를들어 샅바형의 경우 윗꼬리가 있으며 아랫꼬리가 거의 없어야 한다. 윗꼬리가 있어야한다는 조건은 주관적일수 있으므로 조절가능하게 함수를 만들었다.
# 단일캔들패턴의 result가 1이면 양봉 2면 음봉이다.
#####!!!!!!!!!!!!!!!!!!!
import pandas as pd
import numpy as np

df_15 = pd.read_csv("C:/Users/rlaxo/Desktop/bitcoin/BTCUSDT15m.csv")

#캔들 패턴 세팅!!!!!!!!!!!!!!!!!!!!!!!!1
def SettingCandlePattern(df):
  #총 크기
  df['totaldiff'] = df['high'] - df['low']
  #몸통의 크기
  df['bodydiff'] = abs(df['open']-df['close'])
  #윗꼬리 크기
  df['highdiff'] = df['high'] - df[['open','close']].max(axis=1)
  #아랫꼬리 크기
  df['lowdiff'] = df[['open','close']].min(axis=1) - df['low']
  #윗꼬리 비율
  df['high_rat'] = df['highdiff']/ (df['totaldiff'])
  #아래꼬리 비율
  df['low_rat'] = df['lowdiff'] / (df['totaldiff'])

SettingCandlePattern(df_15)

##단일 캔들 패턴!!!!!!!!!!!!!!!!!!!!!!!!!!!
###꼬리가 거의 없다: 0.15, 꼬리가 있어야할 경우: 0.2<a<0.4?, 꼬리가 더크다: 0.5<a<=0.8, 꼬리가 있긴한데 없다고 생각할만큼 납득가능하다:<0.3
def Upbelt(df, lr=0.15, hr=0.24, k=1.2, hrr=0.46):
    # 윗꼬리 캔들 or 상승샅바형
    # lr: low_rat , hr: high_rat, k: highdiff>k*lowdiff, hrr: high_rat<=hrr
    cond = [(df['bodydiff'] > 10) & (df['close'] > df['open']) & (df['low_rat'] < lr) & (df['high_rat'] > hr) & (
                df['highdiff'] > k * df['lowdiff']) \
            & (df['high_rat'] <= hrr),
            (df['bodydiff'] > 10) & (df['close'] < df['open']) & (df['low_rat'] < lr) & (df['high_rat'] > hr) & (
                        df['highdiff'] > k * df['lowdiff']) \
            & (df['high_rat'] <= hrr)]

    choices = [1, 2]
    df['Upbelt'] = np.select(cond, choices, default=0)


def FullCandle(df, lr=0.15, hr=0.3):
    # 몸통찬 캔들
    # lr: low_rat, hr: high_rat in bullish, hr:low_rat, lr:high_rat in bearish
    cond = [(df['bodydiff'] > 10) & (df['close'] > df['open']) & (df['low_rat'] < lr) & (df['high_rat'] < hr), \
            (df['bodydiff'] > 10) & (df['close'] < df['open']) & (df['low_rat'] < hr) & (df['high_rat'] < lr)]
    choices = [1, 2]
    df['FullCandle'] = np.select(cond, choices, default=0)


def ReverseHammer(df, lr=0.15, hr=0.5, hrr=0.8):
    # lr: low_rat, hr: high_rat, hrr: high_rat<=hrr
    cond = [(df['bodydiff'] > 10) & (df['close'] > df['open']) & (df['low_rat'] < lr) & (df['high_rat'] >= hr) & (
                df['high_rat'] < hrr) \
        , (df['bodydiff'] > 10) & (df['close'] < df['open']) & (df['low_rat'] < lr) & (df['high_rat'] >= hr) & (
                        df['high_rat'] < hrr)]
    choices = [1, 2]
    df['ReverseHammer'] = np.select(cond, choices, default=0)


def Hammer(df, lr=0.5, hr=0.15, lrr=0.8):
    cond = [(df['bodydiff'] > 10) & (df['close'] > df['open']) & (df['high_rat'] < hr) & (df['low_rat'] >= lr) & (
                df['low_rat'] < lrr) \
        , (df['bodydiff'] > 10) & (df['close'] < df['open']) & (df['high_rat'] < hr) & (df['low_rat'] >= lr) & (
                        df['low_rat'] < lrr)]
    choices = [1, 2]
    df['Hammer'] = np.select(cond, choices, default=0)


def Downbelt(df, lr=0.24, hr=0.15, k=1.2, lrr=0.46):
    # 아랫꼬리 캔들 or 하락샅바형
    # lr: low_rat , hr: high_rat, k: highdiff>k*lowdiff, hrr: high_rat<=hrr
    cond = [(df['bodydiff'] > 10) & (df['close'] > df['open']) & (df['low_rat'] > lr) & (df['high_rat'] < hr) & (
                df['lowdiff'] > k * df['highdiff']) \
            & (df['low_rat'] <= lrr),
            (df['bodydiff'] > 10) & (df['close'] < df['open']) & (df['low_rat'] > lr) & (df['high_rat'] < hr) & (
                        df['lowdiff'] > k * df['highdiff']) \
            & (df['low_rat'] <= lrr)]

    choices = [1, 2]
    df['Downbelt'] = np.select(cond, choices, default=0)


Upbelt(df_15)
print("Upbelt: ", df_15['Upbelt'].value_counts())
FullCandle(df_15)
print("FullCandle: ", df_15['FullCandle'].value_counts())
ReverseHammer(df_15)
print("ReverseHammer: ", df_15['ReverseHammer'].value_counts())
Hammer(df_15)
print("Hammer: ", df_15['Hammer'].value_counts())
Downbelt(df_15)
print("Downbelt: ", df_15['Downbelt'].value_counts())