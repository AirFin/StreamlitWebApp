import streamlit as st
import pandas as pd
from graphviz import Digraph

# 定义数据合并函数
def merge_and_clean(left_df, right_dfs, left_on, right_ons):
    current_df = left_df
    for right_df, right_on in zip(right_dfs, right_ons):
        current_df = pd.merge(current_df, right_df, how='left', left_on=left_on, right_on=right_on)
        # 删除right_on中不在left_on中的列
        cols_to_drop = [col for col in right_on if col not in left_on]
        current_df.drop(cols_to_drop, axis=1, inplace=True)
    return current_df

# 设置页面标题
st.title("中国上市企业数据合并工具")

# 在侧边栏上传文件
with st.sidebar:
    st.header("上传数据文件")
    uploaded_file_1 = st.file_uploader(":one:上传左侧表格 (1个)", type=["xlsx", "csv"])
    uploaded_files_2 = st.file_uploader(":two:上传要右侧表格（多个）", type=["xlsx", "csv"], accept_multiple_files=True)

# 检查文件上传状态
if not uploaded_file_1 and not uploaded_files_2:
    # 展示提示文字
    st.markdown("请在侧边栏上传数据文件进行合并，多个右侧表格会按照一定规则被合并到左侧表格中。")
    
    # 创建一个Graphviz图示
    dot = Digraph(format='png')
    dot.attr(rankdir='RL')  # 从左到右布局
    
    # 添加节点
    dot.node('A', '左侧表格', shape='box', style='rounded')
    dot.node('B', '右侧表格1', shape='box', style='rounded')
    dot.node('C', '右侧表格2', shape='box', style='rounded')
    dot.node('D', '右侧表格3', shape='box', style='rounded')
    
    # 设置同一列的表格水平对齐
    with dot.subgraph() as s:
        s.attr(rank='same')  # 保证右侧表格垂直对齐
        s.node('B')
        s.node('C')
        s.node('D')
    
    # 添加连接线
    dot.edge('B', 'A')
    dot.edge('C', 'A')
    dot.edge('D', 'A')
    
    # 渲染Graphviz图并展示
    st.graphviz_chart(dot)
else:
    # 当文件上传后，处理用户上传文件的逻辑
    if uploaded_file_1 is not None:
        # 读取左侧表格
        if uploaded_file_1.name.endswith("xlsx"):
            df_controls = pd.read_excel(uploaded_file_1)
        else:
            df_controls = pd.read_csv(uploaded_file_1)
        
        # 使用两列并排展示数据预览和合并键选择
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("左侧表格的数据预览:")
            st.dataframe(df_controls.head())
        
        with col2:
            # 让用户选择left_on的两列
            columns_left_on = st.multiselect(
                "选择左边合并键（left_on）的两列", 
                options=df_controls.columns.tolist(), 
            )

    if uploaded_files_2:
        right_dfs = []
        right_ons = []
        
        for uploaded_file_2 in uploaded_files_2:
            # 读取第2个文件
            if uploaded_file_2.name.endswith("xlsx"):
                df_right = pd.read_excel(uploaded_file_2)
            else:
                df_right = pd.read_csv(uploaded_file_2)
            
            # 使用两列并排展示数据预览和合并键选择
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"文件 {uploaded_file_2.name} 的数据预览:")
                st.dataframe(df_right.head())
            
            with col2:
                # 让用户选择right_on的合并键
                columns_right_on = st.multiselect(
                    f"选择文件 {uploaded_file_2.name} 的 right_on 列", 
                    options=df_right.columns.tolist()
                )
                right_dfs.append(df_right)
                right_ons.append(columns_right_on)
    
    # 添加分割线
    st.divider()
    
    # 合并数据
    if uploaded_file_1 and uploaded_files_2 and st.button("合并数据"):
        if len(columns_left_on) == 2 and right_dfs and right_ons:
            # 执行合并操作
            df_merge = merge_and_clean(df_controls, right_dfs, columns_left_on, right_ons)
            
            # 显示合并后的结果
            st.write("合并后的数据预览:")
            st.dataframe(df_merge.head())
            
            # 保存合并后的数据为Excel文件
            output_filename = "result.xlsx"
            df_merge.to_excel(output_filename, index=False)
            
            # 提供下载链接
            st.download_button(
                label="下载合并后的数据 (result.xlsx)",
                data=open(output_filename, "rb").read(),
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error(":exclamation:请确保正确选择了合并键！")
