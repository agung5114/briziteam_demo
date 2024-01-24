# import sys
# if sys.version_info > (3, 0):
#     from io import StringIO
# else:
#     from io import BytesIO as StringIO
    
# from pdfminer.layout import LAParams
# from pdfminer.high_level import extract_text_to_fp
# from pdfminer.high_level import extract_text
# # from pdfminer.high_level import extract_text
# import re

# # def extract_pdf(file):
# #     aDict = {}
# #     txtObj = extract_text(file,laparams=LAParams(),codec="utf-8")

# def getBagian(files):
#     aDict = {}
#     aDict['pasal'] = {}
#     txtObj = extract_text(files,laparams=LAParams(),codec="utf-8")
#     start, stop, key = 0,0,""
#     for each in re.finditer('[A-Z ]{7,}',txtObj):
#     #     print(each)
#         if each[0].strip() == key : continue
#         for item in ['melawan', "sengketa", "perkara",'permasalahan',"analisa","pertimbangan", "ketentuan", "mengadili"]:
# #         for item in ["sengketa", "mengadili"]:
#             if item in  each[0].lower().replace(" ","") :
#                 stop = each.span()[0]
#                 if start > 0 :  aDict['pasal'][key] = txtObj[start:stop].strip()
#                 key = each[0].strip()
#                 start = each.span()[1]
#     aDict['pasal'][key] = txtObj[start:-1].strip()
#     try :
#         aDict['pasal']['results'] = re.match('([A-Za-z]+ +){2}',aDict['pasal'][key])[0].lower()
#     except :
#         print('pasal')
#     return aDict


# def getBagian2(files):
#     aDict = {}
#     aDict['pasal'] = {}
#     # files = 'pdf/' + file + ".pdf"
#     txtObj = extract_text(files,laparams=LAParams(),codec="utf-8")
#     start, stop, key = 0,0,""
#     for each in re.finditer('[A-Z ]{7,}',txtObj):
#     #     print(each)
#         if each[0].strip() == key : continue
# #         for item in ['melawan', "sengketa", "perkara",'permasalahan',"analisa","pertimbangan", "ketentuan", "mengadili"]:
# #         for item in ["sengketa", "mengadili"]:
#         for item in ["tanggapanterbanding", "kesimpulandanusul"]:
#             if item in  each[0].lower().replace(" ","") :
#                 stop = each.span()[0]
#                 if start > 0 :  aDict['pasal'][key] = txtObj[start:stop].strip()
#                 key = each[0].strip()
#                 start = each.span()[1]
#     aDict['pasal'][key] = txtObj[start:-1].strip()
#     try :
#         aDict['pasal']['results'] = re.match('([A-Za-z]+ +){2}',aDict['pasal'][key])[0].lower()
#     except :
#         print('pasal')
#     return aDict

# def extract_pasal(aDict):
#     dictPasal = {}
#     for item in aDict:
#         key = list(aDict[item])[1]

#         aList = []
#         for each in re.findall('pasal [0-9]+[abcde]{0,1}[ (ayt)0-9]+', aDict[item][key].lower()):
#             tList = re.findall('[0-9]+', each)
#             if len(tList) > 1:
#                 aList.append("pasal " + tList[0] + " ayat " + tList[1])
#             else:
#                 aList.append("pasal " + tList[0])
#         dictPasal[item] = aList
#         aList = []
#     return dictPasal

# def extract_pasal2(aDict):
#     dictPasal = {}
#     for item in aDict :
#         key = list(aDict[item])[0]
        
#         aList = []
#         for each in re.findall('pasal [0-9]+[ (ayt)0-9]+', aDict[item][key].lower()) :
#             tList = re.findall('[0-9]+',each)
#             if len(tList) > 1 : aList.append("pasal " + tList[0] + " ayat " + tList[1])
#             else :  aList.append("pasal " + tList[0] )
#         dictPasal[item] = aList
#         aList = []
#     return dictPasal

# import pandas as pd
# import numpy as np
# import re
import os


folder_drive = '/root/projectx/briziteam/media/SMALL'
dir_files = [f for f in os.listdir(folder_drive) if os.path.isfile(os.path.join(folder_drive, f)) and f[-3:] == 'pdf']
dir_files.sort()
# print(dir_files[:10])
print(dir_files[-10:])