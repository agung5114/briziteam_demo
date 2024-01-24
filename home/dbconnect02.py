import os
import sqlite3
from core.settings import BASE_DIR
import pandas as pd

# Connecting to the geeks database
connection = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite'),check_same_thread=False)

dfsum = pd.read_feather(os.path.join('', 'media/sumData.ft'))
dfpasal = pd.read_feather(os.path.join('', 'media/countPasal.ft'))
dftopik = pd.read_feather(os.path.join('', 'media/countTopik.ft'))
dfobjek = pd.read_feather(os.path.join('', 'media/objek.ft'))
dfkoreksi = pd.read_feather(os.path.join('', 'media/koreksi.ft'))

dfkategori = pd.read_csv(os.path.join('', 'media/pasal.csv'),sep=";")

def get_sengketaText(filelist):
    query1 = f'''select file_names,pokok_sengketa from SENGKETA
                where file_names in ({','.join(["'"+str(x)+"'" for x in filelist])})
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sengketa(text):
    query1 = f'''select file_names from SENGKETA
                where pokok_sengketa like '%{text}%'
                '''
    df = pd.read_sql_query(query1,connection)
    return df

# def get_sengketaFilter(text1,text2):
#     query1 = f'''select file_names from SENGKETA
#                 where pokok_sengketa like '%{text1}%'
#                 and hasil_putusan in ('{text2}')
#                 '''
#     df = pd.read_sql_query(query1,connection)
#     return df

def get_sengketaFilter(text1,text2):
    query1 = f'''select file_names from SENGKETA
                where hasil_putusan in ('{text2}')
                and pokok_sengketa like '%{text1}%'
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

# def get_sengketa_multi(filelist):
#     query1 = f'''select file_names,substr(pokok_sengketa,1,3500) as pokok_sengketa from SENGKETA
#                 where file_names in ({','.join(["'"+str(x)+"'" for x in filelist])})
#                 '''
#     df = pd.read_sql_query(query1,connection)
#     # pokok = df['pokok_sengketa'].tolist()
#     return df

def get_sengketa_multi(filelist):
    query1 = f'''select file_names,pokok_sengketa from SENGKETA
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

import re
def extractPasal(text):
    pasalList = dfkey['keyword'][65:].tolist()
    pList = []
    count = []
    for pasal in pasalList:
        p = re.findall(pasal, text)
        if len(p)> 0:
            pList.append(pasal)
            count.append(len(p))
        else:
            pass
    dfpasal = pd.DataFrame(list(zip(pList,count)),columns=['pasal','jumlah_pasal'])
    return dfpasal

def extractTopik(text):
    topikList = dfkey['keyword'][:65].tolist()
    pList = []
    count = []
    for topik in topikList:
        p = re.findall(topik, text)
        if len(p)> 0:
            pList.append(topik)
            count.append(len(p))
        else:
            pass
    dfpasal = pd.DataFrame(list(zip(pList,count)),columns=['kata_kunci','jumlah_kata'])
    return dfpasal

dfsubjek = pd.read_feather(os.path.join('', 'media/subjek.ft'))
dfobjek2 = pd.read_feather(os.path.join('', 'media/objek2.ft'))
dfhitung = pd.read_feather(os.path.join('', 'media/penghitungan.ft'))
dfterutang = pd.read_feather(os.path.join('', 'media/terutang.ft'))
dfsektor = pd.read_feather(os.path.join('', 'media/sektor.ft'))
dfnpwp = pd.read_feather(os.path.join('', 'media/00npwp.ft'))

# dfsampel = pd.read_feather(os.path.join('', 'media/gvsample.ft'))
def get_sengketaSample(text1):
    query1 = f'''select file_names from SAMPEL
                where pokok_sengketa like '%{text1}%'
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sengketaSampleFilter(text1,text2):
    query1 = f'''select file_names from SAMPEL
                where hasil_putusan in ('{text2}')
                and pokok_sengketa MATCH '%{text1}%'
                '''
    df = pd.read_sql_query(query1,connection)
    return df

def get_sampel_multi(filelist):
    query1 = f'''select file_names,pokok_sengketa from SAMPEL
                where file_names in ({','.join(["'"+str(x)+"'" for x in filelist])})
                '''
    df = pd.read_sql_query(query1,connection)
    # pokok = df['pokok_sengketa'].tolist()
    return df

import os
import glob
def check_file():
    # path = os.getcwd()
    path = os.path.join(BASE_DIR, 'pdf')
    pdf_files = glob.glob(os.path.join(path,f"","*.pdf"))
    pdflist = [str(x).replace('/pdf/',"") for x in pdf_files]
    pdflist = [str(x).replace('.pdf',".txt") for x in pdflist]
    return pdflist
