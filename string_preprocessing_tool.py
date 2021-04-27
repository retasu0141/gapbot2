# -*- coding: utf-8 -*-
#
# 自然言語の前処理の集まり
# 必要条件
# 

import re
import unicodedata
from operator import itemgetter
import datetime
import string



def translate_half_width_character(src_str:str):
    """全角の英数字を半角英数字に変換する
    
    Args:
        src_str (str): 変換対象の文字列
    
    Returns:
        [type]: 変換後の文字列
    """
    src_str = src_str.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

    return src_str


def get_now_datetime():
    """現在の日時を取得する
    
    Returns:
        [type]: 現在の日時の文字列
    """
    dt_now = datetime.datetime.now()
    date_time = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    return date_time

#カッコ内の文字列を取得する
def brackets_preprocess(text):
    output = ""

    r = re.search(r'「.+?」', text)
    if(r != None):
        output = r[0]
        
    if(len(output) == 0):
        r = re.search(r'『.+?』', text)
        if(r != None):
            output = r[0]

    if(len(output) == 0):
        r = re.search(r'\(.+?\)', text)
        if(r != None):
            output = r[0]

    if(len(output) == 0):
        r = re.search(r'（.+?）', text)
        if(r != None):
            output = r[0]
    
    if(len(output) > 1):
        output = output.replace('『',' ').replace('』',' ').replace('「',' ').replace('」',' ').replace('(',' ').replace(')',' ')
        output = output.replace('（',' ').replace('）',' ')
        output = output.strip()
    return output



def duplication_exclusion(keyword_list:object):
    """重複を弾く

    Args:
        keyword_list (Object): キーワードのリスト

    Returns:
        [type]: キーワードを弾いた後のリスト
    """
    out_puts = []

    for i in keyword_list:
        if( i not in out_puts):
            #登録されていなければ追加する
            out_puts.append(i)

    return out_puts
        


            
def format_text(text):
    """文字列から濁点など削除する(前処理)

    Args:
        text ([type]): 文字列

    Returns:
        [type]: 濁点など抜いた文字列
    """
    text = unicodedata.normalize("NFKC", text)  # 全角記号をざっくり半角へ置換

    # 記号を消し去るためのテーブル作成
    table = str.maketrans("", "", string.punctuation  + "「」、。・■□】【『』×")
    text = text.translate(table)

    return text

def clean_keyword_list(keyword_list):
    """前処理(ここに来るときは、形態素分析が終わっていること前提)

    Args:
        keyword_list ([type]): 形態素処理後

    Returns:
        [type]: 処理後のキーワードリスト
    """
    
    output_list = []
    for keyword in keyword_list:
        
        #置換処理
        keyword = keyword.replace('\n', '').replace(' ', '')
        
        #数字のみ
        if(keyword.isdecimal() == True):
            #数字のみ
            continue
            
        if(len(keyword) == 1):
            name = unicodedata.name(keyword)
            
            #平仮名
            if('KATAKANA' in name or 'HIRAGANA' in name ):
                continue
                
        #データセット
        if(len(keyword)>0):
            output_list.append(keyword)
        
    return output_list