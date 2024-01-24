# import dash
# from dash import Dash, dcc, html, dash_table
# from django_plotly_dash import DjangoDash
# import plotly.express as px
# import plotly.graph_objects as go
# from dash.dependencies import Input, Output, State
# # import dash_table
# from dash.dash_table.Format import Format, Group, Scheme, Symbol
# import dash_bootstrap_components as dbc
# import pandas as pd
# # import dash_draggable
# # from dash_draggable import DashDraggable2

# class Layout():
#     def __init__(self):
#         pass
#     def tabstyle():
#         style = {
#                     'borderBottom': '1px solid #d6d6d6',
#                     'padding': '6px',
#                     'fontWeight': 'bold'
#                 }
#         return style
#     def color_bs(key):
#         colors = {
#             'primary' : '#1C4E80',
#             'success' : '#35b779',
#             'info' : '#5193b0',
#             'danger': '#EA6A47',
#             'warning': '#ffa600',
#             'secondary':'#7E909A',
#             'prim_off':'#A5D8DD',
#             'warn_off':'#ffd8c9',
#             'info_off':'#9095CD',
#             'danger_off':'#d1807c'
#         }
#         return colors[key]
#     def stdfig():
#         return dict(clickmode='event+select',
#                     hovermode='closest',
#                     autosize=True,
#                     margin = dict( l=20,r=20,b=20,t=15),
#                     font=dict(color="#191A1A"),
#                     title_font=dict(color="#191A1A", size=14),
#                     plot_bgcolor ='#fffcfc',
#                     paper_bgcolor ='#fffcfc',
#                     showlegend = True,
#                     # color_discrete_sequence=px.colors.qualitative.Pastel,
#                     # color_continuous_scale='Rainbow',
#                     )
#     def nrfig():
#         return dict(clickmode='event+select',
#                     hovermode='closest',
#                     autosize=True,
#                     margin = dict( l=5,r=5,b=5,t=1),
#                     font=dict(color="#191A1A"),
#                     title_font=dict(color="#191A1A", size=14),
#                     plot_bgcolor ='#fffcfc',
#                     paper_bgcolor ='#fffcfc',
#                     showlegend = False,
#                     # color_discrete_sequence=px.colors.qualitative.Pastel,
#                     # color_continuous_scale='Rainbow',
#                     )
#     def figstyle():
#         stl = {
#                 "border-radius": "4px",
#                 # "background-color": "#C6CBEF",
#                 # "background-color":"#ffedcf",
#                 "box-shadow": "0 4px 6px rgba(0,0,0,.08), 0 0 6px rgba(0,0,0,.05)",
#                 "transition": ".3s transform cubic-bezier(.155,1.105,.295,1.12),.3s box-shadow,.3s -webkit-transform cubic-bezier(.155,1.105,.295,1.12)",
#                 "padding": "18px 30px 18px 30px",
#                 "cursor": "pointer"
#                 }
#         return stl

#     def rowdeck(rlist):
#         return html.Div([dbc.CardDeck(rlist),
#                         ], style={'padding': '25px'})

#     def setconfig():
#         return dict(displaylogo= False, scrollZoom=False,displayModeBar='hover')

#     def rowstyle():
#         return dict(padding= '5px 5px 5px 5px')
#     def flat_cardstyle():
#         return dict()


# class Plot():
#     def __init__(self):
#         pass
#     def create_card(card_id,v1,v2,v3,color):
#         return dbc.Card([dbc.CardHeader(
#                             html.H5(children=v1, id=str(card_id)+"v1")),
#                         dbc.CardBody([
#                             html.H3(children=v2, id=str(card_id)+"v2"),
#                             html.H6(children=v3, id=str(card_id)+"v3")
#                             ])]
#                             ,color=color
#                             ,className="shadow p-4 mt-0 mr-0 mb-2")
#                             # ,style={"height": "100%", "background-color": "#dfe5e8"})
                        
