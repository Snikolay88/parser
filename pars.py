# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from random import randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import string




class GoogleSearch():
    
    def __init__(self):
        #https://2ip.ru/proxy/
        PROXY = "174.138.27.185:8080" # IP:PORT or HOST:PORT
        '''
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        self.driver = webdriver.Chrome("D:\PROJECT\parser\path\chromedriver.exe",options=chrome_options)
        '''

        '''
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        print(userAgent)
        options.add_argument(f'user-agent={userAgent}')
        
        self.driver = webdriver.Chrome(executable_path='D:\PROJECT\parser\path\chromedriver.exe',options=options)
        '''

        self.driver = webdriver.Chrome(executable_path='D:\PROJECT\parser\path\chromedriver.exe')
        self.driver.get('http://www.google.com/');



    def check_current_position(self,title):

        current_position = list()
        current_position.append([
            'Talent',
            'Recruiter',
            'Recruitment',
            'Recruiting',
            'Sourcing',
            'Sourcer',
            'people',
            'HR',
            'human',
            'Operations',
            'Assistant',
            'Office',
            'COO',
            'CEO',
            'Founder',
            'Co-Founder',
            'Managing',
            'Partner',
            'Owner',
            'Automotive',
            'Technician',
            'Buyer',
            'Appraiser',
            'Sales'])

        for cur_pos in current_position:
            for pos in cur_pos:
                if pos in title: 
                    return True
        return False
        
        
    def search(self,line):
        searcheText = '(intitle:"%s") site:linkedin.com/in/' % line     #название запроса
        search_box = self.driver.find_element_by_name('q') #google
        #search_box = self.driver.find_element_by_name('text') #yandex
        numSearch = 1

        search_box.send_keys(Keys.CONTROL + 'a')
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(searcheText)
        randSleep = randint (2,6)
        time.sleep(randSleep)
        search_box.submit()
        scroll = randint(350, 550)
        self.driver.execute_script(f'window.scrollTo(0,{scroll});')
        randSleep = randint (3,8)
        time.sleep(randSleep)

        html = self.driver.page_source
        bs_obj = BeautifulSoup(html, 'html5lib')
        


        titCompany = ''
        name = ''
        job_title = ''
        link = ''

        print("1")
        res_tag = bs_obj.find('div', {'id': 'res'})
        while True:
            if not res_tag:
                statPrv = True
                while statPrv:
                    print("2.1")
                    time.sleep(30)
                    html = self.driver.page_source
                    bs_obj = BeautifulSoup(html, 'html5lib')
                    res_tag = bs_obj.find('div', {'id': 'res'})
                    if not res_tag:
                        statPrv = True
                    else:
                        statPrv = False
                
                continue
                
            else:
                res_tags = res_tag.find_all('div', {'class': 'g'})
                print("3")
                break;

        res = list()
        for res_tag in res_tags:
            
            h3 = res_tag.h3.get_text()
            print(h3)
            splitted_h3 = h3.split(' - ')
            if len(splitted_h3) == 1:
                another_split = h3.split(' – ')[0]
                if len(another_split) == 1:
                    print("4")
                    continue
                name = another_split[0]
                job_title = another_split[1]
                titCompany = another_split[2]
                print("5")
            else:
                if (len(splitted_h3)>2):
                    name = splitted_h3[0].replace('"','')
                    job_title = splitted_h3[1]
                    titCompany = splitted_h3[2].split('|')
                else:
                    name = splitted_h3[0]
                    job_title = splitted_h3[1]
                    titCompany = " "
                print("6")
            # если у нас нет текущих слов в job title
            # то пропускаем
            print(name)
            print(job_title)
            print(titCompany[0])
            print("!")
            if not self.check_current_position(job_title):
                print("7")
                continue
            link = ''
            if 'href' in res_tag.a.attrs:
                link = res_tag.a['href']
            print("8")
            res.append({'name': name, 'title': job_title, 'company': titCompany[0],  'link': link, 'linkBrouser':self.driver.current_url,
                        'numSearch':numSearch})

            for r in res:
                with open('res.csv', 'a',encoding='utf-8') as f:
                    print("9")
                    f.write(f"{r['name']};{r['title']};{r['company']};{r['link']};{r['linkBrouser']};{r['numSearch']};\n")

            numSearch+=1    #номер запроса
           

    def clos(self):
        self.driver.close()



if __name__ == "__main__":

    srch = GoogleSearch()
    f = open('parsed_name.txt', 'r')
    for line in f.readlines():
        srch.search(line.split('\n'))
        
    srch.clos()
        
