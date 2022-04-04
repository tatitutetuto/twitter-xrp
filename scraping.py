from bs4 import BeautifulSoup
import requests
import config
import datetime

from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import json
import os
from dotenv import load_dotenv
load_dotenv()
from requests import Request, Session

CMC_AK = os.environ.get('CMC_AK')
CMC_XRP_ID = config.CMC_XRP_ID


class Scraping:

    ##
    ## CoinMarketCapより情報取得
    ##
    def get_xrp_info(self):
        # APIでXRPの情報取得
        cmc = CoinMarketCapAPI(CMC_AK)

        print("cmc:" + str(cmc))
        res = cmc.cryptocurrency_quotes_latest(id=CMC_XRP_ID, convert='JPY')
        print(res)

        # json形式に変更
        res = str(res.data).replace("'", '"') .replace('None', '"None"')
        data = json.loads(res)
        # print(data)

        # 価格取得、小数点第3位を四捨五入
        correct_price = float(data[CMC_XRP_ID]["quote"]["JPY"]["price"])
        price = round(correct_price, 2)
        print(f'リップルの価格は現在{price}円です')
        
        # 出来高取得、小数点第3位を四捨五入
        volume_change_24h = float(data[CMC_XRP_ID]["quote"]["JPY"]["volume_change_24h"])
        volume_change_24h = round(volume_change_24h, 2)
        if volume_change_24h > 0:
            print(f'リップルの出来高は24時間前に比べて{volume_change_24h}%上がっています')

        else:
            print(f'リップルの出来高は24時間前に比べて{volume_change_24h}%下がっています')

        # コインマーケットキャップ内の時価総額取得
#         cmc_rank = data[CMC_XRP_ID]["cmc_rank"]   
#         print(f'リップルの時価総額ランキングは現在{cmc_rank}位です')

        # 24時間前との値段比較、小数点第3位を四捨五入
        correct_percent_change_24h = float(data[CMC_XRP_ID]["quote"]["JPY"]["percent_change_24h"])
        percent_change_24h = round(correct_percent_change_24h, 2)
        if percent_change_24h > 0:
            print(f'リップルの値段は24時間前に比べて{percent_change_24h}%上がっています')

        else:
            print(f'リップルの値段は24時間前に比べて{percent_change_24h}%下がっています')

        return price, volume_change_24h, percent_change_24h
