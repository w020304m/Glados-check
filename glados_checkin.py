import requests
import json
import os

# pushplus秘钥
sckey = os.environ.get("PUSHPLUS_TOKEN", "")
sendContent = ''

# glados账号cookie
cookies = os.environ.get("GLADOS_COOKIE", "").split("&")
if cookies[0] == "":
    print('未获取到COOKIE变量') 
    cookies = []
    exit(0)

def start():    
    url_checkin = "https://glados.rocks/api/user/checkin"
    url_status = "https://glados.rocks/api/user/status"
    url_points = "https://glados.rocks/api/user/points"  # 假设的点数查询接口

    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {'token': 'glados.one'}

    for cookie in cookies:
        # 签到
        checkin_response = requests.post(url_checkin, headers={
            'cookie': cookie,
            'referer': referer,
            'origin': origin,
            'user-agent': useragent,
            'content-type': 'application/json;charset=UTF-8'
        }, data=json.dumps(payload))

        # 获取状态
        status_response = requests.get(url_status, headers={
            'cookie': cookie,
            'referer': referer,
            'origin': origin,
            'user-agent': useragent
        })

        # 获取点数
        points_response = requests.get(url_points, headers={
            'cookie': cookie,
            'referer': referer,
            'origin': origin,
            'user-agent': useragent
        })

        # 解析状态信息
        status_data = status_response.json()['data']
        time = status_data['leftDays'].split('.')[0]
        email = status_data['email']

        # 解析点数信息
        points_data = points_response.json()['data']
        current_points = points_data['currentPoints']
        points_today = points_data['pointsToday']

        if 'message' in checkin_response.text:
            mess = checkin_response.json()['message']
            print(f"{email}----结果--{mess}----剩余({time})天----当前点数({current_points})----今天获得({points_today})点数")  # 日志输出
            sendContent += f"{email}----{mess}----剩余({time})天----当前点数({current_points})----今天获得({points_today})点数\n"
        else:
            requests.get(f'http://www.pushplus.plus/send?token={sckey}&content={email} cookie已失效')
            print('cookie已失效')  # 日志输出

    if sckey != "":
        requests.get(f'http://www.pushplus.plus/send?token={sckey}&title=签到成功&content={sendContent}')

def main_handler(event, context):
    return start()

if __name__ == '__main__':
    start()
