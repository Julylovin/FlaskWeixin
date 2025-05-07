from bs4 import BeautifulSoup
def extract_a_tag_info(html_list):
    all_results = []
    for html in html_list:
        soup = BeautifulSoup(html, 'html.parser')
        h3_a = soup.select_one('h3 a')
        pid_name = h3_a.text
        pid = h3_a.get('data_id')

        a_tag_list = []
        for a in soup.select('ul.food_list li a'):
            title = a.text
            data_id = a.get('data_id')
            data_pid = a.get('data_pid')
            a_tag_list.append({
                'title': title,
                'data_id': data_id,
                'data_pid': data_pid
            })

        result = {
            'pid_name': pid_name,
            'pid': pid,
            'list': a_tag_list
        }
        all_results.append(result)
    return all_results


html_list = [
    '''
    <div class="food_sc food_box food_bg">
     <div class="food_sc_top food_border">
       <h3><a href="foodlist_0_12_0_0_0_1.htm" data_id="12" data_pid="0" target="_blank">蔬菜类及制品</a></h3>
     </div>
     <ul class="food_list">
       <li><a href="foodlist_0_12_45_0_0_1.htm" data_id="45" data_pid="12" target="_blank">根菜类</a></li>
       <li><a href="foodlist_0_12_46_0_0_1.htm" data_id="46" data_pid="12" target="_blank">鲜豆类</a></li>
       <li><a href="foodlist_0_12_47_0_0_1.htm" data_id="47" data_pid="12" target="_blank">茄果、瓜菜类</a></li>
       <li><a href="foodlist_0_12_48_0_0_1.htm" data_id="48" data_pid="12" target="_blank">葱蒜类</a></li>
       <li><a href="foodlist_0_12_49_0_0_1.htm" data_id="49" data_pid="12" target="_blank">嫩茎、叶、花菜类</a></li>
       <li><a href="foodlist_0_12_50_0_0_1.htm" data_id="50" data_pid="12" target="_blank">水生蔬菜类</a></li>
       <li><a href="foodlist_0_12_51_0_0_1.htm" data_id="51" data_pid="12" target="_blank">薯芋类</a></li>
       <li><a href="foodlist_0_12_52_0_0_1.htm" data_id="52" data_pid="12" target="_blank">野生蔬菜类</a></li>
     </ul>
   </div>
    ''',
    # 可以添加更多的 HTML 片段
]

final_result = extract_a_tag_info(html_list)

# 直接使用 final_result 变量
# 示例：打印第一个元素的 pid_name
# print(final_result)
print(f"#{final_result[0]['pid_name']}")
#
# # 示例：遍历 list 里的每个元素并打印 title
# for item in final_result[0]['list']:
#     print(item['title'])

print(f"categoryOne = {final_result[0]['pid']}")
print(f"categoryOneName = '{final_result[0]['pid_name']}'")
print("category_two_map = {")
for item in final_result[0]['list']:
    print(f"{item['data_id']} : '{item['title']}' ,")
print("}")
