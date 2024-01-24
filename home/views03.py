from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from core.settings import HOME_TEMPLATES
import plotly_express as px
from .forms import DateForm, topiclist
from datetime import date, timedelta
import pandas as pd
from core.settings import BASE_DIR
from .dbconnect02 import *

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
def search(request):
    import re
    from collections import Counter
    putusan_color = {"Menolak": "#de425b", "Mengabulkan_Sebagian": "#96ac5a", "Mengabulkan_Seluruhnya": "#488f31",
                     'Menambah_Jumlah_Pajak':"#ec8569",'Tidak_Dapat_Diterima':"#f4bc92",'Membetulkan_Kesalahan_Tulis/Hitung':"#d2ca90",
                     'Membatalkan':"#b6ba74", 'Tidak_ditemukan':"#ffedcf"}
    form = searchForm(initial={'topic': 'Barang Strategis','putusan':'All'})
    topic = "Barang Strategis"
    hasil = "All"
    if request.method == 'POST':
        form = searchForm(request.POST, request.FILES)
        if form.is_valid():
            topic = str(request.POST.get('topic'))
            hasil = str(request.POST.get('putusan'))
    else:
        pass

    if hasil == "All":
        dfall = get_sengketa(topic.lower())
    else:
        dfall = get_sengketaFilter(topic.lower(),hasil)
    
    df = dfsum[dfsum['file_names'].isin(dfall['file_names'])]
    plist = []
    for ps in df['pasal']:
        for p in ps:
            plist.append(p)
    pasal = Counter(plist).keys() # equals to list(set(words))
    counts = Counter(plist).values() # counts the elements' frequency
    dfig = pd.DataFrame(list(zip(pasal,counts)),columns=['Pasal','Jumlah'])
    fig1 = px.bar(dfig.sort_values('Jumlah',ascending=False).head(10), x='Pasal', y='Jumlah', color='Jumlah',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
    df['Jumlah'] = 1
    fig2 = px.pie(df,names='hasil_putusan',values='Jumlah',color='hasil_putusan',color_discrete_map=putusan_color)
    # df = df.sort_values('tahun',ascending=False)[:100]
    # df['pokok_sengketa'] = [ [dfkey.lookup(dfkey.index, x)] for x in df['pasal']]
    df['topik_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in df['pasal']]
    dftext = get_sengketaText(df['file_names'].tolist())
    df = df.merge(dftext[['file_names','pokok_sengketa']],how='left',on='file_names')
    # df = df.merge(dftext,how='left',on='file_names')
    df['pokok_sengketa'] = df['pokok_sengketa'].fillna('')
    df = df.drop_duplicates(subset='file_names', keep="last")
    # Kalimat mengandung kata kunci
    def get_sentence(topic,line):
        tmp = []
        searchObj = [ t for t in line.split('. ') if topic.lower() in t]
        for match in searchObj:
            tmp.append(match)
        return ['...</p><br><p>...'.join(tmp[:3]),len(tmp)]
    df['kalimat'] = [ get_sentence(topic,x)[0] for x in df['pokok_sengketa']]
    df['kalimat'] = ["<p>"+f'{x}'+"</p>" for x in df['kalimat']]
    df['jumlah'] = [ get_sentence(topic,x)[1] for x in df['pokok_sengketa']]
    # Jumlah ditemukan
    # def count_key(key,text):
    #     pat1 = re.compile(topic)
    #     p = re.findall(pat1, text)
    #     return len(p)
    df = df.sort_values('jumlah',ascending=False)[:100]
    # df = df.sort_values('jumlah',ascending=False)[:20]
    first = df['file_names'].str.replace('.txt','').values[0]

    context = {'form': form,'total':len(dfall.index),'chart1':fig1.to_html(),'chart2':fig2.to_html(),'selected':topic,
            #    'table2':dfff,
                'files':df,'first':first
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
    # doc = fitz.open(os.path.abspath(os.path.join("/home/agungseptia/projects/projex/pdf", f"{id}.pdf")))
    doc = fitz.open(os.path.abspath(os.path.join("pdf", f"{id}.pdf")))
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
            
            texthasil = splitText(text.lower(),'mengadili')
            text = splitText(text.lower(),'pokok_sengketa') 

            features = get_features(text)
            topic = get_topic(features)
            similarity = get_sim(features,topic[0])[:20]
            listfile = similarity['file_names'].tolist()
            listfile.sort()
            dftext = dfsum[dfsum['file_names'].isin(listfile)]
            similarity = pd.merge(similarity,dftext[['file_names','pasal','topik','hasil_putusan']],on='file_names', how='left')
            similarity['pokok_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in similarity['pasal']]
            similarity['kemiripan'] = [f'{int(x*1000)/10} Persen' for x in similarity['similarity']]
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
            return render(request, 'pdf_extract.html', {'form': form,'text':text[:3150],'topic':topic[1],'linkpdf':linkpdf,'figtopik':figtopik.to_html(),
                                                        'similarity':similarity,'texthasil':texthasil[:2150],'figpasal':figpasal.to_html(), 
                                                        'hasil':prediksi_hasil,'topfitur':topfitur,'jumlahtop':jumlahtop[0],'cek':cek[0]})
    else:
        form = PdfExtractForm()
        return render(request, 'pdf_extract.html', {'form': form})

def detail_putusan(request, id):
    file = dfsum[dfsum['file_names'].isin([str(id)])]
    texthasil = file['hasil_putusan'].values[0]
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
    similarity = pd.merge(similarity,dftext[['file_names','pasal','topik','hasil_putusan']],on='file_names', how='left')
    similarity['pokok_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in similarity['pasal']]
    similarity['similarity'] = [f'{int(x*10000)/100} %' for x in similarity['similarity']]
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
    cek = [0 if text=='' else 1]
    linkpdf = file['file_names'].values[0]
    noput = dfsum[dfsum['file_names'].isin([df['file_names'].values[0]])]['noput'].values[0]
    return render(request, 'detail_putusan.html', {'text':text[:3150],'topic':topic[1],'file':file,'noput' :noput,'figpasal':figpasal.to_html(), 
                                                'similarity':similarity[1:],'textputusan':textputusan[:2150],'linkpdf':linkpdf,'figtopik':figtopik.to_html(), 
                                                'texthasil':texthasil,'cek':cek[0]})

# @xframe_options_exempt
def dashboard(request):
    return render(request,'dashboard.html')

def search_sampel(request):
    import re
    from collections import Counter
    putusan_color = {"Menolak": "#de425b", "Mengabulkan_Sebagian": "#96ac5a", "Mengabulkan_Seluruhnya": "#488f31",
                     'Menambah_Jumlah_Pajak':"#ec8569",'Tidak_Dapat_Diterima':"#f4bc92",'Membetulkan_Kesalahan_Tulis/Hitung':"#d2ca90",
                     'Membatalkan':"#b6ba74", 'Tidak_ditemukan':"#ffedcf"}
    form = searchForm(initial={'topic': 'Barang Strategis','putusan':'All'})
    topic = "Barang Strategis"
    hasil = "All"
    if request.method == 'POST':
        form = searchForm(request.POST, request.FILES)
        if form.is_valid():
            topic = str(request.POST.get('topic'))
            hasil = str(request.POST.get('putusan'))
    else:
        pass

    if hasil == "All":
        dfsam = get_sengketaSample(topic.lower())
        dfall = get_sengketa_multi(dfsam['file_names'].tolist())
    else:
        dfsam = get_sengketaSampleFilter(topic.lower(),hasil)
        dfsam = dfsam[dfsam['hasil_putusan'].isin([hasil])]
        dfall = get_sengketa_multi(dfsam['file_names'].tolist())
    
    def get_sentence(topic,line):
        tmp = []
        searchObj = [ t for t in line.split('. ') if topic.lower() in t]
        for match in searchObj:
            tmp.append(match)
        return ['...</p><br><p>...'.join(tmp[:1]),len(tmp)]
    
    df = dfsum[dfsum['file_names'].isin(dfall['file_names'])]
    plist = []
    for ps in df['pasal']:
        for p in ps:
            plist.append(p)
    pasal = Counter(plist).keys() # equals to list(set(words))
    counts = Counter(plist).values() # counts the elements' frequency
    dfig = pd.DataFrame(list(zip(pasal,counts)),columns=['Pasal','Jumlah'])
    fig1 = px.bar(dfig.sort_values('Jumlah',ascending=False).head(10), x='Pasal', y='Jumlah', color='Jumlah',color_continuous_scale=["#ffedcf","#ec8569","#de425b"])
    df['Jumlah'] = 1
    fig2 = px.pie(df,names='hasil_putusan',values='Jumlah',color='hasil_putusan',color_discrete_map=putusan_color)
    # df = df.sort_values('tahun',ascending=False)[:100]
    # df['pokok_sengketa'] = [ [dfkey.lookup(dfkey.index, x)] for x in df['pasal']]
    df['topik_sengketa'] = [np.unique(np.array([keydict[y] for y in x])) for x in df['pasal']]
    dftext = get_sengketaText(df['file_names'].tolist())
    df = df.merge(dftext[['file_names','pokok_sengketa']],how='left',on='file_names')
    # df = df.merge(dftext,how='left',on='file_names')
    df['pokok_sengketa'] = df['pokok_sengketa'].fillna('')
    df['kalimat'] = [ get_sentence(topic,x)[0] for x in df['pokok_sengketa']]
    df['kalimat'] = ["<p>"+f'{x}'+"</p>" for x in df['kalimat']]

    dfsam2 = get_sampel_multi(df['file_names'])
    dfsam2 = dfsam2.drop_duplicates(subset='file_names', keep="last")
    dfsam2['pokok_sampel'] = dfsam2['pokok_sengketa']
    df = df.merge(dfsam2[['file_names','pokok_sampel']],how='left',on='file_names')
    df['kalimat_sampel'] = [ get_sentence(topic,x)[0] for x in df['pokok_sampel']]
    df['kalimat_sampel'] = ["<p>"+f'{x}'+"</p>" for x in df['kalimat_sampel']]
    df['jumlah'] = [ get_sentence(topic,x)[1] for x in df['pokok_sampel']]
    df = df.drop_duplicates(subset='noput', keep="last")
    df = df.sort_values('jumlah',ascending=False)[:20]

    context = {'form': form,'total':len(dfall.index),'chart1':fig1.to_html(),'chart2':fig2.to_html(),'selected':topic,
            #    'table2':dfff,
                'files':df
                }
    return render(request, 'pencarian_sampel.html',context)

def select_pdf(request, id):
    return str(id)
    
def preview_pdf(request, id):
    with open(os.path.join(BASE_DIR, 'media/extracted_page.pdf'), 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=extracted_page.pdf'
        return response
