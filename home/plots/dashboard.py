# import dash
# from dash import dcc, html, dash_table
# import json
# import pandas as pd
# import plotly.express as px
# # import dash_core_components as dcc
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# from django_plotly_dash import DjangoDash
# import plotly.graph_objs as go

# # from django.conf import settings
# # from django.core.cache.backends.base import DEFAULT_TIMEOUT
# # from django.shortcuts import render
# # from django.views.decorators.cache import cache_page
# from core.settings import BASE_DIR
# from ..dbconnect02 import *
# # from functioncaching import cached_function
# import json
# import plotly.io as pio
# pio.templates.default = "simple_white"

# from .layouts import Plot, Layout
# import plotly.io as pio
# pio.templates.default = "simple_white"
# from .api import *
# from .wcloud import *

# from datetime import datetime,date
# import time
# curdate = time.strftime("%d")
# curmonth = time.strftime("%m")
# curyear = time.strftime("%Y")

# import os
# # df = dfsum
# dfitur = pd.read_feather(os.path.join(BASE_DIR, 'media/fitur.ft'))
# listfit = ['All'] + dfkategori['TopikSengketa'].unique().tolist()

# # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = [dbc.themes.LITERA]
# # external_stylesheets = [dbc.themes.BOOTSTRAP]
# scolor = {"Menolak": "#de425b", "Mengabulkan_Sebagian": "#96ac5a", "Mengabulkan_Seluruhnya": "#488f31",
#                     'Menambah_Jumlah_Pajak':"#ec8569",'Tidak_Dapat_Diterima':"#f4bc92",'Membetulkan_Kesalahan_Tulis/Hitung':"#d2ca90",
#                     'Membatalkan':"#b6ba74", 'Tidak_ditemukan':"#ffedcf"}
# app = DjangoDash('dashboard',external_stylesheets = external_stylesheets,serve_locally = False)
# # app = DjangoDash('maindash1', assets_external_path='static/assets/', add_bootstrap_links = True)

# app.layout = dbc.Container([
#                 dbc.Row([ 
#                     dbc.Col([
#                             dcc.Loading(html.Div(id='g0',children=[]))
#                         ],md=12,
#                         # ),
#                         style={'display':'none'}
#                     ),
#                     dbc.Col([
#                             # html.Div(children='Hello'),
#                             dcc.Loading(html.Div(id='g01',children=[]))
#                         ],md=12,
#                         style={'display':'none'}
#                     ),
#                     dbc.Col([
#                             # html.Div(children='Hello'),
#                             dcc.Loading(html.Div(id='g02',children=[]))
#                         ],md=12,
#                         # style={'display':'none'}
#                     ),
#                 ],style={'height':'2vh'}),
#                 dbc.Row([
#                     dbc.Col([
#                         html.Div([
#                                 "Dari",
#                                 dcc.DatePickerSingle(
#                                     id='date-start',
#                                     date=date(int(curyear)-2, int(curmonth), 1),
#                                     className='m-2',
#                                     placeholder=" Dari"
#                                     ),
#                                 "Sampai",
#                                 dcc.DatePickerSingle(
#                                     id='date-end',
#                                     date=date(int(curyear), int(curmonth), int(curdate)),
#                                     className='m-2',
#                                     placeholder=" Sampai"
#                                     )
#                         ]),
#                         Plot.vRadioButtons('rd','Kasus Berdasarkan',[' Objek Pajak',' Jenis Kasus',' Sektor'],' Objek Pajak'),
#                         html.Div(id='dd',children=[Plot.create_dropsingle('key',listfit,'All')]),
#                         html.Div(id='df',children=[],style={'display':'none'}),
#                     ],md=3),
#                     dbc.Col([
#                         dcc.Loading(html.Div(dcc.Graph(figure={}, id='g1a'),))
#                     ],md=9,style=Layout.rowstyle()),
#                 ]),
#                 dbc.Row([
#                     dbc.Col([
#                         dcc.Loading(html.Div(id='g1b')),
#                         ],md=6,style=Layout.figstyle()),
#                     dbc.Col([dcc.Loading(html.Div('Objek Sengketa')),
#                             dcc.Loading(html.Div(id='g1c'))
#                         ],md=3, style=Layout.figstyle()),
#                     dbc.Col([dcc.Loading(html.Div('Materi Sengketa')),
#                             dcc.Loading(html.Div(id='g1e'))
#                         ],md=3, style=Layout.figstyle()),
#                 ]),
#                 # dbc.Row([
#                 #     dbc.Col([
#                 #             dcc.Loading(html.Div([
#                 #                             dash_table.DataTable(
#                 #                                 id='table0',
#                 #                                 columns=[],
#                 #                                 markdown_options={"html": True},
#                 #                                 data=[],
#                 #                                 # editable=True,
#                 #                                 # filter_action="native",
#                 #                                 # filter_options={"case":"insensitive"},
#                 #                                 sort_action="native",
#                 #                                 # sort_mode="multi",
#                 #                                 # column_selectable="single",
#                 #                                 row_selectable="single",
#                 #                                 # row_deletable=True,
#                 #                                 selected_columns=[],
#                 #                                 selected_rows=[],
#                 #                                 page_action="native",
#                 #                                 page_current= 0,
#                 #                                 page_size= 15,
#                 #                                 style_cell={
#                 #                                     'whiteSpace': 'normal',
#                 #                                     'width': 'auto',
#                 #                                     'textAlign':'center',
#                 #                                     'overflow': 'hidden',
#                 #                                     'textOverflow': 'ellipsis',
#                 #                                     'border': '1px solid grey',
#                 #                                     'font_family': 'calibri',
#                 #                                     # 'maxWidth': 0
#                 #                                 },
#                 #                                 style_table={
#                 #                                     'overflowX': 'auto',
#                 #                                     'padding': '10px',
#                 #                                     # 'overflowY': 'auto'
#                 #                                 },
#                 #                                 style_data_conditional=[],
#                 #                                 style_header={'backgroundColor': '#2C4061',
#                 #                                                 'color': 'white',
#                 #                                                 'textAlign': 'center',
#                 #                                                 'border': '1px solid grey',
#                 #                                                 'font_family': 'calibri'},
#                 #                             )],))
#                 #         ],md=3, style=Layout.figstyle()),
#                 #     dbc.Col([
#                 #         dcc.Loading(
#                 #         html.Iframe(id="pdf", src="https://docs.google.com/viewerng/viewer?url=https://setpp.kemenkeu.go.id/risalah/ambilFileDariDisk/96331&embedded=true",
#                 #                     width=1200,height=800))
#                 #     ],md=9,style=Layout.figstyle())
#                 # ],style=Layout.rowstyle()),
#             ], fluid=True)


