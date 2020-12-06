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
interview_jobs= ['Software']

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
parser.add_argument('-l', '--limit', default=25,
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
        with open('secret.json') as f:
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
        return interview[1]

    def scrape_application(interview):
        flag= False
        app=""
        for line in interview:
            if line=='Application':
                flag= True
            elif line!='Application' and not flag:
                continue
            elif line!='Application' and flag:
                app=app+ line+ " "
        return app

    def scrape_interview(interview):
        flag = False
        Interview = ""
        for line in interview:
            if line == 'Interview':
                flag = True
            elif line != 'Interview' and not flag:
                continue
            elif line != 'Interview' and flag:
                app = app + line + " "
        return app

    def scrape_interview_questions(interview):
        flag = False
        answer_questions = ""
        for line in interview:
            if line == 'Answer Questions':
                flag = True
            elif line != 'Answer Questions' and not flag:
                continue
            elif line != 'Answer Questions' and flag:
                app = app + line + " "
        return app


    funcs = [
        scrape_emp_title,
        scrape_application,
        scrape_interview,
        scrape_interview_questions
    ]

    fdict = dict((s, f) for (s, f) in zip(SCHEMA, funcs))
    fdict['Job title'](interview)
    fdict['Application'](interview)

    return fdict[field](interview)


def more_pages():
    try:
        # paging_control = browser.find_element_by_class_name('pagingControls')
        next_ = browser.find_element_by_class_name('pagination__PaginationStyle__next')
        next_.find_element_by_tag_name('a')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False


def go_to_next_page():
    logger.info(f'Going to page {page[0] + 1}')
    # paging_control = browser.find_element_by_class_name('pagingControls')
    next_ = browser.find_element_by_class_name(
        'pagination__PaginationStyle__next').find_element_by_tag_name('a')
    browser.get(next_.get_attribute('href'))
    time.sleep(1)
    page[0] = page[0] + 1


def no_reviews():
    return False
    # TODO: Find a company with no reviews to test on


def no_interviews():
    return False
    # TODO: Find a company with no interviews to test on

def navigate_to_interviews():
    logger.info('Navigating to company interviews')

    browser.get(args.url)
    time.sleep(1)

    inputElement = browser.find_element_by_id("KeywordSearch")
    inputElement.send_keys('nice')
    inputElement.send_keys(Keys.ENTER)


    try:
        interviews_place = browser.find_elements_by_class_name("interviewEmployerList")[0]
        time.sleep(1)
        time.sleep(1)
    except:
        pass

    time.sleep(1)
    interviews_place_path = interviews_place.find_element_by_tag_name('a').get_attribute('href')
    browser.get(interviews_place_path)
    interviews_details = browser.find_element_by_tag_name('ol').text.split('Helpful')

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

def extract_interviews_from_page(interviews):

    def is_relevant_interview(interview, interview_jobs):
        try:
            interview_details= interview.split('\n')
            if len(interview_details)>1:
                interview_job= interview_details[1]

                interview_job_words= interview_job.split(' ')
                for word in interview_job_words:
                    if(word in interview_jobs):
                        return True
                else:
                    return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def extract_interview(interview):
        interview= interview.split('\n')
        for field in SCHEMA:
            res[field] = scrape(field, interview)

        assert set(res.keys()) == set(SCHEMA)
        return res

    res = {}

    for interview in interviews:
        if is_relevant_interview(interview, interview_jobs):
            data = extract_interview(interview)
            logger.info(f'Scraped data for "{data["review_title"]}"\({data["date"]})')
            res.loc[idx[0]] = data
        else:
            logger.info('Discarding a featured review')
        idx[0] = idx[0] + 1

    if args.max_date and \
        (pd.to_datetime(res['date']).max() > args.max_date) or \
            args.min_date and \
            (pd.to_datetime(res['date']).min() < args.min_date):
        logger.info('Date limit reached, ending process')
        date_limit_reached[0] = True

    return res


def interview_main():
    logger.info(f'Scraping up to {args.limit} interviews.')

    res = pd.DataFrame([], columns=SCHEMA)

    sign_in()
    interviews_exist=[]
    if not args.start_from_url:
        interviews_exist = navigate_to_interviews()
        if not interviews_exist:
            return
    else:
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)

    interviews_df = extract_interviews_from_page(interviews_exist)
    res = res.append(interviews_df)


    while more_pages() and \
            len(res) < args.limit and \
            not date_limit_reached[0]:
        go_to_next_page()
        interviews_exist = navigate_to_interviews()
        res = res.append(interviews_exist)

    logger.info(f'Writing {len(res)} reviews to file {args.file}')
    res.to_csv(args.file, index=False, encoding='utf-8')

    end = time.time()
    logger.info(f'Finished in {end - start} seconds')


if __name__ == '__main__':
    interview_main()
    # main()
