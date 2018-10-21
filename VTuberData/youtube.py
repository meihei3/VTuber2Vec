from apiclient.discovery import build
from apiclient.errors import HttpError

import argparse
import pandas as pd
from datetime import datetime, timedelta

from config import API_KEY

DEVELOPER_KEY = "%s"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

SIRO_CHANNEL_ID = "UCLhUvJ_wO9hOvv_yYENu4fQ"


def check_http_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    return wrapper


def YouTube(api=API_KEY):
    if api == "":
        raise ValueError("You must input API key.")
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api)


def video_id_to_channel_id(yt: str, mid: str):
    return yt.search().list(
        q=mid,
        part="snippet"
    ).execute()["items"][0]["snippet"]["channelId"]


class Channel(object):
    def __init__(self, _youtube, channel_id):
        self._youtube = _youtube
        self._channel_id = channel_id
        self.__update()
        if self.__channel_response["pageInfo"]["totalResults"] != 1:
            raise ValueError("This channel id is not found.")

    def get_video(self):
        # nextPageTokenはバグるけど100件なら行ける！
        res = {"published_at": [], "video_id": [], "title": []}
        token = None
        for _ in range(2):
            search_response = self.__search(part="snippet", max_result=50, token=token)
            res["title"] += [item["snippet"]["title"] for item in search_response["items"]]
            res["published_at"] += [item["snippet"]["publishedAt"] for item in search_response["items"]]
            res["video_id"] += [item["id"]["videoId"] for item in search_response["items"]]
            if search_response["pageInfo"]["totalResults"] == 0:
                break
            if "nextPageToken" in search_response:
                token = search_response["nextPageToken"]
        return res

    @check_http_error
    def __update(self):
        self.__channel_response = self._youtube.channels().list(
            part="id, snippet, brandingSettings, contentDetails, invideoPromotion, statistics, topicDetails",
            id=self._channel_id
        ).execute()

    @check_http_error
    def __search(self, part="id", max_result=25, order="date", token=None):
        return self._youtube.search().list(
            channelId=self._channel_id,
            part=part,
            maxResults=max_result,
            order=order,
            type="video",
            pageToken=token
        ).execute()


def create_df(api="", channel_id=SIRO_CHANNEL_ID, n=100):
    yt = YouTube(api)
    ch = Channel(yt, channel_id)
    df = pd.DataFrame(ch.get_video())
    df["url"] = df["video_id"].apply(lambda s: "https://www.youtube.com/watch?v=%s" % s)
    df["published_at"] = df["published_at"].apply(
        lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=9))
    df = df.sort_values("published_at").reset_index(drop=True)
    return df


def main(options):
    df = create_df(api=options.api, channel_id=options.target_id, n=options.count)
    df.to_csv("videos.csv")
    print(df)


def update(options):
    # 過去n件からでーたを習得してcsvデータファイルに追加
    # 過去n件以上の差があると穴ができる
    # 仕様変えたので使ってはいけない
    assert False, "TODO：新仕様に対応"
    df = pd.read_csv("videos.csv", index_col=0, parse_dates=["published_at"])
    last = df["published_at"].iloc[-1]
    new_df = create_df(api=options.api, channel_id=options.target_id, n=options.count)
    df = pd.concat([df, new_df[new_df["published_at"] > last]])
    df.to_csv("videos.csv")
    print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The csv of videos data creator from YouTube API")
    parser.add_argument("--update", action='store_true', help="update the csv data if there is")
    parser.add_argument("-t", "--target_id", type=str, help="the target channel id", default=SIRO_CHANNEL_ID)
    parser.add_argument("-x", "--api", type=str, help="the GCP API key", required=True)
    parser.add_argument("-n", "--count", type=int, help="the number of results", default=100)
    args = parser.parse_args()
    if args.update:
        update(args)
    else:
        main(args)
