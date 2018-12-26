# © Robert Geil 2018
import requests
import time
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)
    if response.status_code >= 400:
        print("Error, unable to scrape page {url}".format(url=url))
        return None
    if response.text is None or response.text == "":
        print("No DOM or an empty value was given")
        return None
    return response.text

# Returns a list of all public projects for each user
def get_projects(username):
    url = "https://github.com/{}/?tab=repositories".format(username)
    page = get_page(url)
    soup = BeautifulSoup(page, "lxml")
    repos_raw = soup.select("a[itemprop*=codeRepository]")
    repos = []
    for r in repos_raw:
        repos.append(r.text.strip("\n\t\r "))
    return repos


# Recursively gets files from a base tree for a GitHub project
# Returns a list of URLs
def get_files_urls(url):
    # Slow down requests to not overburden GitHub's servers
    time.sleep(1)
    page = get_page(url)
    soup = BeautifulSoup(page, "lxml")
    lines = soup.select("tr.js-navigation-item")
    urls_to_check = []
    for line in lines:
        # Don't follow directory if it is a parent directory
        if "up-tree" in line["class"]:
            continue
        filetype = line.select("svg")[0]["aria-label"]
        filename = line.select(".content")[0].select("a")[0]["title"]
        if filetype == "file":
            urls_to_check.append(url+"/"+filename)
        elif filetype == "directory":
            urls_to_check += get_files_urls(url+"/"+filename)
    return urls_to_check

# Returns the language of a program, and None if a language cannot be
# determined
def get_language(url):
    pos = url.rfind(".")
    ending = url[pos+1:]
    return "a"


# Returns an integer for the number of lines of code in a project
def get_line_count(url):
    soup = BeautifulSoup(get_page(url), "lxml")

    return 1



def get_language_frequency(username, project):
    base_url = "https://github.com/{u}/{p}/tree/master".format(u=username, p=project)
    urls = get_files_urls(base_url)
    languages = {}
    for url in urls:
        lang = get_language(url)
        if lang is not None:
            if lang in languages:
                languages[lang] += get_line_count(url)
            else:
                languages[lang] = get_line_count(url)
            # Wait to reduce stress on GitHub's servers
            time.sleep(1)
    return languages




urls = get_files_urls("https://github.com/Infirmarian/MovieBlog/tree/master")
for u in urls:
    print(u)