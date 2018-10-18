# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd

from youtube import YouTube, movieId2channelId

BASE_URL = 'https://virtual-youtuber.userlocal.jp'
RANKING_URL = BASE_URL + '/document/ranking'


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
    mid = get_one_video(url).split('?v=')[-1]
    return movieId2channelId(YouTube(), mid)


def get_one_video(url: str):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("div", attrs={"class": "card card-video"})[0].get("data-video-url")


if __name__ == '__main__':
    for i, n, u in ranking(n=51):
        print(i, n, u)