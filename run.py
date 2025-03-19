import streamlit as st
import csv
import zipfile
import os

# 标题
st.title("工厂分组工具")
st.write("上传 CSV 文件，按工厂分组并生成压缩包。")

# 文件上传组件
uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

if uploaded_file is not None:
    try:
        # 读取 CSV 文件
        reader = csv.DictReader(uploaded_file.read().decode('utf-8').splitlines())
        data = list(reader)
        
        # 筛选包含 "Nancy" 的行
        filtered_data = [row for row in data if 'Nancy' in row.get('Buyer', '')]
        
        # 按工厂分组
        grouped_data = {}
        for row in filtered_data:
            factory = row.get('FACTORY', '')
            if factory not in grouped_data:
                grouped_data[factory] = []
            grouped_data[factory].append(row)
        
        SUM = sum(len(group) for group in grouped_data.values())

        # 创建临时文件夹
        temp_dir = "temp_factory_groups"
        os.makedirs(temp_dir, exist_ok=True)

        # 将 ZIP 文件保存到 D:/container 文件夹中
        output_dir = "D:/container"
        os.makedirs(output_dir, exist_ok=True)  # 确保文件夹存在
        zip_filename = os.path.join(output_dir, "FACTORY_Groups.zip")

        # 创建 zip 文件
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for factory, group in grouped_data.items():
                filename = f"{factory}.csv"
                st.write(f"{factory}: {len(group)} 条")
                
                # 创建临时 CSV 文件
                temp_filename = os.path.join(temp_dir, filename)
                with open(temp_filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=group[0].keys())
                    writer.writeheader()
                    writer.writerows(group)
                
                # 将文件添加到 zip 文件中
                zipf.write(temp_filename, filename)
                
                # 删除临时文件
                os.remove(temp_filename)

        st.success(f"一共有 {SUM} 条记录。")
        st.success(f"所有分组已成功保存到单独的 CSV 文件中，并压缩到 {zip_filename} 中。")

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
    except Exception as e:
        st.error(f"发生错误: {e}")
else:
    st.info("请上传一个 CSV 文件。")
