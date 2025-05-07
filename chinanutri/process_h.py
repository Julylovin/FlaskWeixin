import requests
import pandas as pd
import time
import random

# 定义目标 URL
url = "https://nlc.chinanutri.cn/fq/FoodInfoQueryAction!queryFoodInfoList.do"

# 定义请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "JSESSIONID=13E677F2B7EDBD6DF58CB7A69EE4DAAC; Hm_lvt_f1641da686b7b197f19488d93a0ff060=1746583477; HMACCOUNT=90279A50DBD586C6; Hm_lvt_a85b7882f3efa6808738cdb1067540af=1746584446; JSESSIONID=6CB05E66A5C79699EFE19A0B532D49D6; Hm_lpvt_a85b7882f3efa6808738cdb1067540af=1746586164; acw_tc=276aedcc17465935146061496e61e90b4a86a4dc14313e527f48325796f97b; Hm_lpvt_f1641da686b7b197f19488d93a0ff060=1746593515; SERVERID=dfa5750dc967fb59c0663a02d1acb9ec|1746593530|1746593514",
    "Host": "nlc.chinanutri.cn",
    "Origin": "https://nlc.chinanutri.cn",
    "Referer": "https://nlc.chinanutri.cn/fq/foodlist_0_1_0_0_0_1.htm",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

#蔬菜类及制品
categoryOne = 12
categoryOneName = '蔬菜类及制品'
category_two_map = {
    45 : '根菜类' ,
    46 : '鲜豆类' ,
    47 : '茄果、瓜菜类' ,
    48 : '葱蒜类' ,
    49 : '嫩茎、叶、花菜类' ,
    50 : '水生蔬菜类' ,
    51 : '薯芋类' ,
    52 : '野生蔬菜类' ,
}



# 初始化存储所有数据的列表
all_data = []

# 循环请求每个 categoryTwo
for category_two_code, category_two_name in category_two_map.items():
    print(f"正在处理 categoryTwo: {category_two_name} ({category_two_code})")

    # 请求第一页以获取总页数
    payload = {
        "categoryOne": categoryOne,           # 一级分类
        "categoryTwo": category_two_code,  # 二级分类
        "foodName": "0",              # 食品名称，默认为 0
        "pageNum": "1",               # 初始页码
        "field": "0",                 # 排序字段
        "flag": "0",                  # 标志位
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()       # 解析 JSON 数据

        # 提取总页数
        total_pages = int(data.get("totalPages", 1))
        print(f"categoryTwo: {category_two_name}, 总页数：{total_pages}")

        # 如果没有数据，跳到下一个 categoryTwo
        if total_pages == 0:
            print(f"categoryTwo: {category_two_name} 没有数据，跳到下一个。")
            continue

        # 循环请求所有页数
        for page_num in range(1, total_pages + 1):
            print(f"正在请求 categoryTwo: {category_two_name}, 第 {page_num} 页...")

            # 更新请求参数中的页码
            payload["pageNum"] = str(page_num)

            # 发送请求
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            page_data = response.json()

            # 提取当前页数据
            food_data = page_data.get("list", [])
            if not food_data:
                print(f"categoryTwo: {category_two_name}, 第 {page_num} 页无数据。")
                continue

            # 添加 categoryTwo 和名称
            for item in food_data:
                item.append(categoryOne)  # 添加 categoryTwoCode 到最后一列
                item.append(category_two_code)  # 添加 categoryTwoCode 到最后一列
                item.append(category_two_name)  # 添加 categoryTwoName 到最后一列
                all_data.append(item)

            # 随机延迟 1-3 秒，避免触发反爬机制
            time.sleep(random.uniform(1, 3))

    except requests.exceptions.RequestException as e:
        print(f"请求过程中出现错误：{e}")
        continue

# 将数据保存到 Excel 文件
if all_data:
    # 转换为 DataFrame
    df = pd.DataFrame(all_data)

    # 导出到 Excel 文件
    output_file = f"food_{categoryOne}_{categoryOneName}.xlsx"
    try:
        df.to_excel(output_file, index=False, engine="openpyxl", header=False)  # 不添加默认表头
        print(f"所有数据已成功导出到 {output_file}")
    except Exception as e:
        print(f"保存 Excel 文件时出现错误：{e}")
else:
    print("未获取到任何数据")
