"""
@author:Wang Xinsheng
@File:getShiPing.py
@description:...
@time:2021-08-16 14:24
"""
import requests
from urllib import parse
import pdfkit
from bs4 import BeautifulSoup
# import pyh
from bottle import template
import parsetime

base_url = 'http://opinion.people.com.cn'
def get_liks(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    # fragment = '/n1/2021/0520/c1003-32108107.html'
    # result = parse.urljoin(base_url,fragment)
    urls = []
    response = requests.get(url,header)
    content = response.content.decode('gbk')
    soup = BeautifulSoup(content,'html.parser')
    table_links = soup.find('table',attrs={'style':'background:'})
    links_ = table_links.find_all('a')
    for link in links_:
        url_fragment = link['href']
        url_ = parse.urljoin(base_url,url_fragment)
        urls.append(url_)
    print(urls)
    return urls


def get_content(url):
    content_p_list = []
    response = requests.get(url)
    text = response.content.decode('gbk')

    soup = BeautifulSoup(text,'html.parser')
    div_content = soup.find('div',attrs={'class':'col col-1 fl'})
    if div_content is None:
        div_parent = soup.find('div',attrs={'class':'layout rm_txt cf'})
        div_content = div_parent.find('div',attrs={'class':'col col-1'})

    content_time = soup.find('div',attrs={'class':'col-1-1 fl'})
    if content_time is None:
        content_time = div_content.find('div',attrs={'class':'col-1-1'})
    time = parsetime.get_time(content_time.text)
    print(div_content)



    div_content.find('div',attrs={'class':'rm_relevant rm_download cf'}).decompose()
    box = div_content.find('div',attrs={'class':'rm_relevant cf box_news'})
    if box is not None:
        box.decompose()
    div_content.find('p',attrs={'class':'paper_num'}).decompose()
    title = div_content.find('h1').text.strip().replace(u'\xa0', '-')
    print('title',title)
    print('-------------------------------------')
    content_div = div_content.find('div',attrs={'class':'rm_txt_con cf'})
    content_ps = content_div.find_all('p')
    for p in content_ps:
        content_p_list.append(p.text)
    return time,title,content_p_list
    # return result

def htmlToPdf(html:str,name):
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        # 'cookie': [
        #     ('cookie-name1', 'cookie-value1'),
        #     ('cookie-name2', 'cookie-value2'),
        # ],
        # 可以改变文字大小
        # 'dpi':96,
        'outline-depth': 10
    }

    confg = pdfkit.configuration(wkhtmltopdf=r'data/wkhtmltox/bin/wkhtmltopdf.exe')

    #这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径
    # pdfkit.from_url(url, 'jmeter_下载文件2.pdf',configuration=confg)
    # pdfkit.from_string(content, 'jmeter_下载文件2.pdf',configuration=confg)
    # from_url这个函数是从url里面获取内容
    # 这有3个参数，第一个是url，第二个是文件名，第三个就是khtmltopdf的路径

    # pdfkit.from_url('temp.html', 'jmeter_下载文件8.pdf',configuration=confg,options=options)
    # from_file这个函数是从文件里面获取内容
    # 这有3个参数，第一个是一个html文件，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径

    pdfkit.from_string(html, '{}.pdf'.format(name),configuration=confg)
    # from_file这个函数是从一个字符串里面获取内容
    # 这有3个参数，第一个是一个字符串，第二个是文生成的pdf的名字，第三个就是khtmltopdf的路径

def generate(time,title, content_p_list):
    # 定义想要生成的Html的基本格式
    # 使用%来插入python代码
    # % for link in items:
    # <img style="width: 150px;height: 150px;" src="{{link}}">
    # %end

    template_demo = """
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
            <style>
                .text{
                    word-wrap: break-word;
                    word-break: normal;
                    padding-top: 15px
                }
                img{
                    padding-top: 15px;
                }
                .content_p{
                    font-size:23px
                }
            </style>
        </head>
        <title>{{title}}</title>
        <body>
     
        <h1 align="center">{{ title }}</h1>
        <div style="width:100%;text-align:auto">
         % for content_p in content_p_list:
        <p class="content_p">{{content_p}}</p>
        %end
        <br>
        </div>
        </body>
        </html>
        """

    html = template(template_demo, title=title, content_p_list=content_p_list)
    # print(html)

    out_name = '{}-{}'.format(time,title)
    htmlToPdf(html,out_name)
    # filename = "10.html"
    #
    # with open(filename, 'wb') as f:
    #     f.write(html.encode('utf-8'))

def get_article(url):
    time,title,content_p_list = get_content(url)
    generate(time,title,content_p_list)

if __name__ == '__main__':

    # 时评的url链接
    # url='http://opinion.people.com.cn/n1/2021/0127/c1003-32013065.html'#一篇博客的url
    # get_article(url)
    # 一次生成多篇
    url= 'http://opinion.people.com.cn/GB/8213/353915/353916/index.html'

    urls = get_liks(url)
    for url_ in urls:
        get_article(url_)




