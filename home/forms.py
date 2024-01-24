from django import forms
from django.forms import ModelForm
from .models import Tweets
from datetime import date, timedelta
import datetime

from crispy_forms.helper import FormHelper

#get current time
d = datetime.datetime.now()
mt = d.strftime("%m")
yr = d.strftime("%y")

today = date.today()
yesterday = date.today() - timedelta(days=1)
h30 = date.today() - timedelta(days=30)
topic = Tweets.objects.all().values_list('keyword', flat=True).distinct()
topiclist = [('kemenkeu','kemenkeu'),('pajak','pajak')]
def create_drop(cat):
    llist=[('All','All')]
    for i in cat:
        llist.append((i,i))
    return llist

putlist = ['Menolak','Mengabulkan_Sebagian','Mengabulkan_Seluruhnya',
           'Menambah_Jumlah_Pajak','Tidak_Dapat_Diterima',
           'Membetulkan_Kesalahan_Tulis/Hitung','Membatalkan','Tidak_ditemukan']
class DateForm(forms.Form):
    topic = forms.ChoiceField(choices=topiclist)
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=h30)
    end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=today)

class DailyForm(forms.Form):
    topic = forms.ChoiceField(choices=topiclist)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=yesterday)

class TopicForm(forms.Form):
    addtopic = forms.ChoiceField(choices=topiclist)
    startdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=h30)
    enddate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),initial=today)

class DateInput(forms.DateInput):
    input_type = 'date'

class PdfExtractForm(forms.Form):
    file = forms.FileField(label="Upload PDF Document")
    # page = forms.CharField(max_length=20, label="Page Number")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Only pdf documents are allowed. ")
        return file
    
class searchForm(forms.Form):
    topic = forms.CharField(label="")
    # tahun = forms.ChoiceField(label='Tahun',choices=create_drop(['All','2023','2022','2021','2020','2019','2018']))
    putusan = forms.ChoiceField(label='Hasil Putusan',choices=create_drop(putlist))
    jumlah = forms.ChoiceField(label='Jumlah Ditampilkan',choices=create_drop(['30','100','200']),initial=('30','30'))


        