# import packages 导包
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64





def data_deal(df_test):
    '''数据处理'''
    s = df_test
    s.iloc[:,0] = pd.to_datetime(s.iloc[:,0] )
    s.index = s.iloc[:,0]
    s = s.iloc[:,1]
    return s 

def function_plot(df_test, detect_model):
    '''示意图'''
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_test.iloc[:,0], y=df_test.iloc[:,1],mode='lines' ,name='data'))
    fig.add_trace(go.Scatter(x=df_test[df_test[detect_model] == 1].iloc[:,0], y=df_test[df_test[detect_model] == 1].iloc[:,1], mode='markers',name='Anomaly'))
    fig.update_layout(showlegend=False, xaxis=dict(rangeslider=dict(visible=True)))
    return fig 


def download_csv(df_test):
    '''导出结果'''
    csv = df_test.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### **⬇️ Download output CSV File **')
    href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download csv file</a>'
    st.markdown(href, unsafe_allow_html=True)



# 应用标题
st.title('基于ADTK的时间序列异常值检测')

# 1 查看简介
st.sidebar.markdown('# 1 使用说明')
checkbox_introduction = st.sidebar.checkbox('点我查看使用说明')
if checkbox_introduction == False:
    st.markdown('点击左侧按钮可以查看使用说明哟！')
else:
    st.markdown('# 1 什么是时间序列？')
    st.markdown('时间序列（英语：time series）是一组按照时间发生先后顺序进行排列的数据点序列，通常一组时间序列的时间间隔为一恒定值（如1秒，5分钟，12小时，7天，1年）。')
    st.markdown('# 2 什么是时间序列中的异常值？')
    st.markdown('时间序列异常值检测时间序列中的异常数值，传统意义上，过大或过小的数据（outlier）都可以被认为是异常值，如下图中红色的点')
    st.markdown('![](https://adtk.readthedocs.io/en/stable/_images/notebooks_demo_6_0.png)')
    st.markdown('此外，根据定义的不同，异常值也不同。比如，我们想找出时间序列中明显数值异常上升的点，如下图中红色区域')
    st.markdown('![](https://adtk.readthedocs.io/en/stable/_images/notebooks_demo_22_0.png)')
    st.markdown('# 3 这个网页怎么使用？')
    st.markdown('在这个网页中，你可以上传文件，通过python中的[ADTK](https://adtk.readthedocs.io/)包进行时间序列异常值检测。文件要求：必须是csv文件，且文件中有仅有两列数据，第一列是时间或日期格式，第二列是数值格式，如下所示')
    data_example={
            "date":['2000/1/1', '2000/1/2', '2000/1/3'],
            "y":[1.155, 1.43, 1.2]
                }
    st.table(data_example)
    
    st.markdown('1.在左侧上传文件试试看吧！如果不上传文件，会用示例数据进行展示。')
    st.markdown('2.可根据不同模型进行参数调整，对应图表会进行改变。')
    st.markdown('3.点击`导出结果`下载检测后的csv文件，会在原有基础上新增一列，异常值点为1，其他为0。')

# 2 上传文件
st.sidebar.markdown('# 2 上传文件')

uploaded_file = st.sidebar.file_uploader('点击按钮上传csv文件，否则用示例数据进行演示')

if uploaded_file is None:
    st.sidebar.markdown('文件上传状态:**未上传**')
else:
    st.sidebar.markdown('文件上传状态:**上传成功**')
    
# 3 选择模型
st.sidebar.markdown('# 3 选择模型')
detect_model = st.sidebar.selectbox('请选择要使用的检测模型', ('ThresholdAD', 'QuantileAD', 'InterQuartileRangeAD', 'GeneralizedESDTestAD' , 'PersistAD'  ))



if detect_model == 'ThresholdAD':
    # 导包
    from adtk.detector import ThresholdAD
    # 如果未上传文件，则使用示例数据进行展示
    if uploaded_file is None:
        df_test = pd.read_csv('./ADTK/data/temperature.csv')

    else:
        df_test = pd.read_csv(uploaded_file)
    
    
    s = data_deal(df_test)
    
    st.markdown('# '+ detect_model)
    
    # 参数设置

    st.markdown('请查看' + detect_model +'的 [官方示例](https://adtk.readthedocs.io/en/stable/notebooks/demo.html#ThresholdAD) 和 [参数说明](https://adtk.readthedocs.io/en/stable/api/detectors.html?highlight=ThresholdAD#adtk.detector.ThresholdAD) ')
    st.markdown('## 参数设置')
    
    col1, col2= st.beta_columns(2)
    with col1:
        ThresholdAD_low = float(st.text_input('low', value=15))
    with col2:
        ThresholdAD_high = float(st.text_input('high', value=30))

    threshold_ad = ThresholdAD( low=ThresholdAD_low, high=ThresholdAD_high)
    anomalies = threshold_ad.detect(s)
    df_test[detect_model] = anomalies.values

    
    # 示意图
    st.markdown('## 示意图')
    fig = function_plot(df_test, detect_model)
    st.plotly_chart(fig)
    
    # 导出结果
    st.markdown('## 导出结果')
    button_export = st.button('点我导出结果')
    if button_export == True:
        download_csv(df_test)


