import json
import csv
import re
import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# 获取网页响应的json文件
def get_html(url):
    headers = {
        "User-Agent": UserAgent().random,
        "Referer": "https://weibo.com/"
    }
    cookies = {
        "cookie": "XSRF-TOKEN=XaDTHukbo_9ceDlHubg0YUVn; SUB=_2A25IPPiLDeRhGeFN7FcU8SrPyj-IHXVrMHRDrDV8PUNbmtB-LUqtkW9NQ8xs_zg2qVv5KD7fA_gitxJLaJQsqidj; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhRmGUpZbrV0HPsqUxcq0rm5JpX5KzhUgL.FoM0S0-feKB0eKe2dJLoIEXLxK.LBozLBonLxKqL1KnLB-qLxK-L1KeLB.2LxKBLBo.LBoeLxKMLBo2LB.zt; ALF=1729739867; SSOLoginState=1698203867; WBPSESS=bE-DSIeJx2-KcY3Ei0BWA1o0YvVu8ngn1V7S6gVQrc7pumI6EQy9mTFqnMJpsHOhG7il_mnm50lq3AqqE_CahbltDZCvD2945g6IsZhHN1pwYs3bmjEjRa5wpD8J7PwnXUoUVDCMLXcu7osrISJfbQ=="
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(3)   # 加上3s 的延时防止被反爬
    return response.text


def get_string(text):
    t = ''
    flag = 1
    for i in text:
        if i == '<':
            flag = 0
        elif i == '>':
            flag = 1
        elif flag == 1:
            t += i
    return t


# 保存评论
def save_text_data(filename,text_data):
    text_data = get_string(text_data)
    with open(filename, "a", encoding="utf-8", newline="")as fi:
        fi = csv.writer(fi)
        fi.writerow([text_data])


# 获取二级评论
def get_second_comments(filename, father_comment_id, user_id):
    max_id = 0
    url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={father_comment_id}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={max_id}&count=20&uid={user_id}locale=zh_CN'
    while True:
        response = get_html(url.format(father_comment_id, max_id, user_id))
        content = json.loads(response)
        comments = content['data']
        # max_id = content['max_id']
        for comment in comments:
            comment_text = comment['text']
            save_text_data(filename,comment_text)
        if max_id == 0:		# 如果max_id==0表明评论已经抓取完毕了
            break


# 获取一级评论
def get_first_comments(filename, weibo_id):

    # 获取发布该条微博的用户id
    url = f'https://weibo.com/ajax/statuses/show?id={weibo_id}'
    header = {
        'user-agent': UserAgent().random
    }
    res = requests.get(url=url, headers=header)
    json_data = res.json()
    weibo_id = json_data['id']
    user_id = json_data['user']['idstr']
    print(id, user_id)
    max_id = ''
    # 获取评论
    page = 0
    while max_id != 0:
        url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={weibo_id}&is_show_bulletin=2&is_mix=0&max_id={max_id}&count=10&uid={user_id}'
        response = get_html(url.format(weibo_id, max_id, user_id))
        content = json.loads(response)
        content_list = content['data']
        max_id = content['max_id']
        cnt = 0
        for content in content_list:
            comment_content = content['text']
            comment_id = content['id']
            sub_comment_number = content['total_number']
            if int(sub_comment_number) != 0:  # 如果有二级评论就去获取二级评论。
                get_second_comments(filename, comment_id,user_id)
            save_text_data(filename, comment_content)
            cnt += 1
        page += 1
        print(f'已保存{page}页')
        # if int(max_id) == 0:    # 如果max_id==0表明评论已经抓取完毕了
        #     break


if __name__ == '__main__':
    # 狗咬女童: 4960132863627574
    weibo_ids = ["4960132863627574"] # 你要爬取的微博的id
    for weibo_id in weibo_ids:
        print("============微博ID： " + weibo_id + " 爬取开始============")
        filename = "data_" + weibo_id + ".csv"
        try:
            get_first_comments(filename,weibo_id)    # 爬取一级评论
            print("============微博ID： " + weibo_id + " 爬取完毕！============")
        except Exception as e:
            print("============微博ID： " + weibo_id + " 爬取失败！============")
            print(e)
            continue

    print("============全部爬取完毕！============")