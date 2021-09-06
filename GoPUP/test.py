# import packages 导包
import streamlit as st
import pandas as pd
import gopup as gp
import base64
import plotly.graph_objects as go
import plotly.express as px

token = 'bfbe946025bd49c3604eb8a78b14ffe7'

# 函数 导出数据
def download_csv(df_test):
    '''导出结果'''
    # 这里的 encoding='utf-8_sig' 是为了解决中文乱码
    csv = df_test.to_csv(encoding='utf-8_sig')
    b64 = base64.b64encode(csv.encode(encoding='utf-8_sig')).decode(encoding='utf-8_sig')
    st.markdown('### **⬇️ Download output CSV File **')
    href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download csv file</a>'
    st.markdown(href, unsafe_allow_html=True)




# 应用标题
st.title('在线数据下载')



st.sidebar.markdown('# 说明')
checkbox_introduction = st.sidebar.checkbox('点我查看使用说明')
if checkbox_introduction == False:
    st.markdown('点击左侧按钮可以查看使用说明哟！')
else:
    st.markdown('通过调用 `gopup` 的接口，在网页端进行数据的直接下载，方便使用。')


# 数据目录
data_category = st.sidebar.selectbox('请选择要下载的数据', ('网络指数数据', '中国宏观经济数据', '新经济数据', 'KOL数据', '信息数据', '生活数据', '疫情数据' ))


if data_category == '网络指数数据':
    data_index = st.sidebar.selectbox('你想下载哪种网络指数呢？', ('微博指数数据','百度指数数据','算数数据','谷歌数据','搜狗指数数据'))
    
    if data_index == '微博指数数据':
    
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('微指数是对提及量、阅读量、互动量加权得出的综合指数，更加全面的体现关键词在微博上的热度情况。该应用是获取指定 **词语** 的微博指数。')
        st.markdown('目标地址: https://data.weibo.com/index/newindex')
        st.markdown('## 参数说明')
        st.markdown('**词语**：你想查找的词语的指数，比如`股票`、`电脑`、`CBA`')
        st.markdown('**时间**：')
        st.markdown('1. `1hour`表示当下时间距离一小时前的搜索指数，每5分钟一个数据点 ')
        st.markdown('2. `1day`表示当下时间距离一天前的搜索指数，每1小时一个数据点')
        st.markdown('3. `1month`表示当下时间距离一个月前的搜索指数，每1天一个数据点')
        st.markdown('4. `3month`表示当下时间距离三个月前的搜索指数，每1天一个数据点')

        # 2 参数选择
        st.markdown('# 2 参数选择')
        col1, col2= st.beta_columns(2)
        with col1:
            word = str(st.text_input('词语', value='股票'))
        with col2:
            time_type = str(st.selectbox('时间', ('1hour', '1day', '1month', '3month')))


        # 3 数据展示
        df_result = gp.weibo_index(word=word, time_type=time_type)
        st.markdown('# 3 数据展示')
        df_result

        # 4 数据可视化
        st.markdown('# 4 数据可视化')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_result.index, y=df_result[word] ,mode='lines+markers'))
        fig.update_layout(showlegend=False, title = word + '-' + time_type)
        
        fig

        # 5 导出数据
        st.markdown('# 5 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
           
    elif data_index == '百度指数数据':
        st.text('开发中，敬请期待！')
    elif data_index == '算数数据':
        st.text('开发中，敬请期待！')
    elif data_index == '谷歌数据':
        st.text('开发中，敬请期待！')
    elif data_index == '搜狗指数数据':
        # 1 数据介绍
        st.markdown('已于2021年6月3日0时正式关闭服务，这没办法。详见官方公告 http://zhishu.sogou.com/')
        
        
elif data_category == '中国宏观经济数据':
    data_macro = st.sidebar.selectbox('你想下载哪种中国宏观经济数据呢？', ('中国宏观杠杆率数据', '国内生产总值数据', '居民消费价格指数数据(CPI)', '工业品出厂价格指数(PPI)', '采购经理人指数(PMI)', '存款准备金率数据', '货币供应量数据', '外汇和黄金储备数据', '货币汇率数据','工业增加值增长','财政收入','社会消费品零售总额','信贷数据','外商直接投资数据(FDI)'))
    
    if data_macro == '中国宏观杠杆率数据':
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取中国宏观杠杆率数据,目标地址: http://114.115.232.154:8080/handler/download.ashx')
        
        # 2 数据展示
        df_result = gp.marco_cmlrd()
        st.markdown('# 2 数据展示')
        df_result
        
        # 3 数据可视化
        st.markdown('# 3 数据可视化')
        fig = px.line(df_result, x='年份', y=df_result.columns)
        fig
        
        # 4 导出数据
        st.markdown('# 4 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '国内生产总值数据':
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取中国国内生产总值数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_gdp_quarter()
        st.markdown('# 2 数据展示')
        df_result
        
        # 3 数据可视化
        st.markdown('# 3 数据可视化')
        fig = px.line(df_result, x='季度', y=df_result.columns[[0,1,3,5,7]])
        fig
        
        fig_2 = px.line(df_result, x='季度', y=df_result.columns[[2,4,6,8]])
        fig_2
        # 4 导出数据
        st.markdown('# 4 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '居民消费价格指数数据(CPI)':
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取居民消费价格指数数据(CPI),目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_cpi()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '工业品出厂价格指数(PPI)':
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取工业品出厂价格指数(PPI),目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_pmi()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '采购经理人指数(PMI)':
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取采购经理人指数(PMI),目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_pmi()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '存款准备金率数据':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取存款准备金率数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_rrr()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)            
    elif data_macro == '货币供应量数据':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取货币供应量数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_money_supply()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)         
    elif data_macro == '外汇和黄金储备数据':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取外汇和黄金储备数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_gold_and_foreign_reserves()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '货币汇率数据':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取货币汇率数据,目标地址: https://chl.cn/')
        
        # 2 参数选择
        st.markdown('# 2 参数选择')
        col1, col2= st.beta_columns(2)
        with col1:
            date = str(st.text_input('日期', value='2021-08-16'))
        with col2:
            currency = str(st.selectbox('币种', ('美元', '欧元', '日元', '英镑', '卢布', '韩元', '澳元', '加元', '泰铢', '港币', '台币', '新币')))
        
        # 2 数据展示
        g = gp.pro_api(token = token)
        df_result = g.exchange_rate(date=date, currency=currency)
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '工业增加值增长':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取工业增加值增长,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_industrial_growth()
        st.markdown('# 2 数据展示')
        df_result
        
        # 3 数据可视化
        st.markdown('# 3 数据可视化')
        fig = px.bar(df_result, x='月份', y=df_result.columns)
        fig
        
        
        # 4 导出数据
        st.markdown('# 4 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '财政收入':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取财政收入数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_fiscal_revenue()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '财政收入':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取社会消费品零售总额数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_consumer_total()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)
    elif data_macro == '信贷数据':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取社信贷数据数据,目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_credit_data()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)       
    elif data_macro == '外商直接投资数据(FDI)':     
        # 1 数据介绍
        st.markdown('# 1 数据介绍')
        st.markdown('获取外商直接投资数据(FDI),目标地址: http://datainterface.eastmoney.com')
        
        # 2 数据展示
        df_result = gp.get_fdi_data()
        st.markdown('# 2 数据展示')
        df_result
        
        
        # 3 导出数据
        st.markdown('# 3 导出数据')
        button_export = st.button('点我导出结果')
        if button_export == True:
            download_csv(df_result)