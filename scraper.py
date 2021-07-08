import time
import pandas as pd
import requests
from requests_html import HTML
import sys


def extract_from_url(url):
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        print("error")
        return "error while finding the data"
    html_text = r.text
    formatted_html = HTML(html=html_text)
    data_summary = formatted_html.find(".question-summary")
    data = []
    classes_needed = ['.vote-count-post', '.question-hyperlink']
    final_data = []
    for question in data_summary:
        question_votes = question.find('.vote-count-post', first=True).text
        question_data = question.find('.question-hyperlink', first=True).text
        question_tags = question.find('.tags', first=True).text
        data = {}
        data["question"] = question_data
        data["votes"] = question_votes
        data["tags"] = question_tags
        final_data.append(data)
    return final_data


def scrape_stack(tag="python", page=1, pagesize="20", sortby="votes"):
    base_url = "https://stackoverflow.com/questions/tagged/"
    all_page_data = []
    # iterating through each pages
    for i in range(1, page + 1):
        url = f"{base_url}{tag}?tab={sortby}&page={i}&pagesize={pagesize}"
        all_page_data += extract_from_url(url)
    df = pd.DataFrame(all_page_data)
    df.to_csv(f"{tag}.csv", index=False)

if __name__ == '__main__':
    tag = sys.argv[1]
    scrape_stack(tag=tag, page=1, pagesize="20", sortby="votes")
