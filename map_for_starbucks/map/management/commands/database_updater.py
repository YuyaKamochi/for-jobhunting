import datetime
from ...models import ShopList
import time
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json #緯度軽度用
import re
from tqdm import tqdm

# Linux上でcronコマンドから自動実行
# python manage.py database_updater

class Command(BaseCommand):
    help = "Update database"

    def handle(self, *args, **options):
    # # スクレイピングを実行
        try:
            maxid = ShopList.objects.latest('id').id
            if maxid<4372: maxid=4372
        except:
            maxid = 4372
        for i in tqdm(range(int(maxid)+100)):
            data = get_shop_detail(i) #スクレイピング
            time.sleep(1)

            # スクレイピング結果をデータベースに保存または更新
            if ShopList.objects.filter(id=i).exists(): #id=iのレコードが存在する
                if len(data) == 0: #スクレイピング結果なし
                    shop = ShopList.objects.get(id=i)
                    setattr(shop, "closed", True)
                    shop.save()
                else: #スクレイピング結果あり
                    data = hour_exchanger(data)
                    shop = ShopList.objects.get(id=i)
                    setattr(shop, "name", data['name']) #店舗名更新（open情報を消す）
                    setattr(shop, "closed", False)
                    setattr(shop, "monday", data['monday'])
                    setattr(shop, "tuesday", data['tuesday'])
                    setattr(shop, "wednesday", data['wednesday'])
                    setattr(shop, "thursday", data['thursday'])
                    setattr(shop, "friday", data['friday'])
                    setattr(shop, "saturday", data['saturday'])
                    setattr(shop, "sunday", data['sunday'])
                    setattr(shop, "holiday", data['holiday'])
                    shop.save()
            elif not len(data) == 0: #スクレイピング結果あり
                data = hour_exchanger(data)
                data.rename({'number':'id'},inplace=True)
                data['yuya'] = False
                data['non'] = False
                data['add_day'] = datetime.date.today()
                dic_data = data.to_dict()
                ShopList.objects.create(**dic_data) #dataの中身をdictで渡す

        print(datetime.datetime.today())

def get_shop_detail(shop_num,base='https://store.starbucks.co.jp/detail-'):
    url = base + str(shop_num) +'/'
    
    html = requests.get(url) # リクエスト
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'lxml')
    
    try:
        address = soup.find_all(class_='store-detail__text-detail line-height-22')[0].string
        addlis = address.strip().split('　',1)

        # 新しい行を作成するために、空のSeriesを作成
        new_row = pd.Series(dtype='str')
        
        # 新しい行に値を設定
        new_row['postcode'] = addlis[0]
        new_row['address'] = addlis[1]
        new_row['prefecture'] = addlis[1].split(' ',1)[0]
        new_row['number'] = shop_num
        new_row['name'] = soup.find_all(class_ = 'store-detail__title-text')[0].string

        #緯度軽度
        script_tags = soup.find_all('script', {'type': 'application/ld+json'})
        for script_tag in script_tags:
            json_data = script_tag.string
            data = json.loads(json_data)
            if 'geo' in data:
                new_row['latitude'] = (data['geo']['latitude'])
                new_row['longitude'] = (data['geo']['longitude'])
        
        #ドライブスルー
        store_type_text = soup.find('div', class_='store-type__text').text if soup.find('div', class_='store-type__text') else 'None'
        if "お車でも便利なドライブスルー店舗です。" in store_type_text:
            new_row['drivethrough'] = True
        else:
            new_row['drivethrough'] = False

        #営業時間
        new_row['businesshour'] = soup.find_all(class_='store-detail__text-detail Sodo-text number-text')[1].text

        new_row['closed'] = False

    except:
        new_row = pd.Series(dtype='str')

    return new_row

def extract_business_hours(pattern, text):
    #get_businesshourで使う
    matches = re.findall(pattern, text)
    return matches

def get_businesshour(text):
    #hour_exchangerで使う
    if pd.isna(text): # 欠損値の場合
        text = ''

    # 営業時間を抽出するための正規表現パターン
    pattern = r'([月火水木金土日祝～・]*)：*(\d{2}:\d{2})～(\d{2}:\d{2})'

    # 曜日の順番を定義
    weekdays = ['月', '火', '水', '木', '金', '土', '日', '祝']

    # 営業時間を抽出
    business_hours_list = extract_business_hours(pattern, text)

    # 曜日ごとに開店時間を表にまとめる
    opening_hours = {}
    for text, start_time, end_time in business_hours_list:
        if not text: # 曜日なしの場合
            text = '月～祝'
        if '～' in text:
            days = weekdays[weekdays.index(text[0]):weekdays.index(text[2])+1]
        elif '・' in text:
            for i in range(len(text)):
                days.append(text[i])
        elif text in weekdays: #土
            days = [text]
        elif text[1] in weekdays: #日祝
            days = []
            for i in range(len(text)):
                days.append(text[i])
        
        for day in days:
            opening_hours[day] = (start_time, end_time)

    # Seriesに変換
    opening_hours_series = pd.Series(opening_hours)

    # 曜日の順番を設定し、ない曜日は欠損値 (NaN) を設定
    opening_hours_series = opening_hours_series.reindex(weekdays)

    return opening_hours_series

def hour_exchanger(row):
    """
    pd.Seriesを受け取り、月～日祝までの項目を足して返す。

    Paramateres
    ----------------
    row : pd.Series

    Returns
    ----------------
    row : pd.Series
    """
    opening_hours_series = get_businesshour(row['businesshour'])
    weekdays = ['月', '火', '水', '木', '金', '土', '日', '祝']
    eng_weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','holiday']
    for day,eng_day in zip(weekdays,eng_weekdays):
        row[eng_day] = opening_hours_series[day]
    
    return row