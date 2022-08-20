from abc import ABC, abstractmethod
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.views import addJob
from .models import Job

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
    """ 104 產品線"""

    def scrape(self, keyword=''):
            try:
                print(f'scrape : {keyword}')
                payload = []
                chrome_options = Options() 
                chrome_options.add_argument('--headless')  # 啟動Headless 無頭
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.get("https://www.104.com.tw/jobs/main/") #  Website URL
                locator_search_bar = (By.XPATH,"//*[@id='ikeyword']")  # 定位器 定位搜尋框
                search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator_search_bar),"找不到指定的元素") # 動態等待
                search_input.send_keys(keyword) # 傳入字串
                button = driver.find_element(By.XPATH,"/html/body/article[1]/div/div/div[4]/div/button") #  Click Button
                button.click()

                # For Scroll down -> get Data -> Next page
                cnt = -1
                for i in range(0,13):
                    # Scroll down
                    driver.execute_script("action=document.documentElement.scrollTop=10000")
                    sleep(2)
                    # print(f'Current Page : {driver.current_url}')
                    
                    response = requests.get(str(driver.current_url))
                    soup = BeautifulSoup(response.content,'html.parser')
                    
                    cnt = -1
                    job_titles = soup.find_all('a',{'data-qa-id':'jobSeachResultTitle'})
                    for job_title_1 in job_titles:
                        payload_content = [{'job_title':''},{'company_name':''},{'work_address':''},{'degree':''},{'experience':''},{'industry':''},{'detail_link':''}]
                        cnt +=1
                        payload.append(payload_content)
                        # print(payload)
                        # print(f'{job_title.text}') # job_title
                        payload[cnt][0]['job_title'] = job_title_1.text
                        # print(cnt)
                        # print(job_title_1.text)
                        # print(payload)
                        # print(payload[cnt])
                        # print(payload[cnt][0])
                        # print(payload[cnt][0]['job_title'])
                        link = job_title_1.get('href')
                        # print(f'{link[2:]}') # detail_link)
                        payload[cnt][6]['detail_link'] = link[2:]
                    
                    cnt = 0
                    companies = soup.find_all('ul',{'class':'b-list-inline b-clearfix'})
                    for company in companies:
                        company_name = company.select('a')
                        company_name = company_name[0].get("title").split('\n')
                        # print(f'{company_name[0][4:]}\n{company_name[1][5:]}') # company_name, company address
                        payload[cnt][1]['company_name'] = company_name[0][4:]
                        company_industry = company.select('li')
                        company_industry = company_industry[2].text
                        # print(f'{company_industry} \n') # industry
                        payload[cnt][5]['industry'] = company_industry
                        cnt +=1
                    
                    cnt = 0
                    requirements = soup.find_all('ul',{'class':'b-list-inline b-clearfix job-list-intro b-content'})
                    for requirement in requirements:
                        requirement = requirement.select('li')
                        # print(requirement[0].text) # work_address
                        payload[cnt][2]['work_address'] = requirement[0].text
                        # print(requirement[1].text) # experience
                        payload[cnt][4]['experience'] = requirement[1].text
                        # print(requirement[2].text) # degree
                        payload[cnt][3]['degree'] = requirement[2].text
                        cnt +=1
                    break
                    #  Next page
                    page_button = driver.find_element(By.XPATH,'//*[@id="js-job-content"]/div[3]/button[2]')
                    page_button.click()
                    # print(driver.current_url)
                driver.close() # 關閉瀏覽器視窗
                driver.quit()
                for cnt in range(cnt):
                    # print(payload[cnt])
                    Job.objects.update_or_create(job_title=payload[cnt][0]['job_title'],company_name=payload[cnt][1]['company_name'],work_address=payload[cnt][2]['work_address'],degree=payload[cnt][3]['degree'],experience=payload[cnt][4]['experience'],industry=payload[cnt][5]['industry'],detail_link=payload[cnt][6]['detail_link'])
                # url = "http://127.0.0.1:8000/api/add/"
                # for cnt in range(cnt):
                #     requests.post(url, data=payload[cnt])
                print('Finished')
            except :
                driver.close() # 關閉瀏覽器視窗
                driver.quit()
                # url = "http://127.0.0.1:8000/api/add/"
                for cnt in range(cnt):
                    # print(payload[cnt])
                    Job.objects.update_or_create(job_title=payload[cnt][0]['job_title'],company_name=payload[cnt][1]['company_name'],work_address=payload[cnt][2]['work_address'],degree=payload[cnt][3]['degree'],experience=payload[cnt][4]['experience'],industry=payload[cnt][5]['industry'],detail_link=payload[cnt][6]['detail_link'])
                    # requests.post(url, data=payload[cnt])
                
                print('Finished')

