import requests
from instagram import follow_instagram
import json
import random

with open("./cookies_data.json", "r", encoding='utf8') as file: COOKIES_DATA = json.load(file)
HEADERS = None

def get_jobs(insta_golike_id):
    try:
        get_job = requests.get(
            url=f"https://gateway.golike.net/api/advertising/publishers/instagram/jobs?instagram_account_id={insta_golike_id}&data=null",
            headers=HEADERS
        )
        gjj = get_job.json()
        if gjj['status'] == 400:
            raise ValueError("đã hết jobs để làm")
        insta_link = gjj['data']['link']
        insta_user_id = gjj['data']['id']
        task_type = gjj['data']['type']
        object_id = gjj['data']['object_id']
        return insta_link, insta_user_id, task_type, object_id, {"status_code": gjj['status'], 'status': gjj['success']}
    except Exception as e:
        print(f"đã có lỗi khi nhận job mã lỗi: {e}")
        return {"error": True, "status_code": gjj['status']}


def verify_complete_job(insta_user_id, insta_myaccount_id):
  try:
      complete_job = requests.post(
        url="https://gateway.golike.net/api/advertising/publishers/instagram/complete-jobs",
        headers=HEADERS,
        json={"async": True, "captcha": "recaptcha", "data": None, "instagram_account_id": insta_myaccount_id, "instagram_users_advertising_id": insta_user_id}
      )
      c = complete_job.json()
      return (c['status'], f"trạng thái: [{c['status']}] -> {'thành công' if c['success'] else 'không thành công'}", f"tiền công -> {c['data']['prices']}đ")
  except Exception as e:
      print(f"đã có lỗi khi xác minh hoàn thành job mã lỗi: {e}")
      return {"error": True}
  

def check_instagram_account_id():
    response = requests.get(
        url="https://gateway.golike.net/api/instagram-account",
        headers=HEADERS
    )
    resj = response.json()
    insta_id = [insta_account_id['id'] for insta_account_id in resj['data']]
    return insta_id


def check_valid_jobs_acc_id(id_cookies: dict, insta_check=True):
    accounts_id = check_instagram_account_id()
    account_valid = []
    for id in accounts_id:
        if insta_check:
            try: check_follow = follow_instagram("https://www.instagram.com/nwuinie/", "37136874147", random.choice(id_cookies[str(id)]))
            except Exception as e:
                print(f"mã lỗi tài khoản instagram: {e}")
                continue
            if "error" in check_follow:
                continue
            elif not check_follow['following_status'] and not check_follow['outgoing_request']:
                continue
            else:
                account_valid.append(id)
    if str(account_valid) == "[]":
        account = (False, "không còn bất kỳ account id nào còn jobs")
    else:
        account = (True, account_valid)
    print(f"có tổng cộng {len(accounts_id)} account hoạt động được là {len(account_valid)}")
    return account