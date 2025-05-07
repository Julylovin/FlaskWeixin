import requests
import pandas as pd
import time
import random
import json
import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# 目标 URL
url = "https://m.haodf.com/nhospital/hospital/list/ajaxGetHosList"

# 设置请求头 (Headers)
headers = {
    "Host": "m.haodf.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "acw_tc=276aedd517430433446103934e2065f172a4b386a097558298a651245835ca; g=10400_1743043346548; Hm_lvt_d4ad3c812a73edcda8ff2df09768997d=1743043347; HMACCOUNT=0CCDB55D8759C5B6; Hm_lpvt_d4ad3c812a73edcda8ff2df09768997d=1743043455",
    "Origin": "https://m.haodf.com",
    "Referer": "https://m.haodf.com/hospital/list.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "X-Hdf-Ssr": "client",
    "X-Requested-With": "XMLHttpRequest"
}

# 存储所有医院数据的列表
all_hospital_data = []

# 设置重试机制
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))




def fetch_page_data(place_id, province_info):
    """
    请求一页数据并返回解析结果。

    参数:
        place_id (str): 请求参数中的 options[placeId]。
        province_info (dict): 包含省份和城市信息的字典。

    返回:
        list: 当前页的医院数据。
    """
    params = {
        "nowPage": 1,
        "pageSize": 50,
        "options[diseaseId]": "",
        "options[facultyId]": "",
        "options[placeId]": place_id,
        "options[hospitalGrade]": "",
        "options[hospitalCategory]": "",
        "options[hospitalCharacter]": "",
    }

    try:
        response = session.post(url, headers=headers, data=params)
        if response.status_code == 200:
            data = response.json()
            hospital_data = data.get("data", {}).get("data", [])
            # 为每条医院数据添加省份和城市信息
            for item in hospital_data:
                item.update(province_info)
            return hospital_data
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"请求过程中出现错误：{e}")
        return []


try:
    # 导出到 Excel 文件

    # 获取当前时间并格式化为字符串（例如：2023-10-05_14-30-00）
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 动态生成文件名
    output_file = f"all_hospitals_by_province_with_name_{current_time}.xlsx"

     # 加载省份和城市数据
    provinces = [
        {'province_name': '宁夏回族自治区', 'province_id': '64', 'city_name': '银川市', 'city_id': '6401'},
        {'province_name': '宁夏回族自治区', 'province_id': '64', 'city_name': '石嘴山市', 'city_id': '6402'},
        {'province_name': '宁夏回族自治区', 'province_id': '64', 'city_name': '吴忠市', 'city_id': '6403'},
        {'province_name': '宁夏回族自治区', 'province_id': '64', 'city_name': '固原市', 'city_id': '6404'},
        {'province_name': '宁夏回族自治区', 'province_id': '64', 'city_name': '中卫市', 'city_id': '6405'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '乌鲁木齐市...', 'city_id': '6501'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '克拉玛依市...', 'city_id': '6502'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '昌吉州', 'city_id': '6523'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '博尔塔拉蒙...', 'city_id': '6527'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '巴音郭楞蒙...', 'city_id': '6528'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '阿克苏地区...', 'city_id': '6529'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '喀什地区', 'city_id': '6531'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '和田地区', 'city_id': '6532'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '伊犁州', 'city_id': '6540'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '塔城地区', 'city_id': '6542'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '阿勒泰地区...', 'city_id': '6543'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '吐鲁番市', 'city_id': '6504'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '哈密市', 'city_id': '6505'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '克孜勒苏柯...', 'city_id': '6530'},
        {'province_name': '新疆维吾尔自治区', 'province_id': '65', 'city_name': '自治区直辖...', 'city_id': '6590'}
    ]

    # 遍历省份列表
    for province in provinces:
        print(f"正在处理省份：{province['province_name']} 城市 {province['city_name']} (ID: {province['province_id']})")

        # 动态设置请求参数中的 placeId
        place_id = province["city_id"]
        province_info = {
            "province_name": province["province_name"],
            "province_id": province["province_id"],
            "city_name": province["city_name"],
            "city_id": province["city_id"],
        }

        # 获取第一页数据以提取总页数
        response = session.post(url, headers=headers, data={"options[placeId]": place_id})
        if response.status_code == 200:
            data = response.json()
            total_pages = data.get("data", {}).get("pageInfo", {}).get("totalPage", 0)

            # 循环请求该省份的所有页数据
            for page in range(1, total_pages + 1):
                print(f"正在请求省份 {province['province_name']} 城市 {province['city_name']} 第 {page} 页...")
                time.sleep(random.uniform(3, 7))  # 随机延迟 1-3 秒

                # 发送请求获取当前页数据
                current_page_data = fetch_page_data(place_id, province_info)
                all_hospital_data.extend(current_page_data)
        else:
            print(f"请求省份 {province['province_name']} 第一页失败，状态码：{response.status_code}")

    # 去重处理
    all_hospital_data = [dict(t) for t in {tuple(d.items()) for d in all_hospital_data}]

    # 检查是否成功获取数据
    if not all_hospital_data:
        print("未获取到任何数据")
    else:
        # 转换为 DataFrame
        df = pd.DataFrame(all_hospital_data)


        df.to_excel(output_file, index=False, engine="openpyxl")

        print(f"所有数据已成功导出到 {output_file}")
except Exception as e:
    print(f"请求过程中出现错误：{e}")
finally:
    session.close()  # 关闭会话
