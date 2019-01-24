import requests
import re
import data
import time
import sys
import os
import argparse
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# Scraper

def get_links():
    links = []
    keyword = 'server-list'
    index_url = 'http://www.proxyserverlist24.top/'
    page = requests.get(index_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    temp_links = soup.find_all('a')
    for atag in temp_links:
        link = atag.get('href')
        if atag.get('href') is None:
            pass
        elif keyword in link and '#' not in link and link not in links:
            links.append(link)
    return links

def scrape(links):
    url = links[0]
    page = requests.get(url)
    ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', page.text)
    return max_proxies(ip_list,data.max)


def save_scraped(ip_list):
    if os.path.isfile(data.filename):
        os.remove(data.filename)
    with open(data.filename,'a') as wfile:
        for ip in ip_list:
            wfile.write(ip)
            wfile.write('\n')
    print('[!] {} Proxies were scraped and saved ! '.format(len(ip_list)))


def max_proxies(ip_list, max):
    ip_list = ip_list.copy()
    return ip_list[0:max]

# Checker

def is_good(p):
    proxy = {'https' : '{}'.format(p)}
    try :
        r = requests.get(data.url,proxies=proxy,headers=data.headers,timeout=data.timeout)
        if r.status_code is 200:
            hits_count(p)
            save_hits(p)
    except (requests.exceptions.Timeout,
            requests.exceptions.ProxyError,
            requests.exceptions.SSLError,
            requests.exceptions.ConnectionError) as e:
        pass


def save_hits(p):
    with open('{} Checked ProxyList.txt'.format(data.date),'a') as wfile:
        wfile.write(p)
        wfile.write('\n')

def hits_count(p):
    data.hits += 1
    print('[+] HIT - {}'.format(p))

def hits():
    print('[!] {} Proxies checked and saved !'.format(data.hits))

def check_args(args=None):
    parser = argparse.ArgumentParser(description='A script to quickly get alive HTTPS proxies')
    parser.add_argument('-u', '--url', type=str, help='url to check proxy against', default='https://www.google.com')
    parser.add_argument('-m', '--max', type=int, help='maximum proxies to scrape', default=800)
    parser.add_argument('-t', '--timeout', type=int, help='set proxy timeout limit', default=8)
    parser.add_argument('-st', '--set-threads', type=int, help='set number of threads to run', default=30)


    results = parser.parse_args(args)
    return(results.url, results.max, results.timeout, results.set_threads)

def check(p_list):

    pool = ThreadPool(data.num_threads)
    pool.map(is_good,p_list)
    pool.close()
    pool.join()

def main():

    save_scraped(scrape(get_links()))
    p_list = open(data.filename).read().splitlines()
    check(p_list)
    hits()

if __name__ == "__main__":
    data.url, data.max, data.timeout, data.num_threads = check_args(sys.argv[1:])
    main()
