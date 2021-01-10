from spiders.spider import download_book
import argparse

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--url', '-u', required=True, help='book url')
    args_parser.add_argument(
        '--output', '-o', required=True, help='output epub path')
    args = args_parser.parse_args()
    download_book(args.url, args.output)
