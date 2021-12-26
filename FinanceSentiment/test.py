# import packages 导包
import streamlit as st
import pandas as pd
from snownlp import SnowNLP
import base64
# import plotly.graph_objects as go
import plotly.express as px

from autoscraper import AutoScraper
import re

st.title('投资者情绪监测看板')

st.markdown('# 0 简介')
st.markdown(
    '爬取[东方财富股吧](https://guba.eastmoney.com/)中每个帖子的信息，并使用[snownlp](https://github.com/isnowfy/snownlp)对帖子标题进行情感分析，最后汇总为日数据进行数据展示。'
)


col1, col2 = st.columns(2)
with col1:
    asset_code = st.text_input('请输入资产代码', '605258')
with col2:
    pages = st.text_input('请输入要爬取的页数', '1')

pages = int(pages)

checkbox_start = st.checkbox('点我继续！')
if checkbox_start is False:
    st.markdown('注意，页数不要太多，反复多次点击很可能会拒绝访问。')
else:
    st.markdown('# 1 数据展示')
    '''这部分是用autoscraper爬取的'''

    dfcf_scraper = None
    dfcf_scraper = AutoScraper()
    # 加载爬取规则
    # dfcf_scraper.load('/app/streamlitwebapp/FinanceSentiment/model.json')
    dfcf_scraper.load('model.json')

    df_all = pd.DataFrame()

    # 如果是2就是第一页，如果是3，就是前两页
    year = 2022
    for page in range(1, pages + 1):
        url = 'https://guba.eastmoney.com/list,' + asset_code + '_' + str(
            page) + '.html'

        result = dfcf_scraper.get_result_similar(url=url, grouped=True)

        df = pd.DataFrame(result)
        df = df.iloc[:, [0, 1, -1]]

        df_all = pd.concat([df_all, df])

    df_all.rename(columns={
        df_all.columns[0]: 'title',
        df_all.columns[1]: 'writer',
        df_all.columns[2]: 'time'
    },
                inplace=True)

    # 重设索引，不重设索引的话，索引会：每一页都是0-79
    df_all.reset_index(inplace=True)
    df_all.drop(columns=['index'], inplace=True)

    # 格式化日期
    df_all["time_before"] = df_all["time"].shift(1)

    # 删除第一行，因为经过shift后，time_before的第一行为NaN
    df_all.drop(index=[0], inplace=True)

    year = 2021
    df_date = pd.DataFrame(columns=['date'])
    for row in df_all.iterrows():
        this_line = row[1]['time']
        before_line = row[1]['time_before']

        this_line_month = re.search(r"(\d{2})", this_line)
        this_line_month = this_line_month.group(0)

        before_line_month = re.search(r"(\d{2})", before_line)
        before_line_month = before_line_month.group(0)

        month_and_day = re.search(r"\d{2}-\d{2}", this_line)
        month_and_day = month_and_day.group(0)

        if this_line_month == "12" and before_line_month == "01":
            year = year - 1
        else:
            year = year

        formatted_date = str(year) + "-" + month_and_day

        df_date = df_date.append({'date': formatted_date}, ignore_index=True)

    df_all['date'] = df_date['date']

    # 删除不需要的两列
    del df_all['time']
    del df_all['time_before']

    # 删除最后一行，因为date的最后一行为NaN
    df_all.drop(df_all.tail(1).index, inplace=True)


    # 使用snownlp对title进行情感分析
    def sentiment_snownlp(text):
        result = SnowNLP(text).sentiments
        return result


    df_all['sentiment_snownlp'] = df_all['title'].apply(sentiment_snownlp)

    df_all
    df_all.to_csv('data.csv', index=False)

    st.markdown('---')


    # 函数 导出数据
    def download_csv(df_test):
        '''导出结果'''
        # 这里的 encoding='utf-8_sig' 是为了解决中文乱码
        csv = df_test.to_csv(encoding='utf-8_sig')
        b64 = base64.b64encode(
            csv.encode(encoding='utf-8_sig')).decode(encoding='utf-8_sig')
        st.markdown('### **⬇️ Download output CSV File **')
        href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download csv file</a>'
        st.markdown(href, unsafe_allow_html=True)


    button_export = st.button('点我导出结果')
    if button_export is True:
        download_csv(df_all)

    st.markdown('# 2 数据可视化展示')
    df_plot_mean = df_all.groupby(by='date').mean()
    df_plot_std = df_all.groupby(by='date').std()

    fig_mean = px.line(df_plot_mean,
                    x=df_plot_mean.index,
                    y='sentiment_snownlp',
                    error_y=df_plot_std['sentiment_snownlp'] * 0.1,
                    title='日均情感走势图')

    fig_mean.add_hline(y=0.5, line_width=3, line_dash="solid", line_color="Brown")

    select_text_show = st.checkbox('显示每日数值')
    if select_text_show is True:
        fig_mean = px.line(df_plot_mean,
                        x=df_plot_mean.index,
                        y='sentiment_snownlp',
                        text='sentiment_snownlp',
                        error_y=df_plot_std['sentiment_snownlp'] * 0.1,
                        title='日均情感走势图')
        fig_mean.update_traces(texttemplate='%{text:.2f}',
                            textposition='bottom right',
                            textfont=dict(
                                family="sans serif",
                                size=15,
                            ))

    st.plotly_chart(fig_mean, use_container_width=True)
