import tweepy
import pandas as pd
import time

# X APIの認証情報
api_key = '4iCl1L1WZMk2rpyaIyyJHSt1R'
api_key_secret = 'U3tHghMJuQMxg5VlVART9gm4RUIYIoXy393XHDmZSWTnb380sE'
access_token = '1669039493322530821-GJa8OmmrUd1xNfo6VA1QTngbaKW6aM'
access_token_secret = 'FEZOJAMyNDoBn6Hhvp5kkj8bJLMt21CIR8HzUcyDeuBOc'

# 認証プロセスの設定
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# アカウントのユーザー名
username = 'J5Lee'

# 全ツイートを保存するリスト
posts = []

# 最初のリクエスト時のID設定（過去のツイートを取得）
max_id = None

# ツイートを取得し続ける
while True:
    try:
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=max_id, tweet_mode="extended")
        if not new_tweets:
            break
        posts.extend([[tweet.created_at, tweet.full_text] for tweet in new_tweets])
        max_id = new_tweets[-1].id - 1
        time.sleep(1)  # 適切な待機時間を設定（必要に応じて調整）
    except tweepy.TweepError as e:
        print(f"Error: {e}")
        time.sleep(60)  # エラー時に60秒待機して再試行
        continue

# CSVに書き出す
df = pd.DataFrame(posts, columns=['Date', 'Text'])
df.to_csv(f'{username}_all_tweets.csv', index=False, encoding='utf-8-sig')

print(f"Successfully saved {len(posts)} tweets to {username}_all_tweets.csv")
