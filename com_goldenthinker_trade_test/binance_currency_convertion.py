# -*- coding: utf-8 -*-

import requests

class GTTrader:
    
    
    def __init__(self):
        self.headers = {
            'authority': 'www.binance.com',
            'x-trace-id': '5ab94ce4-0023-472d-8b84-24f740cafaae',
            'dnt': '1',
            'csrftoken': 'b8564db6762eb17c53b266628e8eca7d',
            'x-ui-request-trace': '5ab94ce4-0023-472d-8b84-24f740cafaae',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'en',
            'fvideo-id': '3130dbfcde75a2b493df80ae96ece9d70867e428',
            'sec-ch-ua-mobile': '?0',
            'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjkwMCwxNDQwIiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiODIwLDE0NDAiLCJzeXN0ZW1fdmVyc2lvbiI6Ik1hYyBPUyAxMS4wLjAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6ImVuLVVTIiwidGltZXpvbmUiOiJHTVQrMSIsInRpbWV6b25lT2Zmc2V0IjotNjAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMV8wXzApIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84OC4wLjQzMjQuMTgyIFNhZmFyaS81MzcuMzYiLCJsaXN0X3BsdWdpbiI6IkNocm9tZSBQREYgUGx1Z2luLENocm9tZSBQREYgVmlld2VyIiwiY2FudmFzX2NvZGUiOiJjZjRiMGUyOSIsIndlYmdsX3ZlbmRvciI6IkFwcGxlIiwid2ViZ2xfcmVuZGVyZXIiOiJBcHBsZSBNMSIsImF1ZGlvIjoiMTI0LjA0MzQ0OTY4NDc1MTk4IiwicGxhdGZvcm0iOiJNYWNJbnRlbCIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9EdWJsaW4iLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWODguMC40MzI0LjE4MiAoTWFjIE9TKSIsImZpbmdlcnByaW50IjoiNGU1NDU3OTM4M2M4NTNiMWNiZjcwNjY1YTM4ZTAyNDAiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIxNjE4MjEyOTU0NTA4SXdtYVdrQzcwaEZPa2ZTYzZ3biJ9',
            'bnc-uuid': '08e0a698-4fab-45fc-ba62-449b78caac4b',
            'clienttype': 'web',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'accept': '*/*',
            'origin': 'https://www.binance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.binance.com/en/convert',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            'cookie': 'cid=IvH3ZRoS; _h_desk_key=9f267458dc9f46198e4a0162d9809da9; s9r1=3DE30ECFF3F63DB930A23BCE4C9818D8; cr00=15678D973EBED4BDC480E82BA0A1CBBC; d1og=web.105633607.BC249ACCCAB6F3746F0529BAEDB302A9; r2o1=web.105633607.EDF4EBFF825B3AE64F778611569613B2; f30l=web.105633607.93365FE74FF2D98E613B667A1DE785FD; __BINANCE_USER_DEVICE_ID__={"17e88c0e55d5a10ce27ad490daf1e30a":{"date":1618212954666,"value":"1618212954508IwmaWkC70hFOkfSc6wn"}}; p20t=web.105633607.34F71238DFC24DFB2F43D9A8E1368F23; userPreferredCurrency=EUR_USD; bnc-uuid=08e0a698-4fab-45fc-ba62-449b78caac4b; _ga=GA1.2.1724420543.1618224179; _gid=GA1.2.31563713.1618224179; source=referral; campaign=www.binance.com; BNC_FV_KEY=3130dbfcde75a2b493df80ae96ece9d70867e428; BNC_FV_KEY_EXPIRE=1618252204028; fiat-prefer-currency=EUR',
            }
        

    def login():
        print("Visit: https://www.binance.com/en/login  and login with your normal username password")
        print("Then paste the new headers from the login here similar as in the constructor: ")



    def get_quote(headers,fromCoin,requestAmount,requestCoin,toCoin):
        headers = {
            'authority': 'www.binance.com',
            'x-trace-id': '5ab94ce4-0023-472d-8b84-24f740cafaae',
            'dnt': '1',
            'csrftoken': 'b8564db6762eb17c53b266628e8eca7d',
            'x-ui-request-trace': '5ab94ce4-0023-472d-8b84-24f740cafaae',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'en',
            'fvideo-id': '3130dbfcde75a2b493df80ae96ece9d70867e428',
            'sec-ch-ua-mobile': '?0',
            'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjkwMCwxNDQwIiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiODIwLDE0NDAiLCJzeXN0ZW1fdmVyc2lvbiI6Ik1hYyBPUyAxMS4wLjAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6ImVuLVVTIiwidGltZXpvbmUiOiJHTVQrMSIsInRpbWV6b25lT2Zmc2V0IjotNjAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMV8wXzApIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84OC4wLjQzMjQuMTgyIFNhZmFyaS81MzcuMzYiLCJsaXN0X3BsdWdpbiI6IkNocm9tZSBQREYgUGx1Z2luLENocm9tZSBQREYgVmlld2VyIiwiY2FudmFzX2NvZGUiOiJjZjRiMGUyOSIsIndlYmdsX3ZlbmRvciI6IkFwcGxlIiwid2ViZ2xfcmVuZGVyZXIiOiJBcHBsZSBNMSIsImF1ZGlvIjoiMTI0LjA0MzQ0OTY4NDc1MTk4IiwicGxhdGZvcm0iOiJNYWNJbnRlbCIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9EdWJsaW4iLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWODguMC40MzI0LjE4MiAoTWFjIE9TKSIsImZpbmdlcnByaW50IjoiNGU1NDU3OTM4M2M4NTNiMWNiZjcwNjY1YTM4ZTAyNDAiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIxNjE4MjEyOTU0NTA4SXdtYVdrQzcwaEZPa2ZTYzZ3biJ9',
            'bnc-uuid': '08e0a698-4fab-45fc-ba62-449b78caac4b',
            'clienttype': 'web',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'accept': '*/*',
            'origin': 'https://www.binance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.binance.com/en/convert',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            'cookie': 'cid=IvH3ZRoS; _h_desk_key=9f267458dc9f46198e4a0162d9809da9; s9r1=3DE30ECFF3F63DB930A23BCE4C9818D8; cr00=15678D973EBED4BDC480E82BA0A1CBBC; d1og=web.105633607.BC249ACCCAB6F3746F0529BAEDB302A9; r2o1=web.105633607.EDF4EBFF825B3AE64F778611569613B2; f30l=web.105633607.93365FE74FF2D98E613B667A1DE785FD; __BINANCE_USER_DEVICE_ID__={"17e88c0e55d5a10ce27ad490daf1e30a":{"date":1618212954666,"value":"1618212954508IwmaWkC70hFOkfSc6wn"}}; p20t=web.105633607.34F71238DFC24DFB2F43D9A8E1368F23; userPreferredCurrency=EUR_USD; bnc-uuid=08e0a698-4fab-45fc-ba62-449b78caac4b; _ga=GA1.2.1724420543.1618224179; _gid=GA1.2.31563713.1618224179; source=referral; campaign=www.binance.com; BNC_FV_KEY=3130dbfcde75a2b493df80ae96ece9d70867e428; BNC_FV_KEY_EXPIRE=1618252204028; fiat-prefer-currency=EUR',
            }

        data = '{"fromCoin":"USDT","requestAmount":"10","requestCoin":"USDT","toCoin":"BTC"}'

        response = requests.post('https://www.binance.com/bapi/margin/v1/private/new-otc/get-quote', headers=headers, data=data)

        return response

        # {"code":"000000","message":null,"messageDetail":null,"data":{"quoteId":"11528284918","quotePrice":"0.00001666","expireTime":4,"expireTimestamp":1618224525436,"fromCoin":"USDT","toCoin":"BTC","toCoinAmount":"0.00016659","fromCoinAmount":"10","requestCoin":"USDT","requestAmount":"10","fromCoinAsset":"61.4234962","message":null},"success":true}

    def execute_quote(quoteId):

        headers = {
            'authority': 'www.binance.com',
            'x-trace-id': 'fe6cb1bc-fe34-43e0-86bc-0ba21eee1cc0',
            'dnt': '1',
            'csrftoken': 'b8564db6762eb17c53b266628e8eca7d',
            'x-ui-request-trace': 'fe6cb1bc-fe34-43e0-86bc-0ba21eee1cc0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'en',
            'fvideo-id': '3130dbfcde75a2b493df80ae96ece9d70867e428',
            'sec-ch-ua-mobile': '?0',
            'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjkwMCwxNDQwIiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiODIwLDE0NDAiLCJzeXN0ZW1fdmVyc2lvbiI6Ik1hYyBPUyAxMS4wLjAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6ImVuLVVTIiwidGltZXpvbmUiOiJHTVQrMSIsInRpbWV6b25lT2Zmc2V0IjotNjAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMV8wXzApIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84OC4wLjQzMjQuMTgyIFNhZmFyaS81MzcuMzYiLCJsaXN0X3BsdWdpbiI6IkNocm9tZSBQREYgUGx1Z2luLENocm9tZSBQREYgVmlld2VyIiwiY2FudmFzX2NvZGUiOiJjZjRiMGUyOSIsIndlYmdsX3ZlbmRvciI6IkFwcGxlIiwid2ViZ2xfcmVuZGVyZXIiOiJBcHBsZSBNMSIsImF1ZGlvIjoiMTI0LjA0MzQ0OTY4NDc1MTk4IiwicGxhdGZvcm0iOiJNYWNJbnRlbCIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9EdWJsaW4iLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWODguMC40MzI0LjE4MiAoTWFjIE9TKSIsImZpbmdlcnByaW50IjoiNGU1NDU3OTM4M2M4NTNiMWNiZjcwNjY1YTM4ZTAyNDAiLCJkZXZpY2VfaWQiOiIiLCJyZWxhdGVkX2RldmljZV9pZHMiOiIxNjE4MjEyOTU0NTA4SXdtYVdrQzcwaEZPa2ZTYzZ3biJ9',
            'bnc-uuid': '08e0a698-4fab-45fc-ba62-449b78caac4b',
            'clienttype': 'web',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'accept': '*/*',
            'origin': 'https://www.binance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.binance.com/en/convert',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            'cookie': 'cid=IvH3ZRoS; _h_desk_key=9f267458dc9f46198e4a0162d9809da9; s9r1=3DE30ECFF3F63DB930A23BCE4C9818D8; cr00=15678D973EBED4BDC480E82BA0A1CBBC; d1og=web.105633607.BC249ACCCAB6F3746F0529BAEDB302A9; r2o1=web.105633607.EDF4EBFF825B3AE64F778611569613B2; f30l=web.105633607.93365FE74FF2D98E613B667A1DE785FD; __BINANCE_USER_DEVICE_ID__={"17e88c0e55d5a10ce27ad490daf1e30a":{"date":1618212954666,"value":"1618212954508IwmaWkC70hFOkfSc6wn"}}; p20t=web.105633607.34F71238DFC24DFB2F43D9A8E1368F23; userPreferredCurrency=EUR_USD; bnc-uuid=08e0a698-4fab-45fc-ba62-449b78caac4b; _ga=GA1.2.1724420543.1618224179; _gid=GA1.2.31563713.1618224179; source=referral; campaign=www.binance.com; BNC_FV_KEY=3130dbfcde75a2b493df80ae96ece9d70867e428; BNC_FV_KEY_EXPIRE=1618252204028; fiat-prefer-currency=EUR',
            }

        data = [
            ('{"fromCoin":"USDT","requestAmount":"10","requestCoin":"USDT","toCoin":"BTC"}', ''),
            ('{"fromCoin":"USDT","requestAmount":"10","requestCoin":"USDT","toCoin":"BTC"}', ''),
            ('{"fromCoin":"USDT","requestAmount":"10","requestCoin":"USDT","toCoin":"BTC"}', ''),
            ('{"fromCoin":"USDT","requestAmount":"10","requestCoin":"USDT","toCoin":"BTC"}', ''),
            ('{"quoteId":"11528282784"}', ''),
            ('{"quoteId":"11528284918"}', ''),
            ]

        response = requests.post('https://www.binance.com/bapi/margin/v1/private/new-otc/get-quote', headers=headers, data=data)
        return response