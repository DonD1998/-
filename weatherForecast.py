# -*- coding: utf-8 -*-
"""
author: DonD
Location: 北京
breaf: weather forecast
Date: 2022_10_10
version: 0.3.1
"""

import requests
import bs4
import os
import sys
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

url = "https://weather.cma.cn/web/weather/54511"

# 爬取网页内容
def get_web(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    res = requests.get(url, headers=header, timeout=5)
    content = res.text.encode('utf-8')
    return content

# 得到一个天气预报的list
def parse_content(content):
    # 将网页爬取内容转化为可视化内容
    s = bs4.BeautifulSoup(content, 'html.parser')

    # 存放天气预报内容,准备好循环体
    list_temp = s.find_all('div', class_='pull-left day')
    list_temp2 = s.find_all('div', class_="row hb days")

    # 生成原始预测列表
    temp_str = list_temp[0].text.strip()
    temp_str2 = list_temp2[0].text.strip()
    temp_list = temp_str.split('\n')
    temp_list2 = temp_str2.split('\n')
    # 删除list中空值
    temp_list = [i for i in temp_list if i != '']
    temp_list2 = [i for i in temp_list2 if i !='']
    wendu = temp_list2[4]
    temp_list.append(wendu)

    return  temp_list



def convert(list_1):
    # 转化为不包括湿度的所需列表
    temp_list = []
    temp_list.append('**Weather Forocast**\n')
    temp_list.append(f'日期:{list_1[0]}\n')

    # 判断天气情况的输出
    if list_1[1] != list_1[5]:
        temp_list.append(f'天气:{list_1[1]}-{list_1[5]}\n')
    else:
        temp_list.append(f'天气:{list_1[1]}\n')

    # 输入气温
    tem_list = list_1[4].split('℃')
    temp_list.append(f'气温：{tem_list[0]}℃-{tem_list[1]}℃\n')
    tem_list_today = list_1[8].split('℃')
    tem_list.append(tem_list_today)
    # 判断风力的输出
    if list_1[3] != list_1[7]:
        temp_list.append(f'风力:{list_1[3]}-{list_1[7]}\n')
    else:
        temp_list.append(f'风力:{list_1[3]}\n')

    return temp_list, tem_list


# 获取湿度信息
def get_wet(content):
    s = bs4.BeautifulSoup(content, 'html.parser')
    list_hum = s.find_all('table', class_='hour-table')

    # 生成列表，并去除空值
    hum = list_hum[0].text.strip()
    hum_list = hum[hum.find('湿'):hum.find('云')].split('\n')
    hum_list = [i for i in hum_list if i != '' and i != ' ']

    # 排序结果
    hum_list.sort()

    # 输出
    hum_str = f'{hum_list[-1]}:{hum_list[0]}-{hum_list[-2]}\n'

    # 输出每日提醒
    hum_data = float(hum_list[0][:-1])
    if hum_data <= 20:
        hum_notion = '今日湿度低\n'
    elif hum_data <= 60:
        hum_notion = '今日湿度适中\n'
    else:
        hum_notion = '今日湿度高\n'
    return hum_str, hum_notion

# 获取湿度值


# 准备每日提醒
def notion(weather_convert):
    temp_list = []
    temper_max = float(weather_convert[1][0])
    temper_min = float(weather_convert[1][1])
    temp_today = float(weather_convert[1][3][0])

    # 雨伞模块
    if weather_convert[0][2].find("雨") != -1:
        umbrella = '有雨带伞\n'
    elif weather_convert[0][2].find("晴") != -1 and temper_max >= 30:
        umbrella = '太阳强带伞\n'
    else:
        umbrella = '不用带伞\n'


    # 紫外线模块
    if weather_convert[0][2].find('晴') != -1 and temper_max >= 30:
        ultra = '注意防晒\n'
    else:
        ultra = '适当防晒\n'

    # 穿衣模块
    if temper_min >= 24:
        colthes = '适宜短袖\n'
    elif temper_min >= 15:
        colthes = '适宜长袖\n'
    elif temper_min >= 5:
        colthes = '适宜风衣夹克\n'
    else:
        colthes = '适宜棉衣羽绒服\n'


    # 温差
    if temper_max - temper_min >= 10:
        between = '昼夜温差大\n'
    else:
        between = '昼夜温差小\n'

    # 昨日温差
    if temp_today - temper_max >= 3:
        wencha = f"与昨日相比降温很多哦，温度下降:{temp_today - temper_max}℃\n"
    elif temp_today - temper_max >=0:
        wencha = f"与昨日相比降温不大，温度下降：{temp_today - temper_max}℃\n"
    elif temp_today - temper_max >=-3:
        wencha = f"与昨日相比温差不大，温度上升：{abs(temp_today - temper_max)}℃\n"
    else:
        wencha = f"与昨日相比温差很大，温度上升:{abs(temp_today - temper_max)}℃\n"

    temp_list.append(between)
    temp_list.append(colthes)
    temp_list.append(ultra)
    temp_list.append(umbrella)
    temp_list.append(wencha)

    return temp_list

import time
class GetInitialDate(object):
    #  The first date
    #  请更换你的纪念日， 如果数量很多， 可以生成列表，
    #  遍历传值，不懂的可以私聊我
    #  其实这个天数也可以直接从对象中传值过来，但是必须得是 ****-**-** 这样的格式
    Initial_date = "2022-07-14"
    shengliqi = "2023-3-29"

    def __init__(self):
        self.date_item = self.get_items
        self.now_date = self._get_now_date()
        # self.Initial_date_sum = self.get_sum_date(self.Initial_date)
        # self.now_date_sum = self.get_sum_date(self.now_date)
        self.all_date = self.get_sum_date(self.Initial_date, self.now_date)
        self.shengliqi_date = self.get_sum_date(self.shengliqi, self.now_date)

    def __str__(self):
        """稍微修饰一下,"""
        return  f"宝宝今天是我们在一起第{self.all_date}天呢\n今天也是爱你的一天呢，早安！\n\n"

    def __str2__(self):
        if 33-self.shengliqi_date+1>=0:
            return f"距离下次生理期还有：{29 - self.shengliqi_date + 1}天\n\n"
        else:
            return "距离下次生理期还有：?天\n\n"

    def dapipi(self):
        return f'现在需要打屁屁{self.all_date-28}次\n\n'

    @property
    def get_items(self):
        """遍历或者字典天数
         as:  {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181, 7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
         如果是闰年 后续需要加一天"""
        date_items = {}
        s = 0
        for i in range(1, 13):
            if i in [1, 3, 5, 7, 8, 10, 12]:
                s += 31
            elif i == 2:
                s += 28
            else:
                s += 30
            date_items[i] = s
        return date_items

    def get_sum_date(self, old_date, new_date):
        """ start sum the date """
        old_year, old_month, old_d = map(int, old_date.split("-"))
        new_year, new_month, new_d = map(int, new_date.split('-'))
        #  先计算初始日期的天数
        is_leap = True if self._is_leap(old_year) else False
        if not is_leap:
            The_date = self.date_item[old_month] + old_d
        else:
            The_date = self.date_item[old_month] + 1 + old_d
            # 计算新的日期
        is_leap_now = True if self._is_leap(new_year) else False
        if not is_leap:
            The_date_now = self.date_item[new_month] + new_d
        else:
            The_date_now = self.date_item[new_month] + 1 + new_d
        # 比较

        if old_year == new_year:
            return The_date_now - The_date + 2
        else:
            # 2019  2020
            ss = 0
            for i in range(new_year - old_year):
                if self._is_leap(old_year + i):
                    s = 366
                else:
                    s = 365
                ss += s
            return ss + The_date_now - The_date + 2

    def _get_now_date(self):
        """Return the  localtime as: "****-**-**" date """
        return time.strftime("%Y-%m-%d", time.localtime())

    def _is_leap(self, year):
        "year -> 1 if leap year, else 0."
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# print(GetInitialDate())
time_record = GetInitialDate().__str__()
shengliqi_record = GetInitialDate().__str2__()


# 准备一个入口函数
def result(url):
    web_content = get_web(url)
    weather_content = parse_content(web_content)
    weather_convert = list(convert(weather_content))
    weather_convert.append(list(get_wet(web_content)))
    weather_convert.append(notion(weather_convert))
    weather_final = []
    weather_final.append(time_record)
    weather_final.append(shengliqi_record)



    for item in weather_convert[0]:
        weather_final.append(item)

    weather_final.append(weather_convert[2][0])
    weather_final.append('********************\n')
    weather_final.append("记得擦护手霜\n")
    for item in weather_convert[3]:
        weather_final.append(item)
    weather_final.append(weather_convert[2][1])


    return weather_final


if __name__ == '__main__':
    with open('weather_nextgeneration.txt', 'w', encoding='utf-8') as f:

        for item in result(url):
            f.write(item)


    # print(result(url), '\n', '完成天气预报')
    print('完成天气预报')