#     def card_single(idval,text1,text2,bcolor,fcolor):
#         return html.Div([
#                             html.H5(children=text1),
#                             html.H4(id=idval,children=None),
#                             html.H6(children=text2),
#                             ]
#                             # color=color
#                             ,className="card card-body shadow p-2 mt-0 mb-2 mr-0 ml-2"
#                             ,style=dict(background=bcolor, border= 'light grey', color=fcolor,family='Verdana, sans-serif'))
#     def card_text(idval,text1,text2,bcolor,fcolor):
#         return html.Div([
#                             html.H5(children=text1),
#                             html.H4(id=idval,children=None),
#                             html.H6(children=text2),
#                             ]
#                             # ,color=fcolor
#                             ,className="p-1 mt-1 mb-0"
#                             ,style={'border': 'light grey','background-color':bcolor,'color':fcolor})
                                                 
#     def create_cardsingle(id1,id2,id3,color):
#         return dbc.Card(dbc.CardBody([
#                             html.H5(children=None, id=id1),
#                             html.H6(children=None, id=id2),
#                             html.H6(children=None, id=id3),
#                             ]),color=color
#                             ,className="p-1 mt-1 mb-0"
#                             ,style={'border': 'light grey'})

#     def cardWithHeader(card_id,v1,v2,v3,color):
#         return dbc.Card([dbc.CardHeader(
#                             html.H5(children=v1, id=str(card_id)+"v1")),
#                         dbc.CardBody([
#                             html.H3(children=v2, id=str(card_id)+"v2"),
#                             html.H6(children=v3, id=str(card_id)+"v3")
#                             ])]
#                             ,color=color
#                             ,className="p-1 mt-1 mb-0"
#                             ,style={'border': 'light grey'})

