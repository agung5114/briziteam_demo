# from wordcloud import WordCloud
# import json
# from urllib.request import urlopen

# import nltk
# # nltk.download('punkt')
# from nltk.tokenize import word_tokenize
# from nltk.util import ngrams
# from core.settings import BASE_DIR
# import pandas as pd
# import plotly.express as px

# def get_ngrams(text, n=2):
#     text = str(text)
#     n_grams = ngrams(text.split(), n)
#     returnVal = []
#     try:
#         for grams in n_grams:
#             returnVal.append('_'.join(grams))
#     except(RuntimeError):
#         pass
#     # return list(','.join(returnVal).strip())
#     return returnVal

# def get_stopwords_list(stop_file_path):
#     """load stop words """
    
#     with open(stop_file_path, 'r', encoding="utf-8") as f:
#         stopwords = f.readlines()
#         stop_set = set(m.strip() for m in stopwords)
#         return list(frozenset(stop_set))

# def create_wordcloud(df,column,judul):
#     df.dropna(subset = [column], inplace=True)
#     text = df[column].tolist()
#     if text == []:
#         text = ["Katakunci tidakditemukan"]
#     else:
#         pass
#     # nltk_tokens = nltk.word_tokenize(text)
#     stopwords_path = f'{BASE_DIR}/home/plots/indonesian.txt'
#     sw = get_stopwords_list(stopwords_path) 
#     #   bigrams_list = get_ngrams(text,n)
#     wordcloud = WordCloud (
#             background_color = 'white',
#             width = 800,
#             stopwords =sw+["kalo","gk","0"],
#             height = 500
#                 ).generate(' '.join(text))
#     fig = px.imshow(wordcloud)
#     fig.update_yaxes(title=None, visible=False)
#     fig.update_xaxes(title=None, visible=False)
#     return fig

# import itertools
# def create_wordcloud2(df,key,number):
#     text = []
#     for letter, number in zip(df[key].tolist(), df[number].tolist()):
#         text.extend(itertools.repeat(letter, number))
#     stopwords_path = f'{BASE_DIR}/home/plots/indonesian.txt'
#     sw = get_stopwords_list(stopwords_path) 
#     # bigrams_list = get_ngrams(text,1)
#     wordcloud = WordCloud (
#             background_color = 'white',
#             width = 512,
#             stopwords =sw+["kalo","gk","0"],
#             height = 350
#                 ).generate(' '.join(text))
#     fig = px.imshow(wordcloud,title=f'Wordcloud')
#     fig.update_yaxes(title=None, visible=False)
#     fig.update_xaxes(title=None, visible=False)
#     return fig