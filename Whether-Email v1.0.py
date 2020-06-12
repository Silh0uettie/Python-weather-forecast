#!/usr/bin/env python
# coding: utf-8

# In[1]:


from email.message import EmailMessage
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import schedule
import smtplib
import time
import os


# # get & send today's weather

# In[2]:


def send_morning():
    try:
        # collect data from the website
        url = 'http://www.weather.com.cn/weather/101190401.shtml' # city is Suzhou
        web_data = requests.get(url)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'html.parser')
        day = soup.select('ul.t.clearfix > li > h1') 
        weather = soup.select('ul.t.clearfix > li > p.wea')
        max_tem = soup.select('ul.t.clearfix > li > p.tem > span')
        min_tem = soup.select('ul.t.clearfix > li > p.tem > i')
        wind = soup.select('ul.t.clearfix > li > p.win > i')
        wind_dir = soup.select('ul.t.clearfix > li > p.win > em > span')
        uv = soup.select( 'li.li1 > span')
        clothing = soup.select( 'li.li3.hot > a > p')
        air = soup.select( 'li.li6 > span')
        info ={}
        i = 0

        # organize the data and put them in a dictionary
        for day, weather, max_tem, min_tem, wind, uv, clothing, air in zip(day, weather, max_tem, min_tem, wind, uv, clothing, air):
            day_text = day.get_text()
            weather_text = weather.get_text()
            max_tem_text = max_tem.get_text()
            min_tem_text = min_tem.get_text()
            wind_text = wind.get_text()
            wind1 = wind_dir[2*i]['title']
            wind2 = wind_dir[2*i+1]['title']
            if wind1 == wind2:
                wind_dir_text = wind1
            else:
                wind_dir_text = (wind1 + str('转') + wind2)
            uv_text = uv.get_text()
            clothing_text = clothing.get_text()
            air_text = air.get_text()
            collectinfo = {
                i: [
                day_text,
                weather_text,
                max_tem_text,
                min_tem_text,
                wind_text,
                wind_dir_text,
                uv_text,
                clothing_text,
                air_text
                ]
            }
            info.update(collectinfo)
            i = i+1

        # generate some sentences (strings) about the weather
        today = (
            str('苏州今天')+
            str(info[0][1])+ # weather
            str(',')+
            str(info[0][2])+ # temp1
            str('-')+
            str(info[0][3])+ # temp2
            str('。')+
            str(info[0][5])+ # wind_dir
            str(info[0][4])+ # wind
            str('。紫外线指数：')+
            str(info[0][6])+ # uv
            str('；空气质量：')+
            str(info[0][8])+ # air
            str('。')+
            str(info[0][7]) # clothing
        )

        # send an email
        EMAIL_ADDRESS = os.environ.get('BOT_USER')
        EMAIL_PASSWORD = os.environ.get('BOT_PASS')
        msg = EmailMessage()
        msg['Subject'] = '明日天气'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'example@example.com'
        msg.set_content(today)
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:    
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        pass


# # get & send tomorrow's weather

# In[3]:


def send_night():
    try:
        # collect data from the website
        url = 'http://www.weather.com.cn/weather/101190401.shtml' # city is Suzhou
        web_data = requests.get(url)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text, 'html.parser')
        day = soup.select('ul.t.clearfix > li > h1') 
        weather = soup.select('ul.t.clearfix > li > p.wea')
        max_tem = soup.select('ul.t.clearfix > li > p.tem > span')
        min_tem = soup.select('ul.t.clearfix > li > p.tem > i')
        wind = soup.select('ul.t.clearfix > li > p.win > i')
        wind_dir = soup.select('ul.t.clearfix > li > p.win > em > span')
        uv = soup.select( 'li.li1 > span')
        clothing = soup.select( 'li.li3.hot > a > p')
        air = soup.select( 'li.li6 > span')
        info ={}
        i = 0

        # organize the data and put them in a dictionary
        for day, weather, max_tem, min_tem, wind, uv, clothing, air in zip(day, weather, max_tem, min_tem, wind, uv, clothing, air):
            day_text = day.get_text()
            weather_text = weather.get_text()
            max_tem_text = max_tem.get_text()
            min_tem_text = min_tem.get_text()
            wind_text = wind.get_text()
            wind1 = wind_dir[2*i]['title']
            wind2 = wind_dir[2*i+1]['title']
            if wind1 == wind2:
                wind_dir_text = wind1
            else:
                wind_dir_text = (wind1 + str('转') + wind2)
            uv_text = uv.get_text()
            clothing_text = clothing.get_text()
            air_text = air.get_text()
            collectinfo = {
                i: [
                day_text,
                weather_text,
                max_tem_text,
                min_tem_text,
                wind_text,
                wind_dir_text,
                uv_text,
                clothing_text,
                air_text
                ]
            }
            info.update(collectinfo)
            i = i+1

        # generate some sentences (strings) about the weather
        tomorrow = (
            str('苏州明天')+
            str(info[1][1])+ # weather
            str(',')+
            str(info[1][2])+ # temp1
            str('-')+
            str(info[1][3])+ # temp2
            str('。')+
            str(info[1][5])+ # wind_dir
            str(info[1][4])+ # wind
            str('。紫外线指数：')+
            str(info[1][6])+ # uv
            str('；空气质量：')+
            str(info[1][8])+ # air
            str('。')+
            str(info[1][7]) # clothing
        )

        # send an email
        EMAIL_ADDRESS = os.environ.get('BOT_USER')
        EMAIL_PASSWORD = os.environ.get('BOT_PASS')

        msg = EmailMessage()
        msg['Subject'] = '明日天气'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'example@example.com'
        msg.set_content(tomorrow)

        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:    
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        pass


# In[4]:


schedule.every().day.at("07:00").do(send_morning)


# In[5]:


schedule.every().day.at("21:00").do(send_night)


# In[6]:


while True:
    schedule.run_pending()
    time.sleep(1)


# # Reference

# https://blog.csdn.net/feiyang5260/article/details/80372907

# # Acknowledgements

# Yinhao Zhang\
# Jin Li
