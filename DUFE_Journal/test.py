import streamlit as st
import pandas as pd

# Function to load data

def load_data():
    # file_path 在本地使用的话，路径要修改为本地的绝对路径
    file_path = './DUFE_Journal/data/data.xlsx'
    df_en = pd.read_excel(file_path, sheet_name='英文')
    df_zh = pd.read_excel(file_path, sheet_name='中文')
    return df_en, df_zh

# Load data
df_en, df_zh = load_data()

# Streamlit app layout
st.title("东北财经大学期刊期刊目录查询")

# Input box for journal name
journal_name = st.text_input("请输入要查询的中文或英文期刊全名：")

# Function to search in English dataframe
def search_in_english(journal_name):
    result = df_en[df_en['Journal'].str.contains(journal_name, case=False, na=False)]
    if not result.empty:
        rank = result.iloc[0]['Rank']
        area = result.iloc[0]['Area']
        return f"期刊级别为**{rank}**，期刊领域为**{area}**"
    else:
        return "不在期刊列表里"

# Function to search in Chinese dataframe
def search_in_chinese(journal_name):
    result = df_zh[df_zh['期刊名称'].str.contains(journal_name, case=False, na=False)]
    if not result.empty:
        rank = result.iloc[0]['级别']
        area = result.iloc[0]['主办单位']
        return f"期刊级别为**{rank}**，主办单位为**{area}**"
    else:
        return "不在期刊列表里"

# Perform search in English and then in Chinese if not found
search_result = search_in_english(journal_name)
if search_result == "不在期刊列表里":
    search_result = search_in_chinese(journal_name)

st.markdown(search_result)
