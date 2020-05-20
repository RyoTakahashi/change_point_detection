from pykakasi import kakasi
import pandas as pd
import argparse
from src.func import calc_speak_time, change_point_detection

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--file",
                        help="Amazon Transcribe output file",
                        type=str)
    parser.add_argument("--output_path",
                        help="Output file",
                        type=str)
    parser.add_argument("--speaker_id",
                        help="Speaker_id you want to analyze",
                        type=str)
    parser.add_argument("--window_size",
                        help="window size is a parameter to calculate the base metrics for change point "
                             "/detection : default is 5",
                        type=int)
    parser.add_argument("--threshold",
                        help="threshold is a parameter uses to detect the change point : default is 0.15",
                        type=float)
    parser.add_argument("--output_type",
                        help="output_type is a parameter uses to decide output format: default is extract",
                        type=str)

    args = parser.parse_args()

    if not args.file:
        raise Exception('Please set your transcribe file. --file="path/to/your/file"')

    if not args.output_path:
        raise Exception('Please set output file path . --output_path="path/to/output/file"')

    if not args.speaker_id:
        args.speaker_id = None

    if not args.window_size:
        args.window_size = 5

    if not args.threshold:
        args.threshold = 0.15

    if not args.output_type:
        args.output_type = 'extract'

    df = pd.read_csv(args.file)
    kakasi = kakasi()

    df1 = calc_speak_time(df=df, kakasi=kakasi, speaker_id=args.speaker_id)

    remark_df = change_point_detection(df1, window_size=args.window_size, threshold=args.threshold, output_type=args.output_type)

    remark_df.to_excel(args.output_path, index=False)

    print(remark_df)


