import webvtt
import requests
from pysubparser import parser


# class CaptionsParser:
#     def save_captions(self, urlad, type, filename="data."):
#         # sending get request and saving the response as response object
#         r = requests.get(url=urlad)
#         # extracting data in json format
#         with open('data.' + str(type), 'wb') as f:
#             f.write(r.content)
#
#     def get_captions(self, file_name: str):
#         """Extract text from the currently loaded file."""
#         pass
#

# class VttParser(CaptionsParser):
def get_vtt_captions(file_name: str):
    subs = []
    language = "en"
    suffix = "en.us"
    totaltime = 0.0
    for caption in webvtt.read(file_name):
        duration = caption.end_in_seconds - caption.start_in_seconds
        subs.append((duration, caption.text))
        totaltime = caption.end_in_seconds
    return subs, totaltime

#
# class SRTParser(CaptionsParser):
#     def get_captions(self, file_name: str):
#         subtitles = parser.parse(file_name)
#         subs = []
#         language = "en"
#         suffix = "en.us"
#         totaltime = 0.0
#         for subtitle in subtitles:
#             totaltime += subtitle.duration
#             subs.append((subtitle.duration, subtitle.text))
#         return subs, suffix, language, totaltime
