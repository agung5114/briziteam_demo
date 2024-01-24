from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from core.settings import HOME_TEMPLATES
import plotly_express as px
import plotly.graph_objects as go

from .forms import DateForm, topiclist
from datetime import date, timedelta
import pandas as pd
from core.settings import BASE_DIR
from .dbconnect import *


def text_cleaning(text):
    text = text.lower()
    text = text.replace(r'@(\w|\d)+',' ')
    text = text.replace(r'#(\w|\d)+',' ')
    text = text.replace(r'(http|https)\S+',' ')
    text = text.replace('\n',' ')
    return text

def splitText(text,delim):
    parts = re.split(delim, text_cleaning(text),1)
    if len(parts) > 1:
        hasil = parts[-1]
    else:
        hasil = parts [0]
    return hasil
# # @login_required(login_url="/login/")

def extractNPWP(text):
    aList = []
    for each in re.findall('(?<=npwp ).*?(?=\s)', text) :
        tList = re.findall('[0-9]+',each)
        aList.append(tList)
    # final_list = [w for w in aList if w not in ['pasal 1','pasal 6','pasal 15','pasal 16']]
    listnpwp = []
    for x in filter(None,aList):
        if len("".join(x))==15:
            listnpwp.append("".join(x))
        else:pass
    result = ",".join(list(set(listnpwp)))
    return result

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


from  .forms import PdfExtractForm,searchForm
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

