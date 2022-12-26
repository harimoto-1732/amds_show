import pandas as pd
# moduleをインポート

file = "./log/_data.json"
# ファイルディレクトリを指定

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
