import os
import sqlite3
from core.settings import BASE_DIR
import pandas as pd

# Connecting to the geeks database
connection = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite'),check_same_thread=False)


dfsum = pd.read_feather(os.path.join('', 'media/sumData.ft'))

# import vaex
# from cache_memoize import cache_memoize
# from functioncaching import cached_function
# # @cache_memoize(30*60,store_result=True)
# @cached_function(timeout=24*60*60, freshness_timeout=60*60)
# def get_vxdata(path):
#     df = vaex.open(path)
#     return df
# @cached_function(timeout=24*60*60, freshness_timeout=60*60)
# def get_pasaltopik():
#     dfpasal = pd.read_feather(os.path.join('', 'media/countPasal.ft'))
#     dftopik = pd.read_feather(os.path.join('', 'media/countTopik.ft'))
#     return [dfpasal,dftopik]

# dfpasal = get_pasaltopik()[0]
# dftopik = get_pasaltopik()[1]

dfpasal = pd.read_feather(os.path.join('', 'media/countPasal.ft'))
dftopik = pd.read_feather(os.path.join('', 'media/countTopik.ft'))
# def get_sengketa(text):
#     df = dfsengketa[dfsengketa.pokok_sengketa.str.contains(text)==True]
    # df= df.to_pandas.df()
#     return df

# def get_sengketa_id(filename):
#     dfsengketa = get_vxdata(os.path.join(BASE_DIR,'textSengketa.feather'))
#     df = dfsengketa[dfsengketa.file_names == str(filename)]
#     return df

# def get_putusan_id(filename):
#     dfputusan = get_vxdata(os.path.join(BASE_DIR,'textPutusan.feather'))
#     df = dfputusan[dfputusan.file_names == str(filename)]
#     return df

# def get_sengketa_multi(filelist):
#     dfsengketa = get_vxdata(os.path.join(BASE_DIR,'textSengketa.feather'))
#     df = dfsengketa[dfsengketa.file_names.isin(filelist)]
#     # dfp = df.to_pandas.df()
#     return df

# def get_sengketaFilter(text1,text2):
#     df = dfsengketa[dfsengketa.pokok_sengketa.str.contains(text1)==True]
#     df = dfsengketa[dfsengketa.hasil_putusan==str(text2)]
    # df= df.to_pandas.df()
#     return df

def get_sengketa(text):
    query1 = f'''select file_names from SENGKETA
                where pokok_sengketa like '%{text}%'
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sengketaFilter(text1,text2):
    query1 = f'''select file_names from SENGKETA
                where pokok_sengketa like '%{text1}%'
                and hasil_putusan in ('{text2}')
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sengketaFilterTahun(text1,text2,text3):
    query1 = f'''select file_names from SENGKETA
                where pokok_sengketa like '%{text1}%'
                and hasil_putusan in ('{text2}')
                and tahun = {text3}
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sengketa_multi(filelist):
    query1 = f'''select file_names,left(pokok_sengketa,500) as pokok_sengketa from SENGKETA
                where file_names in ({','.join(["'"+str(x)+"'" for x in filelist])})
                '''
    df = pd.read_sql_query(query1,connection)
    # pokok = df['pokok_sengketa'].tolist()
    return df

def get_sengketa_id(filename):
    query1 = f'''select file_names,substr(pokok_sengketa,1,3500) as pokok_sengketa from SENGKETA
                where file_names in ('{filename}')
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_putusan_id(filename):
    query1 = f'''select substr(putusan,1,3500) as putusan from HASIL
                where file_names in ('{filename}')
                '''
    df = pd.read_sql_query(query1,connection)
    return df

dfkey = pd.read_csv(os.path.join(BASE_DIR,'media/newkeys.csv'),sep=";")
keydict = {dfkey['keyword'][i]: dfkey['keterangan'][i] for i in range(len(dfkey['keyword']))}