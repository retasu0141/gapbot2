from pytwitterscraper import TwitterScraper
#import twint
import os
import json
from janome.tokenizer import Tokenizer
import collections
import re
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
font = r'font/keifont.ttf'
fp = FontProperties(fname=font, size=50)
import time, calendar
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from tenacity import retry


@retry
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = lxml.html.fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:30]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    proxy_pool = itertools.cycle(proxies)
    tw = TwitterScraper(proxy_enable=True, proxy_http=next(proxy_pool))
    return tw

keyword = 'ビットコイン'


def twintSearchKeyword(classification, keyword, limit, onlyLink):
    """
    キーワードを指定
    """
    new_dir_path = 'data2/'+keyword+'/'
    try:
        os.mkdir(new_dir_path)
    except:
        pass
    twint.output.tweets_list = []
    c = twint.Config()
    c.Output = 'data2/'+keyword+'/'+keyword+".csv"
    c.Store_object = True
    #c.Format = 'twint search: '+classification+' - '+keyword+' - {username} - {id}'
    #c.Format = 'twint search: '+keyword+' - {username} - {id}'
    # recent or popular
    c.Format = "Time {time} | Username {username} | Tweet {tweet} "
    c.Popular_tweets = True
    # RTを除外
    Filter_retweets = True
    # リンクを含むツイートのみ
    if onlyLink:
        c.Links = 'include'
    c.Limit = limit
    c.Search = keyword
    twint.output.clean_lists()
    twint.run.Search(c)
    new_dir_path = 'data/'+keyword+'/'
    #tweets = twint.output.tweets_list
    return twint.output.tweets_list
    #print(twint.tweet.tweet)
    #twint.output.clean_lists()
    #print(tweets)




def CountWord(tweet_list):
    #tweet_list
    all_tweet = "\n".join(tweet_list)

    t = Tokenizer()

    # 原形に変形、名詞のみ、1文字を除去、漢字・平仮名・カタカナの連続飲みに限定
    c = collections.Counter(token.base_form for token in t.tokenize(all_tweet)
                            if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1
                            and token.base_form.isalpha() and not re.match('^[a-zA-Z]+$', token.base_form))

    freq_dict = {}
    mc = c.most_common()
    for elem in mc:
        freq_dict[elem[0]] = elem[1]

    return freq_dict


def color_func(word, font_size, position, orientation, random_state, font_path):
    return 'white'



def DrawWordCloud(word_freq_dict, fig_title):

    # デフォルト設定を変更して、colormapを"rainbow"に変更
    wordcloud = WordCloud(background_color='white', min_font_size=15, font_path=font,
                          max_font_size=200, width=1000, height=500, prefer_horizontal=1.0, relative_scaling=0.0, colormap="rainbow")
    wordcloud.generate_from_frequencies(word_freq_dict)
    plt.figure(figsize=[20,20])
    plt.title(fig_title, fontproperties=fp)
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis("off")
    plt.savefig('data2/'+keyword+'/'+keyword+'.png')


tweet_data = {}
mid = -1


#tw = get_proxies()
tw = TwitterScraper()
search = tw.searchkeywords(keyword)
search.users

#print(search.users)
names = []
for data in search.users:
    #print(data['url'])
    id_data = data['url'].replace("https://twitter.com/","")
    #print(id_data)
    names.append(id_data)

#print()

ids = []

for name in names:
    profile = tw.get_profile(name=name)
    ids.append(profile.__dict__['id'])

text_data =[]
for id in ids:
    try:
        print(id)
        tweets = tw.get_tweets(id, count=500)
    except:
        pass
    #rint(tweets.contents)

    for data in tweets.contents:
        text_data.append(data['text'])
'''
for tweet in tweets:
    print(tweet.tweet)
#print(tweets.tweet.tweet)

#print(tweets.Tweet)
'''
new_dir_path = 'data2/'+keyword+'/'

try:
    os.mkdir(new_dir_path)
except:
    pass


words = CountWord(text_data)

DrawWordCloud(words,keyword+'に関連するワード')


# 頻出順にソート
words_data = sorted(words.items(), key = lambda x: x[1], reverse=True)

# 単語を ID 順に CSV ファイルへ保存  # BOW を CSV ファイルへ保存
Table = pd.DataFrame(words_data)
'''
with open('data2/'+keyword+'/'+keyword+".csv", mode="w", encoding="shift_jis", errors="ignore") as f:
    # pandasでファイルオブジェクトに書き込む
    Table.to_csv(f, index=False)
'''
#Table.to_csv('Table.csv', index=False, encoding="shift_jis")

#python3 tw3.py
