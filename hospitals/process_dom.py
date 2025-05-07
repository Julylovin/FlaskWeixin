import requests
from bs4 import BeautifulSoup
import pandas as pd

# 省份数据
provinces = [
    {"name": "北京", "url": "https://www.haodf.com/hospital/list-11.html"},
    {"name": "天津", "url": "https://www.haodf.com/hospital/list-12.html"},
    {"name": "河北省", "url": "https://www.haodf.com/hospital/list-13.html"},
    {"name": "山西", "url": "https://www.haodf.com/hospital/list-14.html"},
    {"name": "内蒙古自治区", "url": "https://www.haodf.com/hospital/list-15.html"},
    {"name": "辽宁省", "url": "https://www.haodf.com/hospital/list-21.html"},
    {"name": "吉林省", "url": "https://www.haodf.com/hospital/list-22.html"},
    {"name": "黑龙江省", "url": "https://www.haodf.com/hospital/list-23.html"},
    {"name": "上海", "url": "https://www.haodf.com/hospital/list-31.html"},
    {"name": "江苏省", "url": "https://www.haodf.com/hospital/list-32.html"},
    {"name": "浙江省", "url": "https://www.haodf.com/hospital/list-33.html"},
    {"name": "安徽省", "url": "https://www.haodf.com/hospital/list-34.html"},
    {"name": "福建省", "url": "https://www.haodf.com/hospital/list-35.html"},
    {"name": "江西省", "url": "https://www.haodf.com/hospital/list-36.html"},
    {"name": "山东省", "url": "https://www.haodf.com/hospital/list-37.html"},
    {"name": "河南省", "url": "https://www.haodf.com/hospital/list-41.html"},
    {"name": "湖北省", "url": "https://www.haodf.com/hospital/list-42.html"},
    {"name": "湖南省", "url": "https://www.haodf.com/hospital/list-43.html"},
    {"name": "广东省", "url": "https://www.haodf.com/hospital/list-44.html"},
    {"name": "广西壮族自治区", "url": "https://www.haodf.com/hospital/list-45.html"},
    {"name": "海南省", "url": "https://www.haodf.com/hospital/list-46.html"},
    {"name": "重庆", "url": "https://www.haodf.com/hospital/list-50.html"},
    {"name": "四川省", "url": "https://www.haodf.com/hospital/list-51.html"},
    {"name": "贵州省", "url": "https://www.haodf.com/hospital/list-52.html"},
    {"name": "云南省", "url": "https://www.haodf.com/hospital/list-53.html"},
    {"name": "西藏自治区", "url": "https://www.haodf.com/hospital/list-54.html"},
    {"name": "陕西省", "url": "https://www.haodf.com/hospital/list-61.html"},
    {"name": "甘肃省", "url": "https://www.haodf.com/hospital/list-62.html"},
    {"name": "青海省", "url": "https://www.haodf.com/hospital/list-63.html"},
    {"name": "宁夏回族自治区", "url": "https://www.haodf.com/hospital/list-64.html"},
    {"name": "新疆维吾尔自治区", "url": "https://www.haodf.com/hospital/list-65.html"},
]

# 设置请求头 (Headers)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.haodf.com/",
}


def extract_province_city_data(provinces):
    """
    提取省份和城市数据，并返回一个二维数组。

    参数:
        provinces (list): 包含省份名称和 URL 的字典列表。

    返回:
        list: 包含省份、省份 ID、城市名称、城市 ID 的二维数组。
    """
    # 存储最终结果的列表
    result_array = []

    try:
        # 遍历每个省份
        for province in provinces:
            print(f"正在处理省份：{province['name']}")

            # 提取省份 ID
            province_id = province["url"].split("-")[-1].split(".")[0]

            # 发送 GET 请求获取网页内容
            response = requests.get(province["url"], headers=headers)

            if response.status_code == 200:
                # 使用 BeautifulSoup 解析 HTML
                soup = BeautifulSoup(response.text, "html.parser")

                # 查找目标 <div id="el_tree_1000000" class="v">
                target_div = soup.find("div", {"id": "el_tree_1000000", "class": "v"})

                if target_div:
                    # 在目标 div 中查找所有 <div class="ksbd">
                    ksbd_divs = target_div.find_all("div", class_="ksbd")

                    # 提取每个 <div class="ksbd"> 中的所有 <a> 标签的内容
                    for ksbd in ksbd_divs:
                        a_tags = ksbd.find_all("a")  # 查找所有 <a> 标签
                        if a_tags:
                            for a in a_tags:
                                href = a.get("href")  # 获取 href 属性
                                text = a.get_text(strip=True)  # 获取标签内的文本内容

                                # 提取城市 ID（假设 href 的格式为 /hospital/list-<id>.html）
                                city_id = href.split("-")[-1].split(".")[0] if href else "未知"

                                # 将省份名称、省份 ID、城市名称、城市 ID 添加到结果数组
                                result_array.append([province["name"], province_id, text, city_id])
                else:
                    print(f"未找到目标 <div id='el_tree_1000000' class='v'>")
            else:
                print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"请求过程中出现错误：{e}")

    return result_array


# 调用函数提取数据
result_array = extract_province_city_data(provinces)

# 打印结果数组（便于调试）
print("\n提取的二维数组：")
for row in result_array:
    print(row)

# 如果需要保存为 Excel 文件，可以使用以下代码：
output_file = "province_city_data.xlsx"
df = pd.DataFrame(result_array, columns=["省份", "省份ID", "城市", "城市ID"])
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"\n数据已成功导出到 {output_file}")