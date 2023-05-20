import urllib.request
import json
import time
import requests as req
import datetime as dt

TOKEN = 'your token'
api_url = 'https://notify-api.line.me/api/notify'

WEATHER_TRANS = json.load(open("transweather.json", "r"))
OFFICES_AREA_CODE = "230000"
CLASS_AREA_CODE = "2320300"
AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
warning_bool=False
warning_text_new=[]
warning_text_old=[]
warning_status=[]
warning_text=[]

url = "https://www.jma.go.jp/bosai/warning/data/warning/%s.json" % (OFFICES_AREA_CODE)
def warnings():
    global warning_text,warning_status,warning_texts
    area_data = urllib.request.urlopen(url=AREA_URL)
    area_data = json.loads(area_data.read())
    area = area_data["class20s"][CLASS_AREA_CODE]["name"]
    warning_info = urllib.request.urlopen(url=url)
    warning_info = json.loads(warning_info.read())
    warning_codes = [warning["code"]
                    for class_area in warning_info["areaTypes"][1]["areas"]
                        if class_area["code"] == CLASS_AREA_CODE
                            for warning in class_area["warnings"]
                                if warning["status"] != "発表警報・注意報はなし"]
    warning_status = [warning["status"]
                    for class_area in warning_info["areaTypes"][1]["areas"]
                        if class_area["code"] == CLASS_AREA_CODE
                            for warning in class_area["warnings"]]
    warning_texts = [WEATHER_TRANS["warninginfo"][code] for code in warning_codes]
    return (warning_texts,area)

def main():
    global warning_bool,warning_text_new,warning_text_old,warning_status,warning_text
    print("https://www.jma.go.jp/bosai/warning/#area_type=class20s&area_code=%s&lang=ja" % (CLASS_AREA_CODE))
    print("%sの気象警報・注意報" % (warnings()[1]))
    if warnings()[0] == []:
        warning_bool=False
        print("現在発表警報・注意報はありません。")
    else:
        warning_bool=True
    if warning_bool==True:
        warning_text_old=warning_text_new
        warning_text_new=warnings()[0]
        if warning_text_new!=warning_text_old:
            if warning_status[0]!="発表警報・注意報はなし":
                for i in range(len(warning_texts)):
                    warning_text.append(f"{warning_texts[i]}:{warning_status[i]}")
            send=""
            for i in range((len(warning_text))):
                send=f"{send}{warning_text[i]}\n"
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_contents=f"警報・注意報の発表\n{now}時点\n{send}"
            TOKEN_dic = {'Authorization': 'Bearer'+' '+TOKEN}
            send_dic = {'message': send_contents}
            try:
                req.post(api_url, headers=TOKEN_dic, data=send_dic)
                print(send_contents)
            except Exception as e:
                print(f"Error {e}")
    warning_text=[]

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
