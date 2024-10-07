from golike_insta import (
    get_jobs,
    verify_complete_job,
    check_valid_jobs_acc_id,
    follow_instagram
)
import golike_insta
import time
import random
from instagram import follow_instagram
import instagram
from colorama import Fore, Style
import colorama
import random
colorama.init()


def waiting_ui(timeout=5, text=""):
    for i in range(1, timeout+1):
        print(Fore.YELLOW + f"\r{i}s " + Style.RESET_ALL, end="")
        print(Fore.BLUE + text + Style.RESET_ALL, end="")
        time.sleep(1)
    print()
    return 0


def auto_golike_insta(id_cookies: dict, timeout: int = 20, max_of_times: int = 40):
    account_id_ = check_valid_jobs_acc_id(id_cookies)
    print(Fore.GREEN + f"các id hợp lệ là: {account_id_}" + Style.RESET_ALL)

    if str(account_id_[-1]) == "[]" or False in account_id_:
        print(Fore.RED + "không còn bất kỳ account nào có thể hoạt động!" + Style.RESET_ALL)
        input(">>>")
        exit()
    else:
        golike_job_total_err = 0
        insta_follow_total_err = 0
        max_err = 10
        i = 1
        for account_id in account_id_[-1]:
            print(Fore.YELLOW + f"{i}. {account_id}" + Style.RESET_ALL)
            i += 1

        while True:
            try:
                choose_inp = int(input(Fore.YELLOW + "nhập số thứ tự tương ứng với id bạn muốn chạy: " + Style.RESET_ALL))
                break
            except:
                print(Fore.YELLOW + "vui lòng nhập đúng số thứ tự" + Style.RESET_ALL)
                continue
        
        for account_id in account_id_[-1][choose_inp-1:]:
            times_count = 0
            while times_count <= max_of_times:
                times_count += 1

                print(Fore.GREEN + f"account id đang làm việc là -> {account_id}" + Style.RESET_ALL)
                output_job = get_jobs(account_id)

                if "error" not in output_job:
                    insta_link, insta_user_id, task_type, object_id, status = output_job
                    print(Fore.GREEN + "đã nhận job thành công!" + Style.RESET_ALL)

                    if status['status_code'] != 200:
                        print(Fore.RED + f"tài khoản {account_id} đã bị lỗi khi nhận jobs" + Style.RESET_ALL)
                        if golike_job_total_err > max_err:
                            print(f"account id {account_id} lỗi nhận job bỏ qua account id này")
                            golike_job_total_err = 0
                            break
                        else:
                            waiting_ui(timeout, "vẫn còn cơ hội thử lại đợi để quay lại...")
                            golike_job_total_err += 1
                            continue
                    else:
                        golike_job_total_err = 0

                elif output_job['status_code'] == 400:
                    print(Fore.RED + f"tài khoản {account_id} đã hết jobs" + Style.RESET_ALL)
                    if golike_job_total_err > 2:
                        print(f"account id {account_id} lỗi nhận job bỏ qua account id này")
                        golike_job_total_err = 0
                        break
                    else:
                        waiting_ui(timeout, "vẫn còn cơ hội thử lại đợi để quay lại...")
                        golike_job_total_err += 1
                        continue

                else:
                    print(Fore.RED + "đã có lỗi khi nhận job" + Style.RESET_ALL)
                    if golike_job_total_err > max_err:
                        print(f"account id {account_id} lỗi nhận job bỏ qua account id này")
                        golike_job_total_err = 0
                        break
                    else:
                        waiting_ui(timeout, "vẫn còn cơ hội thử lại đợi để quay lại...")
                        golike_job_total_err += 1
                        continue

                waiting_ui(5, "đang đợi để tiếp tục follow instagram")

                follow_status = follow_instagram(insta_link, object_id, random.choice(id_cookies[str(account_id)]))
                if "error" in follow_status or not follow_status['following_status'] and not follow_status['outgoing_request']:
                    print(Fore.RED + f"follow tài khoản instagram {insta_link.split('/')[-1]} thất bại" + Style.RESET_ALL)
                    if insta_follow_total_err > max_err:
                        print(Fore.RED + f"bỏ qua account {account_id} ra do bị lỗi follow" + Style.RESET_ALL)
                        insta_follow_total_err = 0
                        break
                    else:
                        waiting_ui(timeout, "vẫn còn cơ hội thử lại đợi để quay lại...")
                        insta_follow_total_err += 1
                        continue
                else:
                    print(Fore.GREEN + f"follow instagram cho tài khoản {insta_link.split('/')[-1]} thành công" + Style.RESET_ALL)
                    insta_follow_total_err = 0
            
                waiting_ui(5, "đang đợi để xác minh job")

                output_verify_job = verify_complete_job(insta_user_id, account_id)
                if "error" not in output_verify_job:
                    if output_verify_job[0] == 200:
                        print(Fore.GREEN + str(output_verify_job) + Style.RESET_ALL)
                        waiting_ui(timeout, "đợi nhận job mới...")
                else:
                    print(Fore.RED + str(output_verify_job) + Style.RESET_ALL)
                    print(Fore.RED + "có lỗi khi xác minh job!" + Style.RESET_ALL)
                    waiting_ui(timeout, "đợi để quay lại...")
                    continue
    print(Fore.YELLOW + "đã hết account còn job hãy quay lại vào ngày mai nhé" + Style.RESET_ALL)
    input(Fore.YELLOW + ">>>" + Style.RESET_ALL)


def tool_init():
    golike_insta.HEADERS = golike_insta.COOKIES_DATA['golike_headers']
    instagram.HEADERS = golike_insta.COOKIES_DATA['insta_headers']
    instagram.DATA = golike_insta.COOKIES_DATA['insta_follow_payloads']
    instagram.HEADERS['user-agent'] = random.choice(golike_insta.COOKIES_DATA['instagram_user_agent'])
    print("các nhóm:")
    for golike_account in golike_insta.COOKIES_DATA['golike_accounts'].keys():
        print(golike_account)
    while True:
        choose_golike_account = input("lựa nhập nhóm tài khoản của bạn: ")
        try:
            golike_group = golike_insta.COOKIES_DATA['golike_accounts'][choose_golike_account]
            break
        except:
            print("vui lòng nhập đúng tên nhóm")
            continue
    timeout = golike_insta.COOKIES_DATA["timeout"]
    golike_insta.HEADERS['Authorization'] = golike_group["authorization"]
    return golike_group, timeout


if __name__ == "__main__":
    golike_group, timeout = tool_init()
    auto_golike_insta(
        golike_group["insta_id_cookies"],
        random.choice([i for i in range(timeout[0], timeout[1])]),
        max_of_times=25
    )