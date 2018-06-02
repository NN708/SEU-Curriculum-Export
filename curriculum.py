import requests
import time

def converttime(timestamp):
    localtime = time.localtime(timestamp / 1000)
    return time.strftime("%Y%m%dT%H%M%S", localtime)

print("东南大学课程表导出工具")
print("========================================")
cardnum = input("请输入东南大学一卡通号：")
password = input("请输入统一身份认证密码：")
print("注意：学期请以类似 17-18-3 的格式输入，如需导出多个学期，各学期请以半角逗号分隔。")
terms = input("请输入要导出的学期：")
terms = terms.split(",")
print("========================================")

print("登录中……")
postdata = {"cardnum": cardnum, "password": password, "gpassword": "", "platform": "web"}
r = requests.post("https://myseu.cn/ws3/auth", data=postdata)
if r.status_code != 200:
    print("连接失败")
    input()
    exit()
responsedata = r.json()
if responsedata["success"] != True:
    print("用户名或密码错误")
    input()
    exit()
token = responsedata["result"]

print("获取课表中……")
headers = {"token": token}
f = open("curriculum.ics", "w", encoding='UTF-8')
f.write("""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
DTSTART:16010101T000000
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
END:STANDARD
END:VTIMEZONE
""")
for term in terms:
    params = {"term": term}
    r = requests.get("https://myseu.cn/ws3/api/curriculum", params=params, headers=headers)
    if r.status_code != 200:
        print("连接失败")
        input()
        exit()
    responsedata = r.json()
    if responsedata["success"] != True:
        print("学期" + term + "获取失败")
        input()
        exit()
    for course in responsedata["result"]["curriculum"]:
        for event in course["events"]:
            f.write("BEGIN:VEVENT\n")
            f.write("SUMMARY:" + course["courseName"] + "\n")
            f.write("LOCATION:" + course["location"] + "\n")
            f.write("DTSTART;TZID=Asia/Shanghai:" + converttime(event["startTime"]) + "\n")
            f.write("DTEND;TZID=Asia/Shanghai:" + converttime(event["endTime"]) + "\n")
            f.write("END:VEVENT\n")
f.write("END:VCALENDAR")
f.close()
print("已导出为 curriculum.ics")
input()