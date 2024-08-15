import tweepy
import pandas as pd
import time

# X APIの認証情報
api_key = 'TyFGQe7ZCwEiCOuwciFmAMwsk'
api_key_secret = 'f0KyuYSShTyN2eB4RLbWHNIjxHXirmcyWY0xHxL1i5e2WHJOys'
access_token = '1669039493322530821-ICB0L6aiYRqIocHXqjIWRV6EfmLHP0'
access_token_secret = 'kvzOAD26OETCdPUuSYXfhI4vDan7uVkjouHgsbKbGxhIW'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAEt7vQEAAAAAOvwEAZbuBPSZdv1IwuzccobMUTM%3DpP1hbNQHjn6CW48fQHdLFdN7Aeg8fiitIQsPdKN6ts5cpplEkb'  # v2ではBearer Tokenも必要です

# クライアントの設定 (API v2)
client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

# アカウントのユーザー名
username = 'J5Lee'

try:
    # ユーザーIDを取得
    user = client.get_user(username=username)
    user_id = user.data.id

    # ツイートを取得 (最近のツイート)
    tweets = client.get_users_tweets(id=user_id, max_results=100)

    # ツイート内容を保存するリスト
    posts = []

    # 取得したツイートをリストに追加
    for tweet in tweets.data:
        posts.append([tweet.created_at, tweet.text])

    # CSVに書き出す
    df = pd.DataFrame(posts, columns=['Date', 'Text'])
    df.to_csv(f'{username}_tweets.csv', index=False, encoding='utf-8-sig')

    print(f"Successfully saved {len(posts)} tweets to {username}_tweets.csv")

except tweepy.errors.TwitterServerError as e:
    print("Twitter API returned a 500 Internal Server Error. Trying again later.")
    time.sleep(60)  # 1分待機して再試行
