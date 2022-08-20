# Factory Method
# Web Scraping
# Multithreading
# Xpath


from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # 104 ===========
# chrome_options = Options() 
# chrome_options.add_argument('--headless')  # 啟動Headless 無頭
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.get("https://www.104.com.tw/jobs/main/") #  Website URL
# locator_search_bar = (By.XPATH,"//*[@id='ikeyword']")  # 定位器 定位搜尋框
# search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator_search_bar),"找不到指定的元素") # 動態等待
# search_input.send_keys("Django") # 傳入字串
# button = driver.find_element(By.XPATH,"/html/body/article[1]/div/div/div[4]/div/button") #  Click Button
# button.click()
# # For Scroll down -> get Data -> Next page
# for i in range(0,13):
#     # Scroll down
#     driver.execute_script("action=document.documentElement.scrollTop=10000")
#     sleep(2)
#     # print(f'Current Page : {driver.current_url}')
#     response = requests.get(str(driver.current_url))
#     soup = BeautifulSoup(response.content,'html.parser')
#     sleep(2)
#     job_titles = soup.find_all('a',{'data-qa-id':'jobSeachResultTitle'})
#     for job_title in job_titles:
#         print(f'{job_title.text}') # job_title
#         link = job_title.get('href')
#         print(f'{link}') # detail_link

#     companies = soup.find_all('ul',{'class':'b-list-inline b-clearfix'})
#     for company in companies:
#         company_name = company.select('a')
#         company_name = company_name[0].get("title").split('\n')
#         print(f'{company_name[0][4:]}\n{company_name[1][5:]}') # company_name, company address
#         company_industry = company.select('li')
#         company_industry = company_industry[2].text
#         print(f'{company_industry} \n') # industry

#     requirements = soup.find_all('ul',{'class':'b-list-inline b-clearfix job-list-intro b-content'})
#     for requirement in requirements:
#         requirement = requirement.select('li')
#         print(requirement[0].text) # work_address
#         print(requirement[1].text) # experience
#         print(requirement[2].text) # degree
#         sleep(5)

#     #  Next page
#     page_button = driver.find_element(By.XPATH,'//*[@id="js-job-content"]/div[3]/button[2]')
#     page_button.click()
#     print(driver.current_url)
#     sleep(2)

# driver.close() # 關閉瀏覽器視窗
# driver.quit()

# 1111 =========
# response = requests.get('https://www.1111.com.tw/search/job?ks=Django')
# soup = BeautifulSoup(response.text, 'html.parser')
# jobs = soup.find_all('div',{'class':'job_item_info'})

# for job in jobs:
#     job_link = job.select('a')[0].get('href') # detail_link
#     print(job_link)
#     company_name = job.select('h6')[0].text # company_name
#     print(company_name)
#     job_title = job.select('h5')[0].text # Job title
#     print(job_title)

#     job_link =str(job_link)

#     response_sub = requests.get(job_link)
#     soup_sub = BeautifulSoup(response_sub.text, 'html.parser')
#     work_address = soup_sub.find('a',{'class':'area-style'}).text # work_address
#     work_address = work_address.replace(' ', '')
#     work_address = work_address.replace('\n', '')
#     print(work_address)
#     degree = soup_sub.find('div',{'class':'ui_items job_education'}) # degree
#     degree = degree.select('p')[0].text
#     degree = degree.replace(' ', '')
#     degree = degree.replace('\n', '')
#     print(degree)
#     experiences = soup_sub.find_all('span',{'class':'job_info_content'}) # Experience
#     experience = experiences[7].text
#     experience = experience.replace(' ', '')
#     experience = experience.replace('\n', '')
#     print(experience)
#     industry = soup_sub.find('p',{'class':'body_3'}).text # Industry
#     print(industry)
#     print('===========')


# Design Pattern : Factory
# from abc import ABC, abstractmethod


# class Website_Factory():
#     @staticmethod
#     def scrape(website):
#         try:
#             if website == '104':
#                 return Product_104()
#             elif website == '111':
#                 return Product_1111()
#             else:
#                 pass
#         except AssertionError as e:
#             print(e)


# def Abstract_Factory(ABC):

#     @abstractmethod
#     def scrape(self):
#         pass


# class Product_104(Abstract_Factory):
#     """ 104 產品線"""
    
    
#     def __init__(self):
#         self.process = "生產A產品"
    
    
#     def scrape(self):
#         try:
#             pass
#         except:
#             pass


