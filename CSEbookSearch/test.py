
import streamlit as st
import requests
from lxml import etree

keyword = st.sidebar.text_input('请输入关键词：', '人工智能')
st.sidebar.markdown('---')
st.sidebar.markdown('选择搜索来源')
checkbox_bookstack = st.sidebar.checkbox('书栈网', value=True)
checkbox_jikbook = st.sidebar.checkbox('极客图书', value=True)
st.sidebar.markdown('---')
button_start = st.sidebar.button('点击搜索')
st.sidebar.markdown('---')

if not button_start:
    st.title('计算机电子书一键搜')
    st.write(':sunglasses: 请在侧边栏进行操作，输入关键词，选择搜索来源，点击搜索按钮。')
else:
    if checkbox_bookstack:
        try: 
            URL = f'https://www.bookstack.cn/search/result?page=1&tab=book&wd={keyword}'
            UA = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }

            response = requests.get(url=URL, headers=UA).text
            mainpage = etree.HTML(response)


            page_number = mainpage.xpath(
                '/html/body/div/div[1]/div[2]/div/ul[3]/li[6]/a/text()')
            page_number = page_number[0].split('.')[-1]
            page_number = int(page_number[0])


            for page in range(1, page_number + 1):
                URL = f'https://www.bookstack.cn/search/result?page={page}&tab=book&wd={keyword}'
                UA = {
                    'user-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                }
                response = requests.get(url=URL, headers=UA).text
                mainpage = etree.HTML(response)

                title = mainpage.xpath('/html/body/div/div[1]/div[2]/div/ul[2]//div[2]/a/h4/text()')

                link = mainpage.xpath('/html/body/div/div[1]/div[2]/div/ul[2]//div[2]/a/@href')

                link_real = []
                for i in link:
                    j = 'https://www.bookstack.cn' + i
                    link_real.append(j)

                dict_compose = dict(zip(title, link_real))

                list_results = []
                for title, link_real in dict_compose.items():
                    result = f'【书栈网】[{title}]({link_real})'
                    st.markdown(result)
        except:
            st.markdown(':sob: 【书栈网】网站没有找到相关内容')

    if checkbox_jikbook:
        try: 
            URL = f'https://jikbook.com/page/1?s={keyword}'
            UA = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
            }

            response = requests.get(url=URL, headers=UA).text
            mainpage = etree.HTML(response)

            # 获取总页数
            # 注意这里的 /a[last()-1] ，是定位同级倒数第二个元素
            # 为什么要这么写呢？因为倒数第一个元素是“下一页”，而倒数第二个元素是“最后一页”的页数
            page_number = mainpage.xpath(
                '//*[@id="primary"]/nav/div/a[last()-1]/text()')



            page_number = int(page_number[0])


            for page in range(1, page_number + 1):
                URL = f'https://jikbook.com/page/{page}?s={keyword}'
                UA = {
                    'user-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                }
                response = requests.get(url=URL, headers=UA).text
                mainpage = etree.HTML(response)

                title = mainpage.xpath('/html/body/div[1]/div/div/main/div//h2/a/text()')

                link = mainpage.xpath('/html/body/div[1]/div/div/main/div//h2/a/@href')


                dict_compose = dict(zip(title, link))

                list_results = []
                for title, link in dict_compose.items():
                    result = f'【极客图书】[{title}]({link})'
                    st.markdown(result)
        except:
            st.markdown(':sob: 【极客图书】网站没有找到相关内容')