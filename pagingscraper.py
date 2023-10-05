from bs4 import BeautifulSoup
import pandas as pd
import requests

page_list = ["Page$" + str(i) for i in range(1, 56)]

rows = []

def scrapelist(list):
    count1 = 0

    cookies = {
        'ASP.NET_SessionId': 'orjno0fquq5zsvpgq22knvuv',
    }

    headers = {
        'authority': 'forestsclearance.nic.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'ASP.NET_SessionId=orjno0fquq5zsvpgq22knvuv',
        'referer': 'https://forestsclearance.nic.in/Wildnew_Online_Status_New.aspx',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    
    while count1 < len(list):
        url = list[count1]
        page = requests.get(
        url,
        cookies=cookies,
        headers=headers,
        verify=False
        )

        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find_all("span", {"class": "li2"})

        count2 = 0
        row_dict = {}


        for result in results:
            splitdata = result.text.split(": ")

            if len(splitdata) < 2:
                continue

            key = splitdata[0].strip()
            value = splitdata[1].strip()
            
            if "Unnamed" in key:
                continue
            row_dict[key] = value
            count2 += 1
        
        tables = soup.find_all("table", {"class": "ez1"})

        for table in tables:
            table_rows = table.find_all('tr')
            if len(table_rows) >= 3:
                title = table_rows[0].string
                header_row = table_rows[1].find_all("th")
                data_rows = table_rows[2:]
                row_dict[title] = " "

                header_strings = [*map(lambda arg : arg.text.strip(), header_row)]
                header_strings.pop(0)


                datacount = 0
                datastr = ""
                for data_row in data_rows:
                    data_strings = [*map(lambda arg: arg.text.strip(), data_row.find_all("td"))]
                    data_strings.pop(0)

                    for hs, ds in zip(header_strings, data_strings):
                        row_dict[hs + "(" + title.strip() + ")" + datastr] = ds

                    datacount = datacount + 1
                    datastr = str(datacount)

        rows.append(row_dict)
        count1 += 1
    


for page in page_list:
    baseurl = "https://forestsclearance.nic.in/"
    cookies = {
        'ASP.NET_SessionId': 'orjno0fquq5zsvpgq22knvuv',
    }

    headers = {
        'authority': 'forestsclearance.nic.in',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'ASP.NET_SessionId=orjno0fquq5zsvpgq22knvuv',
        'origin': 'https://forestsclearance.nic.in',
        'referer': 'https://forestsclearance.nic.in/Wildnew_Online_Status_New.aspx',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-microsoftajax': 'Delta=true',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$Button1',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': page,
        '__VIEWSTATE': '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',
        '__VIEWSTATEGENERATOR': 'E2DF0C67',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': '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',
        'ctl00$ContentPlaceHolder1$ddlyear': '-All Years-',
        'ctl00$ContentPlaceHolder1$ddl3': 'Select',
        'ctl00$ContentPlaceHolder1$ddlcategory': '-Select All-',
        'ctl00$ContentPlaceHolder1$DropDownList1': '-Select All-',
        'ctl00$ContentPlaceHolder1$txtsearch': '',
        'ctl00$ContentPlaceHolder1$HiddenField1': '',
        'ctl00$ContentPlaceHolder1$HiddenField2': '',
        '__ASYNCPOST': 'true',
        'ctl00$ContentPlaceHolder1$Button1': 'SEARCH',
    }

    response = requests.post(
        'https://forestsclearance.nic.in/Wildnew_Online_Status_New.aspx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False
    )

    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.find_all("a", {"title": "click on for Viewing Report of PartI"})
    hreflist = []
    for res in results:
        href = res.attrs["href"][2:]
        hreflist.append(baseurl + href)

    scrapelist(hreflist)
    print("finished " + page)

pdata = pd.DataFrame(rows)
pdata.to_csv("data/newdata.csv")