# @app.callback(Output('dd','children'),
#                 Input('rd', 'value'))
# # @cached_function(timeout=60*5, freshness_timeout=60*60)
# def update_radio(value1):
#     df =pd.DataFrame()
#     if value1 == ' Objek Pajak':
#         df = dfobjek2
#     elif value1 == ' Sektor':
#         df = dfsektor
#         val = 'All'
#     else:
#         df = pd.concat([dfhitung,dfterutang,dfsubjek])
#         # ops = ['All'] + dfhitung['topik'].unique().tolist()+ dfterutang['topik'].unique().tolist() +dfsubjek['topik'].unique().tolist()
#         # val = 'All'
#     ops = ['All'] + df['topik'].unique().tolist()
#     val = 'All'
#     dd = Plot.create_dropsingle('key',ops,val)
#     return dd

# @app.callback(Output('g0','children'),
#                 [Input('rd', 'value'),
#                  Input('key', 'value'),
#                 Input('date-start', 'date'),
#                 Input('date-end', 'date')])
# # @cached_function(timeout=60*5, freshness_timeout=60*60)
# def update_search(value1,value2,from_date,end_date):
#     if value2 == 'All':
#         dk = dfsum
#     else:
#         if value1 == ' Objek Pajak':
#             df = dfobjek2
#         elif value1 == ' Sektor':
#             df = dfsektor
#         else:
#             df = pd.concat([dfhitung,dfterutang,dfsubjek])
        
#         tpk = df[df['topik'].isin([value2])]
#         # tpk = dfkategori[dfkategori['topik'].isin([value1])]
#         # tpk = dfkategori[dfkategori['TopikSengketa'].isin([value1])]
#         # tpk = dfpasal[dfpasal['pasal'].isin(tpk['PasalDetil'])]
#         dk = dfsum[dfsum['file_names'].isin(tpk['file_names'])]
#     dk['dateris'] = pd.to_datetime(dk['dateris']).dt.date
#     dk = dk[dk['dateris']>=datetime.strptime(from_date, '%Y-%m-%d').date()]
#     dk = dk[dk['dateris']<=datetime.strptime(end_date, '%Y-%m-%d').date()]
#     # dk = dk.groupby(by=['dateris',])
#     # dkjson = dk.to_dict(orient='records')
#     datajson =  dk[['file_names']].head(19961).to_json()
#     return datajson

# @app.callback([Output('g1a','figure'),
#                 Output('g1b','children'),
#                 Output('g1c','children'),
#                 # Output('table0','data'),
#                 # Output('table0','columns'),
#                 # Output('table0','style_data_conditional'),
#                 Output('g1e','children'),
#                 # Output('g1f','children'),
#                 # Output('g1g','children'),
#                 # Output('g1i','children')
#                 ],
#                 [Input('g0','children'),Input('g01','children')])
# # @cached_function(timeout=60*5, freshness_timeout=60*60)
# def update_search(dfdata,selected):
#     df = pd.read_json(dfdata)
#     dk = dfsum[dfsum['file_names'].isin(df['file_names'])]
#     dk['jumlah'] = 1
#     if selected == [] or selected == 'All' or selected == None:
#         dk = dk
#     else:
#         dk = dk[dk['hasil_putusan'].isin([str(selected)])]
    
