# -*- coding: utf-8 -*-

# from twitterscraper import query_tweets
# import os
# import socks

# proxy=(socks.SOCKS5, "127.0.0.1", "1080")

# os.environ["HTTPS_PROXY"] = "https://161.202.226.195:8123/"
# os.environ["HTTPS_PROXY"] = "https://61.118.35.94:55725/"

# if __name__ == '__main__':
    # list_of_tweets = query_tweets("Trump OR Clinton", 10)

    # print the retrieved tweets to the screen:
    # for tweet in query_tweets("Trump OR Clinton", 10):
    #     print(tweet)

    # Or save the retrieved tweets to file:
    # file = open("output.txt", "w")
    # for tweet in query_tweets("Trump OR Clinton", 10):
    #     file.write(str(tweet.text.encode('UTF-8')))
    # file.close()

from twitterscraper.query import query_tweets
import datetime as dt


def query():
    list_of_tweets = query_tweets("秘密", 10, begindate=dt.date(2020, 3, 21))
    for te in list_of_tweets:
        print(te.text)


if __name__ == '__main__':
    query()
