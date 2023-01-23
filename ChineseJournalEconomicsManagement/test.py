# import packages
import streamlit as st
# data processing
import pandas as pd

import plotly.express as px

# 在GitHub上路径要这样写
df_ec_mn = pd.read_excel("/app/streamlitwebapp/ChineseJournalEconomicsManagement/df_ec_mn.xlsx")

st.title('中文经管期刊影响因子速查')

name_journal = st.text_input('请输入要查询的期刊名称', '中国管理科学')

# (2022)复合影响因子 rank pct
df_ec_mn['(2022)复合影响因子 rank pct'] = df_ec_mn['(2022)复合影响因子'].rank(pct=True, ascending=False)
df_ec_mn['(2022)复合影响因子 rank pct'] = df_ec_mn['(2022)复合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

df_ec_mn['(2022)综合影响因子 rank pct'] = df_ec_mn['(2022)综合影响因子'].rank(pct=True, ascending=False)
df_ec_mn['(2022)综合影响因子 rank pct'] = df_ec_mn['(2022)综合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

# '(2022)复合影响因子', '(2022)综合影响因子'，bar图，分别统计两个因子的频数，不显示标签
fig = px.bar(df_ec_mn, x='期刊名称',y=['(2022)复合影响因子', '(2022)综合影响因子'], title='经济与管理科学 (2022)复合影响因子与(2022)综合影响因子 柱状图', barmode='group')

# 不显示X和y轴标签
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)


fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

# 使用绿色突出显示name_journal，并添加箭头和文字
fig.add_annotation(
    x=name_journal,
    y=0,
    text=name_journal,
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-275,
    font=dict(
        family="Courier New, monospace",
        size=15,
        color="green"
    )
)


# 图表显示
fig

# ---分界线---
st.markdown('# :pushpin:期刊信息 ')

df_target = df_ec_mn[df_ec_mn['期刊名称']== name_journal]

st.markdown(':one:' + '2022年复合影响因子：' + '**' + str(df_target['(2022)复合影响因子'].values[0]) + '**' +'，排名百分比：' + '**' +str(df_target['(2022)复合影响因子 rank pct'].values[0])+ '**')
st.markdown(':two:' + '2022年综合影响因子：' + '**' +str(df_target['(2022)综合影响因子'].values[0]) + '**' +'，排名百分比：' + '**' +str(df_target['(2022)综合影响因子 rank pct'].values[0])+ '**')
st.markdown(':three:' + '是否为CSSCI期刊：' + '**' +str(df_target['被中文社会科学引文索引(2021-2022)来源期刊收录'].values[0])+ '**')
st.markdown(':four:' + '是否为CSSCI期刊扩展版：' + '**' +str(df_target['被中文社会科学引文索引(2021-2022)来源期刊(扩展版)收录'].values[0])+ '**')
st.markdown(':five:' + '是否为北大核心期刊：' + '**' +str(df_target['被北京大学《中文核心期刊总览》来源期刊收录'].values[0]) + '**')

st.markdown('所有信息')
df_target


# ---分界线---
st.markdown('# :pushpin:相似等级期刊 学科大类')

# df_ec_mn 按照(2022)复合影响因子 降序排列
df_ec_mn_fh = df_ec_mn.sort_values(by='(2022)复合影响因子', ascending=False).reset_index(drop=True)
# df_ec_mn 按照(2022)综合影响因子 降序排列
df_ec_mn_zh = df_ec_mn.sort_values(by='(2022)综合影响因子', ascending=False).reset_index(drop=True)
# name_journal在 df_ec_mn_fh 的index
index_target_fh = df_ec_mn_fh[df_ec_mn_fh['期刊名称'].isin([name_journal])].index
# name_journal在 df_ec_mn_zh 的上下5行
index_target_zh = df_ec_mn_zh[df_ec_mn_zh['期刊名称'].isin([name_journal])].index

# 这里要进行一个判断，因为如果开头的index小于0就不行，但是结尾的index大于dataframe的长度却可以
if index_target_fh.values[0]-5 < 0:
    index_target_fh_begin = 0
else:
    index_target_fh_begin = index_target_fh.values[0]-5
    
if index_target_zh.values[0]-5 < 0:
    index_target_zh_begin = 0
else:
    index_target_zh_begin = index_target_zh.values[0]-5

st.markdown( '**' +name_journal + '**' + '的学科大类（专辑名称）为' +  '**' + df_target['专辑名称'].values[0]+  '**')
# 2列
col1, col2 = st.columns(2)
with col1:
    st.markdown('**学科大类 复合影响因子前后5名期刊**')
    df_ec_mn_fh.iloc[index_target_fh_begin:index_target_fh.values[0]+6,:]
with col2:
    st.markdown('**学科大类 综合影响因子前后5名期刊**')
    df_ec_mn_zh.iloc[index_target_zh_begin:index_target_zh.values[0]+6,:]

# ---分界线---
st.markdown('# :pushpin:相似等级期刊 学科小类')
st.markdown('---')

# 大函数
def sub_fun(sub):
    # 筛选df_ec_mn_fh 的专题名称包含sub
    df_ec_mn_fh_sub = df_ec_mn_fh[df_ec_mn_fh['专题名称'].str.contains(sub)].reset_index(drop=True)
    # 筛选df_ec_mn_zh 的专题名称包含sub
    df_ec_mn_zh_sub = df_ec_mn_zh[df_ec_mn_zh['专题名称'].str.contains(sub)].reset_index(drop=True)

    # df_ec_mn_sub 的专题名称包含sub
    df_ec_mn_sub = df_ec_mn[df_ec_mn['专题名称'].str.contains(sub)].reset_index(drop=True)
    fig_sub = px.bar(df_ec_mn_sub, x='期刊名称',y=['(2022)复合影响因子', '(2022)综合影响因子'], title= sub+'  (2022)复合影响因子与(2022)综合影响因子 柱状图', barmode='group')
  
    # 不显示X和y轴标签
    fig_sub.update_xaxes(showticklabels=False)
    fig_sub.update_yaxes(showticklabels=False)


    fig_sub.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # 使用绿色突出显示name_journal，并添加箭头和文字
    fig_sub.add_annotation(
        x=name_journal,
        y=0,
        text=name_journal,
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-275,
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="green"
        )
    )


    # 图表显示
    fig_sub
    


    # name_journal在 df_ec_mn_fh_sub 的index
    index_target_fh_sub = df_ec_mn_fh_sub[df_ec_mn_fh_sub['期刊名称'].isin([name_journal])].index
    # name_journal在 df_ec_mn_zh_sub 的index
    index_target_zh_sub = df_ec_mn_zh_sub[df_ec_mn_zh_sub['期刊名称'].isin([name_journal])].index
    
    if index_target_fh_sub.values[0]-5 < 0:
        index_target_fh_begin = 0
    else:
        index_target_fh_begin = index_target_fh_sub.values[0]-5
    
    if index_target_zh_sub.values[0]-5 < 0:
        index_target_zh_begin = 0
    else:
        index_target_zh_begin = index_target_zh_sub.values[0]-5
    
    # 2列
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('**学科小类 复合影响因子前后5名期刊**')
        df_ec_mn_fh_sub.iloc[index_target_fh_begin:index_target_fh_sub.values[0]+6,:]
    with col2:
        st.markdown('**学科小类 综合影响因子前后5名期刊**')
        df_ec_mn_zh_sub.iloc[index_target_zh_begin:index_target_zh_sub.values[0]+6,:]

    st.markdown('---')

# 如果专题名称包含分号，分割成两个专题名称，否则原样输出
if '；' in df_target['专题名称'].values[0]:
    sub = df_target['专题名称'].values[0].split('；')[0]
    sub_2 = df_target['专题名称'].values[0].split('；')[1]
    

    st.info(':one:首先，它属于' + '**' + sub + '**' + '小类' )
    sub_fun(sub)
    st.info(':two:其次，它属于' + '**' + sub_2 + '**' + '小类' )
    sub_fun(sub_2)




else:
    sub = df_target['专题名称'].values[0]
    sub_fun(sub)


st.markdown('感谢使用，更多信息请访问')
st.success('网站：[https://www.sharkfin.top/](https://www.sharkfin.top/)')
st.info('微信公众号：沙克芬 SharkFin')
