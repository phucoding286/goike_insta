from cookies_data_manager import main, error_color, success_color, system_color, wait_color
from auto_insta_golike import tool_init, auto_golike_insta
import random

if __name__ == "__main__":
    while True:
        print(system_color("1. chạy tool golike"))
        print(system_color("2. chạy tool quản lý tài khoản"))
        choose = input(system_color("vui lòng nhập lựa chọn của bạn theo số vị trí\n>>> "))
        try: choose = int(choose)
        except:
            print(error_color("vui lòng nhập đúng định dạng!"))
            input(system_color("enter để quay lại\n>>>"))
            continue

        if choose == 1:
            print(wait_color("bạn đã chọn phần chạy tool golike instagram!"))
            try: max_of_times = int(input(system_color("vui lòng nhập số lần tương tác tối đa mỗi account instagram\n>>> ")))
            except: print(error_color("vui lòng nhập đúng định dạng là số!"))

            golike_group, timeout = tool_init()
            auto_golike_insta(
                golike_group["insta_id_cookies"],
                random.choice([i for i in range(timeout[0], timeout[1])]),
                max_of_times=max_of_times
            )

        elif choose == 2:
            print(wait_color("bạn đã chọn phần quản lý tài khoản!"))
            main()
