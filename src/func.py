from pykakasi import kakasi
import pandas as pd
from scipy.stats import norm
import json

# 実行前にkakasiを立ち上げる必要あり
# from pykakasi import kakasi
# kakasi = kakasi()

def json_to_csv(file_path, stop_words):
    """
    :param file_path: String(File Path)
    :param stop_words: List
    :return: Pandas DataFrame
    """

    # jsonの読み込み
    df = pd.read_json(file_path)

    # jsonから各情報を取得
    word_df = pd.DataFrame(df['results']['items'])
    segment_df = pd.DataFrame(df['results']['speaker_labels']['segments'])
    spk_df = pd.DataFrame([item for x in segment_df.index for item in segment_df['items'][x]])

    # 単語認識結果と話者情報を結合
    for i in spk_df.index:
        key = spk_df.start_time[i]
        word_df.loc[word_df['start_time'] == key, 'type'] = spk_df.speaker_label[i]

    word_df = word_df.dropna()

    word_df = word_df.reset_index(drop=True)

    # 出力データフレームの定義
    cols = ['speaker', 'start_time', 'end_time', 'transcript']
    sentence_df = pd.DataFrame(index=[], columns=cols)

    sentence = ''
    starttime = word_df.start_time[word_df.index[0]]
    for i in word_df.index:
        word = word_df.alternatives[i][0]['content']
        speaker = word_df.type[i]
        sentence = sentence + word

        if i != word_df.index[-1]:
            next_speaker = word_df.type[i + 1]
            if speaker != next_speaker:
                # センテンス切り替え
                endtime = word_df.end_time[i]
                sentence_df = sentence_df.append(
                    pd.Series([speaker, starttime, endtime, sentence], index=sentence_df.columns), ignore_index=True)
                sentence = ''
                starttime = word_df.start_time[i + 1]
            else:
                if word in stop_words:
                    next_word = word_df.alternatives[i + 1][0]['content']
                    if next_word in stop_words:
                        continue
                    else:
                        # センテンスの切り替え
                        endtime = word_df.end_time[i]
                        sentence_df = sentence_df.append(
                            pd.Series([speaker, starttime, endtime, sentence], index=sentence_df.columns),
                            ignore_index=True)
                        sentence = ''
                        starttime = word_df.start_time[i + 1]
                else:
                    continue
        else:
            # センテンス切り替え
            endtime = word_df.end_time[i]
            sentence_df = sentence_df.append(
                pd.Series([speaker, starttime, endtime, sentence], index=sentence_df.columns), ignore_index=True)

    return sentence_df

def calc_speak_time(df, kakasi, speaker_id=None):
    """
    :param df: Pandas DataFrame
    :param kakasi: Kakasi Instance
    :param speaker_id: String
    :return: Pandas DataFrame
    """

    # ひらがなへのconverter準備
    kakasi.setMode('J', 'H')
    conv = kakasi.getConverter()

    speak_scores = []

    for i in df.index:
        speak_time = float(df.end_time[i]) - float(df.start_time[i])
        speak_length = len(conv.do(df.transcript[i]))
        speak_score = speak_time / speak_length
        speak_scores.append(speak_score)

    df['speak_scores'] = speak_scores

    if speaker_id is not None:
        if speaker_id not in df.speaker.unique():
            raise Exception(str(speaker_id) + ' does not exist in speaker column ')
        else:
            df = df[df.speaker == str(speaker_id)]
            df.reset_index(drop=True, inplace=True)

    return df

def change_point_detection(df, window_size=5, odds=0.10, low_side= True,output_type='extract'):
    """
    :param df: Pandas DataFrame
    :param window_size: Int
    :param odds: Float
    :param low_side: Boolean (True or False)
    :param output_type: String
    :return: Pandas DataFrame
    """

    if 'speak_scores' not in df.columns:
        raise Exception('speak_scores does not exist in df. Please do calc_speak_time() in advance.')

    roll_ave = df.speak_scores.rolling(window=window_size).mean()

    # 正規分布による近似を実施
    sample_points = df.speak_scores - roll_ave
    param = norm.fit(sample_points.dropna())
    upper_thres = norm.ppf(q=(1-odds), loc=param[0], scale=param[1])
    print('upper threshold is ' + str(upper_thres))

    if low_side is True:
        lower_thres = norm.ppf(q=odds, loc=param[0], scale=param[1])
        print('lower threshold is ' + str(lower_thres))
    else:
        lower_thres = -10000

    target_ind = df[(df.speak_scores - roll_ave >= upper_thres) | (df.speak_scores - roll_ave <= lower_thres)].index
    if output_type == 'extract':
        result = df[target_ind]
    elif output_type == 'all':
        df['roll_ave'] = roll_ave
        df['change_points'] = [1 if i in target_ind else 0 for i in df.index]
        result = df
    else:
        raise Exception('output_type should be "extract" or "all"')

    return result
