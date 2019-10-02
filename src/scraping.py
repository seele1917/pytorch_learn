import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pykakasi import kakasi

def get_member_name():
    '''
    欅坂46の公式HPからメンバーの名前をgetし，名前（漢字），名前(ふりがな）, 名前(ローマ字）のpandasフレームを返す関数
    '''
    
    url = 'http://www.keyakizaka46.com/s/k46o/search/artist'     # 欅坂46の公式HPのurl
    html = requests.get(url) # urlからhtmlを取得
    soup = BeautifulSoup(html.text, "html5lib") # html5libでパース
    members = soup.find('div', class_='current') # currentクラスのdomを取得
    name = members.find_all('p', class_='name')  # 名前（漢字）を含んだpタグを取得
    ruby = members.find_all('p', class_='furigana') # 名前（ふりがな）を含んだpタグを取得
    *name, = map(lambda x:x.string.strip(), name) # pタグから名前(漢字）を取得
    *ruby, = map(lambda x:x.string.strip(), ruby) # pタグから名前(ふりがな）を取得
    
    # ふりがなからローマ字を取得するためのライブラリ
    kakasi_ = kakasi()  # Generate kakasi instance

    kakasi_.setMode("H", "a")  # Hiragana to ascii
    kakasi_.setMode("K", "a")  # Katakana to ascii
    kakasi_.setMode("J", "a")  # Japanese(kanji) to ascii
    kakasi_.setMode('C', True)
    kakasi_.setMode("r", "Hepburn")  # Use Hepburn romanization

    conv = kakasi_.getConverter()
    
    ruby_roman = [] # 名前（ローマ字）を格納するリスト
    for r in ruby:
        result = conv.do(r)
        ruby_roman.append('_'.join(list(map(lambda x: x.capitalize(), result.split())))) # ローマ字の先頭を大文字にして追加
        
    data = np.stack([name, ruby, ruby_roman], 0).T
    keyaki_member = pd.DataFrame(data, columns=['name', 'ruby', 'ruby_roman'])
    
    return keyaki_member