from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.settings import HOME_TEMPLATES
import plotly_express as px
from .forms import DateForm, topiclist
from datetime import date, timedelta
import pandas as pd

# # @login_required(login_url="/login/")

def home(request):
    context = {'title': '',
               }
    # Page from the theme 
    # return render(request, 'pages/index.html')
    return render(request, 'Home.html',context)

def dokumen(request):
    context = {'title': '',
               }
    # Page from the theme 
    # return render(request, 'pages/index.html')
    return render(request, 'Dokumen.html',context)



from  .forms import PdfExtractForm
import PyPDF2
import os
from django.http import FileResponse
import re

def getKeys():
    keywpath = os.path.join('media', 'key_remap.txt')
    with open(keywpath, 'r') as f:
        newKW = f.readlines()

    daftarKW = []
    for line in newKW:
        if line != '\n':
            word = re.sub(r'\s?\n','',line)
            word = word.lower().strip()
            daftarKW.append(word)
    indexKW = {}
    for i,kw in enumerate(daftarKW):
        indexKW[str(i+1)] = kw
    
    all_fword = []
    for text in newKW:
        fword = []
        for word in daftarKW:
            fword.append(len(re.findall(word, text)))
        all_fword.append(fword)
    return [all_fword,indexKW]

keys = getKeys()

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def cari_putusan_single(files, idf, tfidf, occtable, n=5):
    proc_df = files.iloc[:,1:].div(files.iloc[:,1:].sum(axis=1), axis=0).multiply(idf)
    cos = cosine_similarity(proc_df, tfidf.iloc[:,1:])[0]

    # Mendapatkan indeks dari n cosine similarity tertinggi
    top_n_indices = np.argsort(-cos)[:n]

    hasil = pd.concat([files, occtable.iloc[top_n_indices]]).reset_index(drop=True)
    hasil.insert(1,'Similarity',np.insert(cos[top_n_indices], 0, 999, axis=0))

    return hasil

def pdf_extract(request):
    if request.method == 'POST':
        # 如果用户通过POST提交
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            # 获取上传的文件
            f = form.cleaned_data['file']
            # 转化为PDF文件对象
            reader = PyPDF2.PdfReader(f)
            pages = len(reader.pages)
            # Extracted pdf file path
            # pdf_file_path = os.path.join('media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            pdf_file_path = os.path.join('media', 'extracted_page.pdf')
            pdfOutputFile = open(pdf_file_path, 'ab+')

            # 利用PyPDF2创建新的Pdf Writer
            pdfWriter = PyPDF2.PdfWriter()

            for page_num in range(pages):
                # pdf文档页码对象编码是从0开始，所以减一
                page_index = int(page_num) - 1

                # 利用PyPDF2提取页码对象
                pageObj = reader.pages[page_index] # 从0编码

                # 添加已读取的页面对象
                pdfWriter.add_page(pageObj)

            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

            extractedPage = open(pdf_file_path, 'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'

            text = ''
            for i in range(pages):
                page = reader.pages[i]
                text += page.extract_text()

            # path = os.getcwd()
            # filename = glob.glob(os.path.join(path,f"data/daily/","*.csv"))
            df = pd.DataFrame([['file',text]],columns=['file_names','file_texts'])
            new_cols = pd.DataFrame(keys[0], columns=list(keys[1].keys()))
            df_fword = pd.concat([df['file_names'],df['file_texts'], new_cols], axis=1)
            df_fword = df_fword.drop(['file_texts'], axis=1)
            keyWords = keys[0]
            rawKey_df = df_fword
            rawKey_df = rawKey_df[rawKey_df.iloc[:,1:].sum(axis=1) != 0].reset_index(drop=True)
            onlyKey_df = rawKey_df.iloc[:,1:]
            import math
            idf = (len(onlyKey_df) / (onlyKey_df[onlyKey_df > 0].count()+1)).apply(math.log)
            tfidf = onlyKey_df.div(onlyKey_df.sum(axis=1), axis=0).multiply(idf)
            tfidf.insert(0, 'file_names',rawKey_df.file_names)

            
            occtable = rawKey_df
            files = rawKey_df.sample(1)
            hasil = cari_putusan_single(files, idf=idf, tfidf=tfidf, occtable=rawKey_df, n=5)
            columns = ['NamaFile','Similarity']
            # hasil.columns = columns+keyWords
            # hasil[columns+hasil.iloc[0,2:].sort_values(ascending=False).index.to_list()]
            table1 = hasil.loc[:, (hasil != 0).any(axis=0)]
            # to_html(index=False).replace('<table border="1" class="dataframe">',
            #     '<table id="fulltable2" class="table-responsive table mt-2 table-striped">')
            keywpath = os.path.join('media', 'key_remap.txt')
            with open(keywpath, 'r') as f:
                newKW = f.readlines()
            daftarKW = []
            for line in newKW:
                if line != '\n':
                    word = re.sub(r'\s?\n','',line)
                    word = word.lower().strip()
                    daftarKW.append(word)
            topics = []
            for x in daftarKW:
                
            topic_idx = table1.columns.tolist()[2:]
            topics = daftarKW
            # for x in topic_idx:
            #     keys[1][x]
            dfff = pd.DataFrame([[topics]],columns=['Topic']).to_html(index=False).replace('<table border="1" class="dataframe">',
                '<table id="fulltable2" class="table-responsive table mt-2 table-striped">')
            return render(request, 'pdf_extract.html', {'form': form,'text':text[:1000],'text2':text[-1000:],'pages':pages,'table1':dfff})
    else:
        form = PdfExtractForm()
        return render(request, 'pdf_extract.html', {'form': form})
