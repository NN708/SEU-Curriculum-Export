import requests
import time
import getpass

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
print("说明：为了保护您的密码，输入密码不会有任何回显，正常输入后按回车即可。")
password = getpass.getpass("请输入统一身份认证密码：")
print("说明：学期请以类似 17-18-3 的格式输入，如需导出多个学期，各学期请以半角逗号分隔。若只希望导出近期物理实验或考试，直接按回车即可。")
terms = input("请输入要导出的学期：")
print("说明：教务处提供的课表中，物理实验没有准确的时间和地点，而且缺少选做实验的课程，一般情况下建议删除此处课表中的物理实验，之后从物理实验中心导出近期物理实验。")
delete_phylab = input("删除课表中的物理实验(Y/N)？")
delete_phylab = (delete_phylab.upper() == "Y")
phylab = input("从物理实验中心导出近期物理实验(Y/N)？")
phylab = (phylab.upper() == "Y")
exam = input("导出近期考试日程(Y/N)？")
exam = (exam.upper() == "Y")
print("========================================")

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
            exit()
        responsedata = r.json()
        if responsedata["success"] != True:
            print("学期" + term + "获取失败")
            exit()
        for course in responsedata["result"]["curriculum"]:
            if "events" in course.keys():
                for event in course["events"]:
                    if not (delete_phylab and "物理实验" in course["courseName"]):
                        f.writeevent(course["courseName"], course["location"], event["startTime"], event["endTime"])
            else:
                print("注意：课程表中暂无" + course["courseName"] + "课程的具体时间安排，程序自动跳过该课程。")

if phylab:
    print("获取物理实验中……")
    r = requests.get("https://myseu.cn/ws3/api/phylab", headers=headers)
    if r.status_code != 200:
        print("连接失败")
        exit()
    responsedata = r.json()
    if responsedata["success"] != True:
        print("物理实验获取失败")
        exit()
    if len(responsedata["result"]) == 0:
        print("注意：暂未查询到近期物理实验。")
    for event in responsedata["result"]:
        f.writeevent("物理" + event["type"] + "：" + event["labName"], "九龙湖物理实验中心（田家炳楼）" + event["location"], event["startTime"], event["endTime"])

if exam:
    print("获取考试中……")
    r = requests.get("https://myseu.cn/ws3/api/exam", headers=headers)
    if r.status_code != 200:
        print("连接失败")
        exit()
    responsedata = r.json()
    if responsedata["success"] != True:
        print("考试获取失败")
        exit()
    if len(responsedata["result"]) == 0:
        print("注意：暂未查询到近期考试日程。")
    for event in responsedata["result"]:
        f.writeevent(event["courseName"] + " 考试", event["campus"] + event["location"], event["startTime"], event["endTime"])

f.writeend()
f.close()
print("已导出为 curriculum.ics")