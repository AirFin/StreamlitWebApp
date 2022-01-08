
import streamlit as st
import requests
from lxml import etree

keyword = st.sidebar.text_input('请输入关键词：', '人工智能')
st.sidebar.markdown('---')
st.sidebar.markdown('选择搜索来源')
checkbox_mckinsey = st.sidebar.checkbox('麦肯锡', value=True)
checkbox_bain = st.sidebar.checkbox('贝恩', value=True)
st.sidebar.markdown('---')
button_start = st.sidebar.button('点击搜索')
st.sidebar.markdown('---')

if not button_start:
    st.title('研报一键搜')
    st.write(':sunglasses: 请在侧边栏进行操作，输入关键词，选择搜索来源，点击搜索按钮。')
else:
    if checkbox_mckinsey:
        try:
            URL = f'https://www.mckinsey.com.cn/?s={keyword}'
            UA = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }
            response = requests.get(url=URL, headers=UA).text
            mainpage = etree.HTML(response)
            page_number = mainpage.xpath(
                '//*[@id="posts-container"]/div[2]/a[1]/text()')
            page_number = int(page_number[0])

            for page in range(1, page_number + 1):
                URL = f'https://www.mckinsey.com.cn/page/{str(page)}/?s={keyword}'
                UA = {
                    'user-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                }
                response = requests.get(url=URL, headers=UA).text
                mainpage = etree.HTML(response)

                title = mainpage.xpath(
                    '//*[@id="posts-container"]//article//h2//a/text()')

                link = mainpage.xpath(
                    '//*[@id="posts-container"]//article//h2//a/@href')

                dict_compose = dict(zip(title, link))

                list_results = []
                for title, link in dict_compose.items():
                    result = f'【麦肯锡】[{title}]({link})'
                    st.markdown(result)
        except:
            st.markdown(':sob: 【麦肯锡】网站没有找到相关内容')

    if checkbox_bain:
        try:
            URL = f'https://www.bain.cn/search.php?keyword={keyword}'
            UA = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }
            response = requests.get(url=URL, headers=UA).text
            mainpage = etree.HTML(response)
            page_number = mainpage.xpath(
                '/html/body/section/div[2]/div/div/b/text()')
            page_number = int(page_number[0].split('/')[1])

            for page in range(1, page_number + 1):
                URL = f'https://www.bain.cn/search.php?act=list&keyword={keyword}&&pager={str(page)}'
                UA = {
                    'user-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                }
                response = requests.get(url=URL, headers=UA).text
                mainpage = etree.HTML(response)

                title = mainpage.xpath(
                    '/html/body/section/div[2]/ul//li//h3/text()')

                link = mainpage.xpath(
                    '/html/body/section/div[2]/ul//li//a/@href')

                dict_compose = dict(zip(title, link))

                list_results = []
                for title, link in dict_compose.items():
                    link = f'https://www.bain.cn/{link}'
                    result = f'【贝恩】[{title}]({link})'
                    st.markdown(result)
        except:
            st.write(':sob:  【贝恩】网站没有找到相关内容')