import json
# @login_required(login_url="/login/")
def search(request):
    import re
    from collections import Counter
    putusan_color = {"Menolak": "#de425b", "Mengabulkan_Sebagian": "#96ac5a", "Mengabulkan_Seluruhnya": "#488f31",
                     'Menambah_Jumlah_Pajak':"#ec8569",'Tidak_Dapat_Diterima':"#f4bc92",'Membetulkan_Kesalahan_Tulis/Hitung':"#d2ca90",
                     'Membatalkan':"#b6ba74", 'Tidak_ditemukan':"#ffedcf"}
    form = searchForm(initial={'topic': 'Barang Strategis','putusan':'All'})
    topic = "Barang Strategis"
    hasil = "All"
    jumlah = 50
    if request.method == 'POST':
        form = searchForm(request.POST, request.FILES)
        if form.is_valid():
            topic = request.POST.get('topic')
            hasil = request.POST.get('putusan')
            jumlah = request.POST.get('jumlah')
    else:
        pass

    if hasil == "All":
        tlist = [x.lower() for x in list(topic.split(" "))]
        dfall = get_sengketa(tlist)
    else:
        tlist = [x.lower() for x in list(topic.split(" "))]
        dfall = get_sengketaFilter(tlist,hasil)
    
    df = dfsum[dfsum['file_names'].isin(dfall['file_names'])].drop_duplicates(subset='file_names', keep="last")
    dftahun = df[['file_names','tahun']].groupby('tahun',as_index=False).agg({'file_names':'count'})
    fig0 = px.bar(dftahun.sort_values(by='tahun', ascending=True), x='tahun', y='file_names', 
                  color='tahun',color_continuous_scale=["#d2ca90","#ffedcf","#f4bc92"],text='file_names')
    fig0.update_layout(showlegend=False,yaxis={'visible': False, 'showticklabels': False},xaxis_title=None,
                       autosize=False,
                       width=300,
                        height=150,)               
    fig0.update_coloraxes(showscale=False)
    df = df[['file_names','pasal']]
    plist = []
    for ps in df['pasal']:
        for p in ps:
            plist.append(p)
    pasal = Counter(plist).keys() # equals to list(set(words))
    counts = Counter(plist).values() # counts the elements' frequency
    dfig = pd.DataFrame(list(zip(pasal,counts)),columns=['Pasal','Jumlah'])
    dfig['Persentase'] = [int(10000*x/len(dfall.index))/100 for x in dfig['Jumlah']]
    dfig1 = dfig.sort_values('Persentase',ascending=False)
    fig1 = px.bar(dfig1.head(10), x='Pasal', y='Persentase', 
                  color='Persentase',color_continuous_scale=["#d2ca90","#ffedcf","#f4bc92"],text='Persentase')
    fig1.update_layout(showlegend=False,yaxis={'visible': False, 'showticklabels': False},xaxis_title=None)               
    fig1.update_coloraxes(showscale=False)
    fig1.update_traces(text= [f'{val} %' for val in dfig1['Persentase']],textangle=0)
    # df['Jumlah'] = 1
    # fig2 = px.pie(df,names='hasil_putusan',values='Jumlah',color='hasil_putusan',color_discrete_map=putusan_color)
    dfall['Jumlah'] = 1
    fig2 = px.pie(dfall,names='hasil_putusan',values='Jumlah',color='hasil_putusan',color_discrete_map=putusan_color,hole=0.6)
    fig2.update_layout(showlegend=False,xaxis={'visible': False})
    fig2.update_traces(textinfo='label+percent',insidetextorientation='horizontal')
    dfall2 = dfall.groupby('hasil_putusan',as_index=False).agg({'Jumlah':'sum'})
    fig3 = px.bar(dfall2.sort_values('Jumlah',ascending=False),x='hasil_putusan',y='Jumlah',
                  color='hasil_putusan',color_discrete_map=putusan_color,text_auto=True)
    fig3.update_layout(showlegend=False,yaxis={'visible': False, 'showticklabels': False},xaxis_title=None)
    dftext = get_sengketa_multi(df['file_names'].tolist(),topic.lower())
    df = df.merge(dftext,how='left',on='file_names')
    df = df.merge(dfall,how='left',on='file_names')
    df = df.drop_duplicates(subset='file_names', keep="last")
    # def get_sentence(topic,line):
    #     tmp = []
    #     searchObj = [ t for t in line.split('. ') if topic.lower() in t]
    #     for match in searchObj:
    #         tmp.append(match)
    #     return len(tmp)
    # # df['kalimat'] = [ get_sentence(topic,x)[0] for x in df['pokok_sengketa']]
    # # df['kalimat'] = ["<p>"+f'{x}'+"</p>" for x in df['kalimat']]
    dftext2 = get_sengketaText(df['file_names'].tolist())
    df = df.merge(dftext2,how='left',on='file_names')
    df = pd.merge(df,dfnpwp[['file_names','npwp']],on='file_names', how='left')
    # df['jumlah'] = [ get_sentence(topic,x) for x in df['kalimat']]
    df = df.sort_values('jumlah',ascending=True)[:int(jumlah)]
    df['rank'] = df['jumlah'].rank(method='first',ascending=True)
    from ast import literal_eval
    df['kalimat'] = df['kalimat'].apply(literal_eval)
    stopw = dfstop['stop'].tolist()+['pajak','banding','nomor','putusan','pasal','undang','ppn']
    df['kalimat'] = [[y for y in x if not y in stopw] for x in df['kalimat']]
    df['kalimat'] = [[item for item in x if not item.isdigit()] for x in df['kalimat']]
    
    df['pasal'] = [', '.join(x) for x in df['pasal']]
    # dfirst = df.loc[:1]
    first = df['file_names'].str.replace('.txt','').values[0]
    from .logging import search_log
    search_log(str(request.user), topic.lower())

    context = {'form': form,'total':len(dfall.index),
               'chart1':fig1.to_html(),'chart2':fig2.to_html(),'chart3':fig3.to_html(),'chart0':fig0.to_html(),
               'selected':topic,
            #    'table2':dfff,
                'topik':topic,
                'files':df,'first':first,
                # 'listpdf': df['file_names'].unique().tolist()
                # 'listpdf':check_file()
                }
    return render(request, 'pencarian.html',context)

from django.views.decorators.clickjacking import xframe_options_exempt

# @xframe_options_exempt
def view_pdf(request, id):
    df = pd.read_feather(os.path.join(BASE_DIR,'media/putusanList.feather'))
    # file = df[df['file_names']==id]
    # file = df[df['file_names'].isin(['1-004996.16.2020w.txt'])]
    file = df[df['file_names'].isin([str(id)])]
    # http://docs.google.com/gview?url='''+&embedded=true"
    file = file['link'].values[0]
    link = f'http://docs.google.com/gview?url={file}&embedded=true'

    frame ='''<iframe onload="hideLoader()" src='''+(link)+''' 
            frameborder="0" style="width:800px; height:1200px;">
            </iframe>'''
    return render(request, 'view_pdf.html', {'frame': frame})

