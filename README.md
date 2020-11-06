# stock
2020 금융 빅데이터 페스티벌 - 미래에셋대우
고려대학교 - 손도희, 이태호, 김재영

## Introduction

대회 주최측에서 제공한 데이터
- 각 그룹별 201907 ~ 202006 기간동안 매수고객수 / 매도고객수 / 평균매수수량 / 평균매도수량 / 매수가격_중앙값 / 매도가격_중앙값
- 각 종목별 20190701 ~ 20200728 기간동안 종목시가 / 종목고가 / 종목저가 / 종목종가 / 거래량 / 거래금액_만원단위 

목표
202007 에 각 그룹별 가장 많이 매수할 종목 예측


## Dependencies

* Python
* Numpy
* pandas
* torch


## Files

```
.
├── core
    ├── __init__.py
    ├── args.py
    ├── dataloader.py
    ├── model.py
    ├── trainer.py
├── feature_engineering
    ├── 고객그룹별대분류선호도그래프
    ├── 고객그룹별선호도벡터
    ├── 고객그룹별중분류선호도그래프
    ├── 고객그룹별코스닥코스피선호도그래프
    ├── 종목분류별주가추이
    ├── KOSPI_KOSDAQ_preference.py
    ├── client-stock.py
    ├── lastest_purchase_tendency.py
    ├── prevSellNum_prevBuyNum.py
    ├── price_tendency.py
├── Dockerfile
├── README.md
├── docker-compose.yml
├── main.py
├── requirements.txt
├── result.csv
```

### Train Model

```bash
$ python main.py -b 10
```

### Test Model

```bash
$ python main.py -b 1 —ckpt checkpoint.pt -m test
```
