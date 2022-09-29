import requests, json, ndjson, datetime, os
from time import sleep
# moduleをインポート


def json_get(URL):
    # URLからjsonを取得
    return (json.loads(requests.get(URL).text))
    # jsonをtextに変換しdictとして読み込み


def json2list(data):
    # jsonから必要な値を取り出しlistに格納
    kion = data['temp']
    uryou = data['precipitation10m']
    fuuko = data['windDirection']
    fuusoku = data['wind']
    jikan = data['dataTime']
    # 各値を代入

    list = [jikan[0][:10], jikan[0][11:16], kion[0], uryou[0], fuuko[0], fuusoku[0]]
    # 代入された値からdictを作成
    return list
    # listの値を返す


def time_set():
    # 現在時刻を取得
    dt_now = datetime.datetime.now()
    # PC設定から現在時刻を取得
    return (dt_now.strftime('%Y%m%d%H:%M'))
    # ファイル名用に日付を代入


def write_line(list):
    with open(FILENAME, 'a') as f:
        # 書き込み先ファイルを開く
        writer = ndjson.writer(f)
        writer.writerow(list)
        # ファイルに書き込む 


URL = "https://api.cultivationdata.net/amds?point=69101"
# jsonを取得するURL

FILENAME = './log/_data.json'
# デフォルトのファイル名

lastjkn = "99:99"
# 時刻の初期値を設定
hdk = datetime.datetime.now().strftime('%Y/%m/%d')
# 日付の初期値を設定

l = 0
# ファイル名に番号を追加

while True:
    try:
        # エラーを検知
        data = json_get()
        list = json2list(data)
        # URLからjsonを取得し、listに格納

    except Exception:
        # エラーが出た場合
        # ※"hh:00"と重なると高確率で500 Errorとなる
        i = 0
        # カウンターの初期値設定
        while i < 5:
            # 5回再試行
            sleep(30)
            # 30秒待機
            try:
                data = json_get()
                list = json2list(data)
                # 再試行

            except Exception:
                i += 1
                if i >= 4:
                    list = [hdk, 'problem occured:' + time_set()[8:], 'Missing data']
                    # 5回全てエラーの場合、欠測を表示

                else:
                    pass
                    # エラーが出た場合は一度tryを抜けてループに戻る

            else:
                break
                # エラーが出なくなればループを抜けてそのまま続行

    if list[0] != hdk:
        # 日付が前回と変わっていた場合
        flname = time_set()[:8]
        # ファイル名用に現在時刻から日付を取得
        flname = str(int(flname) - 1)
        # 昨日の日付にするため-1する、concatするため文字型に変換
        if os.path.exists('./log/' + flname + '.json') or os.path.exists('./log/' + flname + '_' + l + '.json'):
            # 既にファイルが存在している場合
            l += 1
            # 番号に1追加
            os.rename(FILENAME, './log/' + flname + '_' + l + '.json')
            # ファイル名を"yyyymmdd_"に変更

        else:
            os.rename(FILENAME, './log/' + flname + '.json')
            # ファイル名を"yyyymmdd"に変更

        hdk = list[0]
        # 今回の日付をhdkに代入

    if list[1] != lastjkn:
        # 時間が前回と変わっていた場合
        write_line(list)
        # データを新しい行に記録
        lastjkn = list[1]
        # 今回の時間をlastjknに代入

    sleep(60)
    # 1分間待機

# 以下無限ループ