class Product_1111(Abstract_Factory):
    """ 1111 產品線"""

    
    def scrape(self, keyword=''):
        cnt = 0
        try:
            payload = []
            url_1111 = f'https://www.1111.com.tw/search/job?ks={keyword}'
            response = requests.get(url_1111)
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = soup.find_all('div',{'class':'job_item_info'})
            cnt = 0
            for job in jobs:
                payload_content = [{'job_title':''},{'company_name':''},{'work_address':''},{'degree':''},{'experience':''},{'industry':''},{'detail_link':''}]
                payload.append(payload_content)
                job_link = job.select('a')[0].get('href') # detail_link
                # print(job_link)
                payload[cnt][6]['detail_link'] = job_link

                company_name = job.select('h6')[0].text # company_name
                # print(company_name)
                payload[cnt][1]['company_name'] = company_name

                job_title = job.select('h5')[0].text # Job title
                # print(job_title)
                payload[cnt][0]['job_title'] = job_title

                job_link =str(job_link)
                response_sub = requests.get(job_link)
                soup_sub = BeautifulSoup(response_sub.text, 'html.parser')
                if soup_sub:
                    work_address = soup_sub.find('a',{'class':'area-style'}).text # work_address
                    work_address = work_address.replace(' ', '')
                    work_address = work_address.replace('\n', '')
                    # print(work_address)
                    payload[cnt][2]['work_address'] = work_address

                    degree = soup_sub.find('div',{'class':'ui_items job_education'}) # degree
                    degree = degree.select('p')[0].text
                    degree = degree.replace(' ', '')
                    degree = degree.replace('\n', '')
                    degree = degree.replace('\r', '')
                    # print(degree)
                    payload[cnt][3]['degree'] = degree

                    experiences = soup_sub.find_all('span',{'class':'job_info_content'}) # Experience
                    experience = experiences[7].text
                    experience = experience.replace(' ', '')
                    experience = experience.replace('\n', '')
                    experience = experience.replace('\r', '')
                    # print(experience)
                    payload[cnt][4]['experience'] = experience

                    industry = soup_sub.find('p',{'class':'body_3'}).text # Industry
                    # print(industry)
                    payload[cnt][5]['industry'] = industry
                    # print('===========')
                    cnt += 1
            for cnt in range(cnt):
                # print(payload[cnt])
                Job.objects.update_or_create(job_title=payload[cnt][0]['job_title'],company_name=payload[cnt][1]['company_name'],work_address=payload[cnt][2]['work_address'],degree=payload[cnt][3]['degree'],experience=payload[cnt][4]['experience'],industry=payload[cnt][5]['industry'],detail_link=payload[cnt][6]['detail_link'])
            print('Finished')
        except:
            
            for cnt in range(cnt):
                # print(payload[cnt])
                Job.objects.update_or_create(job_title=payload[cnt][0]['job_title'],company_name=payload[cnt][1]['company_name'],work_address=payload[cnt][2]['work_address'],degree=payload[cnt][3]['degree'],experience=payload[cnt][4]['experience'],industry=payload[cnt][5]['industry'],detail_link=payload[cnt][6]['detail_link'])
            print('Finished')