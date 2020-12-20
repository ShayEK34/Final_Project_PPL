'''
main.py
----------
Matthew Chatham
June 6, 2018

Given a company's landing page on Glassdoor and an output filename, scrape the
following information about each employee review:

Review date
Employee position
Employee location
Employee status (current/former)
Review title
Employee years at company
Number of helpful votes
Pros text
Cons text
Advice to mgmttext
Ratings for each of 5 categories
Overall rating
'''

import time
import pandas as pd
from argparse import ArgumentParser
import argparse
import logging
import logging.config
from selenium import webdriver as wd
import selenium
import numpy as np
from selenium.webdriver.common.keys import Keys

from schema import SCHEMA
import json
import urllib
import datetime as dt

start = time.time()

DEFAULT_URL = ('https://www.glassdoor.com/Interview/index.htm')

parser = ArgumentParser()
parser.add_argument('-u', '--url',
                    help='URL of the company\'s Glassdoor landing page.',
                    default=DEFAULT_URL)
parser.add_argument('-f', '--file', default='glassdoor_ratings.csv',
                    help='Output file.')
parser.add_argument('--headless', action='store_true',
                    help='Run Chrome in headless mode.')
parser.add_argument('--username', help='Email address used to sign in to GD.')
parser.add_argument('-p', '--password', help='Password to sign in to GD.')
parser.add_argument('-c', '--credentials', help='Credentials file')
parser.add_argument('-l', '--limit', default=100,
                    action='store', type=int, help='Max reviews to scrape')
parser.add_argument('--start_from_url', action='store_true',
                    help='Start scraping from the passed URL.')
parser.add_argument(
    '--max_date', help='Latest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews ASCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
parser.add_argument(
    '--min_date', help='Earliest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews DESCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
args = parser.parse_args()

if not args.start_from_url and (args.max_date or args.min_date):
    raise Exception(
        'Invalid argument combination:\
        No starting url passed, but max/min date specified.'
    )
elif args.max_date and args.min_date:
    raise Exception(
        'Invalid argument combination:\
        Both min_date and max_date specified.'
    )

if args.credentials:
    with open(args.credentials) as f:
        d = json.loads(f.read())
        args.username = d['username']
        args.password = d['password']
else:
    try:
        with open('backend/scrape_interviews/secret.json') as f:
            d = json.loads(f.read())
            args.username = d['username']
            args.password = d['password']
    except FileNotFoundError:
        msg = 'Please provide Glassdoor credentials.\
        Credentials can be provided as a secret.json file in the working\
        directory, or passed at the command line using the --username and\
        --password flags.'
        raise Exception(msg)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(lineno)d\
    :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)

logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)


def scrape(field, interview):

    def scrape_emp_title(interview):
        for sentence in interview:
            if 'Interview' in sentence:
                return sentence


    def scrape_interview(interview):
        flag = False
        Interview = ""
        for line in interview:
            if line == 'Interview':
                flag = True
            elif line != 'Interview' and not flag:
                continue
            elif line != 'Interview' and line != 'Interview Questions' and flag:
                Interview = Interview + line + " "
            elif line == 'Interview Questions' and flag:
                return Interview
        return Interview

    def scrape_interview_questions(interview):
        flag = False
        answer_questions = ""
        for line in interview:
            if line == 'Interview Questions':
                flag = True
            elif line != 'Interview Questions' and not flag:
                continue
            elif line == '1 Answer' or line == 'Answer Question' or 'Helpful' in line:
                continue
            elif line != 'Interview Questions' and flag:
                answer_questions = answer_questions + line + " "

        return answer_questions


    funcs = [
        scrape_emp_title,
        scrape_interview,
        scrape_interview_questions
    ]

    fdict = dict((s, f) for (s, f) in zip(SCHEMA, funcs))

    return fdict[field](interview)


def more_pages():
    try:
        # paging_control = browser.find_element_by_class_name('pagingControls')
        next_ = browser.find_element_by_class_name('next')
        next_.find_element_by_tag_name('a')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False


def go_to_next_page():
    logger.info(f'Going to page {page[0] + 1}')
    # paging_control = browser.find_element_by_class_name('pagingControls')
    next_ = browser.find_element_by_class_name(
        'next').find_element_by_tag_name('a')
    browser.get(next_.get_attribute('href'))
    time.sleep(1)
    page[0] = page[0] + 1


def no_reviews():
    return False
    # TODO: Find a company with no reviews to test on


def no_interviews():
    return False
    # TODO: Find a company with no interviews to test on

def navigate_to_interviews(company, location):
    logger.info('Navigating to company interviews')

    browser.get(args.url)
    time.sleep(1)

    inputElement_place = browser.find_element_by_id("KeywordSearch")
    # company= 'nice'
    inputElement_place.send_keys(company)

    inputElement_location = browser.find_element_by_id("LocationSearch").clear()
    # location= 'Tel Aviv (Israel)'
    browser.find_element_by_id("LocationSearch").send_keys(location)

    inputElement_place.send_keys(Keys.ENTER)
def get_interviews_from_page():

    interviews_details = None
    while interviews_details == None:
        try:
            try:
                interviews_place = browser.find_elements_by_class_name("interviewEmployerList")[0]
                time.sleep(8)
                print('go into interview page...')
                interviews_place_path = interviews_place.find_element_by_tag_name('a').get_attribute('href')
                time.sleep(6)
                browser.get(interviews_place_path)
                print('create the data...')
                time.sleep(10)
                interviews_details = browser.find_element_by_tag_name('ol').text.split('Helpful')
                time.sleep(8)
            except:
                interviews_place=browser.find_elements_by_id("EmployerInterviews")[0]
                if(interviews_place.text!= ''):
                    interviews_details= interviews_place.text
                    # print(interviews_details, 'interviews_details4')
                    return interviews_details

                time.sleep(5)
                interviews_details= interviews_place.find_elements_by_tag_name('li')
                time.sleep(5)
                print(interviews_details, 'interviews_details4')

        except:
            pass
            break

    time.sleep(1)
    return interviews_details


    if no_interviews():
        logger.info('No interviews to scrape. Bailing!')
        return False


