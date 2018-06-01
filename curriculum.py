import requests
import time

def converttime(timestamp):
    localtime = time.localtime(timestamp / 1000)
    return time.strftime("%Y%m%dT%H%M%S", localtime)

cardnum = input("请输入一卡通号：")
password = input("请输入密码：")
term = input("请输入要导出的学期（如 18-19-1）：")

print("登录中……")
postdata = {"cardnum": cardnum, "password": password, "gpassword": "", "platform": "web"}
r = requests.post("https://myseu.cn/ws3/auth", data=postdata)
if r.status_code != 200:
    print("连接失败")
    exit()
responsedata = r.json()
if responsedata["success"] != True:
    print("用户名或密码错误")
    exit()
token = responsedata["result"]

print("获取课表中……")
params = {"term": term}
headers = {"token": token}
r = requests.get("https://myseu.cn/ws3/api/curriculum", params=params, headers=headers)
if r.status_code != 200:
    print("连接失败")
    exit()
if responsedata["success"] != True:
    print("获取失败")
    exit()
responsedata = r.json()

print("导出ics文件……")
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
print("已导出为curriculum.ics")