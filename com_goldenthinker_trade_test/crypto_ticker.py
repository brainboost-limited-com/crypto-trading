import requests

headers = {
    'authority': 'crypto.com',
    'exchange-token': '',
    'exchange-language': 'en_US',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'content-type': 'application/json;charset=utf-8',
    'accept': 'application/json, text/plain, */*',
    'dnt': '1',
    'exchange-client': 'pc',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://crypto.com/exchange/trade/spot/BTC_USDC',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cookie': '__cfduid=d267a6aeca9214d3e055a5335d744bb061615460281; _gcl_au=1.1.1942430318.1615461537; _fbp=fb.1.1615461546741.1732236189; intercom-id-ruozuwky=0ceb447f-6410-4a9d-85b4-02f0c34be484; OptanonAlertBoxClosed=2021-03-11T11:24:13.039Z; intercom-session-ruozuwky=; _ga=GA1.1.1392504052.1617385281; _rdt_uuid=1617978396231.4f4449bc-dde3-40f0-b607-4c3fb953d132; OptanonConsent=isIABGlobal=false&datestamp=Fri+Apr+09+2021+15%3A26%3A36+GMT%2B0100+(Irish+Standard+Time)&version=6.5.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=%3B&AwaitingReconsent=false; __cf_bm=a9f72bec601492135378ac4d3e264c81f734ae2e-1617984680-1800-AVVib/4iqLF7n4W4xCAUTn8ad5V+C0+r4HdeFKCvCPUXBnXgwiqwQvBEJJ6Rw82VmLetxm/1isU/oiVdhNpS+nk=; _ga_KTR8M2WC2H=GS1.1.1617984694.3.0.1617984694.0; __cfruid=8f321857f6db8c765e4d8ba2c2be86a700c0d400-1617984763; crypto.locale=en; ab.storage.deviceId.f0b34276-b425-488f-b279-4aa6ec4ad814=%7B%22g%22%3A%223c4cc76a-2bc1-cb88-ca6b-89bb955b64e9%22%2C%22c%22%3A1617984767086%2C%22l%22%3A1617984767086%7D; ab.storage.sessionId.f0b34276-b425-488f-b279-4aa6ec4ad814=%7B%22g%22%3A%2255e82fba-49a4-4d9f-5ab5-448dd3982781%22%2C%22e%22%3A1617986567103%2C%22c%22%3A1617984767085%2C%22l%22%3A1617984767103%7D; ajs_anonymous_id=%22a1ca1c2b-4a22-4ce1-8768-b626147b551d%22',
}


print("CRYPTO.COM PUBLIC TICKER TESTING")


response = requests.get('https://crypto.com/fe-ex-api/market-data/v2/public/get-ticker', headers=headers)
print(response.content)

print("CRYPTO.COM PUBLIC API TESTING")