def sign_in():
    logger.info(f'Signing in to {args.username}')

    url = 'https://www.glassdoor.com/profile/login_input.htm'
    browser.get(url)

    # import pdb;pdb.set_trace()

    email_field = browser.find_element_by_name('username')
    password_field = browser.find_element_by_name('password')
    submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')

    email_field.send_keys(args.username)
    password_field.send_keys(args.password)
    submit_btn.click()

    time.sleep(3)
    browser.get(args.url)

def get_browser():
    logger.info('Configuring browser')
    chrome_options = wd.ChromeOptions()
    if args.headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser


def get_current_page():
    logger.info('Getting current page number')
    paging_control = browser.find_element_by_class_name('pagingControls')
    current = int(paging_control.find_element_by_xpath(
        '//ul//li[contains\
        (concat(\' \',normalize-space(@class),\' \'),\' current \')]\
        //span[contains(concat(\' \',\
        normalize-space(@class),\' \'),\' disabled \')]')
        .text.replace(',', ''))
    return current


def verify_date_sorting():
    logger.info('Date limit specified, verifying date sorting')
    ascending = urllib.parse.parse_qs(
        args.url)['sort.ascending'] == ['true']

    if args.min_date and ascending:
        raise Exception(
            'min_date required reviews to be sorted DESCENDING by date.')
    elif args.max_date and not ascending:
        raise Exception(
            'max_date requires reviews to be sorted ASCENDING by date.')


browser = get_browser()
page = [1]
idx = [0]
date_limit_reached = [False]
limit_pages=110


def hasNumbers(param):
    return any(char.isdigit() for char in param)


def extract_interviews_from_page(interviews, interview_jobs):

    interviews_current_page= {}

    def is_relevant_interview(interview, interview_jobs):
        flag= False
        interview_details=""
        try:
            if isinstance(interview, str):
                interview_details = interview.split('\n')
            else:
                interview_details= interview.text.split('\n')
            while len(interview_details)!=0 and (interview_details[0]==''\
                    or hasNumbers(interview_details[0])):
                interview_details.remove(interview_details[0])
                flag=True


            if len(interview_details)>1:
                if flag:
                    interview_job= interview_details[0]
                else:
                    interview_job= interview_details[1]

                interview_job_words= interview_job.split(' ')
                for word in interview_job_words:
                    if(word.lower() in interview_jobs):
                        return True
                else:
                    return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def extract_interview(interview):
        res = {}
        if(isinstance(interview, str)):
            interview= interview.split('\n')
        else:
            interview= interview.text.split('\n')
        for field in SCHEMA:
            res[field] = scrape(field, interview)

        assert set(res.keys()) == set(SCHEMA)
        return res


    if not isinstance(interviews, list):
        interviews= interviews.split('Helpful')

    for interview in interviews:
        if is_relevant_interview(interview, interview_jobs):
            data = extract_interview(interview)
            interviews_current_page[data['Job title']]= data
    return interviews_current_page


def interview_main(company,location,job_title):
    def synony_jobs(job_title):
        # return ['Software']
        return [job_title.lower()]

    pages=0
    logger.info(f'Scraping up to {args.limit} interviews.')

    res = pd.DataFrame([], columns=SCHEMA)

    interview_jobs= synony_jobs(job_title)

    sign_in()
    interviews_exist=[]
    if not args.start_from_url:
        navigate_to_interviews(company, location)
        time.sleep(5)
        interviews_exist = get_interviews_from_page()
        if not interviews_exist:
            return
    else:
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)

    interviews_df = extract_interviews_from_page(interviews_exist, interview_jobs)
    for found in list(interviews_df.values()):
        df_tmp= {'Job title':found['Job title'],
                    'Interview':found['Interview'] ,'Interview Questions' : found['Interview Questions']}
        res=res.append(df_tmp, ignore_index=True)
        print(res)

    while more_pages() and \
            len(res) < args.limit and \
            pages< limit_pages:
        go_to_next_page()
        pages= pages+1
        interviews_exist_urls = get_interviews_from_page()
        interviews_exist=[]

        if(isinstance(interviews_exist_urls[0],str)):
            interviews_exist = interviews_exist_urls

        else:        
            for inter in interviews_exist_urls:
                if inter.text!='' and hasNumbers(inter.text.split('\n')[0][0:20]):
                    interviews_exist.append(inter.text)


        interviews_df = extract_interviews_from_page(interviews_exist, interview_jobs)
        for found in list(interviews_df.values()):
            df_tmp = {'Job title': found['Job title'],
                    'Interview': found['Interview'], 'Interview Questions': found['Interview Questions']}
            res=res.append(df_tmp, ignore_index=True)
            print(res)

    path='backend/interview_outputs/'+company+'_'+job_title+'Jobs_interviews.csv'
    res.to_csv(str(path))
    print('interviews file updated')

if __name__ == '__main__':
    company = input("Enter the company name: ")
    location = input("Enter the job location : ")
    job_title = input("Enter the job title : ")
    interview_main(company,location,job_title )
    browser.close()


