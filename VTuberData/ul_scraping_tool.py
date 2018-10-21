# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from tqdm import tqdm
import argparse

from youtube import YouTube, movieId2channelId

BASE_URL = 'https://virtual-youtuber.userlocal.jp'
RANKING_URL = BASE_URL + '/document/ranking'

YouTube = YouTube()


def get_ranking_page(page: int = 1):
    html = requests.get(RANKING_URL+"?page={}".format(page)).text
    return BeautifulSoup(html, 'html.parser')


def ranking(n: int = 100):
    for page in range(int(n/50+1)):
        soup = get_ranking_page(page+1)
        for i, tr in enumerate(soup.find_all("tr")):
            if 50 * page + i >= n:
                break
            yield 50 * page + i + 1, tr.a.img.get("alt"), BASE_URL+tr.get("data-href")


def get_channel_id(url: str):
    for url in get_videos_url(url):
        try:
            mid = url.split("?v=")[-1]
            return movieId2channelId(YouTube, mid)
        except IndexError:
            pass
    raise IndexError


def get_videos_url(url: str):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return [c.get("data-video-url") for c in soup.find_all("div", attrs={"class": "card card-video"})]


def create_ranking_csv(n: int = 100):
    d = {"name": [], "ranking": [], "userlocal-url": [], "youtube-url": [], "channel_id": []}
    for i, name, url in tqdm(ranking(n), total=n):
        d["name"].append(name)
        d["ranking"].append(i)
        d["userlocal-url"].append(url)
        cid = get_channel_id(url)
        d["youtube-url"].append("https://www.youtube.com/channel/"+cid)
        d["channel_id"].append(cid)
        time.sleep(3)  # サーバーに負荷をかけないため
    pd.DataFrame(d).to_csv("VTuber_list.csv")


def update():
    # ToDo:実装
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scraping UserLocal data and Save videos meta data from YouTube API")
    parser.add_argument("--init", action='store_true', help="create new VTuber ranking cvs")
    parser.add_argument("--update", action='store_true', help="update csv data")
    args = parser.parse_args()
    if args.init:
        create_ranking_csv(100)
    elif args.update:
        update()