def download_pdf(request, id):
    df = pd.read_feather(os.path.join(BASE_DIR,'media/putusanList.feather'))
    # file = df[df['file_names']==id]
    # file = df[df['file_names'].isin(['1-004996.16.2020w.txt'])]
    file = df[df['file_names'].isin([str(id)])]
    # http://docs.google.com/gview?url='''+&embedded=true"
    file = file['link'].values[0]
    return HttpResponseRedirect(file) 

from django.http import FileResponse, Http404
import fitz
def open_pdf(request,id,key):
    # link = os.path.join('media', 'extracted_page.pdf')
    doc = fitz.open(os.path.join(BASE_DIR, f"pdf/{id}.pdf"))
    for page in doc:
    ### SEARCH
        text = key
        text_instances = page.search_for(text)
        ### HIGHLIGHT
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    ### OUTPUT
    doc.save(os.path.join(BASE_DIR,'media/highlighted.pdf'), garbage=4, deflate=True, clean=True)
    link = os.path.join(BASE_DIR,'media/highlighted.pdf')
    # link = os.path.abspath(os.path.join("/home/agungseptia/projects/projex/files", f"{id}.pdf"))
    with open(link, 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=extracted_page.pdf'
        return response

def get_features(text):
    dfkey = pd.read_csv(os.path.join(BASE_DIR,'media/keys.csv'),sep=";")
    daftarKW = dfkey['keyword'].tolist()
    # daftarKW = [keydict.values()]
    fword = []
    for word in daftarKW:
        fword.append(len(re.findall(word, text)))
    features = pd.DataFrame([[x for x in fword]], columns=dfkey['index'].tolist())
    return features

def get_topic(df):
    # import pickle
    import joblib
    loaded_model = joblib.load(os.path.join(BASE_DIR,'media/modelknn.pkl'))
    result = loaded_model.predict(df.values)
    topics = pd.read_csv(os.path.join(BASE_DIR,'media/topics.csv'),sep=";")
    topic = topics[topics['kode']==result[0]]
    return result[0],topic['Keterangan'].values[0]

def get_prediction(text):
    # dfkey = pd.read_csv(os.path.join(BASE_DIR,'media/newkeys.csv'),sep=";")
    daftarKW = dfkey['keyword'].tolist()
    fword = []
    for word in daftarKW:
        fword.append(len(re.findall(word, text)))
    features = pd.DataFrame([[x for x in fword]], columns=daftarKW)
    import joblib
    loaded_model = joblib.load(os.path.join(BASE_DIR,'media/modelknn2.pkl'))
    result = loaded_model.predict(features.values)
    prediksi = []
    if result[0]==0:
        prediksi.append('Menolak')
    elif result[0]==1:
        prediksi.append('Mengabulkan_Sebagian')
    elif result[0]==2:
        prediksi.append('Mengabulkan_Seluruhnya')
    elif result[0]==3:
        prediksi.append('Menambah_Jumlah_Pajak')
    elif result[0]==4:
        prediksi.append('Tidak_Dapat_Diterima')
    elif result[0]==5:
        prediksi.append('Membetulkan_Kesalahan_Tulis/Hitung')
    elif result[0]==6:
        prediksi.append('Membatalkan')
    else:
        pass
    # topfeature = features.idxmax(axis=1)
    topfeature = features.columns[features.to_numpy().argmax(axis=1)][0]
    return prediksi[0],topfeature,features[topfeature].values

def get_sim(sample,key):
    dfeat = pd.read_csv(os.path.join(BASE_DIR,'media/features.csv'),sep=";")
    dfeat1= dfeat[dfeat['id_key'].isin([key])]
    dfiles = dfeat1.iloc[:,1:-5]
    result = []
    file = []
    for x in range(len(dfiles)):
        sim = cosine_similarity(np.array([sample.iloc[0,0:]]),np.array([dfiles.iloc[x,1:]]))
        result.append(sim[0][0])
        file.append(dfiles['file_names'].tolist()[x])
        # file.append(x)
    df = pd.DataFrame(list(zip(file,result)),columns=['file_names','similarity'])
    dftop = df.sort_values(by='similarity',ascending=False)
    return dftop

def pdf_extract(request):
    if request.method == 'POST':
        form = PdfExtractForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            reader = PyPDF2.PdfReader(f)
            pages = len(reader.pages)
            pdf_file_path = os.path.join('media', 'extracted_page.pdf')
            pdfOutputFile = open(pdf_file_path, 'ab+')

            pdfWriter = PyPDF2.PdfWriter()

            for page_num in range(pages):
                page_index = int(page_num) - 1
                pageObj = reader.pages[page_index]

                pdfWriter.add_page(pageObj)

            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

            text = ''
            for i in range(pages):
                page = reader.pages[i]
                text += page.extract_text()
            
            texthasil = splitText(text.lower(),'mengadili')
            text = splitText(text.lower(),'pokok_sengketa') 

            npwp = extractNPWP(text)
            features = get_features(text)
            topic = get_topic(features)
            similarity = get_sim(features,topic[0])[:20]
            listfile = similarity['file_names'].tolist()
            listfile.sort()
            dftext = dfsum[dfsum['file_names'].isin(listfile)]
            # similarity = pd.merge(similarity,dftext[['file_names','pasal','topik','hasil_putusan']],on='file_names', how='left')
            similarity = pd.merge(similarity,dftext[['file_names','pasal','topik']],on='file_names', how='left')
            similarity['pokok_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in similarity['pasal']]
            # similarity['kemiripan'] = [f'{int(x*1000)/10} Persen' for x in similarity['similarity']]
            #prediksi
            prediksi= get_prediction(text)
            prediksi_hasil = prediksi[0]
            topfitur = prediksi[1]
            jumlahtop = prediksi[2]
            #count pasal topik
            dfpasal = extractPasal(text)
            figpasal = px.bar(dfpasal.sort_values('jumlah_pasal')[:5],x='jumlah_pasal',y='pasal',orientation='h',color='jumlah_pasal',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
            figpasal.update_layout(coloraxis_showscale=False,xaxis_title=None,yaxis_title=None)
            dftopik = extractTopik(text)
            figtopik = px.bar(dftopik.sort_values('jumlah_kata')[:5],x='jumlah_kata',y='kata_kunci',orientation='h',color='jumlah_kata',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
            figtopik.update_layout(coloraxis_showscale=False,xaxis_title=None,yaxis_title=None)
            cek = [0 if text=='' else 1]
            linkpdf = os.path.join(BASE_DIR,'media/extracted_page.pdf')
            similarity = pd.merge(similarity,dfnpwp,on='file_names', how='left').drop_duplicates(subset='file_names', keep="last")
            
            # similarity = similarity[similarity['file_names'].isin(check_file())]
            similarity= similarity.sort_values('similarity',ascending=False)[:20]
            similarity['similarity'] = [f'{int(x*10000)/100} %' for x in similarity['similarity']]
            #tambah npwp and hasil
            # similarity = pd.merge(similarity,dfnpwp,on='file_names', how='left')
            first = similarity['file_names'].str.replace('.txt','').values[1]
            return render(request, 'pdf_extract.html', {'form': form,'text':text[:100],'topic':topic[1],'linkpdf':linkpdf,'figtopik':figtopik.to_html(),
                                                        'similarity':similarity,'texthasil':texthasil[:100],'figpasal':figpasal.to_html(),'npwp':npwp,'first':first,
                                                        'hasil':prediksi_hasil,'topfitur':topfitur,'jumlahtop':jumlahtop[0],'cek':cek[0]})
    else:
        form = PdfExtractForm()
        return render(request, 'pdf_extract.html', {'form': form})
    
def detail_putusan(request, id):
    fname = id.replace('txt','pdf')
    pdfpath = os.path.join(BASE_DIR,f'pdf/{fname}')
    String = ["mengadili",'pokok sengketa']
    hal_putusan = []
    hal_pokok = []
    doc = fitz.open(pdfpath)
    doc.save(os.path.join(BASE_DIR,'pdf/file_putusan.pdf'))
    for page in doc:
        text = ''
        text += text_cleaning(page.get_text())
        if len(re.findall(String[0], text)) > 0:
            hal_putusan.append(page.number)
        else:
            hal_pokok.append(-1)

    doc.select([hal_putusan[-1]])
    doc.save(os.path.join(BASE_DIR,'pdf/hasil_putusan.pdf'))
    
    texthasil = text_cleaning(doc[-1].get_text())
    file = dfsum[dfsum['file_names'].isin([str(id)])]
    # texthasil = file['hasil_putusan'].values[0]
    df = get_sengketa_id(id)
    # df = dfsengketa[dfsengketa.file_names == str(id)]
    # df = df.to_pandas_df()
    text = df['pokok_sengketa'].values[0]
    text = text.lower()
    tp = get_putusan_id(id)
    # tp = dfputusan[dfputusan.file_names == str(id)]
    # tp = tp.to_pandas_df()
    textputusan = tp['putusan'].values[0]
    textputusan = textputusan.lower()

    features = get_features(text)
    topic = get_topic(features)
    similarity = get_sim(features,topic[0])[:20]
    listfile = similarity['file_names'].unique().tolist()
    listfile.sort()
    # daftarput = ["'"+str(x)+"'" for x in listfile]
    dftext = dfsum[dfsum['file_names'].isin(listfile)]
    similarity = pd.merge(similarity,dftext[['file_names','pasal','topik']],on='file_names', how='left')
    similarity['pokok_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in similarity['pasal']]
    # similarity['similarity'] = [f'{int(x*10000)/100} %' for x in similarity['similarity']]
    dfpasal = pd.read_feather(os.path.join('media', 'countPasal.ft'))
    toppasal = dfpasal[dfpasal['file_names'].isin([df['file_names'].values[0]])]
    figpasal = px.bar(toppasal.sort_values('jumlah_pasal'),x='jumlah_pasal',y='pasal',orientation='h',color='jumlah_pasal',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
    figpasal.update_layout(coloraxis_showscale=False,xaxis_title=None,yaxis_title=None)
    dftopik = pd.read_feather(os.path.join('media', 'countTopik.ft'))
    toptopik = dftopik[dftopik['file_names'].isin([df['file_names'].values[0]])]
    figtopik = px.bar(toptopik.sort_values('jumlah_kata'),x='jumlah_kata',y='kata_kunci',orientation='h',color='jumlah_kata',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
    figtopik.update_layout(coloraxis_showscale=False,xaxis_title=None,yaxis_title=None)
    # from .plots.wcloud import create_wordcloud2
    # figtopik = create_wordcloud2(toptopik,'kata_kunci','jumlah_kata')
    #add npwp
    similarity = pd.merge(similarity,dfnpwp,on='file_names', how='left').drop_duplicates(subset='file_names', keep="last")
    
    # similarity = similarity[similarity['file_names'].isin(check_file())]
    similarity= similarity.sort_values('similarity',ascending=False)[:20]
    similarity['similarity'] = [f'{int(x*10000)/100} %' for x in similarity['similarity']]
    # first = similarity['file_names'].str.replace('.txt','').values[0]
    first = similarity['file_names'].str.replace('.txt','').values[1]
    npwpputusan = dfnpwp[dfnpwp['file_names']==str(id)]
    cek = [0 if text=='' else 1]
    linkpdf = file['file_names'].values[0]
    noput = dfsum[dfsum['file_names'].isin([df['file_names'].values[0]])]['noput'].values[0]
    return render(request, 'detail_putusan.html', {'text':text[:3150],'topic':topic[1],'file':file,'noput' :noput,'figpasal':figpasal.to_html(), 
                                                'similarity':similarity[1:],'textputusan':textputusan[:2150],'linkpdf':linkpdf,'figtopik':figtopik.to_html(), 
                                                'texthasil':texthasil,'cek':cek[0],'npwp':npwpputusan['npwp'].values[0],'first':first
                                                })

# @xframe_options_exempt
def dashboard(request):
    return render(request,'dashboard.html')

def select_pdf(request, id):
    return str(id)
    
def preview_pdf(request, id):
    with open(os.path.join(BASE_DIR, 'media/extracted_page.pdf'), 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=extracted_page.pdf'
        return response