#     def create_table(table_id,df,pagesize):
#         # dataframe = df
#         # dataframe.set_index(dataframe[idx],inplace=True, drop=False)
#         # data_columns = ['Kode KPP','Nama KPP']
#         # df_columns = ['kode_kpp', 'nama_kpp']
#         return  html.Div(dash_table.DataTable(
#                                     id=table_id,
#                                     columns=[{"name": i.upper(), 
#                                                 "id": i,
#                                                 "type" :'numeric',
#                                                 "format": Format(
#                                                 scheme=Scheme.fixed,
#                                                 precision=0,
#                                                 group=Group.yes,
#                                                 groups=3,
#                                                 group_delimiter=".",
#                                                 symbol=Symbol.yes, 
#                                                 symbol_prefix=u'Rp '
#                                                 )
#                                                 } for i in df.columns],
#                                     # columns=[{'name': col, 
#                                     #         'id': df_columns[idx]
#                                     #         } for (idx, col) in enumerate(data_columns)],
#                                     data =df.to_dict('records'),
#                                     selected_row_ids =[],
#                                     selected_rows = [],
#                                     selected_columns = [],
#                                     row_selectable = False,
#                                     # row_selectable="multi",
#                                     # column_selectable="multi",
#                                     filter_action="native",
#                                     sort_action="native",
#                                     sort_mode="single",
#                                     page_size=pagesize,
#                                     dropdown_data = True,
#                                     style_cell={
#                                         'whiteSpace': 'normal',
#                                         'height': 'auto',
#                                         'textAlign':'center',
#                                         'overflow': 'hidden',
#                                         'textOverflow': 'ellipsis',
#                                         'border': '1px solid grey',
#                                         'font_family': 'calibri',
#                                         # 'maxWidth': 0
#                                     },
#                                     style_table={
#                                         'overflowX': 'auto',
#                                         'padding': '10px',
#                                         # 'overflowY': 'auto'
#                                     },
#                                     style_header={'backgroundColor': '#2C4061',
#                                                     'color': 'white',
#                                                     'textAlign': 'center',
#                                                     'border': '1px solid grey',
#                                                     'font_family': 'calibri'},
#                                     )
#                 # ,body=True
#                 ,className="shadow m-2")
#     def bs_table(df):
#         return dbc.Table.from_dataframe(df, size='sm',responsive=True, bordered=True, hover=True)
#     def create_dropval(dd_id,col,val):
#         return html.Div(
#                 dcc.Dropdown(id =dd_id,
#                             options=[{'label': i, 'value': i} for i in col],
#                             multi=False,
#                             value=str(val))
#                 ,className="shadow p-1 mt-2 mb-2 mr-2 ml-2")
#                 # ,className="p-2 mt-2 mb-0")
#     def create_dropdown(dd_id,col,val):
#         return html.Div(
#                 dcc.Dropdown(id =dd_id,
#                             options=[{'label': i, 'value': i} for i in col],
#                             multi=False,
#                             placeholder=str(val))
#                 ,className="p-1 mt-1 mb-0")
#     def create_dropsingle(dd_id,col,val):
#         return dbc.Card(
#                 dcc.Dropdown(id =dd_id,
#                             options=[{'label': i, 'value': i} for i in col],
#                             value=val,
#                             multi=False)
#                 ,body=True
#                 ,className="p-1 mt-2 mb-2 mr-2 ml-2")
#     def graph_drop(title,drop_id,graph_id):
#         return dbc.Card([
#                 dbc.CardHeader(
#                     html.H5(title, className="card-title")),
#                 dbc.CardBody([
#                     dcc.Dropdown(id=drop_id, options=[],value=[],multi=True),
#                     dcc.Graph(id=graph_id,config=Layout.setconfig(),clear_on_unhover =True)]
#                     )]
#                 ,style={'padding': '2px 2px 2px 2px'}
#                 ,className="shadow p-2 mt-2 mb-2 bg-white h-100 w-100")
#     def graph(graph_id,title):
#         return dbc.Container([
#                     dbc.Row(
#                         html.Div(str(title)),
#                     ),
#                     dbc.Row(
#                         dcc.Graph(id=graph_id,config=Layout.setconfig(),clear_on_unhover =True)
#                     )]
#                     ,className="mt-2",fluid=True
#                     ,style=dict(border= 'light grey', family='Verdana, sans-serif')
#                     )
#                 # ,style={'padding': '2px 2px 2px 2px'}
#                 # ,className="shadow p-2 mt-2 mb-2 bg-white")
#     def create_treemap(graph_id,title):
#         return dbc.Card([
#             html.H5(title, className="card-title"),
#             dcc.Graph(id=graph_id,config=Layout.setconfig(),clear_on_unhover =True)]
#                 ,style={'padding': '1px 1px 1px 1px','height':'90%'}
#                 ,className="shadow p-2 mt-2 mb-2 bg-white h-100 w-100" 
#                 )
#     def create_graphH(graph_id, title):
#         return html.Div([
#             # html.H5(title, className="card-title"),
#             dcc.Graph(id=graph_id,config=Layout.setconfig(),clear_on_unhover =True)]
#             ,style={'padding': '2px 2px 2px 2px','border':'light grey'}
#             ,className="shadow p-2 bg-white h-100 w-100")
#     def vRadioButtons(rd_id,title,ops,val):
#         return dbc.Card([
#                 html.H5(title),
#                 dbc.CardBody([
#                 dcc.RadioItems(id= rd_id,options=[{'label': i, 'value': i} for i in ops],
#                             value=val,
#                             # labelStyle={'display': 'flex'}
#                             )
#                         ])
#                     ]
#                 ,className="p-1 mt-2 mb-4"
#                 )
#     def create_radio(rd_id,title,col):
#         return dbc.Card([
#                 html.H5(title),
#                 dcc.RadioItems(options=[{'label': i, 'value': i} for i in col],
#                             value=[],
#                             labelStyle={'display': 'inline-block'})
#                 ]
#                 ,className="shadow p-1 mt-2 mb-2 mr-2 ml-2"
#                 ,style={'padding': '2px 2px 2px 2px'})
#     def create_check(ch_id,title,col):
#         return dbc.Card([
#                 html.H5(title),
#                 dcc.Checklist(id=ch_id,options=[{'label': i, 'value': i} for i in col])
#                 ]
#                 ,className="shadow p-1 mt-2 mb-2 mr-2 ml-2"
#                 ,style={'padding': '2px 2px 2px 2px'})
                                    
