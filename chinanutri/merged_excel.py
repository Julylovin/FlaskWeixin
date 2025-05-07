import os
import pandas as pd


def merge_excel_files():
    all_dfs = []
    file_dir = 'data'
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path)
                # 在数据框开头插入文件名这一行
                new_row = pd.DataFrame({'文件名': [file]})
                df = pd.concat([new_row, df], ignore_index=True)
                all_dfs.append(df)
    merged_df = pd.concat(all_dfs, ignore_index=True)
    merged_df.to_excel('merged_excel.xlsx', index=False)


if __name__ == '__main__':
    merge_excel_files()
