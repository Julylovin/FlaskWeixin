import pandas as pd
import os

# 定义字段名映射关系
column_mapping = {
    "城市": "city_name",
    "惠誉编码": "nh_code",
    "医院名称": "community_name"
}
# 定义文件路径
excel_file = "./_area.xlsx"
output_file = "./_area.json"

# 检查文件是否存在
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"文件 {excel_file} 不存在，请检查文件路径！")



# 读取 Excel 文件
try:
    df = pd.read_excel(excel_file)
    # 检查并重命名列
    df.rename(columns=column_mapping, inplace=True)
except Exception as e:
    print(f"读取 Excel 文件时出现错误：{e}")
    exit(1)

# 将 DataFrame 转换为 JSON 格式
json_data = df.to_json(orient="records", force_ascii=False)

# 导出为 JSON 文件
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_data)
    print(f"JSON 数据已成功导出到 {output_file}")
except Exception as e:
    print(f"保存 JSON 文件时出现错误：{e}")
    exit(1)