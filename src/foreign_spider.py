#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import xlwt


class getPageSelenium():
    # 初始化方法
    def __init__(self):
        self.url = 'http://cpnp.nmpa.gov.cn/province/webquery/list.jsp'
        self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\\v-yuexia\downloadsoft\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        self.save_filepath = r'C:\Users\v-yuexia\getMakeUpInfo'
        self.all_avail_items, all_avail_element = [],[]

    # 保存所有的link对应的text的内容
    def get_all_items(self, current_page):
        print("current_page:",current_page)
        tmp = current_page[0].text.split('\n')[1:] #处理current_page，使之成为需要的格式
        item_list = []
        for i in tmp:
            if i.isdigit():
                continue
            else:
                item_list.append(i.split('国妆网备进字')[0].strip())
        return item_list                 #返回所有link对应的text内容

    def elements_collect(self, current_window): # 爬取当前窗口所有化妆品成分
        current_page = self.driver.find_elements_by_id('table1') #保存当前页面里所需保存的列表
        items_list = self.get_all_items(current_page)
        all_avail_items = []
        all_avail_element = []
        for item in items_list:
            try:
                go_to_item_info = self.driver.find_element_by_partial_link_text(item)
            except Exception as e:
                continue
            all_avail_items.append(item)
            go_to_item_info.click()
            all_window = self.driver.window_handles  # 根据句柄判断，窗口是否为新打开窗口
            for window in all_window:
                if window != current_window:
                    self.driver.switch_to.window(window)

            item_elements = self.driver.find_element_by_class_name('prt-chengfenr')
            all_avail_element.append(item_elements.text)
            self.driver.switch_to.window(current_window)
        self.driver.switch_to.window(current_window)
        return all_avail_items, all_avail_element

    def write_to_excel(self, items, item_elements, title, path, table_name):
        workbook = xlwt.Workbook(encoding='utf8')
        worksheet = workbook.add_sheet(title)
        for i in range(len(items)):
            worksheet.write(i, 0, items[i])
            worksheet.write(i, 1, item_elements[i])
        workbook.save(path + '\\' + table_name)

    def start(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        time.sleep(4)
        current_window = self.driver.current_window_handle
        self.all_avail_items, self.all_avail_element = self.elements_collect(current_window)
        print("下一页", str(self.all_avail_items).encode('GBK','ignore').decode('GBk') )

        for i in range(12):
            #下一页数据
            # self.driver.refresh()
            go_to_page = self.driver.find_element_by_link_text('下一页')
            go_to_page.click()
            #浏览器跳转时间
            WebDriverWait(self.driver, 10)
            time.sleep(6)

            current_window = self.driver.current_window_handle
            result = self.elements_collect(current_window)
            self.all_avail_items += result[0]
            self.all_avail_element += result[1]
            print(self.all_avail_items)
            current_page = self.driver.find_elements_by_id('table1')
            print("下一页", str(current_page[0].text.split('\n')[1:]).encode('GBK','ignore').decode('GBk'))
        self.write_to_excel(self.all_avail_items, self.all_avail_element, u"foreign_cosmetrics_elements", self.save_filepath, 'cosmetics_elements.xls')

if __name__ == "__main__":
    xy = getPageSelenium()
    xy.start()