#     data = dk.groupby(by=['hasil_putusan','tahun'],as_index=False)['jumlah'].sum()
#     # fig0 = px.sunburst(data,
#     #             path=[px.Constant("All"),'hasil_putusan'], values='jumlah'
#     #             ,color='hasil_putusan',color_discrete_map=scolor
#     #         )
#     fig0 = px.treemap(data,
#                 path=[px.Constant("All"),'hasil_putusan'], values='jumlah'
#                 ,color='hasil_putusan',color_discrete_map=scolor
#                 ,hover_name='hasil_putusan',hover_data={'tahun':False,'hasil_putusan':False}
#             )
#     fig0.update_traces(textinfo="label+percent parent+value")
#     fig0.update_layout(Layout.nrfig())
#     fig0.update_layout(height=300)
#     g1a = fig0
#     dk['month'] = pd.to_datetime(dk['dateris']).dt.strftime('%Y-%m')
#     data3 = dk.groupby(by=['hasil_putusan','month'],as_index=False)['jumlah'].sum()
#     fig2 = px.bar(data3,
#                 x='month',
#                 y='jumlah',
#                 color='hasil_putusan',
#                 color_discrete_map=scolor,
#             #   title=gtitle,
#                 labels={'x': 'Bulan', 'y': 'Jumlah Putusan'},
#                 barmode='stack'
#                   )

#     fig2.update_layout(
#         title={
#             'font_size': 24,
#             'xanchor': 'center',
#             'x': 0.5
#         })
#     fig2.update_layout(Layout.nrfig())
#     g1b= dcc.Graph(id='wc2',figure=fig2, config={'displayModeBar': False})
#     dklink = dk[['file_names']]
#     dklink['link'] = ["<a href="+f"'http://194.163.45.59:5085/search/{x}'"+" target='_blank'>"+f'{x}'+"</a>" for x in dklink['file_names']]
#     g1da = dklink.to_dict(orient='records')
#     # g1db = [{"name": i, "id": i, "selectable": True} for i in dklink.columns]
#     g1db = [{"id": "link", "name": "Daftar Putusan", "presentation": "markdown"},
#             # {"id": "tahun", "name": "tahun"}
#             ]
#     texthl =[{'if': {
#             'filter_query': '{topik} = "{value1}"'
#         },
#         'backgroundColor': '#0074D9',
#         'color': 'white'
#         }]
    
#     dktext1 = dfobjek[dfobjek['file_names'].isin(dk['file_names'].tolist())]
#     fig1 = create_wordcloud(dktext1.sort_values('objekCount').head(100),'objekList','objek sengketa')
#     fig1.update_layout(Layout.stdfig())
#     g1c = dcc.Graph(id='wcloud1',figure=fig1, config={'displayModeBar': False})

#     dktext2 = dfkoreksi[dfkoreksi['file_names'].isin(dk['file_names'].tolist())]
#     fig5 = create_wordcloud(dktext2.sort_values('koreksiCount').head(100),'koreksiList','koreksi penghitungan')
#     fig5.update_layout(Layout.stdfig())
#     g1e = dcc.Graph(id='wcloud2',figure=fig5, config={'displayModeBar': False})
#     return g1a,g1b,g1c,g1e
#     # return g1a,g1b,g1c,g1da,g1db,texthl,g1e
#     # return g1a,g1b,g1da,g1db,texthl,g1f,g1g,g1i


# @app.callback(
#     Output('g01','children'),
#     Input(component_id='g1a', component_property='clickData'),
#     prevent_initial_call=True
# )
# def update_text(chosen_data):
#     return str(chosen_data['points'][0]['label'])

# # def update_text(chosen_data1,chosen_data2):  # the function argument comes from the component property of the Input
# #     if chosen_data1 == None:
# #         if chosen_data2 == None:
# #             selected = None
# #         else:
# #             chosen_data = chosen_data2
# #             selected = str(chosen_data['points'][0]['label'])
# #     else:
# #         chosen_data = chosen_data1
# #         selected = str(chosen_data['points'][0]['label'])
# #     return selected

# @app.callback(
#     Output("g1a", "clickData"),
#     Input("clear", "n_clicks"),    
#     )
# def clear(n_clicks):
#     return None

# @app.callback(
#     Output("g02", "children"),
#     Input("table0", "selected_data"),    
#     )
# def select(row):
#     data = row
#     return str(data)


# # if __name__ == "__main__":
# #     app.run_server(debug=True)