elif detect_model == 'QuantileAD':
    # 导包
    from adtk.detector import QuantileAD
    
    # 如果未上传文件，则使用示例数据进行展示
    if uploaded_file is None:
        df_test = pd.read_csv('./ADTK/data/temperature.csv')

    else:
        df_test = pd.read_csv(uploaded_file)
    
    
    s = data_deal(df_test)
    
    st.markdown('# '+ detect_model)
    
    # 参数设置

    st.markdown('请查看' + detect_model +'的 [官方示例](https://adtk.readthedocs.io/en/stable/notebooks/demo.html#QuantileAD) 和 [参数说明](https://adtk.readthedocs.io/en/stable/api/detectors.html?highlight=QuantileAD#adtk.detector.QuantileAD) ')
    st.markdown('## 参数设置')
    
    col1, col2= st.beta_columns(2)
    with col1:
        QuantileAD_low = float(st.text_input('low', value=0.01))
    with col2:
        QuantileAD_high = float(st.text_input('high', value=0.99))
    
    quantile_ad  = QuantileAD( low=QuantileAD_low, high=QuantileAD_high)
    anomalies = quantile_ad.fit_detect(s)
    df_test[detect_model] = anomalies.values
    

    # 示意图
    st.markdown('## 示意图')
    fig = function_plot(df_test, detect_model)
    st.plotly_chart(fig)
    
    # 导出结果
    st.markdown('## 导出结果')
    button_export = st.button('点我导出结果')
    if button_export == True:
        download_csv(df_test)

elif detect_model == 'InterQuartileRangeAD':
    # 导包
    from adtk.detector import InterQuartileRangeAD
    
    # 如果未上传文件，则使用示例数据进行展示
    if uploaded_file is None:
        df_test = pd.read_csv('./ADTK/data/temperature.csv')

    else:
        df_test = pd.read_csv(uploaded_file)
    
    
    s = data_deal(df_test)
    
    st.markdown('# '+ detect_model)
    
    # 参数设置

    st.markdown('请查看' + detect_model +'的 [官方示例](https://adtk.readthedocs.io/en/stable/notebooks/demo.html#InterQuartileRangeAD) 和 [参数说明](https://adtk.readthedocs.io/en/stable/api/detectors.html?highlight=QuantileAD#adtk.detector.InterQuartileRangeAD) ')
    st.markdown('## 参数设置')
    
    InterQuartileRangeAD_c  =  float(st.text_input('c', value=1.5))
    
    iqr_ad = InterQuartileRangeAD(c=InterQuartileRangeAD_c)
    anomalies = iqr_ad.fit_detect(s)
    df_test[detect_model] = anomalies.values
    

    # 示意图
    st.markdown('## 示意图')
    fig = function_plot(df_test, detect_model)
    st.plotly_chart(fig)
    
    # 导出结果
    st.markdown('## 导出结果')
    button_export = st.button('点我导出结果')
    if button_export == True:
        download_csv(df_test)

elif detect_model == 'GeneralizedESDTestAD':
    # 导包
    from adtk.detector import GeneralizedESDTestAD
    
    # 如果未上传文件，则使用示例数据进行展示
    if uploaded_file is None:
        df_test = pd.read_csv('./ADTK/data/temperature.csv')

    else:
        df_test = pd.read_csv(uploaded_file)
    
    
    s = data_deal(df_test)
    
    st.markdown('# '+ detect_model)
    
    # 参数设置

    st.markdown('请查看' + detect_model +'的 [官方示例](https://adtk.readthedocs.io/en/stable/notebooks/demo.html#GeneralizedESDTestAD) 和 [参数说明](https://adtk.readthedocs.io/en/stable/api/detectors.html?highlight=QuantileAD#adtk.detector.GeneralizedESDTestAD) ')
    st.markdown('## 参数设置')
    
    GeneralizedESDTestAD_alpha  =  float(st.text_input('alpha', value=0.3))
    
    esd_ad = GeneralizedESDTestAD(alpha=GeneralizedESDTestAD_alpha)
    anomalies = esd_ad.fit_detect(s)
    df_test[detect_model] = anomalies.values
    

    # 示意图
    st.markdown('## 示意图')
    fig = function_plot(df_test, detect_model)
    st.plotly_chart(fig)
    
    # 导出结果
    st.markdown('## 导出结果')
    button_export = st.button('点我导出结果')
    if button_export == True:
        download_csv(df_test)
elif detect_model == 'PersistAD':
    # 导包
    from adtk.detector import PersistAD
    
    # 如果未上传文件，则使用示例数据进行展示
    if uploaded_file is None:
        df_test = pd.read_csv('./ADTK/data/price_short.csv')

    else:
        df_test = pd.read_csv(uploaded_file)
    
    
    s = data_deal(df_test)
    
    st.markdown('# '+ detect_model)
    
    # 参数设置

    st.markdown('请查看' + detect_model +'的 [官方示例](https://adtk.readthedocs.io/en/stable/notebooks/demo.html#PersistAD) 和 [参数说明](https://adtk.readthedocs.io/en/stable/api/detectors.html?highlight=PersistAD#adtk.detector.PersistAD) ')
    st.markdown('## 参数设置')
    
    col1, col2= st.beta_columns(2)
    with col1:
        PersistAD_window = int(st.text_input('window', value=1))
    with col2:
        PersistAD_c = float(st.text_input('c', value=3.0))
    
    col3, col4 = st.beta_columns(2)
    with col3:
        PersistAD_side = st.selectbox('side',('both', 'positive', 'negative') )
    with col4:
        PersistAD_min_periods = int(st.text_input('min_periods', value='1'))

    PersistAD_agg = st.selectbox('agg',( 'median', 'mean') )
        
        
    persist_ad = PersistAD(window=PersistAD_window, c=PersistAD_c, side=PersistAD_side, min_periods=PersistAD_min_periods, agg=PersistAD_agg)
    anomalies = persist_ad.fit_detect(s)
    df_test[detect_model] = anomalies.values
    

    # 示意图
    st.markdown('## 示意图')
    fig = function_plot(df_test, detect_model)
    st.plotly_chart(fig)
    
    # 导出结果
    st.markdown('## 导出结果')
    button_export = st.button('点我导出结果')
    if button_export == True:
        download_csv(df_test)
        


    
