from bs4 import BeautifulSoup

# HTML 内容
html_content = """
<div id="el_tree_1000000" class="v">
    <div class="kstl2">
        <a href="//www.haodf.com/hospital/list-11.html">北京</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-12.html">天津</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-13.html">河北省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-14.html">山西</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-15.html">内蒙古自治区</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-21.html">辽宁省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-22.html">吉林省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-23.html">黑龙江省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-31.html">上海</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-32.html">江苏省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-33.html">浙江省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-34.html">安徽省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-35.html">福建省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-36.html">江西省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-37.html">山东省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-41.html">河南省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-42.html">湖北省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-43.html">湖南省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-44.html">广东省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-45.html">广西壮族自治区</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-46.html">海南省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-50.html">重庆</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-51.html">四川省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-52.html">贵州省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-53.html">云南省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-54.html">西藏自治区</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-61.html">陕西省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-62.html">甘肃省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-63.html">青海省</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-64.html">宁夏回族自治区</a>
    </div>
    <div class="kstl">
        <a href="//www.haodf.com/hospital/list-65.html">新疆维吾尔自治区</a>
    </div>
    <div class="cls"></div>
</div>
"""

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")

# 查找所有 <a> 标签
a_tags = soup.find_all("a")

# 提取并打印每个 <a> 标签的 href 和文本内容
for a in a_tags:
    href = a.get("href")  # 获取 href 属性
    text = a.get_text(strip=True)  # 获取标签内的文本内容
    full_url = f"https:{href}"  # 补全 URL
    print(f"名称: {text}, 网址: {full_url}")