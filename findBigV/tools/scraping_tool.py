import time
import requests
import json

def scrape_weibo(url: str):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "client-version": "v2.47.17",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "server-version": "v2025.01.02.1",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": "T4AzRKt61NL_O9l_iaIrGPRG"
    }
    
    cookies = {
        "cookie": """XSRF-TOKEN=T4AzRKt61NL_O9l_iaIrGPRG; SCF=Ahj2i1VRaPK2qUEaFqIZ6NB82aePsVcgmw8JnvLMTtKm9ezexPHM4uo1zD05FzNN-cHeYwrKfpscr5LxlVBa8pM.; SUB=_2A25KcvaCDeRhGeBG4lIT-SbKzT-IHXVpDnZKrDV8PUNbmtANLRX_kW9NQfJlbwqe05JOYp1S3knd4nVy2FmlcBtb; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5jUTZhm.dIlLOsqYroljVx5NHD95Qc1h.7eo.RSoq0Ws4DqcjAi--fi-88iKnRi--fiKn7iK.4i--Xi-i2i-27i--NiKLWiKnXi--fi-82i-20i--RiKyWiKnEeo5p15tt; ALF=02_1738413010; WBPSESS=Z_4pWIJaU9EQ939HfcKbeP2LNOkDcdg1vlxsV9KvIIAZZ2U1YHQwmDn012Qy9xIpYOXkZyZoRAGv8ln3kSaluMDDWLkCBuQk_y6t9G4uApaxG7mb7hi5wFdPm-6Z209TOVjNaIGBoTU2P7PFIJmlLg=="""
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(3)
    return response.text

def get_data(id: str):
    url = f"https://weibo.com/ajax/profile/detail?uid={id}"
    html_str = scrape_weibo(url)
    response = json.loads(html_str)
    return response
