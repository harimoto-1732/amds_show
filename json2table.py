import os, pandas as pd
from time import sleep
# moduleをインポート

file = "./log/_data.json"
# ファイルディレクトリを指定
stmp = ""
# ファイル更新時間の初期値設定

while True:
    while True:
    # 取得できるまでループ
        try:
        # エラーを検知
            tstmp = os.path.getmtime(file)
            # ファイルの最終更新日時を取得
    
        except:
        # 更新日時が取得できなかった場合
            sleep(60)
            # 1分間待機して再試行
            
        else:
            break
            # エラーが出無くなればループを抜けて続行

    if tstmp == stmp:
    # 前回と更新時間が同じ場合
        pass
        # 何もしない

    else:
    # 前回と更新時間が変わっていた場合
        stmp = tstmp
        # 前回の時間を今回の時間と置き換え
        df = pd.read_json(file, lines=True)
        # jsonを読み込み
        df.replace({3: {0: '北', 1: '北北東', 2: '北東', 3: '東北東', 4: '東', 5: '東南東', 6: '南東', 7: '南南東', 8: '南', 9: '南南西', 10: '南西', 11: '西南西', 12: '西', 13: '西北西', 14: '北西', 15: '北北西', 16: '北'}}, inplace=True)
        # 方位を示す数字を置き換え
        df.set_axis(["日時", "気温(℃)", "降水(mm)", "風向(16方位)", "風速(m/s)"], axis=1, inplace=True)
        # 列タイトルを追加

        result = df.to_html(justify='center', index=False).replace('<td>', '<td align="right">')
        # 処理後のjsonをhtmlテーブルに変換/1行目を中央揃え/データを右揃え

        with open("./log/index.html", "w") as out:
        # htmlを書き込みモードで開く/存在しない場合は新たに作る
            out.write(result)
            # htmlテーブルに変換したresultを書き込み
    
    sleep(60)
    # 1分間待機

# 以下無限ループ
