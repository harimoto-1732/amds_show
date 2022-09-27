import requests, json, ndjson, datetime, os
from time import sleep
# moduleをインポート

def json_get():
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
    return(dt_now.strftime('%Y%m%d'))
    # ファイル名用に日付を代入

def write_line():
    with open('log/_data.json', 'a') as f:
        # 書き込み先ファイルを開く
        writer = ndjson.writer(f)
        writer.writerow(list)
        # ファイルに書き込む 
        return(list[1])
        # 今回の時間を返す

def newfile():
# 新しいファイルを作成
    new = open('log/_data.json', 'w')
    # 新しいファイルを作成
    new.close
    # ファイルを閉じる

URL = "https://weather-nkkmd.herokuapp.com/amds?point=69101"

lastjkn = "99:99"
# 時刻の初期値を設定
hdk = "9999/99/99"
# 日付の初期値を設定

while True:
    if os.path.isfile('log/_data.json'):
        try:
            flname = time_set()

            data = json_get()
            list = json2list(data)

            if list[0] != hdk:
            # 日付が前回と変わっていた場合
                filename = filename - 1
                # 昨日の日付にするため-1する
                os.rename('log/_data.json', 'log/' + flname + '.json')
                # ファイル名を日付に変更

            if list[1] != lastjkn:
                lastjkn = write_line()
            
            sleep(60)
            # 1分間待機

        except Exception:
            pass
            # エラーが出た場合はスキップ
            # ※アメダスデータの更新時間と重なると500 Errorとなる場合がある

    else:
        newfile()

    # 以下無限ループ
