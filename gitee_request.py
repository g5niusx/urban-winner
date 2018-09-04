import re

import requests
from bs4 import BeautifulSoup

import db_handler

db_name = 'url.db'

requests_get = requests.get('https://gitee.com/search',
                            params={'language': 'Java', 'q': 'spring', 'type': '', 'page': '1'})
home_url = 'https://gitee.com/'
print('搜索页访问完毕...')

handler_db_handler = db_handler.DBHandler(db_name)
# 初始化表
handler_db_handler.init_table()
# 查询已经爬取过的url
has_insert = handler_db_handler.select_has_insert()


# 获取查询出来的工程总条数
def get_page_count(get):
    beautiful_soup = BeautifulSoup(get.content, features='html.parser')
    find_all = beautiful_soup.find_all(text=re.compile('我们已为您搜索到.*'))
    strip = str(find_all[0])
    return re.findall('\d+', strip)[0]


# 获取搜索出来的列表
def get_project_list(get):
    search_project_list = []
    beautiful_soup = BeautifulSoup(get.content, features='html.parser')
    for a in beautiful_soup.find_all('a', 'ellipsis'):
        search_project_list.append(home_url + a.get('href'))
    return search_project_list


# 获取真实的可以直接预览文件的地址
def get_raw_data(url):
    url_get = requests.get(url)
    beautiful_soup = BeautifulSoup(url_get.content, features='html.parser')
    find = beautiful_soup.find(attrs={'class': 'ui button edit-raw'})
    return home_url + find['href']


# 从一个工程地址中获取配置文件路径
def get_config(project_url):
    project_get = requests.get(project_url)
    print('开始爬取[%s]' % project_url)
    beautiful_soup = BeautifulSoup(project_get.content, features='html.parser')
    # 获取文件
    for file in beautiful_soup.find_all('div', attrs={'class': 'five wide column tree-item-file-name tree-file'}):
        a_href_ = file.a['href']
        if a_href_.endswith('.properties') | a_href_.endswith('.yml'):
            _url = get_raw_data(home_url + a_href_)
            if (_url,) not in has_insert:
                handler_db_handler.insert(_url)
    # 获取目录
    for directory in beautiful_soup.find_all('div',
                                             attrs={'class': 'five wide column tree-item-file-name tree-folder'}):
        href_ = home_url + directory.a['href']
        get_config(href_)


count = get_page_count(requests_get)
if count is None:
    print('没有获取到查询的总量')
    quit(0)
# 计算页数
i = int(int(count) / 15)
# 对于每一页进行循环爬取
for page in range(i):
    print('开始获取第[%d]页数据,总计%d页' % ((page + 1), i))
    requests_get = requests.get('https://gitee.com/search',
                                params={'language': 'Java', 'q': 'spring', 'type': '', 'page': str(page + 1)})
    project_list = get_project_list(requests_get)
    for _project in project_list:
        get_config(_project)
    print('第[%d]已经爬取完毕,总计%d页' % ((page + 1), i))
