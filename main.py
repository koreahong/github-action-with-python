import os
from datetime import datetime
from pytz import timezone
from crawling_yes24 import parsing_beautifulsoup, extract_book_data
from github_utils import get_github_repo, upload_github_issue

if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "github-action-with-python"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")
    category = {
            'IT': "http://www.yes24.com/24/Category/NewProductList/001001003?sumGb=01&ParamSortTp=05&FetchSize=40",
            '경제/경영': "http://www.yes24.com/24/Category/NewProductList/001001025?sumGb=01&ParamSortTp=05&FetchSize=40",
            '인문학': "http://www.yes24.com/24/Category/NewProductList/001001019?sumGb=01&ParamSortTp=05&FetchSize=40",
            '자기계발': "http://www.yes24.com/24/Category/NewProductList/001001026?sumGb=01&ParamSortTp=05&FetchSize=40"
        }
    
    upload_contents = ''
    issue_title = f"YES24 {', '.join(category.keys())} - 신간 도서 알림({today_date})"
    
    for cat, url in category.items():
        upload_contents += f"<h1>{cat}</h1>" + "<br/>\n"
        yes24_it_new_product_url = url
        soup = parsing_beautifulsoup(yes24_it_new_product_url)
        upload_contents += extract_book_data(soup) + "<br/>\n"
        
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")
