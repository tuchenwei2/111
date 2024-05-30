import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


def get_color():
    # 鑾峰彇闅忔満棰滆壊
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("鑾峰彇access_token澶辫触锛岃妫?鏌pp_id鍜宎pp_secret鏄惁姝ｇ‘")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ュ湴鍖哄悕鏄惁鏈夎锛?")
        os.system("pause")
        sys.exit(1)
    elif response["code"] == "401":
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ュ拰椋庡ぉ姘攌ey鏄惁姝ｇ‘锛?")
        os.system("pause")
        sys.exit(1)
    else:
        # 鑾峰彇鍦板尯鐨刲ocation--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 澶╂皵
    weather = response["now"]["text"]
    # 褰撳墠娓╁害
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 椋庡悜
    wind_dir = response["now"]["windDir"]
    # 鑾峰彇閫愭棩澶╂皵棰勬姤
    url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
    response = get(url, headers=headers).json()
    # 鏈?楂樻皵娓?
    max_temp = response["daily"][0]["tempMax"] + u"\N{DEGREE SIGN}" + "C"
    # 鏈?浣庢皵娓?
    min_temp = response["daily"][0]["tempMin"] + u"\N{DEGREE SIGN}" + "C"
    # 鏃ュ嚭鏃堕棿
    sunrise = response["daily"][0]["sunrise"]
    # 鏃ヨ惤鏃堕棿
    sunset = response["daily"][0]["sunset"]
    url = "https://devapi.qweather.com/v7/air/now?location={}&key={}".format(location_id, key)
    response = get(url, headers=headers).json()
    if response["code"] == "200":
        # 绌烘皵璐ㄩ噺
        category = response["now"]["category"]
        # pm2.5
        pm2p5 = response["now"]["pm2p5"]
    else:
        # 鍥藉鍩庡競鑾峰彇涓嶅埌鏁版嵁
        category = ""
        pm2p5 = ""
    id = random.randint(1, 16)
    url = "https://devapi.qweather.com/v7/indices/1d?location={}&key={}&type={}".format(location_id, key, id)
    response = get(url, headers=headers).json()
    proposal = ""
    if response["code"] == "200":
        proposal += response["daily"][0]["text"]
    return weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal


def get_tianhang():
    try:
        key = config["tian_api"]
        url = "http://api.tianapi.com/caihongpi/index?key={}".format(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded'

        }
        response = get(url, headers=headers).json()
        if response["code"] == 200:
            chp = response["newslist"][0]["content"]
        else:
            chp = ""
    except KeyError:
        chp = ""
    return chp


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 鍒ゆ柇鏄惁涓哄啘鍘嗙敓鏃?
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 鑾峰彇鍐滃巻鐢熸棩鐨勭敓鏃?
        try:
            year_date = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("璇锋鏌ョ敓鏃ョ殑鏃ュ瓙鏄惁鍦ㄤ粖骞村瓨鍦?")
            os.system("pause")
            sys.exit(1)

    else:
        # 鑾峰彇鍥藉巻鐢熸棩鐨勪粖骞村搴旀湀鍜屾棩
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 浠婂勾鐢熸棩
        year_date = date(year, birthday_month, birthday_day)
    # 璁＄畻鐢熸棩骞翠唤锛屽鏋滆繕娌¤繃锛屾寜褰撳勾鍑忥紝濡傛灉杩囦簡闇?瑕?+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 鑾峰彇鍐滃巻鏄庡勾鐢熸棩鐨勬湀鍜屾棩
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


def send_message(to_user, access_token, region_name, weather, temp, wind_dir, note_ch, note_en, max_temp, min_temp,
                 sunrise, sunset, category, pm2p5, proposal, chp):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["鏄熸湡鏃?", "鏄熸湡涓?", "鏄熸湡浜?", "鏄熸湡涓?", "鏄熸湡鍥?", "鏄熸湡浜?", "鏄熸湡鍏?"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 鑾峰彇鍦ㄤ竴璧风殑鏃ュ瓙鐨勬棩鏈熸牸寮?
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 鑾峰彇鍦ㄤ竴璧风殑鏃ユ湡宸?
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 鑾峰彇鎵?鏈夌敓鏃ユ暟鎹?
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "region": {
                "value": region_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "temp": {
                "value": temp,
                "color": get_color()
            },
            "wind_dir": {
                "value": wind_dir,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },
            "max_temp": {
                "value": max_temp,
                "color": get_color()
            },
            "min_temp": {
                "value": min_temp,
                "color": get_color()
            },
            "sunrise": {
                "value": sunrise,
                "color": get_color()
            },
            "sunset": {
                "value": sunset,
                "color": get_color()
            },
            "category": {
                "value": category,
                "color": get_color()
            },
            "pm2p5": {
                "value": pm2p5,
                "color": get_color()
            },
            "proposal": {
                "value": proposal,
                "color": get_color()
            },
            "chp": {
                "value": chp,
                "color": get_color()
            },

        }
    }
    for key, value in birthdays.items():
        # 鑾峰彇璺濈涓嬫鐢熸棩鐨勬椂闂?
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "浠婂ぉ{}鐢熸棩鍝︼紝绁漿}鐢熸棩蹇箰锛?".format(value["name"], value["name"])
        else:
            birthday_data = "璺濈{}鐨勭敓鏃ヨ繕鏈墈}澶?".format(value["name"], birth_day)
        # 灏嗙敓鏃ユ暟鎹彃鍏ata
        data["data"][key] = {"value": birthday_data, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ユā鏉縤d鏄惁姝ｇ‘")
    elif response["errcode"] == 40036:
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ユā鏉縤d鏄惁涓虹┖")
    elif response["errcode"] == 40003:
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ュ井淇″彿鏄惁姝ｇ‘")
    elif response["errcode"] == 0:
        print("鎺ㄩ?佹秷鎭垚鍔?")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌onfig.txt鏂囦欢鏄惁涓庣▼搴忎綅浜庡悓涓?璺緞")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("鎺ㄩ?佹秷鎭け璐ワ紝璇锋鏌ラ厤缃枃浠舵牸寮忔槸鍚︽纭?")
        os.system("pause")
        sys.exit(1)

    # 鑾峰彇accessToken
    accessToken = get_access_token()
    # 鎺ユ敹鐨勭敤鎴?
    users = config["user"]
    # 浼犲叆鍦板尯鑾峰彇澶╂皵淇℃伅
    region = config["region"]
    weather, temp, max_temp, min_temp, wind_dir, sunrise, sunset, category, pm2p5, proposal = get_weather(region)
    note_ch = config["note_ch"]
    note_en = config["note_en"]
    if note_ch == "" and note_en == "":
        # 鑾峰彇璇嶉湼姣忔棩閲戝彞
        note_ch, note_en = get_ciba()
    chp = get_tianhang()
    # 鍏紬鍙锋帹閫佹秷鎭?
    for user in users:
        send_message(user, accessToken, region, weather, temp, wind_dir, note_ch, note_en, max_temp, min_temp, sunrise,
                     sunset, category, pm2p5, proposal, chp)
    os.system("pause")
