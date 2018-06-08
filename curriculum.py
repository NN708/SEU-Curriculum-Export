import requests
import time

def converttime(timestamp):
    localtime = time.localtime(timestamp / 1000)
    return time.strftime("%Y%m%dT%H%M%S", localtime)

class icsfile:
    def __init__(self, filename):
        self.f = open(filename, "w", encoding='UTF-8')
    def writestart(self):
        self.f.write("""BEGIN:VCALENDAR
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
    def writeend(self):
        self.f.write("END:VCALENDAR")
    def close(self):
        self.f.close()
    def writeevent(self, summary, location, start, end):
        self.f.write("BEGIN:VEVENT\n")
        self.f.write("SUMMARY:" + summary + "\n")
        self.f.write("LOCATION:" + location + "\n")
        self.f.write("DTSTART;TZID=Asia/Shanghai:" + converttime(start) + "\n")
        self.f.write("DTEND;TZID=Asia/Shanghai:" + converttime(end) + "\n")
        self.f.write("END:VEVENT\n")


print("东南大学课程表导出工具")
print("========================================")
cardnum = input("请输入东南大学一卡通号：")
password = input("请输入统一身份认证密码：")
print("注意：学期请以类似 17-18-3 的格式输入，如需导出多个学期，各学期请以半角逗号分隔。")
terms = input("请输入要导出的学期：")
exam = input("导出近期考试日程(Y/N)？")
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

headers = {"token": token}
f = icsfile("curriculum.ics")
f.writestart()

if terms:
    print("获取课表中……")
    terms = terms.split(",")
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
                f.writeevent(course["courseName"], course["location"], event["startTime"], event["endTime"])

if exam.upper() == "Y":
    print("获取考试中……")
    r = requests.get("https://myseu.cn/ws3/api/exam", headers=headers)
    if r.status_code != 200:
        print("连接失败")
        input()
        exit()
    responsedata = r.json()
    if responsedata["success"] != True:
        print("考试获取失败")
        input()
        exit()
    for event in responsedata["result"]:
        f.writeevent(event["courseName"] + " 考试", event["campus"] + event["location"], event["startTime"], event["endTime"])

f.writeend()
f.close()
print("已导出为 curriculum.ics")
input()