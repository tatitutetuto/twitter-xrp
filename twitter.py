from requests_oauthlib.oauth1_session import OAuth1Session
import tweepy
import config
import json
import os

# トークン等取得
AK = os.environ.get('TWITTER_XRP_API_KEY')
AS = os.environ.get('TWITTER_XRP_API_SECRET_KEY')
AT = os.environ.get('TWITTER_XRP_ACCESS_TOKEN')
ATS = os.environ.get('TWITTER_XRP_ACCESS_TOKEN_SECRET')
BT = os.environ.get('TWITTER_XRP_BEARER_TOKEN')

# Twitterオブジェクトの生成
client = tweepy.Client(BT, AK, AS, AT, ATS)
twitter_api =  OAuth1Session(AK, AS, AT, ATS)

class Twitter:
    def __init__(self, price, volume_change_24h, percent_change_24h):
        self.price = price
        self.volume_change_24h = volume_change_24h
        self.percent_change_24h = percent_change_24h

    ##
    ## リップルの情報をCMCから取得する
    ##
    def tweet_xrp_info(self):
         # 前回の時価総額ランキングを取得
        last_tweet_id = self.get_last_tweet()
        
        # ツイート内容
        content = self.get_tweet_content()
        print('content:' + content)

        # ツイートを投稿
        res = client.create_tweet(text=content)
        print('res:' + res)
        return last_tweet_id
        
    ##
    ## 前回の時価総額ランキングを取得する
    ##
    def get_last_tweet(self):
        # 過去ツイート取得
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {'count':5}
        res = twitter_api.get(url, params=params)
        timeline = json.loads(res.text)
        last_tweet_id = ''

        # ツイート内容確認　5ツイート遡って、出来高ツイートがあるかを調べる
        for i in range(5):
            print("i:" + str(i))
            tweet_content = timeline[i]['text']

            target = 'リップルの出来高は24時間前に比べて'
            idx = tweet_content.find(target)

            # 出来高ツイートがあれば、ループ抜ける
            if(idx != -1):
                last_tweet_id = int(timeline[i]['id_str'])
                break
        
        return last_tweet_id

    ##
    ## リツイートする
    ##
    def retweet(self, last_tweet_id):
        last_tweet_id = str(last_tweet_id)
        # 検索API叩く , 'since_id':since_id
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        params = {
            'q':config.SEARCH_WORD
            , 'lang':'ja'
            , 'result_type':'recent'
            , 'since_id':last_tweet_id
        }
        res = twitter_api.get(url, params=params)
    
        # 返却値json読み込み
        res = json.loads(res.text)
        news_count = len(res['statuses'])
        res_list = res['statuses']
        res_list_size = len(res_list)

        if (news_count != 0):
        # 取得したツイートを回す
            for res_row in range(res_list_size):
                tweet_id = res_list[res_row]['id_str']
                text = res_list[res_row]['text']
                print('tweet_id:' + tweet_id)
                print('text:' + text)
                print('----------------------------------------------')

                if ('リップル' in text or 'XRP' in text):
                    # リツイートAPI叩く
                    url = 'https://api.twitter.com/1.1/statuses/retweet/' + tweet_id + '.json'

                    # リツイートパラメータ設定
                    params = {
                        'id' : tweet_id
                        ,'include_entities' : ''
                    }

                    # リツイート
                    res = twitter_api.post(url, params=params)


    ##
    ## DM通知
    ##
    # def info_direct_message(self):
    #     params = {("count",3)}
    #     getlist = twitter_api.get("https://api.twitter.com/1.1/direct_messages/events/list.json")
    #     dmlist = json.loads(getlist.text)
    #     for line in dmlist:
    #         if len(line) > 0:
    #             print(line["text"])


    ##
    ## ツイート内容を取得する
    ##
    def get_tweet_content(self):
        content = ''
        volume_change_24h_str = str(self.volume_change_24h)
        percent_change_24h_str = str(self.percent_change_24h)
        
        if self.volume_change_24h >= 0:
            volume_change_24h_str = '+' + str(self.volume_change_24h)
            
        if self.percent_change_24h >= 0:
            percent_change_24h_str = '+' + str(self.percent_change_24h)

            
        if self.percent_change_24h < 0:
            content = f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です。\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です。\n\n'            
            content +=  '#XRP #仮想通貨' 
            
        elif 0 <= self.percent_change_24h < 4:
            content = f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です。\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です。\n\n'            
            content += '#XRP #仮想通貨' 
             
        elif 4 <= self.percent_change_24h < 8:
            content = '【いい調子♪】\n'
            content += f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です!\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です!\n\n'            
            content += '#XRP #仮想通貨' 

        elif 8 <= self.percent_change_24h < 13:
            content = '【きてるｳﾎ！】\n'
            content += f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です!\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です!!\n\n'            
            content += '#XRP #仮想通貨' 

        elif 13 <= self.percent_change_24h < 20:
            content = '【うぉおおぉｳﾎｳﾎｳﾎｳﾎ!!】\n'
            content += f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です!!\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です!!\n\n'            
            content += '#XRP #仮想通貨' 

        elif 20 <= self.percent_change_24h < 40:
            content = '【ｳﾎｳﾎｳｯﾎｳﾎｳｯﾎ!!!ｳﾎ!!!】\n'
            content += f'現在リップルの値段は{self.price}円ｳﾎ。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です!!!\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%ｳﾎ!\n\n'
            content += '#XRP #仮想通貨' 

        elif 40 <= self.percent_change_24h < 70:
            content = '【ｳｯﾎｳｯﾎｳﾎｳｯﾎ!!ｳｯﾎｳｯﾎｳﾎｳﾎｳｯﾎｳｯﾎｯﾎ!!!!!!!】\n'
            content += f'ｳｯﾎは{self.price}円ｳｯﾎ。\n'
            content += f'ｳﾎは24時間前に比べて{percent_change_24h_str}%ｳｯﾎｳｯﾎ!!\n'
            content += f'ｳﾎｳﾎは24時間前に比べて{volume_change_24h_str}%ｳﾎ!!\n\n'
            content += '#XRPｳﾎ #XRP' 

        elif 70 <= self.percent_change_24h:
            content = '生きてて良かった・・\n'
            content += f'現在リップルの値段は{self.price}円です。\n'
            content += f'これは24時間前に比べて{percent_change_24h_str}%です。\n'
            content += f'出来高は24時間前に比べて{volume_change_24h_str}%です。\n\n'
            content += '#XRPｳﾎｳﾎ #XRP' 

        return content



