# Change Point Detection
Amazon Transcribe（JP）の結果から、発話量を測定。発話量の変化点を検知する。

## 必要なライブラリ
``
$ pip install -r requirements.txt
``

環境は`Python 3.6.7`

## 利用方法
``
$ python main.py -conf="./src/conf.yml" '
``

## conf.ymlの内容
- input_path: Amazon Transcribeで書き起こしをしたcsvファイルもしくはjsonファイル
- output_path: 出力エクセルファイルの吐き出し先とファイル名
- speaker_id: 対象としたいSpeaker_id（file内のspeakerカラムから持ってくる）。Noneとした場合はSpeakerを区別せず実行。
- window_size: 変化点検知をする際に用いる比較値の算出幅（前後センテンスに対する発話量の平均値を用いるか）。
- odds: 変化点検知をする際に比較値とどのくらい離れていれば変化点とするかのしきい値。推奨は0.10。
- output_type: しきい値以上の変化点のみを出力したい場合は'extract'を指定。すべて出力したい場合は'all'を渡す。デフォルトは'extract'
- stopwords: input_pathがjsonの場合のみ有効。発話を分割する際に利用したい単語のリスト