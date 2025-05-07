import requests
import pandas as pd

# 目标 URL
url = "https://m.haodf.com/nhospital/hospital/list/ajaxGetHosList"

# 设置请求头 (Headers)
headers = {
    ":authority": "m.haodf.com",
    ":method": "POST",  # 注意：HTTP/2 的伪头部字段（如 :method）通常不需要手动设置
    ":path": "/nhospital/hospital/list/ajaxGetHosList",
    ":scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "183",  # 动态计算实际内容长度
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "acw_tc=276aedd517430433446103934e2065f172a4b386a097558298a651245835ca; g=10400_1743043346548; Hm_lvt_d4ad3c812a73edcda8ff2df09768997d=1743043347; HMACCOUNT=0CCDB55D8759C5B6; Hm_lpvt_d4ad3c812a73edcda8ff2df09768997d=1743043455",
    "origin": "https://m.haodf.com",
    "priority": "u=1, i",
    "referer": "https://m.haodf.com/hospital/list.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "x-hdf-ssr": "client",
    "x-requested-with": "XMLHttpRequest"
}

# 构造初始请求参数
params = {
    "nowPage": 1,
    "pageSize": 50,
    "options[diseaseId]": "",
    "options[facultyId]": "",
    "options[placeId]": 0,
    "options[hospitalGrade]": "",
    "options[hospitalCategory]": "",
    "options[hospitalCharacter]": "",
}

# 存储所有医院数据的列表
all_hospital_data = []

try:
    # 获取第一页数据以提取总页数
    response = requests.post(url, headers=headers, data=params)

    if response.status_code == 200:
        data = response.json()
        total_pages = data.get("data", {}).get("pageInfo", {}).get("totalPage", 0)

        # 循环请求所有页数据
        for page in range(1, total_pages + 1):
            print(f"正在请求第 {page} 页...")
            params["nowPage"] = page  # 更新当前页码
            response = requests.post(url, headers=headers, data=params)

            if response.status_code == 200:
                data = response.json()
                hospital_data = data.get("data", {}).get("data", [])
                all_hospital_data.extend(hospital_data)  # 将数据添加到总列表中
            else:
                print(f"请求第 {page} 页失败，状态码：{response.status_code}")
                break
    else:
        print(f"请求第一页失败，状态码：{response.status_code}")

    # 检查是否成功获取数据
    if not all_hospital_data:
        print("未获取到任何数据")
    else:
        # 转换为 DataFrame
        df = pd.DataFrame(all_hospital_data)

        # 导出到 Excel 文件
        output_file = "all_hospitals_no_city.xlsx"
        df.to_excel(output_file, index=False, engine="openpyxl")

        print(f"所有数据已成功导出到 {output_file}")
except Exception as e:
    print(f"请求过程中出现错误：{e}")