# Change Point Detection
Amazon Transcribe（JA）の結果から、発話量を測定。発話量の変化点を検知する。

## 必要なライブラリ
``
$ pip install -r requirements.txt
``

## 利用方法
``
$ python main.py --file="path/to/your/transcribe/file" --speaker_id="spk_1" --window_size=5 --threshold=0.15
``

- file ... Amazon Transcribeで書き起こしをしたcsvファイル
- speaker_id ... 対象としたいSpeaker_id（file内のspeakerカラムから持ってくる）。指定しない場合はSpeakerを区別せず実行。
- window_size ... 変化点検知をする際に用いる比較値の算出幅（前後センテンスに対する発話量の平均値を用いるか）。指定しない場合は5。
- threshold ... 変化点検知をする際に比較値とどのくらい離れていれば変化点とするかのしきい値。指定しない場合は0.15。