import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import mojimoji
import json
import xmltodict

# 現在時刻
dt_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

# 最新の情報を取得
url = "https://www.pref.toyama.jp/120507/kurashi/kenkou/kenkou/covid-19/kj00022038.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
}
r = requests.get(url, headers=headers)
r.raise_for_status()
soup = BeautifulSoup(r.content, "html.parser")

# 一覧エクセルを取得
file_list = soup.find("div", id="tmp_contents")
link = file_list.find("a",text=re.compile('^強化・緩和の判断指標（直近1週間平均）の推移（エクセル')).get("href")
df = pd.read_excel('https://www.pref.toyama.jp' + link, header=None, index_col=None, engine="openpyxl")

# データ部分のみ取り出し
df = df.iloc[2:9, 3:]

# 反転
df = df.T

# リネーム
df.rename(columns={2: "日付", 3: "入院者数", 4: "重症病床稼働率", 5: "新規陽性者数", 6: "感染経路不明者数", 7: "陽性率", 8: "先週対比"}, inplace=True)

# 欠損値が含まれる行を削除
df = df.dropna(how='any')

# データ処理
df["日付"] = df["日付"].apply(lambda x: re.search(r'\d{1,2}\/\d{1,2}', x)[0])
#df["入院者数"] = df["入院者数"].apply(lambda x: float(mojimoji.zen_to_han(x[:-1])))
#df["重症病床稼働率"] = df["重症病床稼働率"].apply(lambda x: round(x * 100, 2))
#df["新規陽性者数"] = df["新規陽性者数"].apply(lambda x: float(mojimoji.zen_to_han(x[:-1])))
#df["感染経路不明者数"] = df["感染経路不明者数"].apply(lambda x: float(mojimoji.zen_to_han(x[:-1])))
#df["陽性率"] = df["陽性率"].apply(lambda x: round(x * 100, 1))

# 日付処理
df.loc[:236, ["日付"]] = '2020/' + df.loc[:236, ["日付"]]
df.loc[237:601, ["日付"]] = '2021/' + df.loc[237:601, ["日付"]]
df.loc[602:, ["日付"]] = '2022/' + df.loc[602:, ["日付"]]
df["日付"] = pd.to_datetime(df["日付"], format="%Y/%m/%d")
df["日付"] = df["日付"].dt.strftime("%Y-%m-%d")

# モニタリング項目の状況
with open('../data/monitoring_summary.json', 'w', encoding='utf-8') as file:
    data = {
        "date": dt_now,
        "data": {
            "日付": df.iloc[-1]["日付"],
            "(1)入院者数": df.iloc[-1]["入院者数"],
            "(2)重症病床稼働率": df.iloc[-1]['重症病床稼働率'],
            "(3)新規陽性者数": df.iloc[-1]['新規陽性者数'],
            "(4)感染経路不明の新規陽性者数": df.iloc[-1]['感染経路不明者数'],
            "(A)陽性率": df.iloc[-1]['陽性率'],
            "(B)先週対比": df.iloc[-1]['先週対比']
        }
    }
    json.dump(data, file, ensure_ascii=False, indent=4)

# モニタリング項目
df_monitoring = df.loc[:, ["日付", "入院者数", "重症病床稼働率", "新規陽性者数", "感染経路不明者数", "陽性率"]]
df_monitoring.rename(columns={"日付": "date", "入院者数": "hospitalized_number", "重症病床稼働率": "severe_bed_occupancy_rate", "新規陽性者数": "patients_number", "感染経路不明者数": "untracked_patients_number", "陽性率": "positive_rate"}, inplace=True)
data = {"date": dt_now, "data": df_monitoring.to_dict(orient="records")}
with open('../data/monitoring_status.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# 最新の情報を取得
url = "https://www.pref.toyama.jp/120507/kurashi/kenkou/kenkou/covid-19/kj00021798.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
}
r = requests.get(url, headers=headers)
r.raise_for_status()
soup = BeautifulSoup(r.content, "html.parser")

# 検査陽性者の状況
summary = soup.find("div", id="tmp_contents").get_text(strip=True)
# 空白をすべて削除
summary = re.sub(r"\s+", "", summary)
# カンマをすべて削除
summary = re.sub(r",", "", summary)
# 新規感染者数
new = int(mojimoji.zen_to_han(re.search(r"新規感染者数(\d+)", summary).group(1)))
# 陽性患者数
total = int(mojimoji.zen_to_han(re.search(r"感染者数累計(\d+)", summary).group(1)))
# 入院中
hospitalized = int(mojimoji.zen_to_han(
    re.search(r"入院者数(\d+)", summary).group(1)))
# 重症
severe = int(mojimoji.zen_to_han(re.search(r"重症者(\d+)", summary).group(1)))
# 無症状・軽症・中等症
mild = hospitalized - severe
# 宿泊療養
lodging = int(mojimoji.zen_to_han(re.search(r"宿泊療養施設入所者数(\d+)", summary).group(1)))
# 自宅療養
home = int(mojimoji.zen_to_han(re.search(r"自宅療養者数(\d+)", summary).group(1))) + int(mojimoji.zen_to_han(re.search(r"入院等調整中(\d+)", summary).group(1)))
# 死亡
death = int(mojimoji.zen_to_han(re.search(r"死亡者数(\d+)", summary).group(1)))
# 退院
discharged = int(mojimoji.zen_to_han(re.search(r"退院及び療養解除者数(\d+)", summary).group(1)))

# 公表日別による新規陽性者数の推移
with open('../data/patients_number.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    data["date"] = dt_now
    if data["data"][-1]["日付"] != datetime.datetime.now().strftime("%Y-%m-%d"):
        data["data"].append({"日付": datetime.datetime.now().strftime("%Y-%m-%d"), "小計": new})
    with open('../data/patients_number.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 検査陽性者の状況
with open('../data/patients_summary.json', 'w', encoding='utf-8') as file:
    data = {
        "date": dt_now,
        "attr": "陽性者数",
        "value": total,
        "children": [{
            "attr": "入院",
            "value": hospitalized,
            "children": [{
                "attr": "軽症・中等症",
                "value": mild
            },
            {
                "attr": "重症",
                "value": severe
            }]
        },
        {
            "attr": "宿泊療養",
            "value": lodging
        },
        {
            "attr": "自宅療養",
            "value": home
        },
        {
            "attr": "死亡",
            "value": death
        },
        {
            "attr": "退院等",
            "value": discharged
        }
        ]
    }
    json.dump(data, file, ensure_ascii=False, indent=4)

# newsItems
url = "https://www.pref.toyama.jp/1021/kurashi/kenkou/iryou/virus/shinchaku/shinchaku.xml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
}
r = requests.get(url, headers=headers)
r.raise_for_status()
dictionary = xmltodict.parse(r.content)["rdf:RDF"]["item"][:5]
with open('../data/news.json', 'w', encoding='utf-8') as file:
    data = {"newsItems": dictionary}
    json.dump(data, file, ensure_ascii=False, indent=4)

# 最終更新日時
with open('../data/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    data["lastUpdate"] = dt_now
    with open('../data/data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
