import requests
from bs4 import BeautifulSoup
import pandas

web_content_list = []
web_content_list_2 = []

for page in range(1,50):

    base = "https://so.haodf.com/index/search?kw=%E6%8B%89%E8%80%83%E6%B2%99%E8%83%BA&page="

    url = ("%s%s" % (base,page))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    content1 = soup.find_all("div", {'class': 'sc-wenzhang'})
    content2 = soup.find_all("div", {'class': 'sc-wenzhen'})

    for c in content1:
            web_content_dict = {}
            web_content_dict["type"] = "articles"
            web_content_dict["title"] = c.find("a", {"class": ["sc-wz-title-a", "a-title"]}).text.replace("\r","").replace("\n", "")
            web_content_dict["date"] = c.find("span", {"class": "sc-wz-f-time"}).text.replace("\r", "").replace("\n","")
            web_content_dict["doctor"] = c.find("span", {"class": "sc-wz-f-doc"}).text.replace("\r", "").replace("\n", "")
            web_content_dict["n_read"] = c.find("span", {"class": "sc-wz-f-read"}).text.replace("\r", "").replace("\n", "")
            if c.find("span", {"class": "sc-wz-f-comment"}) is not None:
                web_content_dict["n_comment"] = c.find("span", {"class": "sc-wz-f-comment"}).text.replace("\r", "").replace(
                "\n", "")
            else:
                web_content_dict["n_comment"] = "NA"

            if c.find("span", {"class": "sc-wz-f-positiverate"}) is not None:
                web_content_dict["rate"] = c.find("span", {"class": "sc-wz-f-positiverate"}).text.replace("\r", "").replace(
                "\n", "")
            else:
                web_content_dict["rate"] = "NA"
            #web_content_dict["text"] = c.find("div", {"class": "sc-wz-txt"}).text.replace("\r","").replace("\n", "")

            web_content_list.append(web_content_dict)

    for x in content2:
            web_content_dict2 = {}
            web_content_dict2["type"] = "consultation"
            web_content_dict2["title"] = x.find("a", {"class": ["sc-wz-title-a", "a-title"]}).text.replace("\r", "").replace(
            "\n", "")
            web_content_dict2["date"] = x.find("span", {"class": "sc-w-f-time"}).text.replace("\r", "").replace("\n", "")

            if x.find("div",{"class":"sc-w-ask"}) is not None:
                web_content_dict2["question"] = x.find("div", {"class": "sc-w-ask"}).text.replace("\r","").replace("\n", "")
            else:
                web_content_dict2["question"] = "NA"

            if x.find("div",{"class":"sc-w-answer"}) is not None:
                web_content_dict2["answer"] = x.find("div", {"class": "sc-w-answer"}).text.replace("\r","").replace("\n", "")
            else:
                web_content_dict2["answer"] = "NA"

            if x.find("span",{"class": "wc-w-a-doc"}) is not None:
                web_content_dict2["doctor"] = x.find("span",{"class":"wc-w-a-doc"}).text.replace("\r","").replace("\n", "")
            else:
                web_content_dict2["doctor"] = "NA"

            if x.find("span",{"class":"sc-w-f-disease"}) is not None:
                web_content_dict2["disease"] = x.find("span", {"class": "sc-w-f-disease"}).text.replace("\r","").replace("\n", "")
            else:
                web_content_dict2["disease"] = "NA"

            if x.find("span", {"class": "sc-w-f-talk"}) is not None:
                web_content_dict2["n_conversation"] = x.find("span", {"class": "sc-w-f-talk"}).text.replace("\r", "").replace(
                "\n", "")
            else:
                web_content_dict2["n_conversation"] = "NA"

            # To store the dictionary to into a list
            web_content_list_2.append(web_content_dict2)


# To make a dataframe with the list
df_article = pandas.DataFrame(web_content_list)
df_consulation = pandas.DataFrame(web_content_list_2)

# To write the dataframe to a csv file
df_article.to_csv("Output_article.csv")
df_consulation.to_csv("Output_consultation.csv")
