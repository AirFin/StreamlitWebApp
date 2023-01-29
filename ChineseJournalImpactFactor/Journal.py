# import packages
import streamlit as st
import pandas as pd
import plotly.express as px

# preparation work
# import data
df = pd.read_excel("/app/streamlitwebapp/ChineseJournalImpactFactor/data.xlsx")
# df = pd.read_excel("data.xlsx")

# 大函数
def main_fun(main):
    df_zhuanji = df[df['专辑名称'].str.contains(main)].reset_index(drop=True)


    # '(2022)复合影响因子', '(2022)综合影响因子'，bar图，分别统计两个因子的频数，不显示标签
    fig_main = px.bar(df_zhuanji, x='期刊名称', y=['(2022)复合影响因子', '(2022)综合影响因子'],
                    title=f'专辑名称为<b>{main}</b>的期刊的复合影响因子与综合影响因子柱状图 2022年数据', barmode='group',)

    # 不显示X和y轴标签
    fig_main.update_xaxes(showticklabels=False)
    fig_main.update_yaxes(showticklabels=False)

    fig_main.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # 使用绿色突出显示name_journal，并添加箭头和文字
    fig_main.add_annotation(
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
    fig_main



    # (2022)复合影响因子 rank pct
    df_zhuanji['(2022)复合影响因子 rank pct'] = df_zhuanji['(2022)复合影响因子'].rank(pct=True, ascending=False)
    df_zhuanji['(2022)复合影响因子 rank pct'] = df_zhuanji['(2022)复合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

    df_zhuanji['(2022)综合影响因子 rank pct'] = df_zhuanji['(2022)综合影响因子'].rank(pct=True, ascending=False)
    df_zhuanji['(2022)综合影响因子 rank pct'] = df_zhuanji['(2022)综合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

    # df_zhuanji 按照(2022)复合影响因子 降序排列
    df_zhuanji_fh = df_zhuanji.sort_values(by='(2022)复合影响因子', ascending=False).reset_index(drop=True)
    # df_zhuanji 按照(2022)综合影响因子 降序排列
    df_zhuanji_zh = df_zhuanji.sort_values(by='(2022)综合影响因子', ascending=False).reset_index(drop=True)

    # name_journal在 df_zhuanji_fh 的index
    index_target_fh_main = df_zhuanji_fh[df_zhuanji_fh['期刊名称'].isin([name_journal])].index
    # name_journal在 df_zhuanji_zh 的index
    index_target_zh_main = df_zhuanji_zh[df_zhuanji_zh['期刊名称'].isin([name_journal])].index

    if index_target_fh_main.values[0]-5 < 0:
        index_target_fh_begin = 0
    else:
        index_target_fh_begin = index_target_fh_main.values[0]-5

    if index_target_zh_main.values[0]-5 < 0:
        index_target_zh_begin = 0
    else:
        index_target_zh_begin = index_target_zh_main.values[0]-5


    st.markdown(':star:' + '2022年复合影响因子：' + '**' + str(df_zhuanji[df_zhuanji['期刊名称']==name_journal]['(2022)复合影响因子'].values[0]) + '**' +f'，在**{main}**大类的排名百分比：' + '**' +str(df_zhuanji[df_zhuanji['期刊名称']==name_journal]['(2022)复合影响因子 rank pct'].values[0])+ '**')
    st.markdown(':star:' + '2022年综合影响因子：' + '**' +str(df_zhuanji[df_zhuanji['期刊名称']==name_journal]['(2022)综合影响因子'].values[0]) + '**' +f'，在**{main}**大类的排名百分比：' + '**' +str(df_zhuanji[df_zhuanji['期刊名称']==name_journal]['(2022)综合影响因子 rank pct'].values[0])+ '**')
    # 2列
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'该期刊在**{main}**学科大类中复合影响因子前后5名的期刊')
        df_zhuanji_zh.iloc[index_target_fh_begin:index_target_fh_main.values[0]+6,:]
    with col2:
        st.markdown(f'该期刊在**{main}**学科大类中综合影响因子前后5名的期刊')
        df_zhuanji_zh.iloc[index_target_zh_begin:index_target_zh_main.values[0]+6,:]
    st.markdown('---')
    

def sub_fun(sub):
    df_zhuanti = df[df['专题名称'].str.contains(sub)].reset_index(drop=True)


    # '(2022)复合影响因子', '(2022)综合影响因子'，bar图，分别统计两个因子的频数，不显示标签
    fig_sub = px.bar(df_zhuanti, x='期刊名称', y=['(2022)复合影响因子', '(2022)综合影响因子'],
                    title=f'专题名称为<b>{sub}</b>的期刊的复合影响因子与综合影响因子柱状图 2022年数据', barmode='group',)

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



    # (2022)复合影响因子 rank pct
    df_zhuanti['(2022)复合影响因子 rank pct'] = df_zhuanti['(2022)复合影响因子'].rank(pct=True, ascending=False)
    df_zhuanti['(2022)复合影响因子 rank pct'] = df_zhuanti['(2022)复合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

    df_zhuanti['(2022)综合影响因子 rank pct'] = df_zhuanti['(2022)综合影响因子'].rank(pct=True, ascending=False)
    df_zhuanti['(2022)综合影响因子 rank pct'] = df_zhuanti['(2022)综合影响因子 rank pct'].map(lambda x: format(x,'.2%'))

    # df_zhuanti 按照(2022)复合影响因子 降序排列
    df_zhuanti_fh = df_zhuanti.sort_values(by='(2022)复合影响因子', ascending=False).reset_index(drop=True)
    # df_zhuanti 按照(2022)综合影响因子 降序排列
    df_zhuanti_zh = df_zhuanti.sort_values(by='(2022)综合影响因子', ascending=False).reset_index(drop=True)

    # name_journal在 df_zhuanti_fh 的index
    index_target_fh_sub = df_zhuanti_fh[df_zhuanti_fh['期刊名称'].isin([name_journal])].index
    # name_journal在 df_zhuanti_zh 的index
    index_target_zh_sub = df_zhuanti_zh[df_zhuanti_zh['期刊名称'].isin([name_journal])].index

    if index_target_fh_sub.values[0]-5 < 0:
        index_target_fh_begin = 0
    else:
        index_target_fh_begin = index_target_fh_sub.values[0]-5

    if index_target_zh_sub.values[0]-5 < 0:
        index_target_zh_begin = 0
    else:
        index_target_zh_begin = index_target_zh_sub.values[0]-5


    st.markdown(':star:' + '2022年复合影响因子：' + '**' + str(df_zhuanti[df_zhuanti['期刊名称']==name_journal]['(2022)复合影响因子'].values[0]) + '**' +f'，在**{sub}**小类的排名百分比：' + '**' +str(df_zhuanti[df_zhuanti['期刊名称']==name_journal]['(2022)复合影响因子 rank pct'].values[0])+ '**')
    st.markdown(':star:' + '2022年综合影响因子：' + '**' +str(df_zhuanti[df_zhuanti['期刊名称']==name_journal]['(2022)综合影响因子'].values[0]) + '**' +f'，在**{sub}**小类的排名百分比：' + '**' +str(df_zhuanti[df_zhuanti['期刊名称']==name_journal]['(2022)综合影响因子 rank pct'].values[0])+ '**')
    # 2列
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'该期刊在**{sub}**学科小类中复合影响因子前后5名的期刊')
        df_zhuanti_zh.iloc[index_target_fh_begin:index_target_fh_sub.values[0]+6,:]
    with col2:
        st.markdown(f'该期刊在**{sub}**学科小类中综合影响因子前后5名的期刊')
        df_zhuanti_zh.iloc[index_target_zh_begin:index_target_zh_sub.values[0]+6,:]
    st.markdown('---')



st.title('中文期刊影响因子速查及可视化')
st.markdown('这个在线应用可以帮助你快速查询中文期刊的影响因子，以及在其所属学科大类和学科小类中的排名情况，并显示和其影响因子相似的期刊。')

st.markdown('# 在这里输入:point_down:')
name_journal = st.text_input('请输入要查询的中文期刊名称：', '遥感学报')
df_target = df[df['期刊名称']== name_journal]

st.markdown('# 期刊基本信息')
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(':old_key:' + '是否为CSSCI期刊：' + '**' +str(df_target['被中文社会科学引文索引(2021-2022)来源期刊收录'].values[0])+ '**')
with col2:
    st.markdown(':old_key:' + '是否为CSSCI期刊扩展版：' + '**' +str(df_target['被中文社会科学引文索引(2021-2022)来源期刊(扩展版)收录'].values[0])+ '**')
with col3:
    st.markdown(':old_key:' + '是否为北大核心期刊：' + '**' +str(df_target['被北京大学《中文核心期刊总览》来源期刊收录'].values[0]) + '**')

st.text('下面为该期刊的所有详细信息')
df_target

st.markdown('# 在学科大类下的影响因子排名')
# 如果专辑名称包含分号，分割成两个专辑名称，否则原样输出
if '；' in df_target['专辑名称'].values[0]:
    main = df_target['专辑名称'].values[0].split('；')[0]
    main_2 = df_target['专辑名称'].values[0].split('；')[1]
    
    st.info(':one:首先，它属于' + '**' + main + '**' + '大类' )
    main_fun(main)
    st.info(':two:其次，它属于' + '**' + main_2 + '**' + '大类' )
    main_fun(main_2)
else:
    main = df_target['专辑名称'].values[0]
    main_fun(main)


st.markdown('# 在学科小类下的影响因子排名')
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

