import requests, json, ndjson, datetime, os
from time import sleep
# moduleをインポート

url = requests.get("https://weather-nkkmd.herokuapp.com/amds?point=69101")
# URLを指定
text = url.text
# jsonをテキストファイルに

data = json.loads(text)
# jsonを配列として読み込み
kion = data['temp']
uryou = data['precipitation10m']
fuuko = data['windDirection']
fuusoku = data['wind']
jikan = data['dataTime']
# 各値を代入
    
list = [jikan[0][:10], jikan[0][11:16], kion[0], uryou[0], fuuko[0], fuusoku[0]]
# 代入された値から配列を作成
hdk = list[0]
# 日付を記録
lastjkn = list[1]
# 時刻を記録

dt_now = datetime.datetime.now()
# PC設定から現在時刻を取得
flname = dt_now.strftime('%Y%m%d')
# ファイル名用に日付を代入

nwe = open('log/' + flname + '.json', 'w')
# 新しいファイルを作成
json.dump(list, nwe)
# 1行目をファイルに書き込み
nwe.close
# ファイルを閉じる

while True:
    dt_now = datetime.datetime.now()
    # PC設定から現在時刻を取得
    flname = dt_now.strftime('%Y%m%d')
    # ファイル名用に日付を代入

    url = requests.get("https://weather-nkkmd.herokuapp.com/amds?point=69101")
    # URLを指定
    text = url.text
    # jsonをテキストファイルに
    result = []
    try:
        data = json.loads(text)
        result.append(data['info'])
        # jsonをdictとして読み込み
    except Exception:
        pass
        # エラーが出た場合はスキップ
        # ※アメダスデータの更新時間と重なると500 Errorとなる
    kion = data['temp']
    uryou = data['precipitation10m']
    fuuko = data['windDirection']
    fuusoku = data['wind']
    jikan = data['dataTime']
    # 各値を代入
    
    list = [jikan[0][:10], jikan[0][11:16], kion[0], uryou[0], fuuko[0], fuusoku[0]]
    # 代入された値からdictを作成

    if list[0] != hdk:
    # 日付が前回と変わっていた場合
        nwe = open('log/' + flname + '.json', 'w')
        # 新しいファイルを作成
        json.dump(list, nwe)
        # 1行目をファイルに書き込み
        nwe.close
        # ファイルを閉じる
        hdk = list[0]
        # 今回の日付を記録


    if list[1] != lastjkn:
    # 時間が前回と変わっていた場合
        with open('log/' + flname + '.json', 'a') as f:
        # 書き込み先ファイルを開く
            writer = ndjson.writer(f)
            writer.writerow(list)
            # ファイルに書き込む 
            lastjkn = list[1]
            # 今回の時間を記録

    sleep(60)
    # 1分間待機
    # 以下無限ループ
