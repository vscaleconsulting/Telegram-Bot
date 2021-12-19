#! C:\Users\kosha\AppData\Local\Programs\Python\Python39\python.exe

import argparse

from scrapers.functions import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="starting index", type=int)
    parser.add_argument("lines", help="number of lines in each file", type=int)
    parser.add_argument("num_files", help="number of files to generate", type=int, nargs='?')
    args = parser.parse_args()

    if 'splits' not in os.listdir():
        os.mkdir('splits')

    split_csv('Campaign.csv', start=args.start, lines=args.lines, num_files=args.num_files, dest='splits/')