# class Product_1111(Abstract_Factory):
#     """ 1111 產品線"""

#     def __init__(self):
#         self.process = "生產B產品"
    
    
#     def scrape(self):
#         try:
#             pass
#         except:
#             pass
# Design Pattern : Factory Combine 

from abc import ABC, abstractmethod
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Website_Factory():

    def __init__(self):
        pass

    def build_scrape(website = ''):
        try:
            if website == '104':
                return Product_104()
            elif website == '1111':
                return Product_1111()
            else:
                pass
        except AssertionError as e:
            print(e)


class Abstract_Factory(ABC):

    @abstractmethod
    def scrape(self):
        pass


class Product_104(Abstract_Factory):

    def scrape(self):
        try:
            chrome_options = Options() 
            chrome_options.add_argument('--headless')  # 啟動Headless 無頭
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get("https://www.104.com.tw/jobs/main/") #  Website URL
            locator_search_bar = (By.XPATH,"//*[@id='ikeyword']")  # 定位器 定位搜尋框
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator_search_bar),"找不到指定的元素") # 動態等待
            search_input.send_keys("Django") # 傳入字串
            button = driver.find_element(By.XPATH,"/html/body/article[1]/div/div/div[4]/div/button") #  Click Button
            button.click()
            # For Scroll down -> get Data -> Next page
            for i in range(0,13):
                # Scroll down
                driver.execute_script("action=document.documentElement.scrollTop=10000")
                sleep(2)
                # print(f'Current Page : {driver.current_url}')
                response = requests.get(str(driver.current_url))
                soup = BeautifulSoup(response.content,'html.parser')
                job_titles = soup.find_all('a',{'data-qa-id':'jobSeachResultTitle'})
                for job_title in job_titles:
                    print(f'{job_title.text}') # job_title
                    link = job_title.get('href')
                    print(f'{link}') # detail_link
                companies = soup.find_all('ul',{'class':'b-list-inline b-clearfix'})
                for company in companies:
                    company_name = company.select('a')
                    company_name = company_name[0].get("title").split('\n')
                    print(f'{company_name[0][4:]}\n{company_name[1][5:]}') # company_name, company address
                    company_industry = company.select('li')
                    company_industry = company_industry[2].text
                    print(f'{company_industry} \n') # industry
                requirements = soup.find_all('ul',{'class':'b-list-inline b-clearfix job-list-intro b-content'})
                for requirement in requirements:
                    requirement = requirement.select('li')
                    print(requirement[0].text) # work_address
                    print(requirement[1].text) # experience
                    print(requirement[2].text) # degree
                #  Next page
                page_button = driver.find_element(By.XPATH,'//*[@id="js-job-content"]/div[3]/button[2]')
                page_button.click()
                # print(driver.current_url)
            driver.close() # 關閉瀏覽器視窗
            driver.quit()
        except:
            pass


class Product_1111(Abstract_Factory):
    """ 1111 產品線"""

    
    def scrape(self):
        try:
            response = requests.get('https://www.1111.com.tw/search/job?ks=Django')
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div',{'class':'job_item_info'})
            for job in jobs:
                job_link = job.select('a')[0].get('href') # detail_link
                print(job_link)
                company_name = job.select('h6')[0].text # company_name
                print(company_name)
                job_title = job.select('h5')[0].text # Job title
                print(job_title)
                job_link =str(job_link)
                response_sub = requests.get(job_link)
                soup_sub = BeautifulSoup(response_sub.text, 'html.parser')
                work_address = soup_sub.find('a',{'class':'area-style'}).text # work_address
                work_address = work_address.replace(' ', '')
                work_address = work_address.replace('\n', '')
                print(work_address)
                degree = soup_sub.find('div',{'class':'ui_items job_education'}) # degree
                degree = degree.select('p')[0].text
                degree = degree.replace(' ', '')
                degree = degree.replace('\n', '')
                print(degree)
                experiences = soup_sub.find_all('span',{'class':'job_info_content'}) # Experience
                experience = experiences[7].text
                experience = experience.replace(' ', '')
                experience = experience.replace('\n', '')
                print(experience)
                industry = soup_sub.find('p',{'class':'body_3'}).text # Industry
                print(industry)
                print('===========')
        except:
            pass


# product_104 = Website_Factory.build_scrape(website='104')
# product_104.scrape()
product_1111 = Website_Factory.build_scrape(website='1111')
product_1111.scrape()