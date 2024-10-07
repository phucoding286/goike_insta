import colorama
import json
import instagram
colorama.init()

def error_color(string: str):
    return colorama.Fore.RED + string + colorama.Style.RESET_ALL
def success_color(string: str):
    return colorama.Fore.GREEN + string + colorama.Style.RESET_ALL
def system_color(string: str):
    return colorama.Fore.YELLOW + string + colorama.Style.RESET_ALL
def wait_color(string: str):
    return colorama.Fore.BLUE + string + colorama.Style.RESET_ALL

def read_cookies_data(file_path: str = "./cookies_data.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file: cookies_data = json.load(file)
    except: return {"error": "đã có lỗi khi đọc file"}
    return cookies_data

def write_cookies_data(cookies_data: json, file_path: str = "./cookies_data_test.json"):
    try:
        with open(file_path, "w", encoding="utf-8") as file: json.dump(cookies_data, file, indent=4)
    except: return {"error": "đã có lỗi khi ghi file"}
    return {"good": "đã lưu cookies data thành công"}

def write_cookies_instagram(
        cookies_data: json,
        golike_account_name: str,
        id_account: str,
        cookies_instagram: str,
        golike_authorization: str = None):
    
    if golike_account_name not in cookies_data['golike_accounts']:
        user_clsf = input(system_color("account name này chưa có trong danh sách bạn muốn thên?(Y/n)\n>>>"))
        if user_clsf.strip().lower() == "y":
            cookies_data['golike_accounts']["authorization"] = ""
            cookies_data['golike_accounts']["insta_id_cookies"] = {}
        else:
            return 0
    
    if golike_authorization is not None:
        cookies_data['golike_accounts'][golike_account_name]["authorization"] = golike_authorization

    if id_account not in cookies_data['golike_accounts'][golike_account_name]['insta_id_cookies']:
        print(system_color("account id này chưa có trong danh sách! bạn có muốn thêm?(Y\\n)"))
        user_clsf = input(system_color(">>>"))
        if user_clsf.strip().lower() == "y":
            cookies_data['golike_accounts'][golike_account_name]['insta_id_cookies'][id_account] = cookies_instagram
            writer_out = write_cookies_data(cookies_data)
            print(error_color(writer_out['error'])) if "error" in writer_out else print(success_color(writer_out['good']))
        else:
            return {"bad": "người dùng đã chọn thoát khỏi chương trình."}
    else:
        print(success_color("account id này có sẳn trong cơ sở dữ liệu."))
        cookies_data['golike_accounts'][golike_account_name]['insta_id_cookies'][id_account].append(cookies_instagram)
        writer_out = write_cookies_data(cookies_data)
        print(error_color(writer_out['error'])) if "error" in writer_out else print(success_color(writer_out['good']))


def main():
    cookies_data = read_cookies_data()
    while True:
        [print(system_color("1. xóa id golike trong cơ sở dữ liệu")), print(system_color("2. thêm cookies và account"))]
        try: 
            user_desicion = int(input(system_color("vui lòng nhập lựa chọn theo số thứ tự\n>>> "))) - 1
            break
        except: print(error_color("vui lòng nhập đúng định dạng số!"))

    if user_desicion+1 == 1:
        for i in range(len(cookies_data['golike_accounts'])):
            print(system_color(f"{i+1}. {list(cookies_data['golike_accounts'].keys())[i]}"))
        user_input_golike_name = input(system_color("nhập vào account golike name tương ứng để xóa\n>>> "))
        try:
            cookies_data['golike_accounts'][user_input_golike_name]
            print(success_color("account name này hợp lệ! tồn tại trong cơ sở dữ liệu!"))
        except:
            print(error_color("account name này không hợp lệ! không tồn tại"))
            input("enter để exit\n>>> ")
            exit()
        user_input_id = input(system_color("nhập id mà bạn muốn xóa\n>>> "))
        try:
            cookies_data['golike_accounts'][user_input_golike_name]['insta_id_cookies'].pop(user_input_id)
            print(success_color("đã xóa account_id thành công!"))
        except:
            print(error_color("account id này không tồn tại để xóa"))
            input("enter để exit\n>>> ")
            exit()
        write_cookies_data(cookies_data)

    elif user_desicion+1 == 2:
        while True:
            count = 0
            for i in range(len(cookies_data['golike_accounts'])):
                print(system_color(f"{i+1}. {list(cookies_data['golike_accounts'].keys())[i]}"))
                count += i
            if count == 0:
                print(error_color("không có bất kỳ account name nào"))
            golike_account_name = None
            account_name_index = None
            authorization = None
            try:
                print(wait_color("thông báo! bạn có thể dùng lệnh 'exit' để thoát bảng này"))
                account_name_index = input(system_color("nhập vào số thứ tự account mà bạn muốn thêm cookies hoặc tên account mới\n>>> "))
                if account_name_index.strip().lower() == "exit":
                    print(error_color("bạn đã chọn thoát chương trình này."))
                    break
                account_name_index = int(account_name_index)-1
                try: golike_account_name = list(cookies_data['golike_accounts'].keys())[account_name_index]
                except: golike_account_name = account_name_index
            except:
                print(error_color("bạn đã chọn một account name mới!"))
                authorization = input(system_color("nhập golike authorization\n>>> "))
            
            while True:
                print(wait_color("thông báo! bạn có thể dùng lệnh 'exit' để thoát khỏi bảng thêm authorization và cookies này"))
                account_id_input = input(system_color("nhập id trên golike để làm key cho cookies của account name của bạn\n>>> "))
                if account_id_input.lower().strip() == "exit":
                    print(error_color("bạn đã chọn thoát chương trình này."))
                    break
                print(wait_color("thông báo! bạn có thể dùng lệnh 'exit' để thoát khỏi bảng thêm authorization và cookies này"))
                cookies_input = input(system_color("nhập vào cookies instagram cho account name của bạn\n>>> "))
                if cookies_input.lower().strip() == "exit":
                    print(error_color("bạn đã chọn thoát chương trình này."))
                    break

                with open("./cookies_data.json", "r", encoding="utf-8") as file: COOKIES_DATA = json.load(file)
                instagram.HEADERS = COOKIES_DATA['insta_headers']
                instagram.DATA = COOKIES_DATA['insta_follow_payloads']
                print(wait_color("đang test thử cookies instagram của bạn..."))
                test_follow = instagram.follow_instagram("https://www.instagram.com/nwuinie/", "37136874147", cookies_input)
                if "error" in test_follow:
                    print(error_color("cookies này bị lỗi! hoặc tài khoản của bạn bị hạn chế"))
                    input(system_color("enter để thoát\n>>>"))
                    break
                else:
                    print(success_color("đã check thành công! tài khoản hoạt động."))
                
                if write_cookies_instagram(
                    cookies_data=cookies_data,
                    golike_account_name=golike_account_name,
                    id_account=account_id_input,
                    cookies_instagram=cookies_input,
                    golike_authorization=authorization
                    ) == 0:
                    print(error_color("bạn đã hủy bỏ phiên lưu account vừa rồi!"))
                else:
                    print(success_color("đã lưu thành công!"))
                
                continue_desicion = input(system_color("bạn có muốn tiếp tục thêm cookies không?(Y/n)\n>>>"))
                if continue_desicion.strip().lower() == "y":
                    continue
                else:
                    break

if __name__ == "__main__":
    main()