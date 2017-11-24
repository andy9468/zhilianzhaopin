import json
import xlwt
import jieba.analyse as anl

# 待分析的文件
parse_file = 'zhilian_django.json'
encoding_u = 'utf-8'

# 获取文件行数
f = open(parse_file, 'r', encoding=encoding_u)
lines_num = len(f.readlines())
f.close()

# 读取待分析文本
ans_data = ''
f = open(parse_file, 'r', encoding=encoding_u)
for i in range(lines_num):
    data = f.readline().replace('},', '}')
    # print(data)
    dict = json.loads(data)
    # print(dict['job_content'])
    ans_data += dict['job_content']
    # print(i)

f.close()
# print(ans_data)
# 名称
app_name = 'python招聘分词'
workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet(app_name)

seg = anl.extract_tags(ans_data, topK=150, withWeight=True)
i = 0
for tag, weight in seg:
    print("%-20s：%3s %-8s" % (weight, i, tag))
    worksheet.write(i, 0, label=i + 1)
    worksheet.write(i, 1, label=tag)
    worksheet.write(i, 2, label=weight)
    i += 1
workbook.save('%s统计.xls' % (app_name,))
