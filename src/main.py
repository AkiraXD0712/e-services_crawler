import argparse
from log import setDebug
import time
from AnalyzeInnerHTML import Analyser
from Eservices_crawler import Crawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, help='username required')
    parser.add_argument('--password', type=str, help='password required')
    parser.add_argument('--mode', type=str, default='i', help='choose info mode(i) or debug mode(d)')
    parser.add_argument('--executable_path',
                        type=str,
                        default="C:\\Users\Akira.DESKTOP-HM7OVCC\Desktop\phantomjs.exe",
                        help='choose info mode(i) or debug mode(d)')
    args = parser.parse_args()
    if args.mode == 'd':
        setDebug()
    if args.username and args.password:
        spider = Crawler(args.username, args.password, args.executable_path)
        analyser = Analyser()
        spider.connect()
        inner = spider.to_note()
        analyser.analyze_notes(inner)
        time.sleep(10)
        inner = spider.to_absence()
        analyser.analyze_absences(inner)