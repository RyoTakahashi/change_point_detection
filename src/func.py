from pykakasi import kakasi
import pandas as pd

# 実行前にkakasiを立ち上げる必要あり
# from pykakasi import kakasi
# kakasi = kakasi()


def calc_speak_time(df, kakasi, speaker_id=None):

    # ひらがなへのconverter準備
    kakasi.setMode('J', 'H')
    conv = kakasi.getConverter()

    speak_scores = []

    for i in df.index:
        speak_time = df.end_time[i] - df.start_time[i]
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


def change_point_detection(df, window_size=5, threshold=0.15, output_type='extract'):

    if 'speak_scores' not in df.columns:
        raise Exception('speak_scores does not exist in df. Please do calc_speak_time() in advance.')

    roll_ave = df.speak_scores.rolling(window=window_size).mean()

    if output_type == 'extract':
        result = df[abs(df.speak_scores - roll_ave) >= threshold]
    elif output_type == 'all':
        df['roll_ave'] = roll_ave
        df['change_points'] = [1 if abs(df.speak_scores[i] - roll_ave[i]) >= threshold else 0 for i in range(len(df.speak_scores))]
        result = df
    else:
        raise Exception('output_type should be "extract" or "all"')

    return result
