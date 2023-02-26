import threading
from selenium import webdriver
from get_addr import get_addr
import time
import matplotlib.pyplot as plt
import numpy as np
import xlrd
import matplotlib
import folium
import dbscan
from dbscan import DBSCAN


dic=[]
def get_poi(addr_name):
    global dic
    print(" %s 号线程 运行开始" % threading.current_thread().getName())
    options = webdriver.ChromeOptions()  # 必须要通过option设置浏览器的位置

    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # options.binary_location
    # 隐藏窗口,注释掉则显现窗口
    options.add_argument('headless')

    browser = webdriver.Chrome(chrome_options=options)
    browser.get("http://aqsc.shmh.gov.cn/gis/getpoint.htm")
    time.sleep(1)

    map_search = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]")

    for i in addr_name:
        # 输入值
        while True:  # 当地区名查找失败，则回退一个字符，并继续查找，直至找到或者字符串为空
            try:
                if i == "":
                    break
                inPut = map_search.find_element_by_class_name('text')
                browser.execute_script("arguments[0].value =arguments[1];", inPut, i)
                # 点击按钮
                button = map_search.find_element_by_class_name('button').click()
                time.sleep(1)  # 等待加载
                ul = browser.find_element_by_class_name('local_s')
                li = ul.find_element_by_id('no_0')
                li = li.find_element_by_tag_name('p')
                text=[]
                LIST=li.text.split("：")[-1].split(",")
                text.append(i)
                text.extend(LIST)
                print(text)
                dic.append(text)
                print(text) #输出字典
                break
            except:
                i = i[:-1]
                print("??")
    print(" %s 号线程 运行结束" % threading.current_thread().getName())
    browser.quit()
    return dic

def createdata():
    from threading import Thread
    global dic
    # 10个线程
    addr_name = get_addr()
    length = len(addr_name)
    lenEach_L = 0
    lenEach_R = int(length / 10)
    thread_list = []

    for i in range(1, 10):
        List = addr_name[lenEach_L:lenEach_L + lenEach_R]
        T = Thread(target=get_poi, args=(List,), name="{}".format(i))
        thread_list.append(T)
        lenEach_L = lenEach_L + lenEach_R

    List = addr_name[lenEach_L:length]
    T = Thread(target=get_poi, args=(List,), name="10")
    thread_list.append(T)

    for t in thread_list:
        t.setDaemon(True)  # 设置为守护线程，不会因主线程结束而中断
        t.start()
    for t in thread_list:
        t.join()  # 子线程全部加入，主线程等所有子线程运行完毕

    print(dic)
    #excel导出
    import pandas as pd
    test1 = pd.DataFrame(dic, columns=['地区名', '经度', '纬度'])
    print(test1)
    file_path = pd.ExcelWriter('地区名-经纬表.xlsx')
    # 输出
    test1.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()
#上海静安区数据
def getjinan_data():
    data = xlrd.open_workbook_xls(r'jinan_data.xls')
    table = data.sheets()[0]
    tables = []
    for i in range(1,table.nrows):
        tables.append([float(table.cell_value(i,1)),float(table.cell_value(i,2))])
    return tables
#上海黄浦区数据
def gethuangpu_data():
    data = xlrd.open_workbook_xls(r'huangpu_data.xls')
    table = data.sheets()[0]
    tables = []
    for i in range(1,table.nrows):
        tables.append([float(table.cell_value(i,1)),float(table.cell_value(i,2))])
    return tables
#上海长宁区数据
def getchangning_data():
    data = xlrd.open_workbook_xls(r'changning_data.xls')
    table = data.sheets()[0]
    tables = []
    for i in range(1,table.nrows):
        tables.append([float(table.cell_value(i,1)),float(table.cell_value(i,2))])
    return tables
#上海徐汇区数据
def getxuhui_data():
    data = xlrd.open_workbook_xls(r'xuhui_data.xls')
    table = data.sheets()[0]
    tables = []
    for i in range(1,table.nrows):
        tables.append([float(table.cell_value(i,1)),float(table.cell_value(i,2))])
    return tables
#上海浦东新区数据
def getpudongxin_data():
    data = xlrd.open_workbook_xls(r'pudongxin_data.xls')
    table = data.sheets()[0]
    tables = []
    for i in range(1,table.nrows):
        tables.append([float(table.cell_value(i,1)),float(table.cell_value(i,2))])
    return tables

def dbscan(X,eps, min):
    est = DBSCAN(eps, min)
    #eps：半径。min_samples：邻域密度阈值
    est.fit(X)
    return est.labels_

def main():
    #先到数据查看分布情况
    data = getxuhui_data() ##设置不同数据
    data = np.array(data)
    #print(data)
    matplotlib.rcParams['font.sans-serif'] = ['KaiTi']#设置字为好看的楷体
    plt.scatter(data[:, 0], data[:, 1], c="red", marker='o', label='see')
    plt.xlabel('经')
    plt.ylabel('纬')
    plt.legend(loc=2)
    #plt.show()
    #高德地图和百度地图的经纬度基本为一个定值
    cha1 = 0.006552
    cha2=0.00606

    db = dbscan(data,0.0054,7);
    labels = db
    #print(labels)   #显示类别标签
    #显示出地图
    map_ = folium.Map(location=[data[70][1], data[70][0]], zoom_start=12,
                      tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                      attr='default')
    #设置以location为中心点，其他为接口参数
    colors = ['#8B008B', '#DB7093', '#FFD700','#008000','#DC143C', '#FFB6C1',  '#C71585','#708090', '#008000', '#FFFF00', '#808000', '#FFD700', '#FFA500', '#FF6347',  '#4B0082', '#7B68EE', '#FFFF00', '#808000',  '#FFA500', '#FF6347','#000000']
    for i in range(len(data)):
        folium.CircleMarker(location=[data[i][1]-cha2, data[i][0]-cha1],
                            radius=4, popup='popup',
                            color=colors[labels[i]], fill=True,
                            fill_color=colors[labels[i]]).add_to(map_)

    map_.save('xuhui.html')
if __name__ == "__main__":
    #createdata()         //生成经纬度坐标系。
    main()
