#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os
import xlwt
import xlrd
import xlutils


def get_useful_page():
    page_tmp = browser.find_element_by_id('pageDiv')  # 找到翻page的位置
    page_list = page_tmp.text.split('\n')[2:-2]  #只提取有用页面，2页开始
    return page_list  # 得到可直接使用的页面序号


#保存所有的link对应的text的内容
def get_all_items():
    current_page=browser.find_elements_by_id('table1') #保存当前页面里所需保存的列表
    print("current_page:",current_page)
    tmp = current_page[0].text.split('\n')[1:] #处理current_page，使之成为需要的格式
    item_list = []
    for i in tmp:
        if i.isdigit():
            continue
        else:
            item_list.append(i.split('国妆网备进字')[0].strip())
    return item_list                 #返回所有link对应的text内容

def elements_collect(current_window): # 爬取当前窗口所有化妆品成分
    items_list = get_all_items()
    all_avail_items = []
    all_avail_element = []
    for item in items_list:
        try:
            go_to_item_info = browser.find_element_by_partial_link_text(item)
        except Exception as e:
            continue
        all_avail_items.append(item)
        go_to_item_info.click()
        all_window = browser.window_handles  # 根据句柄判断，窗口是否为新打开窗口
        for window in all_window:
            if window != current_window:
                browser.switch_to.window(window)

        item_elements = browser.find_element_by_class_name('prt-chengfenr')
        all_avail_element.append(item_elements.text)
        browser.switch_to.window(current_window)
    browser.switch_to.window(current_window)
    return all_avail_items,all_avail_element

#写入表格
def write_to_excel(items,item_elements,title,path,table_name):
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet(title)
    for i in range(len(items)):
        worksheet.write(i, 0, items[i])
        worksheet.write(i, 1, item_elements[i])
    workbook.save(path+'\\'+table_name)

if __name__ == '__main__':
    url = 'http://cpnp.nmpa.gov.cn/province/webquery/list.jsp'
    browser = webdriver.PhantomJS(executable_path=r'C:\Users\\v-yuexia\downloadsoft\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    browser.get(url)
    browser.implicitly_wait(3)
    current_window = browser.current_window_handle

    save_filepath = r'C:\Users\v-yuexia\getMakeUpInfo'

    all_avail_items, all_avail_element = [],[]

    all_avail_items, all_avail_element = elements_collect(current_window)
    print('第一页：',all_avail_items)

    #下一页数据
    go_to_page = browser.find_element_by_link_text('下一页')
    go_to_page.click()
    #浏览器跳转时间
    WebDriverWait(browser,10)

    all_windows = browser.window_handles

    current_page = browser.find_elements_by_id('table1')
    print("下一页:",current_page[0].text.split('\n')[1:])

    # all_windows = browser.window_handles
    # print('current_window1:',current_window)
    # print('all_windows:',all_windows)
    # for win in all_windows[1:]:
    #     browser.switch_to.window(win)
    #     item_elements = browser.find_element_by_class_name('prt-chengfenr')
    #     print(item_elements.text)


    # write_to_excel(all_avail_items,all_avail_element,u"foreign_cosmetrics_elements",save_filepath,'cosmetics_elements.xls' )








