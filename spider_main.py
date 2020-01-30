# -*- encoding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import urllib.error

__author__ = 'yearEamab'


class SpiderMain(object):
    def __init__(self):
        self.image_list=set()

    def get_page_image(self, url):
        if url is None:
            return None
        try:
            response=urllib.request.urlopen(url)
            if response.status!=200:
                return
            html_cont=response.read()
        except urllib.error.URLError as e:
            if hasattr(e,'reason'):
                print(e.reason)
            if hasattr(e,'code'):
                print(e.code)
        if html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        image_parent=soup.find_all('figure',class_='thumbnail')
        for image_node in image_parent:
            self.image_list.add(image_node.find('img')['src'])

#<figure class="thumbnail">
# <a href="http://www.lingyu.me/bizhi/yubanmeiqinshoujibizhi/" target="_blank">
# <img src="http://www.zerodm.tv/wp-content/themes/begin/timthumb.php?src=http://tp.lingyu.me/bz/uploads/2017/07/www.lingyu.me20170722112111545-707x1024.jpg&amp;h=210&amp;w=260&amp;zc=1&amp;a=t" width="260" height="210" alt="御坂美琴手机壁纸[51P]">
# </a>
# <span class="cat"><a href="http://www.zerodm.tv/dmtp/sjbz/">手机壁纸</a></span>
# </figure>

    def download_image(self,image_url,count):
        if image_url is None or count is None:
            return
        response=urllib.request.urlopen(image_url)
        if response.status!=200:
            return
        image_cont=response.read()
        if image_cont is None:
            return
        with open('%s.jpg' %('a'+str(count)),'wb') as fout:
            fout.write(image_cont)
            fout.close()
        print('%d download %s successful' %(count,image_url))
        return True

#<a class="page-numbers" href="http://www.zerodm.tv/dmtp/page/114/">114</a>


if __name__=="__main__":
    root_url='http://www.zerodm.tv/dmtp'
    spider=SpiderMain()
    page=1
    for x in range(1,page+1):
        print('get image in %s' %(root_url+'/page/%d/' %x))
        spider.get_page_image(root_url+'/page/%d/' %x)

    print('start to download!')
    count=1
    for image_url in spider.image_list:
        if image_url is None:
            continue
        try:
            if spider.download_image(image_url,count) is None:
                continue
            count+=1
        except:
            print('craw failure')