#     def create_search(input_id,input_text,button_id,button_text,):
#         return dbc.Card(
#                 [dbc.Input(id=input_id, placeholder=input_text, type="text"),
#                 html.Br(),
#                 dbc.Button(button_text,id=button_id, color="primary", type="submit", n_clicks=0,className="mr-1"),])
#                 # ,className="shadow p-2"
#                 # ,style={'padding': '2px 2px 2px 2px'})
#     def control_card(id1,var1,id2,var2,id3,var3):
#         return dbc.Card([dbc.FormGroup([
#                             dbc.Label(var1),
#                             dcc.Dropdown(
#                                 id=id1,
#                                 options=[],
#                                 value=None,
#                             ),]),
#                         dbc.FormGroup([
#                             dbc.Label(var2),
#                             dcc.Dropdown(
#                                 id=id2,
#                                 options = [],
#                                 value=None,
#                             ),]),
#                         dbc.FormGroup([
#                             dbc.Label(var3),
#                             dcc.Dropdown(
#                                 id=id3,
#                                 options=[],
#                                 value=None,
#                             ),]),
#                         ],
#                         body=True,style={'margin':'5px 5px 5px 5px'}
#                     )
#     def control_cardH(id1,var1,id2,var2,id3,var3):
#         return dbc.CardDeck([dbc.FormGroup([
#                             dbc.Label(var1),
#                             dcc.Dropdown(
#                                 id=id1,
#                                 options=[],
#                                 value=None,
#                             ),]),
#                         dbc.FormGroup([
#                             dbc.Label(var2),
#                             dcc.Dropdown(
#                                 id=id2,
#                                 options = [],
#                                 value=None,
#                             ),]),
#                         dbc.FormGroup([
#                             dbc.Label(var3),
#                             dcc.Dropdown(
#                                 id=id3,
#                                 options=[],
#                                 value=None,
#                             ),]),
#                         ],style={'margin':'5px 5px 5px 5px'}
#                     )
#     def info_card(desc1):
#         return dbc.Card(dbc.Label(desc1),style={'margin':'5px 5px 5px 5px','padding':'5px 5px 5px 5px'})
#     def empty_graph(id1,title1):
#         return html.Div([
#                         html.H4(title1),
#                         dcc.Graph(id=id1)],
#                         style={'margin':'5px 5px 5px 5px','padding':'5px 5px 5px 5px'},
#                         # style=Layout.figstyle(),
#                         className="shadow p-2 bg-white")
#     def card_group(content):
#         return dbc.FormGroup(content,
#                         style={'margin':'5px 5px 5px 5px','padding':'5px 5px 5px 5px'},
#                         className="shadow p-2 bg-white")
#     def card_group_nobg(content):
#         return dbc.FormGroup(content,
#                         style={'margin':'0px 5px 0px 5px','padding':'5px 5px 5px 5px'})
                        
#     def filter_card(id1,var1,ops1):
#         return dbc.Card(dbc.FormGroup([
#                             dbc.Label(var1),
#                             dcc.Dropdown(
#                                 id=id1,
#                                 options=ops1,
#                                 value=None,
#                             ),]),
#                         body=True,style={'margin':'5px 5px 5px 5px'})
#     def flat_table(table_id,pagesize):
#         return  html.Div(
#                     dbc.Card([
#                         dbc.CardHeader("This is the header"),
#                         dbc.CardBody(
#                         (dash_table.DataTable(
#                                     id=table_id,
#                                     page_size=pagesize,
#                                     )))]),
#                 style={'margin':'5px 5px 5px 5px','padding':'5px 5px 5px 5px'},
#                 className="shadow p-2 bg-white")
#     def url_link(id1,val1,color):
#         return html.Div(
#                     dbc.Button(val1, id=id1, color=color, external_link=True, target='_blank'))
                