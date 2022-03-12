"""
github scrapper by code
due to 1,000 result limits by github api,
this program crawls 1,000 codes for each byte.

flow: doCrawlBySize -> searchQuery -> crawlPage -> pushItemsToDB
+------------+----------------------------------------------------------+
| Table name |                           data                           |
+------------+---------+----------------------------+-------------------+
| column     | type    | property                   | description       |
+------------+---------+----------------------------+-------------------+
| id         | INTEGER | Primary key, Autoincrement |                   |
+------------+---------+----------------------------+-------------------+
| file_name  | TEXT    |                            | name of file      |
+------------+---------+----------------------------+-------------------+
| path_name  | TEXT    |                            | path of file      |
+------------+---------+----------------------------+-------------------+
| sha        | TEXT    | Unique                     |                   |
+------------+---------+----------------------------+-------------------+
| url        | TEXT    |                            |                   |
+------------+---------+----------------------------+-------------------+
| code       | TEXT    |                            | encoded by base64 |
+------------+---------+----------------------------+-------------------+
| extension  | TEXT    |                            | extension         |
+------------+---------+----------------------------+-------------------+
| Q          | TEXT    |                            | query             |
+------------+---------+----------------------------+-------------------+
"""

from githubAPI import *
import wget
import os

config = ConfigParser()
config.read('config.ini')
CRAWLED_PAGE = 0
PATH = "/Users/zoniony/CVE/otf/dfont"

"""
TABLE data
id : INTEGER
file_name: TEXT
file_path: TEXT
sha : TEXT
url : TEXT
code : TEXT(BASE 64)
extension : TEXT
Q : TEXT
"""


def crawlPage(sizedQuery: str, pageNo: int) -> bool:
    sleep(10)
    logger(f"CRAWLING Page #{pageNo}")

    page = getSearchPageByCode(sizedQuery, pageNo)
    items = page['items']
    count = 0
    for file in page['items']:
        count += 1

    while(items == False or count != 10):
        page = getSearchPageByCode(sizedQuery, pageNo)
        items = page['items']
        count = 0
        for file in page['items']:
            count += 1      

    f = open("dfont.txt","a+")
    for file in page['items']:
        repos = file['html_url']
        name = file['name']
        f.writelines(repos+'\n')
       # wget.download(url=repos,out=os.path.join(PATH))
        logger(f"successful! create{name}")
        sleep(1)  
    f.close()
    return True


def searchQuery():
    global CRAWLED_PAGE
    sizedQuery = "extension:dfont"
    page = getSearchPageByCode(sizedQuery)
    # try
    results = page['total_count']
    if not results:
        logger(f"NO RESULTS IN !!")
    else:
        while CRAWLED_PAGE < results // 10:
            pageToCrawl = CRAWLED_PAGE + 1
            crawlPage(sizedQuery, pageToCrawl)
            CRAWLED_PAGE += 1
            sleep(5)

        return True

    # except Exception as e:
    #     logger(f"!!!! {cStr('Failed', 'r')} to crawl Size #{sizeIdx}, due to {e} !!!!")
    #     errLogger(page, e)
    #     return False



if __name__ == '__main__':
    searchQuery()
