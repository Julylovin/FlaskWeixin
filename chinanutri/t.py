import requests

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

# 定义请求参数
payload = {
    "categoryOne": "1",   # 一级分类
    "categoryTwo": "30",  # 二级分类，例如：小麦
    "foodName": "0",      # 食品名称，默认为 0
    "pageNum": "1",       # 页码
    "field": "0",         # 排序字段
    "flag": "0",          # 标志位
}

# 发送 POST 请求
try:
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()  # 检查请求是否成功
    data = response.json()  # 解析 JSON 数据

    # 打印返回的数据
    print("接口返回数据：")
    print(data)

except requests.exceptions.RequestException as e:
    print(f"请求过程中出现错误：{e}")
