import os
import pandas as pd

# 定义 data 文件夹路径
data_folder = "data"

# 确保文件夹存在
if not os.path.exists(data_folder):
    print(f"文件夹 {data_folder} 不存在，请检查路径！")
    exit(1)

# 定义表头
headers = [
    'ID',
    '/',
    '食物名称',
    '别名或俗名',
    '英文名称',
    '食部 Edible',
    '水分 Water',
    '能量 Energy',
    '蛋白质 Protein',
    '脂肪 Fat',
    '胆固醇 Cholesterol',
    '灰分 Ash',
    '碳水化合物 CHO',
    '总膳食纤维 Dietary fiber',
    '胡萝卜素 Carotene',
    '维生素 AVitamin',
    'α - TE',
    '硫胺素 Thiamin',
    '核黄素 Riboflavin',
    '烟酸 Niacin',
    '维生素 CVitamin C',
    '钙 Ca',
    '磷 P',
    '钾 K',
    '钠 Na',
    '镁 Mg',
    '铁 Fe',
    '锌 Zn',
    '硒 Se',
    '铜 Cu',
    '锰 Mn',
    '碘 I',
    '饱和脂肪酸 SFA',
    '单不饱和脂肪酸 MUFA',
    '多不饱和脂肪酸 PUFA',
    '合计 Total',
    '一级分类ID',
    '二级分类ID',
    '二级分类名称',
    '一级分类名称'
]

# 初始化存储所有数据的列表
all_data = []
# 遍历 data 文件夹中的所有文件，只处理前三个文件
file_count = 0  # 计数器，用于控制读取的文件数量
# 遍历 data 文件夹中的所有文件
for file_name in os.listdir(data_folder):
    # 检查文件是否为 Excel 文件
    if not (file_name.endswith(".xlsx") or file_name.endswith(".xls")):
        continue  # 跳过非 Excel 文件
    # 如果已经读取了 3 个文件，则停止
    # if file_count >= 3:
    #     break

    file_path = os.path.join(data_folder, file_name)

    # 提取文件名的最后一段作为分类名称
    try:
        category_name_one = file_name.split("_")[-1].split(".")[0]  # 去掉扩展名
    except Exception as e:
        print(f"提取分类名称时出错：{file_name}, 错误信息：{e}")
        continue

    print(f"正在处理文件：{file_name}, 分类名称：{category_name_one}")

    try:
        # 读取 Excel 文件内容
        df = pd.read_excel(file_path, header=None)  # 不读取默认表头

        # 如果 DataFrame 为空，跳过该文件
        if df.empty:
            print(f"文件 {file_name} 内容为空，跳过处理。")
            continue

        # 添加分类名称作为新列
        df["一级分类名称"] = category_name_one

        # 将当前文件的数据追加到 all_data 列表中
        all_data.append(df)

        # 增加计数器
        file_count += 1
    except Exception as e:
        print(f"读取文件 {file_name} 时出现错误：{e}")

# 合并所有数据到一个 DataFrame
if all_data:
    try:
        merged_df = pd.concat(all_data, ignore_index=True)

        # 动态调整列数，确保与 headers 匹配
        num_cols = merged_df.shape[1]
        if num_cols > len(headers):
            merged_df = merged_df.iloc[:, :len(headers)]  # 截断多余列
        elif num_cols < len(headers):
            # 如果列数不足，补充空列
            for i in range(num_cols, len(headers)):
                merged_df[headers[i]] = None

        # 设置表头
        merged_df.columns = headers

        # 导出到新的 Excel 文件
        output_file = "中国疾病预防控制中心营养清单.xlsx"
        merged_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"所有数据已成功导出到 {output_file}")
    except Exception as e:
        print(f"合并数据或保存 Excel 文件时出现错误：{e}")
else:
    print("未找到任何数据")
