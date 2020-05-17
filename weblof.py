import requests
import re
def get_SP500_NQ100_discount():
    response = requests.get(url='https://www.haoetf.com') 
    r = re.compile(r'^(.*)(/qdii/161125)', re.DOTALL)
    m = r.match(response.text)

    index = m.span(2)
    text = response.text[index[0]:index[0]+100]
    r = re.compile(r'(/qdii/161125)(.*)>(.*)%<', re.DOTALL)
    m = r.match(text)
    sp500 = m.group(3)
    # print(sp500)

    r = re.compile(r'^(.*)(/qdii/161130)', re.DOTALL)
    m = r.match(response.text)

    index = m.span(2)
    text = response.text[index[0]:index[0]+100]
    r = re.compile(r'(/qdii/161130)(.*)>(.*)%<', re.DOTALL)
    m = r.match(text)
    nq100 = m.group(3)
    # print(nq100)

    return float(sp500), float(nq100)

if __name__ == "__main__":
    sp500, qn100 = get_SP500_NQ100_discount()
    print(sp500)
    print(qn100)