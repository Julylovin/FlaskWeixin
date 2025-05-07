import requests
import pandas as pd
import time
import random

# 定义请求 URL 和请求头
url = "https://nlc.chinanutri.cn/fq/FoodInfoQueryAction!queryFoodInfoList.do"
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
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# 定义 categoryTwo 集合
category_two_map = {
    "30": "小麦",
    "31": "稻米",
    "32": "玉米",
    "33": "大麦",
    "34": "小米、黄米",
    "35": "其它",
}

# 初始化数据列表
all_data = []

# 循环调用接口
for category_two_code, category_two_name in category_two_map.items():
    print(f"正在处理 categoryTwo: {category_two_name} ({category_two_code})")

    # 初始化页码
    page_num = 1
    while True:
        # 定义请求参数
        payload = {
            "categoryOne": "1",
            "categoryTwo": category_two_code,
            "foodName": "0",
            "pageNum": str(page_num),  # 动态设置页码
            "field": "0",
            "flag": "0",
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析 JSON 数据

            # 提取数据
            food_data = data.get("data", [])
            if not food_data:  # 如果当前页没有数据，跳出循环
                print(f"categoryTwo: {category_two_name} 已无更多数据，跳到下一个。")
                break

            # 添加 categoryTwo 和名称
            for item in food_data:
                item["categoryTwoCode"] = category_two_code
                item["categoryTwoName"] = category_two_name
                all_data.append(item)

            print(f"成功获取 categoryTwo: {category_two_name}, 第 {page_num} 页数据。")
            page_num += 1  # 页码自增
            time.sleep(random.uniform(1, 3))  # 随机延迟 1-3 秒，避免请求过快被封禁
        except requests.exceptions.RequestException as e:
            print(f"请求过程中出现错误：{e}")
            break

# 将数据保存到 Excel 文件
if all_data:
    # 转换为 DataFrame
    df = pd.DataFrame(all_data)

    # 导出到 Excel 文件
    output_file = "food_info_with_category_two.xlsx"
    try:
        df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"所有数据已成功导出到 {output_file}")
    except Exception as e:
        print(f"保存 Excel 文件时出现错误：{e}")
else:
    print("未获取到任何数据")
