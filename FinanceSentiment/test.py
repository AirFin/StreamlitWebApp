# import packages 导包
import streamlit as st
import pandas as pd

import base64
import plotly.graph_objects as go
import plotly.express as px

from autoscraper import AutoScraper
import re




dfcf_scraper = None
dfcf_scraper = AutoScraper()
dfcf_scraper.load('model.json')


df_all = pd.DataFrame()


# 如果是2就是第一页，如果是3，就是前两页
for n in range(1, 3):
    url = f'http://guba.eastmoney.com/list,605258_{n}.html'

    result = dfcf_scraper.get_result_similar(url=url, grouped=True)
    
    df = pd.DataFrame(result)
    df = df.iloc[:,[0,1,-1]]
    
    df_all = pd.concat([df_all, df])


df_all.rename(columns={df_all.columns[0]:'title',
                       df_all.columns[1]:'writer',
                       df_all.columns[2]:'time'
                      }, 
              inplace=True)

# 重设索引，不重设索引的话，索引会：每一页都是0-79
df_all.reset_index(inplace=True)
df_all.drop(columns=['index'], inplace=True)

df_all
