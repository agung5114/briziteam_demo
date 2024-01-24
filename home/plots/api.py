# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker

# # #define sqlite connection url
# # SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

# # # create new engine instance 
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # # create sessionmaker 
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base()

# import pandas as pd
# # from sqlalchemy import text

# # def index():
# #   query1 = 'select * from keywords'
# #   # sql with pandas
# # #  dff = pd.read_sql_query(query1,conn)
# #   sql = text(query1)
# #   with engine.connect() as conn:
# #     result = conn.execute(sql).fetchall()
# #   dd = []
# #   for i in result:
# #       dd.append(i)
# #   dff = pd.DataFrame(dd)
# #   return {"data":dff.to_dict(orient='list')}
#   ## raw sql with sqlalchemy
# #  return "<p>Hello, World!</p>"

# import json
# import requests
# # @app.route("/jobagg/<keyword>/<start_date>/<end_date>")
# def get_jobagg(keyword: str, start_date: str, end_date:str):
#     data = requests.get(f'https://eksis.tech/tweet-list/{keyword}/{start_date}/{end_date}')\
#                          .json()['data']
#     df = pd.read_json(data)
#     return df

# def get_toptweets(keyword: str, start_date: str, end_date:str):
#     data = requests.get(f'https://eksis.tech/tweet-list/{keyword}/{start_date}/{end_date}')\
#                          .json()['data']
#     df = pd.read_json(data)
#     return df


# # df = get_jobagg('kemenkeu', '2023-10-01', '2023-10-10')
# # data = df.head()
# # # data = requests.get('https://eksis.tech/tweet-list/kemenkeu/2023-10-01/2023-10-10')\
# # #                          .json()['data']
# # print(data)