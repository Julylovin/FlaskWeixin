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
    '''<div class="food_twp food_box food_bg clear">
     <div class="food_twp_top food_border">
       <h3><a href="foodlist_0_28_0_0_0_1.htm" data_id="28" data_pid="0" target="_blank">调味品类</a></h3>
     </div>
     <ul class="food_list">
       <li><a href="foodlist_0_28_117_0_0_1.htm" data_id="117" data_pid="28" target="_blank">酱油</a></li>
       <li><a href="foodlist_0_28_118_0_0_1.htm" data_id="118" data_pid="28" target="_blank">醋</a></li>   
       <li><a href="foodlist_0_28_119_0_0_1.htm" data_id="119" data_pid="28" target="_blank">酱</a></li>    
       <li><a href="foodlist_0_28_120_0_0_1.htm" data_id="120" data_pid="28" target="_blank">腐乳</a></li> 
       <li><a href="foodlist_0_28_121_0_0_1.htm" data_id="121" data_pid="28" target="_blank">咸菜类</a></li> 
       <li><a href="foodlist_0_28_122_0_0_1.htm" data_id="122" data_pid="28" target="_blank">辛香料</a></li> 
       <li><a href="foodlist_0_28_123_0_0_1.htm" data_id="123" data_pid="28" target="_blank">盐、味精及其它</a></li>          
     </ul>                 
   </div>''',
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
