import re
import lxml
from lxml import etree
import requests

def get_content():
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    url = 'https://www.lejobadequat.com/emplois'
    response = requests.get(
        url,
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        )
    print(response.status_code)
    #print(response.text)
    with open('dz-4-content', 'w', encoding='utf-8') as f:
        f.write(response.text)

def parse_jobs():
    with open('dz-4-content', 'r', encoding='utf-8') as f:
        content = f.read()
        #print(content.__len__())
    
    pattern = r'<h3 class="jobCard_title m-0">(.*)<\/h3>'
    title_pattern = r'<h3 class="jobCard_title m-0">(.*)<\/h3>'
    url_pattern = r'<a href="(.*)" title'

    card_titles = re.findall(pattern, content)
    for i, c_title in enumerate(card_titles, 1):
            print(f"{i}. {c_title}")

    tree = etree.HTML(content)
    xpath = '//article'
    articles = tree.xpath(xpath)
    jobs = []
    #print(article.tostring(element, encoding='unicode', pretty_print=True))
   
    for i, article in enumerate(articles, 1):
           article_content = etree.tostring(article, encoding='unicode', pretty_print=True)
           title = re.findall(title_pattern, article_content)
           url = re.findall(url_pattern, article_content)
           #print(f"{i}. title: {title[0]} url: {url[0]}")
           jobs.append(
                {
                     "title": title[0],
                     "url": url[0]
                }
           )

    print(jobs)


if __name__ == "__main__":
    parse_jobs()
