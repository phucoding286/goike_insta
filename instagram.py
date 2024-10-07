import requests
import json
import colorama

url = "https://www.instagram.com/graphql/query"
HEADERS = None
DATA = None
colorama.init()

def get_proxies():
    proxy = None
    count = 1
    while True:
        print(colorama.Fore.BLUE + f"\r{count} đang lấy proxy cho instagram..." + colorama.Style.RESET_ALL, end="")
        try:
            get_proxy = requests.get(
                    url="https://gimmeproxy.com/api/getProxy",
                )
            proxy = f"http://{get_proxy.json()['ip']}:{get_proxy.json()['port']}"
            test_proxy = requests.get(
                url="https://google.com/",
                proxies={"http": proxy},
                timeout=2
            )
            if test_proxy.status_code == 200:
                break
            else:
                continue
        except:
            continue
    print()
    print(colorama.Fore.GREEN + f"đã lấy proxy {proxy} thành công!" + colorama.Style.RESET_ALL)
    return proxy

def follow_instagram(insta_link, object_id, cookies: str):
    global DATA
    global HEADERS
    HEADERS["x-csrftoken"] = cookies.split("csrftoken=")[1].split(";")[0]
    HEADERS['cookie'] = cookies
    try:
        HEADERS['referer'] = insta_link
        DATA["variables"] = ('{'f'"target_user_id": "{object_id}",''"container_module": "profile",''"nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected"''}')
        response = requests.post(
            url="https://www.instagram.com/graphql/query",
            headers=HEADERS,
            data=DATA,
            proxies={'http': get_proxies()}
        )
        insta_json_res = response.json()['data']["xdt_create_friendship"]["friendship_status"]
        return {"following_status": insta_json_res["following"], "outgoing_request": insta_json_res['outgoing_request']}
    except Exception as e:
        print(f"lỗi follow instagram: {e}")
        return {'error': True}
    
# if __name__ == "__main__":
#     cookies = "dpr=1.25; mid=ZwC12AALAAEUkEHAX7HDxgq1zrx-; datr=2LUAZ3Qw-rjJd8BZjTV1Bwjz; ig_did=1592CC7E-D813-44E1-BDEE-868347A9A631; ds_user_id=65444176476; sessionid=65444176476%3A1Ib3IK9y6EhzbQ%3A25%3AAYebY6VVc0h4Dq2B8fXYNxXgdM7Gd4Y74RfTsAuG6A; ps_l=1; ps_n=1; csrftoken=jCQINKHba4TSDZyydWQ0aSiT8XxcxWfL; shbid=\"17201\\05465444176476\\0541759635851:01f767b2aeb16d65f665cb51c4094a809d3dcb87de5da53badfcaee16f9c1a31c678a00f\"; shbts=\"1728099851\\05465444176476\\0541759635851:01f7d0cba440dc940c36271e56b9706c1701e3bb790c2531da70f76de8258f72e1c3284c\"; wd=822x746; rur=\"CCO\\05465444176476\\0541759636099:01f7cbebfbfd316c7cc7751086aa32f135f12019c52eba1417b8ccb60572e8be84140b30\""
#     with open("./cookies_data.json", "r", encoding='utf8') as file:
#         COOKIES_DATA = json.load(file)
#     HEADERS = COOKIES_DATA['insta_headers']
#     DATA = COOKIES_DATA['insta_follow_payloads']
#     print(follow_instagram("https://www.instagram.com/nwuinie/", "37136874147", cookies))