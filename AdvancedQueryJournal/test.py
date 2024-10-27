import streamlit as st
import pandas as pd
import os

def process_journal_list_wos(journal_list):
    # 将Journal列变成一个列表，并使用英文双引号进行包裹
    journal_list = journal_list['Journal'].apply(lambda x: f'"{x}"').tolist()
    # 使用 ' OR ' 进行连接，得到最终的字符串
    str_result_wos = ' OR '.join(journal_list)
    # 得到新的字符串，格式为 SO = ( str_result_wos )
    result_string = f"SO = ( {str_result_wos} )"
    return result_string

def process_journal_list_cnki(journal_list):
    # 将期刊名称列变成一个列表，并使用英文单引号进行包裹
    journal_list = journal_list['Journal'].apply(lambda x: f"'{x}'").tolist()
    # 使用 ' + ' 进行连接，得到最终的字符串
    str_result_cnki = ' + '.join(journal_list)
    # 得到新的字符串，格式为 ( LY = str_result_cnki )
    result_string_cnki = f"( LY = {str_result_cnki} )"
    return result_string_cnki

# Streamlit应用程序
st.title('高级检索的文献来源组合工具')

st.header('说明')
st.markdown('上传一个Excel或CSV文件，包含1列（列名为**Journal**），内容是英文期刊名称或中文期刊名称。应用会将其组合为Web of Science或知网可用的检索语句，即查找指定期刊的文献。')

# Web of Science处理
st.header('Web of Science')
uploaded_file_wos = st.file_uploader("在此上传文件", type=["xls", "xlsx", "csv"], key='wos')

if uploaded_file_wos is not None:
    # 判断文件类型并读取
    if uploaded_file_wos.name.endswith('csv'):
        journal_list_wos = pd.read_csv(uploaded_file_wos)
    elif uploaded_file_wos.name.endswith('xlsx') or uploaded_file_wos.name.endswith('xls'):
        journal_list_wos = pd.read_excel(uploaded_file_wos)
    else:
        st.error("不支持的文件格式！")
        st.stop()

    # 确保文件包含所需的列
    if 'Journal' not in journal_list_wos.columns:
        st.error("上传的文件必须包含名为'Journal'的列！")
    else:
        # 处理期刊列表
        result_string_wos = process_journal_list_wos(journal_list_wos)

        # 将结果保存到txt文件
        output_file_wos = 'result.txt'
        with open(output_file_wos, 'w') as f:
            f.write(result_string_wos)

        # 提供下载
        with open(output_file_wos, 'rb') as f:
            st.download_button(
                label="下载Web of Science处理后的期刊列表",
                data=f,
                file_name=output_file_wos,
                mime='text/plain'
            )

        # 删除生成的txt文件，防止临时文件堆积
        os.remove(output_file_wos)

# 知网处理
st.header('知网')
uploaded_file_cnki = st.file_uploader("在此上传文件", type=["xls", "xlsx", "csv"], key='cnki')

if uploaded_file_cnki is not None:
    # 判断文件类型并读取
    if uploaded_file_cnki.name.endswith('csv'):
        journal_list_cnki = pd.read_csv(uploaded_file_cnki)
    elif uploaded_file_cnki.name.endswith('xlsx') or uploaded_file_cnki.name.endswith('xls'):
        journal_list_cnki = pd.read_excel(uploaded_file_cnki)
    else:
        st.error("不支持的文件格式！")
        st.stop()

    # 确保文件包含所需的列
    if 'Journal' not in journal_list_cnki.columns:
        st.error("上传的文件必须包含名为'Journal'的列！")
    else:
        # 处理期刊列表
        result_string_cnki = process_journal_list_cnki(journal_list_cnki)

        # 将结果保存到txt文件
        output_file_cnki = 'result_cnki.txt'
        with open(output_file_cnki, 'w') as f:
            f.write(result_string_cnki)

        # 提供下载
        with open(output_file_cnki, 'rb') as f:
            st.download_button(
                label="下载知网处理后的期刊列表",
                data=f,
                file_name=output_file_cnki,
                mime='text/plain'
            )

        # 删除生成的txt文件，防止临时文件堆积
        os.remove(output_file_cnki)
