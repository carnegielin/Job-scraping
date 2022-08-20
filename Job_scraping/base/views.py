from django.shortcuts import render
from api.views import getJob, addJob
import json
from .scrape import Website_Factory
from .models import Job
import requests

# Scrape Data -> Clear DB -> Update DB -> Get Data From DB -> return 
def index(request):
    if request.method == 'GET':
        context = {}
        jobs = getJob(request)
        jobs = json.loads(jobs.content.decode('utf-8')) 
        # convert byte code to dictionary
            # b'[{"id": 1, "job_title": "Django Developer", "company_name": "DJ", "work_address": "New york", "degree": "Master", "experience": "College", "industry": "Internet", "detail_link": "http"}]'
            #  -> [{'id': 1, 'job_title': 'Django Developer', 'company_name': 'DJ', 'work_address': 'New york', 'degree': 'Master', 'experience': 'College', 'industry': 'Internet', 'detail_link': 'http'}]
        context = {'jobs': jobs}
        return render(request, 'base/index.html', context)
    if request.method == 'POST':
        # Process : Receive Input -> Clear DB -> Scrape Data -> Update DB -> Get Data From DB -> return 
        context = {}
        # Receive Input
        input_search = request.POST.get('input_search')
        print(f'input_search : {input_search}')
        
        #  Clear DB  -> Scrape Data  -> Update DB
        
        #  Clear DB
        old_jobs = Job.objects.all()
        old_jobs.delete()

        # Scrape Data  -> Update DB
        product_104 = Website_Factory.build_scrape(website='104')
        product_104.scrape(keyword = input_search)
        product_1111 = Website_Factory.build_scrape(website='1111')
        product_1111.scrape(keyword = input_search)

        # Get Data From DB -> return 
        response = requests.get(url = "http://127.0.0.1:8000/api")
        jobs = json.loads(response.content.decode('utf-8')) 
        context = {'jobs': jobs}
        return render(request, 'base/index.html', context)
    



    




