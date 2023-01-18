import requests, json, ndjson, datetime, os, re
from time import sleep
# moduleをインポート


def json2list(URL, dtime_d, dtime_t):
    # URLからjsonを取得し、必要な値を取り出してlistに格納
    alldata = json.loads(requests.get(URL).text)
    # jsonをtextに変換しdictとして読み込み
    data = alldata['69101']
    # 倉吉市のデータを参照し、dataに格納
    list = [dtime_d + ' ' + dtime_t, data["temp"][0], data["precipitation10m"][0], data["windDirection"][0], data["wind"][0]]
    # 必要な値を取り出しlistに格納
    return list
    # listの値を返す


def get_time():
    # 現在時刻を取得
    return datetime.datetime.now().strftime('%Y%m%d%H:%M')
    # PC設定から現在時刻を取得し、ファイル名用に日付を返す


def time_now():
    #現在時刻-10分を記号を付けずに取得
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # 現在時刻を取得
    dt_Y = dt[:4]
    # yearを取り出す
    dt_M = dt[4:6]
    # monthを取り出す
    dt_D = dt[6:8]
    # dayを取り出す
    dt_h = dt[8:10]
    # hourを取り出す
    dt_m = dt[10:]
    # minutesを取り出す
    dt_mm = dt[10:11]
    # minutes上の桁のみを取り出す
    if int(dt_M) == 1 and int(dt_D) == 1 and int(dt_h) <= 0 and int(dt_m) < 10:
    # 1月1日の0:10より前だった場合yearを-1/month以降は"12312350"(12/31 23:50)で固定
        dt_Y = int(dt_Y) - 1
        return str(dt_Y) + "12312350"

    elif int(dt_D) == 1 and int(dt_h) <= 0 and int(dt_m) < 10:
    # -1日した際に0以下になる場合はmonthを-1ヵ月する/dayは月によって(うるう年等)合わせる/時間は23:50で固定
        dt_M = int(dt_M) - 1
        if len(str(dt_M)) == 1:
        #  monthを-1した際に1桁になる場合"0"を追加
            dt_M = "0" + str(dt_M)
        if int(dt_Y) % 400 == 0 and dt_M == "2":
        # うるう年の判定(1)
            dt_D = 29
        elif int(dt_Y) % 4 == 0 and int(dt_Y) % 100 != 0 and dt_M == "2":
        # うるう年の判定(2)
            dt_D = 29
        elif dt_M == 1 or dt_M == 3 or dt_M == 5 or dt_M == 7 or dt_M == 8 or dt_M == 10 or dt_M == 12:
        # 西向く士以外
            dt_D = 31
        elif dt_M == 4 or dt_M == 6 or dt_M == 9 or dt_M == 11:
        # 西向く士
            dt_D = 30
        elif dt_M == 2:
        # うるう年以外の2月
            dt_D = 28
        
        return dt[:4] + str(dt_M) + str(dt_D) + "2350"

    elif int(dt_h) <= 0 and int(dt_m) < 10:
    # -1時間した際に0以下になる場合はdayを-1日する/時間は"23:50"で固定
        dt_D = int(dt_D) - 1
        return dt[:6] + str(dt_D) + "2350"
        
    elif int(dt_m) < 10:
    # -10分した際に0以下になる場合はhourを-1時間する/minutesは"50"で固定
        dt_h = int(dt_h) - 1
        dt_m = "50"
        if len(str(dt_h)) == 1:
        #  hourを-1した際に1桁になる場合"0"を追加
            dt_h = "0" + str(dt_h)
        return dt[:8] + str(dt_h) + dt_m
        
    else:
    # minutesを-10分し、下の桁を0にする
        dt_m = int(dt_mm) - 1
        return dt[:10] + str(dt_m) + "0"


def write_line(list, FILENAME):
    with open(FILENAME, 'a') as f:
        # 書き込み先ファイルを開く
        writer = ndjson.writer(f)
        writer.writerow(list)
        # ファイルに書き込む 


FILENAME = '/var/www/html/data/scp/log/_data.json'
# デフォルトのファイル名
logdir = '/var/www/html/data/scp/log/'

if os.path.exists(FILENAME):
    # "_data"が存在するか
    with open(FILENAME, 'r') as ld:
        # 存在する場合最終行を抽出
        lines = ld.readlines()
        # 1行ずつ配列へ代入
        lg = len(lines)
        # 配列の要素数を求める

    if lg < 1:
        # 中が空の場合は初期値を与える
        lastjkn = '99:99'
        # 時刻の初期値を設定
        hdk = datetime.datetime.now().strftime('%Y/%m/%d')
        # 日付の初期値を設定

    else:
        # 中にデータが入っていればそれを参照する
        lstd = lines[lg - 1].strip()
        # 配列の最後のデータを抽出/0から始まるため-1
        lastjkn = lstd[13:18]
        # 最後のデータから時刻を取得
        hdk = lstd[2:12]
        # 最後のデータから日付を取得
        
else:
    # 存在しなければ初期値を与える
    lastjkn = '99:99'
    # 時刻の初期値を設定
    hdk = datetime.datetime.now().strftime('%Y/%m/%d')
    # 日付の初期値を設定

dtime = time_now()
# 時間を取得
URL = "https://www.jma.go.jp/bosai/amedas/data/map/" + str(dtime) + "00.json"
# 取得した時間をもとにjsonを取得するURLを設定
dtime_d = dtime[:4] + "/" + dtime[4:6] + "/" + dtime[6:8]
# dateを取り出す
dtime_t = dtime[8:10] + ":" + dtime[10:]
# timeを取り出す

# 【エラー処理】
# ※データ更新(hh:m2前後)よりも早くアクセスすると404 Errorとなる
# ※更新までに10分程度要することがあったため、最大10分+1回再試行する
i = 0
# カウンターの初期値設定
while i < 21:
# 最大21回再試行
    try:
    # エラーを検知
        list = json2list(data, dtime_d, dtime_t)
        # URLからjsonを取得。倉吉市のデータを取り出し、取得したjsonの必要な値をlistに格納

    except Exception:
    # エラーが出た場合
        i += 1
        # カウンターを+1
        if i >= 20:
            now = get_time()
            list = [dtime_d + ' ' + dtime_t, 'Error!>>' + now[8:], 'Missing data']
            # 21回全てエラーの場合、欠測を表示

        else:
            pass
            # 21回未満の場合は一度tryを抜けてループに戻る
        
        sleep(30)
        # 30秒後に再試行

    else:
        break
        # エラーが出なくなればループを抜けて続行

if list[0][0:10] != hdk:
    # 日付が前回と変わっていた場合
    flname = re.sub(r"\D", "", hdk)
    # 前回記録された日付(もしくは"_data"の最後の日付)から記号(/)を削除
    os.rename(FILENAME, logdir + flname + '.json')
    # ファイル名を"yyyymmdd"に変更
    hdk = list[0][0:10]
    # 今回の日付をhdkに代入

else:
    # 変わっていなければ何もしない
    pass

if list[0][11:16] != lastjkn:
    # 時間が前回と変わっていた場合
    write_line(list, FILENAME)
    # データを新しい行に記録
    lastjkn = list[0][11:16]
    # 今回の時間をlastjknに代入
    import json2table
    # 生成したjsonをhtmlに変換
    
else:
    # 変わっていなければ何もしない
    pass
