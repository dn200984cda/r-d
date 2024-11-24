import re
import requests
import sqlite3
import json
from lxml import etree

from bs4 import BeautifulSoup

def get_content():
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    url = 'https://www.bbc.com/sport'
    response = requests.get(
        url,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        )
    print(response.status_code)
    #print(response.text)
    with open('dz-6-content', 'w', encoding='utf-8') as f:
        f.write(response.text)

def bs_parse():
    with open('dz-6-content.html', 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')
    
    
    # url
    # //div[contains(@class, 'HierachichalCollectionsWrapper')]//div[contains(@class, 'Stack')]/a[not(contains(@href, 'comments'))]

    # topics
    # //div[contains(@class, 'TopicListWrapper')]//a
    # tree = etree.HTML(content)
    # xpath = "//div[contains(@class, 'HierachichalCollectionsWrapper')]//div[contains(@class, 'Stack')]/a[contains(@href, 'articles')]"
    # links = tree.xpath(xpath)
    # for i, article in enumerate(links, 1):
    #        article_content = etree.tostring(article, encoding='unicode', pretty_print=True)
    #        print(article_content)

    #news = soup.find('div', class_=re.compile('HierachichalCollectionsWrapper'))
    #print(news)
    #cards = news.find_all('div', class_=re.compile('.*Stack.*'))

    cards = soup.select('div[class*="HierachichalCollectionsWrapper"] div[class*="Stack"] a[href*="articles"]:not([href*="comments"])')
    print(cards.__len__())
    
    results = []
    for card in cards[:5]:
        url = card.get('href')
        directLink = 'https://www.bbc.com' + url
        print(directLink)
        #parse_page(directLink)
        results.append(parse_page(directLink))

    write_json(results)


def parse_page(url: str) -> dict:
    #print(url)
    response = requests.get(
        url,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        )
    soup = BeautifulSoup(response.text, 'lxml')
    # topics
    # //div[contains(@class, 'TopicListWrapper')]//a
    topicList =[]
    try:
        topics = soup.find('div', class_=re.compile('.*TopicListWrapper.*')).find_all('a')
        for topic in topics:
            topicList.append(topic.text)
    except:
        None

    return {'url': url, 'topics': topicList}

    
def parse_jobs():
    with open('dz-4-content', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<a href="([^"]+?)" title="([^"]+?)"'
    # title_pattern = r'<h3 class="jobCard_title m-0">(.*)<\/h3>'
    # url_pattern = r'<a href="(.*)" title'
    jobs = [
        {"url": url, "title": title} 
        for url, title in re.findall(pattern, content)
    ]
    
    return jobs

def write_db(data: list) -> None:
    filename = 'output.db'

    #create table
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists jobs(
            id integer primary key autoincrement,
            title text,
            url text
        )
    """
    cursor.execute(sql)

    #insert data
    for item in data:
        cursor.execute("""
            insert into jobs (title, url)
                values (?, ?)
        """, (item['title'], item['url']))

    conn.commit()
    
    conn.close()

def read_db() -> None:
    filename = 'output.db'

    #create table
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    #read info
    sql = """
        select id, title
        from jobs
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)

    conn.close()

def del_table() -> None:
    filename = 'output.db'

    #create table
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        DROP TABLE IF EXISTS jobs
    """
    cursor.execute(sql)
    conn.commit()
    conn.close()

def write_json(data: list) -> None:
    filename = 'output.json'

    data = [
        {
            'url': item['url'],
            'topics': item['topics']
        }
        for item in data
    ]

    with open(filename, mode='w') as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    bs_parse()

    #print(parse_page('https://www.bbc.com/sport/rugby-union/articles/c1wjynv81nwo'))

    #get_content()
    #jobs = parse_jobs()
    
    # for i, job in enumerate(jobs, 1):
    #   print(f"{i}. {job['title']} - {job['url']}")
    
    #write_db(jobs)
    #read_db()
    #del_table()

    #write_json(jobs)

