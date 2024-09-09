import requests

def checkin(cookie):
    url = "https://glados.rocks/api/user/checkin"
    headers = {
        "cookie": cookie,
        "content-type": "application/json;charset=UTF-8",
        "user-agent": "Mozilla/5.0"
    }
    data = {"token": "glados_network"}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_status(cookie):
    url = "https://glados.rocks/api/user/status"
    headers = {
        "cookie": cookie,
        "user-agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    cookie = "<YOUR_COOKIE>"
    checkin_result = checkin(cookie)
    status_result = get_status(cookie)

    print(f"Check-in result: {checkin_result}")

    if checkin_result.get("code") == 0:
        earned_points = checkin_result.get("list", [{}])[0].get("change", "No points information")
        print(f"Points earned today: {earned_points}")

    print(f"Account Status: {status_result}")

    if 'data' in status_result:
        left_days = status_result['data']['leftDays']
        traffic_used = status_result['data']['traffic']['used']
        traffic_total = status_result['data']['traffic']['total']
        plan_name = status_result['data']['plan']['name']

        print(f"Remaining Days: {left_days}")
        print(f"Traffic Used: {traffic_used} GB")
        print(f"Total Traffic: {traffic_total} GB")
        print(f"Plan: {plan_name}")

if __name__ == "__main__":
    main()
