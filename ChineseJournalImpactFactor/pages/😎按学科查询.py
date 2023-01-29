# import packages
import streamlit as st
import pandas as pd
import plotly.express as px

# preparation work
# import data
# df = pd.read_excel("/app/streamlitwebapp/ChineseJournalImpactFactor/data.xlsx")
df = pd.read_excel("data.xlsx")
# df = pd.read_excel("/app/streamlitwebapp/ChineseJournalImpactFactor/df_xueke.xlsx")
df_xueke = pd.read_excel("df_xueke.xlsx")


option_0 = st.selectbox('你想按学科大类还是学科小类查询？',('学科大类', '学科小类'))

if option_0 == '学科大类':
    option_1 = st.selectbox('你想查询哪个学科大类？',('信息科技', '农业科技', '医药卫生科技', '哲学与人文科学', '基础科学', '工程科技I', '工程科技II', '社会科学I', '社会科学II', '经济与管理科学'))


    # '(2022)复合影响因子', '(2022)综合影响因子'，bar图，分别统计两个因子的频数，不显示标签
    fig_main = px.bar(df[df['专辑名称']==option_1], x='期刊名称', y=['(2022)复合影响因子', '(2022)综合影响因子'],
                    title=f'专辑名称为<b>{option_1}</b>的期刊的复合影响因子与综合影响因子柱状图 2022年数据', barmode='group',)

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


    # 图表显示
    fig_main

    df_show = df[df['专辑名称']==option_1].sort_values(by='(2022)复合影响因子', ascending=False).reset_index(drop=True)
    st.markdown(f'下面是**{option_1}**学科大类的期刊，按**复合影响因子**排序由高到低的数据表')
    df_show
    st.markdown('---')
    df_show_2 = df[df['专辑名称']==option_1].sort_values(by='(2022)综合影响因子', ascending=False).reset_index(drop=True)
    st.markdown(f'下面是**{option_1}**学科大类的期刊，按**综合影响因子**排序由高到低的数据表')
    df_show_2


else:
    option_1 = st.selectbox('首先，你要选择一个学科大类',('信息科技', '农业科技', '医药卫生科技', '哲学与人文科学', '基础科学', '工程科技I', '工程科技II', '社会科学I', '社会科学II', '经济与管理科学'))
    list_option_2 = df_xueke[df_xueke['专辑名称'] == option_1]['专题名称'].to_list()
    option_2 = st.selectbox('然后，你要选择该一个学科大类下的学科小类',(list_option_2))


    # '(2022)复合影响因子', '(2022)综合影响因子'，bar图，分别统计两个因子的频数，不显示标签
    fig_sub = px.bar(df[df['专题名称']==option_2], x='期刊名称', y=['(2022)复合影响因子', '(2022)综合影响因子'],
                    title=f'专题名称为<b>{option_2}</b>的期刊的复合影响因子与综合影响因子柱状图 2022年数据', barmode='group',)

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


    # 图表显示
    fig_sub
    
    df_show = df[df['专题名称']==option_2].sort_values(by='(2022)复合影响因子', ascending=False).reset_index(drop=True)
    st.markdown(f'下面是**{option_2}**学科小类的期刊，按**复合影响因子**排序由高到低的数据表')
    df_show
    st.markdown('---')
    df_show_2 = df[df['专题名称']==option_2].sort_values(by='(2022)综合影响因子', ascending=False).reset_index(drop=True)
    st.markdown(f'下面是**{option_2}**学科小类的期刊，按**综合影响因子**排序由高到低的数据表')
    df_show_2