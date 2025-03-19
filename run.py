import streamlit as st
import pandas as pd
import zipfile
import os

# 标题
st.title("拆分供应商数据小工具")
st.write("上传 Excel 文件，按工厂分组并生成压缩包。")

# 文件上传组件
uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx"])

if uploaded_file is not None:
    # 读取 Excel 文件
    df = pd.read_excel(uploaded_file)
    df = df.iloc[:, :19]
    
    # 筛选包含 "Nancy" 的行
    df1 = df.loc[df['Buyer'].str.contains('Nancy', na=False, case=False)]
    
    # 按工厂分组
    grouped = df1.groupby('FACTORY')
    SUM = 0

    # 创建临时文件夹
    temp_dir = "D:/container"
    os.makedirs(temp_dir, exist_ok=True)
    zip_filename = os.path.join(temp_dir, "FACTORY_Groups.zip")

    # 创建 zip 文件
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for factory, group in grouped:
            filename = f"{factory}.xlsx"
            SUM += group.shape[0]
            st.write(f"{factory}: {group.shape[0]} 条")
            
            # 创建临时 Excel 文件
            temp_filename = os.path.join(temp_dir, filename)
            with pd.ExcelWriter(temp_filename) as writer:
                group.to_excel(writer, index=False)
            
            # 将文件添加到 zip 文件中
            zipf.write(temp_filename, filename)
            
            # 删除临时文件
            os.remove(temp_filename)

    st.success(f"一共有 {SUM} 条记录。")
    st.success("所有分组已成功保存到单独的 Excel 文件中，并压缩到一个 zip 包中。")

    # 提供下载链接
    with open(zip_filename, "rb") as f:
        st.download_button(
            label="下载压缩包",
            data=f,
            file_name="FACTORY_Groups.zip",
            mime="application/zip"
        )

    # 删除临时文件夹
    os.rmdir(temp_dir)
else:
    st.info("请上传一个 Excel 文件。")
