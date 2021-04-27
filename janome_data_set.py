####janome形態素分析のツール

from janome.tokenizer import Tokenizer

class JanomeDataSet():

    def __init__(self,tokenizer_dict = "" ):
        """初期化
        
        Keyword Arguments:
            tokenizer_dict {str} -- 辞書ファイルのpath (default: {""}) デフォルトは Janome標準
        """
        
        #Tokenizerの設定
        self.janome_tokenizer  = Tokenizer(tokenizer_dict)



    def text_morpheme(self, text, part = "", part2 = ""):
        """janomeで形態素に分ける
        
        Arguments:
            text [type] -- 形態素に分ける文字列
        
        Keyword Arguments:
            part [str] -- 取得する品詞を指定(品詞の設定がない場合はすべて取得)
            part2 [str] -- サ変名詞などの２つ目の品詞
        
        Returns:
            [type] -- 形態素に分けた結果(リストで返す)
        """
        text_list = []
        for token in self.janome_tokenizer.tokenize(text):
            #品詞指定なし
            if(len(part) == 0):
                text_list.append(token.surface)
            elif(len(part) > 0 and len(part2) > 0 ):
                #品詞１、２が設定されているケース
                if(part in token.part_of_speech):
                    if(part2 in token.part_of_speech):
                        text_list.append(token.surface)
            elif(len(part) > 0 and len(part2) == 0):
                #品詞１のみ設定されているケース
                if(part in token.part_of_speech):
                    text_list.append(token.surface)
     
        return text_list

    def text_reading(self, text, part = ""):
        """janomeで形態素に分けるて読みを返す
        
        Arguments:
            text [type] -- 形態素に分けて読みを返す文字列
        
        Keyword Arguments:
            part [str] -- 取得する品詞を指定(品詞の設定がない場合はすべて取得)
        
        Returns:
            [type] -- 形態素に分けた結果(リストで返す)
        """
        text_list = []
        for token in self.janome_tokenizer.tokenize(text):
            #print(token)
            if(len(part) == 0 or part in token.part_of_speech ):
                text_list.append(token.reading)
     
        return text_list


    def tokenize(self, text):
        return self.janome_tokenizer.tokenize(text)