import pandas as pd
import os

# 定义文件路径列表
file_names = [
    "all_hospitals_by_province_with_name_1.xlsx",
    "all_hospitals_by_province_with_name_2.xlsx",
    "all_hospitals_by_province_with_name_3.xlsx",
    "all_hospitals_by_province_with_name_4.xlsx",
]

# 检查文件是否存在
for file_name in file_names:
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"文件 {file_name} 不存在，请检查文件路径！")

# 创建一个空的 DataFrame 用于存储合并后的数据
merged_data = pd.DataFrame()

# 遍历文件列表并读取数据
for file_name in file_names:
    print(f"正在读取文件：{file_name}")
    df = pd.read_excel(file_name)
    merged_data = pd.concat([merged_data, df], ignore_index=True)

# 去重处理（如果需要）
merged_data.drop_duplicates(inplace=True)

# 导出合并后的数据到新的 Excel 文件
output_file = "all_hospitals.xlsx"
merged_data.to_excel(output_file, index=False, engine="openpyxl")

print(f"所有文件已成功合并到 {output_file}")