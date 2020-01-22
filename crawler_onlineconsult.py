import requests

from bs4 import BeautifulSoup

import pandas

print("start")

web_content_list = []

web_content_list_2 = []

for page in range(1, 53):

    base = "https://so.haodf.com/index/search?kw=%E6%8B%89%E8%80%83%E6%B2%99%E8%83%BA&page="

    url = ("%s%s" % (base, page))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get(url, headers=headers)

    c = r.content

    soup = BeautifulSoup(c, "html.parser")

    content1 = soup.find_all("div", {'class': 'sc-wenzhang'})

    content2 = soup.find_all("div", {'class': 'sc-wenzhen'})

    print(page)

    for c in content1:

        web_content_dict = {}

        web_content_dict["type"] = "articles"

        web_content_dict["title"] = c.find("a", {"class": ["sc-wz-title-a", "a-title"]}).text.replace("\r", "").replace(
            "\n", "")

        web_content_dict["date"] = c.find("span", {"class": "sc-wz-f-time"}).text.replace("\r", "").replace("\n", "")

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

        # web_content_dict["text"] = c.find("div", {"class": "sc-wz-txt"}).text.replace("\r","").replace("\n", "")

        web_content_list.append(web_content_dict)

    for x in content2:

        web_content_dict2 = {}

        web_content_dict2["type"] = "consultation"

        for link in x.find_all("a", {"class": "sc-w-title-a"}):

            consult_url = link.get("href")

            if "wenda" in consult_url:
                web_content_dict2["type"] = "clinical"

                web_content_dict2["url"] = "http:" + consult_url

                continue

            print(consult_url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            consult_r = requests.get(consult_url, headers=headers)

            consult_c = consult_r.content

            y = BeautifulSoup(consult_c, "html.parser")

            web_content_dict2["url"] = consult_url

            # title

            web_content_dict2["title"] = y.find("div", {"class": ["fl-title", "ellps"]}).text.replace("\r", "").replace(
                "\n", "")

            # first post date

            if len(y.find_all("div", {"class": "f-c-l-date"})) > 1:

                web_content_dict2["date"] = y.find_all("div", {"class": "f-c-l-date"})[1].text.replace("\r",
                                                                                                       "").replace("\n",
                                                                                                                   "")

            else:

                web_content_dict2["date"] = y.find("div", {"class": "f-c-l-date"}).text.replace("\r", "").replace("\n",
                                                                                                                  "")

            # doctor & hospital

            doc = y.find("div", {"class": "profile-text"})

            name = doc.find("h1", {"class": "doctor-name"}).text.replace("\r", "").replace("\n", "")

            hospital = doc.find("a", {"style": "margin-right:10px;"}).text.replace("\r", "").replace("\n", "")

            web_content_dict2["doctor"] = name

            web_content_dict2["doc_hospital"] = hospital

            # patient information

            # if len(y.find_all("div", {'class': ['f-card', 'clearfix', 'js-f-card']})) >1:

            #    patient = y.find_all("div", {'class': ['f-card', 'clearfix', 'js-f-card']})[1]

            # else:

            #    patient = y.find("div", {'class' : ['f-card', 'clearfix', 'js-f-card']})

            # p_info = ""

            # print(patient)

            # for p1 in patient.find_all("h4",{'class': ['f-c-r-w-subtitle']}):

            #    p1add = p1.text.replace("\r","").replace("\n", "")

            #    p_info = p1add

            #    print(p_info)

            #    for p2 in patient.find_all("p", {'class': 'f-c-r-w-text'}):

            #        p2add = p2.text.replace("\r","").replace("\n", "")

            #        p_info = p_info + ": " + p2add

            #        print(p_info)

            # web_content_dict2["patient_info"] = p_info

            # text

            text = y.find_all("p", {'class': ['f-c-r-w-text', 'f-c-r-doctext']})

            text_ls = ""

            for t in text:
                t1 = t.text.replace("\r", "").replace("\n", "")

                text_ls = text_ls + "," + t1

            web_content_dict2["text"] = text_ls

            # doctor text

            # text_doc = y.find_all("p", {'class': ["f-c-r-w-title",'f-c-r-doctext',"f-c-r-w-subtitle","f-c-r-w-text"})

            # text_d = ""

        # for td in text_doc:

        #   t2 = td.text.replace("\r","").replace("\n", "")

        #  text_d = text_d + "," + t2

        # web_content_dict2["text_doc"] = text_d

        if x.find("span", {"class": "sc-w-f-talk"}) is not None:

            web_content_dict2["n_conversation"] = x.find("span", {"class": "sc-w-f-talk"}).text.replace("\r",
                                                                                                        "").replace(
                "\n", "")

        else:

            web_content_dict2["n_conversation"] = "NA"

        # To store the dictionary to into a list

        web_content_list_2.append(web_content_dict2)

# To make a dataframe with the list

df_article = pandas.DataFrame(web_content_list)

df_consulation = pandas.DataFrame(web_content_list_2)

# To write the dataframe to a csv file

df_article.to_csv("Output_article.csv", encoding='utf_8_sig')

df_consulation.to_csv("Output_consultation.csv", encoding='utf_8_sig')

print("end")
