# Change Point Detection
Amazon Transcribe（JA）の結果から、発話量を測定。発話量の変化点を検知する。

## 必要なライブラリ
``
$ pip install -r requirements.txt
``

## 利用方法
``
$ python main.py --file="path/to/your/transcribe/file" --output_path="hoge/result.xlsx"--speaker_id="spk_1" --window_size=5 --threshold=0.15 --output_type="extract"'
``

- file ... Amazon Transcribeで書き起こしをしたcsvファイル
- output_path ... 出力エクセルファイルの吐き出し先とファイル名
- speaker_id ... 対象としたいSpeaker_id（file内のspeakerカラムから持ってくる）。指定しない場合はSpeakerを区別せず実行。
- window_size ... 変化点検知をする際に用いる比較値の算出幅（前後センテンスに対する発話量の平均値を用いるか）。指定しない場合は5。
- threshold ... 変化点検知をする際に比較値とどのくらい離れていれば変化点とするかのしきい値。指定しない場合は0.15。
- output_type ... しきい値以上の変化点のみを出力したい場合は'extract'を指定。すべて出力したい場合は'all'を渡す。デフォルトは'extract'