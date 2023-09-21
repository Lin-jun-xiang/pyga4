<p align="center">
    <img src='https://github.com/Lin-jun-xiang/pyga4/blob/main/static/images/pyGA4_logo.PNG?raw=true' width='60%' />
</p>

[English version](README.md) | [Chinese version README.md](README.zh-TW.md)

## 大綱

- [大綱](#大綱)
- [簡介](#簡介)
- [如何將 GA4 數據實時串流到 Bigquery?](#如何將-ga4-數據實時串流到-bigquery)
- [功能](#功能)
- [如何使用?](#如何使用)
    - [下載套件](#下載套件)
    - [連接您的 Bigquery](#連接您的-bigquery)
    - [連接 GA4 資料表](#連接-ga4-資料表)
    - [使用 dry run 評估查詢費用](#使用-dry-run-評估查詢費用)
    - [分析使用者屬性](#分析使用者屬性)
    - [分析裝置屬性](#分析裝置屬性)
    - [分析事件](#分析事件)

---

## 簡介

* `pyga4` 是一個 Python 工具箱，設計用於從 **Google Analytics 4 (GA4)** 提取、處理和分析資料。
* 無論您是數位行銷專業人士、數據分析師或有興趣從 GA4 資料中獲得洞見的任何人，這個套件簡化了處理 GA4 資料的流程。

## 如何將 GA4 數據實時串流到 Bigquery?

首先，我們假設每個人都已經將 GA4 資料串接到各自的平台網站上了(相信網上很多教學文章)。

接下來，我們會透過免費第三方服務，將資料串流到 Bigquery 中，詳細操作請參考[官方文檔](https://support.google.com/analytics/answer/9823238?hl=en#zippy=%2Cin-this-article)

如果成功串接，你會在 Bigquery 中看到類似以下的資料表(`analytics_xxxx`)，[圖片來源](https://analyticscanvas.com/knowledge-base/ga4-bigquery-export-tutorial-002-querying-event-params/):

![https://analyticscanvas.com/knowledge-base/ga4-bigquery-export-tutorial-002-querying-event-params/](static/images/2023-09-21-15-04-30.png)


## 功能

- **評估查詢預算**: 提供 Bigquery `dry run` 功能，進行查詢前可以先知道使用量
- **資料提取**: 輕鬆連接到您的 GA4 網站，擷取資料並儲存以進行分析。
- **資料預處理**: 使用內建的資料預處理函數準備和清理 GA4 資料，以便進行分析。
- **自訂查詢**: 根據您的特定需求執行自定查詢以篩選和彙總資料。
- **資料分析**: 執行各種類型的分析，包括使用者行為分析、轉換追蹤等。
- **資料視覺化**: 創建資訊豐富的視覺化和報告，以有效地傳達您的發現。
- **簡單整合**: 無縫地將 `pyGA4` 集成到您的資料管道或分析工作流程中。

## 如何使用?

更多功能，請參考[套件說明檔](https://lin-jun-xiang.github.io/pyga4/)

#### 下載套件

`pip install pyga4`

#### 連接您的 Bigquery 
```python
from google.cloud import bigquery

client = bigquery.Client()
# Or you can use:
# client = bigquery.Client.from_service_account_json(
#    './private/service-project-data-dev-01d11c742ba1.json'
# )
```

#### 連接 GA4 資料表
```python
from pyga4.model import Ga4Table

# Use your project_id, dataset_name(analytics_xxxx)
ga4_table = Ga4Table(client, PROJECT_ID, DATASET_NAME)

# Show the tables list in dataset, ex: analytics_date1, analytics_date2
table_id_list = ga4_table.all_tables_list
print(table_id_list)

# Select the table which want analyze
ga4_table.table_id = 'events_intraday_20200812'
```

#### 使用 dry run 評估查詢費用

```python
    # Query with dry run:
    ga4_table.query_config.dry_run = True
    query = f"""
    SELECT event_timestamp FROM `<project_id>.<dataset_name>.<data_table>`
    """
    results = ga4_table.query(query) # return None, but you can see the query usage!
```

#### 分析使用者屬性

**查詢使用者id、國家列表**

```python
# User attribute
user_id_list = ga4_table.user_id_list
user_country_list = ga4_table.geo_country_list
```

**查詢使用者id、國家分布**

```python
from pyga4.analytic import UserAnalytic

# UserAnalytic
user_analytic = UserAnalytic(ga4_table)
countries_dist = user_analytic.countries_distribution
userid_dist = user_analytic.user_id_distribution
```

#### 分析裝置屬性

```python
# DeviceAnalytic
device_analytic = DeviceAnalytic(ga4_table)
mobile_brand_dist = device_analytic.mobile_brand_distribution
```

#### 分析事件

```python
# EventAnalytic
event_analytic = EventAnalytic(ga4_table)
page_loc_dist = event_analytic.pages_distribution
```

<a href="#top">Back to top</a>
