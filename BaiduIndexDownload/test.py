# import packages
import streamlit as st
import time
import pandas as pd
from qdata.baidu_index import get_search_index
from qdata.baidu_index import get_feed_index
from qdata.baidu_index import get_news_index
from qdata.baidu_index.common import split_keywords
from qdata.baidu_index import PROVINCE_CODE
import datetime
import plotly.express as px

# 下载文件相关函数
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')



# title
st.title('百度指数一键下载')

# imput widgets

keyword1 = st.sidebar.text_input('第一个词','火锅')
keyword2 = st.sidebar.text_input('第二个词','汇率')
keyword3 = st.sidebar.text_input('第三个词')
keyword4 = st.sidebar.text_input('第四个词')
keyword5 = st.sidebar.text_input('第五个词')

keywords_list = [[keyword1], [keyword2], [keyword3], [keyword4], [keyword5]]

province = st.text_input('请输入地区名称（如：全国、北京、广东、香港）', '全国')
if province == '全国':
    province = 0
else:
    province = PROVINCE_CODE[province]


col1, col2 = st.columns(2)
with col1:
    start_dt = st.date_input('开始日期', datetime.date(2022, 8, 20),help='最早可以是2011年')
    start_dt = str(start_dt)
with col2:
    end_dt = st.date_input('结束日期', datetime.date(2022, 8, 24),help='当天的可能无法获取；结束日期要晚于开始日期')
    end_dt = str(end_dt)



time_sleepping = st.number_input('休息时间（每次爬取间隔时间，单位：秒，建议设置大一些，但爬取时间会较慢）', 0.5, step=0.5 )


options = st.multiselect(
     '请选择要查询的指数（可多选）',
     ['搜索指数', '资讯指数', '媒体指数'],
     ['搜索指数'],
     help='一次最好只选一个，不然可能会很慢或崩溃')


cookie = 'BDUSS=' + st.text_input('百度cookie' , type='password', help='它是什么？应如何获取？请搜索一下ヾ(◍°∇°◍)ﾉﾞ')


if st.button('准备好了，开始获取！'):
    try:

        if '搜索指数' in options:
            df_search_index = pd.DataFrame(columns=['keyword','province','type','date','index'])

            for keywords in split_keywords(keywords_list):
                for info in get_search_index(keywords_list = keywords,
                                                start_date = start_dt,
                                                end_date = end_dt,
                                                area  = province,
                                                cookies = cookie):


                    data_each_day = {
                        'keyword':info['keyword'][0],
                        'province': province,
                        'type': info['type'],
                        'date': info['date'],
                        'index': info['index']
                    }

                    # append data_each_day to data_each_day as rows
                    df_search_index = df_search_index.append(data_each_day, ignore_index=True)
                    # df_search_index['keyword'] = df_search_index['keyword'].str.strip('[').strip('}')

                    # 休息，休息一下~
                    time.sleep(time_sleepping)

            # 展示一下表格
            st.markdown('## 搜索指数')
            df_search_index
            csv = convert_df(df_search_index)
            st.download_button(label="点我下载CSV文件", data=csv, file_name='df_search_index.csv',mime='text/csv',)
            if province == 0:
                province = '全国'
            else:
                pass
            fig_search_index = px.line(df_search_index,
                                       x='date',
                                       y='index',
                                       facet_col='type',
                                       color='keyword',
                                       title=f'百度指数-{province}地区')
            # 展示一下图表
            fig_search_index
            # 分割线
            st.markdown('---')







        if '资讯指数' in options:
            df_feed_index = pd.DataFrame(columns=['keyword','province','type','date','index'])

            for keywords in split_keywords(keywords_list):
                for info in get_feed_index(keywords_list = keywords,
                                                start_date = start_dt,
                                                end_date = end_dt,
                                                area  = province,
                                                cookies = cookie):


                    data_each_day = {
                        'keyword':info['keyword'][0],
                        'province': province,
                        'type': info['type'],
                        'date': info['date'],
                        'index': info['index']
                    }

                    # append data_each_day to data_each_day as rows
                    df_feed_index = df_feed_index.append(data_each_day, ignore_index=True)
                    # df_search_index['keyword'] = df_search_index['keyword'].str.strip('[').strip('}')

                    # 休息，休息一下~
                    time.sleep(time_sleepping)


            # 展示一下表格
            st.markdown('## 资讯指数')
            df_feed_index
            csv = convert_df(df_feed_index)
            st.download_button(label="点我下载CSV文件", data=csv, file_name='df_feed_index.csv',mime='text/csv',)
            if province == 0:
                province = '全国'
            else:
                pass
            fig_feed_index = px.line(df_feed_index,
                                       x='date',
                                       y='index',
                                       facet_col='type',
                                       color='keyword',
                                       title=f'资讯指数-{province}地区')
            # 展示一下图表
            fig_feed_index
            # 分割线
            st.markdown('---')



        if '媒体指数' in options:
            df_news_index = pd.DataFrame(columns=['keyword','province','type','date','index'])

            for keywords in split_keywords(keywords_list):
                for info in get_news_index(keywords_list = keywords,
                                                start_date = start_dt,
                                                end_date = end_dt,
                                                area  = province,
                                                cookies = cookie):


                    data_each_day = {
                        'keyword':info['keyword'][0],
                        'province': province,
                        'type': info['type'],
                        'date': info['date'],
                        'index': info['index']
                    }

                    # append data_each_day to data_each_day as rows
                    df_news_index = df_news_index.append(data_each_day, ignore_index=True)
                    # df_search_index['keyword'] = df_search_index['keyword'].str.strip('[').strip('}')

                    # 休息，休息一下~
                    time.sleep(time_sleepping)

            # 展示一下表格
            st.markdown('## 媒体指数')
            df_news_index
            csv = convert_df(df_news_index)
            st.download_button(label="点我下载CSV文件", data=csv, file_name='df_news_index.csv',mime='text/csv',)
            if province == 0:
                province = '全国'
            else:
                pass
            fig_news_index = px.line(df_news_index,
                                       x='date',
                                       y='index',
                                       facet_col='type',
                                       color='keyword',
                                       title=f'资讯指数-{province}地区')
            # 展示一下图表
            fig_news_index
            # 分割线
            st.markdown('---')

    except:
        st.warning('请填写正确的cookie；或者爬取太频繁，请增加休息时间。')

else:
    pass
