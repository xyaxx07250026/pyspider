#coding:utf-8
import xlrd
import json

def deal_with_ingredents(content):
    elements = content.split(':')[1][1:-3].strip().split("\",\"")
    result = []
    for element in elements:
        element = element.replace('\"',"")
        result.append(element)
    return result

def xls_to_json(xls_path,json_name):
    file = xls_path
    outpath = r'C:\Users\v-yuexia\getMakeUpInfo'
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    nrows = table.nrows
    result = []
    for i in range(nrows):
        returnData = {}
        content = table.row_values(i)
        returnData['name'] = content[0]
        returnData['alias'] = content[1].split(':')[0].strip()
        returnData['ingredients'] = deal_with_ingredents(content[1])
        print(returnData['ingredients'])
        result.append(returnData)

    with open(outpath+'\\'+json_name, 'w', encoding='utf-8') as json_file:
        json.dump(result,json_file,ensure_ascii=False)


xls_to_json(r'C:\Users\v-yuexia\getMakeUpInfo\相宜本草.xls','相宜本草.json')
