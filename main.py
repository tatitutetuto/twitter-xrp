import scraping as sp
import twitter as tw
import line as ln

def main():
    try:
        # 値段、出来高を取得 
        scraping = sp.Scraping()
        price, volume_change_24h, percent_change_24h = scraping.get_xrp_info()

        # リップルの情報をツイートする
        twitter = tw.Twitter(price, volume_change_24h, percent_change_24h)
#         last_tweet_id = twitter.tweet_xrp_info()
        twitter.tweet_xrp_info()

        # 関連ニュースをリツイートする
#         twitter.retweet(last_tweet_id)

        # DMをLINEで通知する 
        # twitter.info_direct_message()
        

    except Exception as e:
        print(e)
        
        # エラー内容LINE通知
        line = ln.Line()
        line.send_message(e)

if __name__ == '__main__':
    main()
