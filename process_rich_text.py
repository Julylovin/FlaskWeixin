import os
import re
import requests
import datetime
import uuid
from bs4 import BeautifulSoup
from qiniu import Auth, put_data
import logging

# 初始化日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("process.log"), logging.StreamHandler()]
)

# 七牛云配置
from config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME, QINIU_DOMAIN

# 初始化七牛云客户端
q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

def generate_file_name():
    """生成唯一的文件名"""
    now = datetime.datetime.now()
    time_str = now.strftime('%m%d%H%M%S')
    unique_id = str(uuid.uuid4()).replace('-', '')
    file_name = f"shequ/community/f_{time_str}{unique_id}.png"
    return file_name

def upload_to_qiniu(file_url):
    """
    将图片上传到七牛云
    :param file_url: 图片的原始 URL
    :return: 上传成功返回七牛云的访问地址，失败返回 None
    """
    try:
        # 检查 URL 是否有效
        if not file_url.startswith("http"):
            logging.error(f"无效的图片 URL: {file_url}")
            return None

        # 下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://mp.weixin.qq.com'
        }
        response = requests.get(file_url, headers=headers, timeout=10)
        if response.status_code != 200:
            logging.error(f"下载失败: {file_url}, 状态码: {response.status_code}")
            return None

        # 生成文件名
        file_name = generate_file_name()

        # 生成上传的 Token
        token = q.upload_token(QINIU_BUCKET_NAME, file_name, 3600)

        # 上传图片到七牛云
        ret, info = put_data(token, file_name, response.content)
        if info.status_code == 200:
            logging.info(f"上传成功: {QINIU_DOMAIN}{file_name}")
            return f"{QINIU_DOMAIN}{file_name}"
        else:
            logging.error(f"上传失败: {info}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"网络请求错误: {e}")
        return None
    except Exception as e:
        logging.error(f"未知错误: {e}")
        return None

def replace_image_urls(html_content):
    """解析 HTML 并替换图片路径"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 替换 <img> 标签中的图片
    images = soup.find_all('img', src=lambda src: src and src.startswith("https://mmbiz.qpic"))
    for img in images:
        img_url = img.get('src', '')
        if not img_url:
            continue

        # 上传图片到七牛云
        new_img_url = upload_to_qiniu(img_url)
        if new_img_url:
            img['src'] = new_img_url
        else:
            logging.warning(f"跳过无法上传的图片: {img_url}")

    # 替换 CSS 样式中的背景图片
    styles = soup.find_all(style=lambda style: style and "background-image" in style)
    for style_tag in styles:
        style_content = style_tag['style']
        pattern = r'background-image:\s*url\(([^)]+)\)'
        matches = re.findall(pattern, style_content)
        for match in matches:
            old_url = match.strip('"\'')  # 去除可能存在的引号
            if not old_url.startswith("https://mmbiz.qpic"):
                continue

            # 上传图片到七牛云
            new_url = upload_to_qiniu(old_url)
            if new_url:
                style_content = style_content.replace(match, f'"{new_url}"')
            else:
                logging.warning(f"跳过无法上传的背景图片: {old_url}")
        style_tag['style'] = style_content

    return str(soup)

def process_rich_text(input_html_path, output_html_path):
    """处理富文本内容"""
    try:
        # 读取输入的 HTML 文件
        with open(input_html_path, "r", encoding="utf-8") as f:
            input_html = f.read()

        # 处理富文本
        processed_html = replace_image_urls(input_html)

        # 写入输出的 HTML 文件
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(processed_html)

        logging.info("处理完成！结果已保存到 output.html")
    except Exception as e:
        logging.error(f"处理富文本时发生错误: {e}")

if __name__ == '__main__':
    # 输入和输出文件路径
    input_html_path = "input.html"  # 输入的富文本文件
    output_html_path = "output.html"  # 输出的处理后文件

    # 处理富文本
    process_rich_text(input_html_path, output_html_path)