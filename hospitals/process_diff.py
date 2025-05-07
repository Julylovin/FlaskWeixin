import pandas as pd

# 定义文件路径
file1 = "all_hospitals_no_city.xlsx"
file2 = "all_hospitals_has_city.xlsx"

# 读取 Excel 文件
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# 检查列是否一致
if set(df1.columns) != set(df2.columns):
    raise ValueError("两个文件的列不一致，请检查列名！")

# 对 DataFrame 按照所有列排序（便于比较）
df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
df2 = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

# 找出在 df1 中但不在 df2 中的数据
diff1 = df1[~df1.apply(tuple, 1).isin(df2.apply(tuple, 1))]

# 找出在 df2 中但不在 df1 中的数据
diff2 = df2[~df2.apply(tuple, 1).isin(df1.apply(tuple, 1))]

# 合并差异数据
diff_combined = pd.concat([diff1.assign(Source="Only in all_hospitals_no_city"),
                           diff2.assign(Source="Only in all_hospitals_has_city")])

# 导出差异数据到新的 Excel 文件
output_file = "differences_between_files.xlsx"
diff_combined.to_excel(output_file, index=False, engine="openpyxl")

print(f"两个文件的差异已成功导出到 {output_file}")