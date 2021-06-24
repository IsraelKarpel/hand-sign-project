import requests
from pysubparser import parser


def get_srt_captions(file_name: str):
    subtitles = parser.parse(file_name)
    subs = []
    language = "en"
    suffix = "en.us"
    totaltime = 0.0
    for subtitle in subtitles:
        s= subtitle.start
        e = subtitle.end
        duration = e.second-s.second
        totaltime += duration
        tt= e.second
        subs.append((duration, subtitle.text))
    return subs, tt
