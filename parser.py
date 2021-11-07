import requests
from bs4 import BeautifulSoup


def code_to_url(get_func):
    def wrapper(*args):
        code = args[0]
        url = 'https://www.wildberries.ru/catalog/' + code + '/detail.aspx?targetUrl=GP#c' + code
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return get_func(soup)
    return wrapper


@code_to_url
def get_brand(*args):
    try:
        soup = args[0]
        brand = soup.find_all('span', {'data-link': 'text{:product^brandName}', })[0].text
    except IndexError:
        brand = 'Запрошенный артикул не существует'
    return brand


@code_to_url
def get_title(*args):
    soup = args[0]
    title = soup.find_all('span', {'data-link': 'text{:product^goodsName}', })[0].text
    return title


if __name__ == '__main__':
    print(get_brand('9842676'), sep='\n')
    print(get_title('9842676'), sep='\n')
