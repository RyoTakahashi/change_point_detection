from pykakasi import kakasi
import pandas as pd
import argparse
import yaml
import json
from src.func import calc_speak_time, change_point_detection, json_to_csv

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-conf', help='YAML file path', required=True)
    args = parser.parse_args()

    with open(args.conf, "r") as f:
        configs = yaml.safe_load(f)
    f.close()

    input_file = configs['input_path']
    output_file = configs['output_path']
    speaker_id = configs['speaker_id']
    window_size = configs['window_size']
    odds = configs['odds']
    output_type = configs['output_type']

    if input_file.endswith('.csv'):
        print('===Reading .csv file===')
        df = pd.read_csv(input_file)
    elif input_file.endswith('.json'):
        print('===Reading .json file===')
        stop_words = configs['stop_words']
        df = json_to_csv(file_path=input_file, stop_words=stop_words)
    else:
        Exception('Input file must be .csv or .json format')


    kakasi = kakasi()

    print('===Calculating Scores===')
    df_computed = calc_speak_time(df=df, kakasi=kakasi, speaker_id=speaker_id)

    remark_df = change_point_detection(df_computed,window_size=window_size, odds=odds, low_side=False, output_type=output_type)

    print('===Saving output .xlsx file===')
    remark_df.to_excel(output_file, index=False)

    print('===Saved===')


