# import streamlit as st
# import pandas as pd

# def load_data(filepath):
#     # 加载数据
#     df = pd.read_excel(filepath)
#     return df.iloc[:, :19]

# def filter_data(df):
#     # 筛选数据
#     return df.loc[df['Buyer'].str.contains('nancy', na=False, case=False)]

# def main():
#     st.title('买家数据分析')

#     # 文件上传
#     uploaded_file = st.file_uploader("选择一个文件", type=['xlsx'])
#     if uploaded_file is not None:
#         # 读取数据
#         df = load_data(uploaded_file)

        
#         # 用户输入
#         #buyer_name = st.text_input("输入买家名称进行筛选 (例如: Nancy)", "Nancy")
#         # buyer_name =str(buyer_name)
#         # 筛选数据
#         # if buyer_name:
#         df_filtered = filter_data(df)
#         # st.write(df_filtered)
#         st.write(f"筛选后的数据条数: {df_filtered.shape[0]}")
            
#         # 分组统计
#         grouped = df_filtered.groupby('FACTORY')
#         SUM = 0
#         for factory, group in grouped:
#             SUM += group.shape[0]
#             st.write(f"{factory}: {group.shape[0]} 条")
#         st.write(f"一共有 {SUM} 条")

# if __name__ == '__main__':
#     main()
    
    
import streamlit as st
import pandas as pd
import os
import shutil

def load_data(filepath):
    # 加载数据
    df = pd.read_excel(os.path.join(filepath, "aaa.xlsx"))
    return df.iloc[:, :19]

def filter_data(df, buyer_name):
    # 筛选数据
    return df.loc[df['Buyer'].str.contains(buyer_name, na=False, case=False)]

def clear_directory(directory):
    # 检查目录是否存在
    if os.path.exists(directory):
        # 遍历目录中的所有文件并删除
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def main():
    st.title('拆分供应商数据小工具')

    # 定义文件夹路径
    folder_path = "A:\container"
    # folder_path = 'A:/Desktop/cma'


    # 清空文件夹
    #clear_directory(folder_path)

    # 文件上传
    # uploaded_file = st.file_uploader("选择一个文件", type=['xlsx'])
    #if uploaded_file is not None:
        # 读取数据
    df = load_data(folder_path)
    if df:
        # 用户输入
        buyer_name = st.text_input("输入采购名称进行筛选 (例如: Nancy)", "Nancy")
        if buyer_name:
            # 筛选数据
            df_filtered = filter_data(df, buyer_name)
            st.write(f"筛选后的数据条数: {df_filtered.shape[0]}")

            # 分组统计
            grouped = df_filtered.groupby('FACTORY')
            SUM = 0
            for factory, group in grouped:
                SUM += group.shape[0]
                st.write(f"{factory}: {group.shape[0]} 条")

                # 为每个工厂创建一个文件
                with pd.ExcelWriter(f'{folder_path}/{factory}.xlsx', engine='openpyxl') as writer:
                    group.to_excel(writer, index=False)

            st.write(f"一共有 {SUM} 条数据")

if __name__ == '__main__':
    main()
