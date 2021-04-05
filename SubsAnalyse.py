#Israel
from sys import argv

def getCaptions(path):
    file = open(path,"r")
    lines = file.readlines()
    subs = []
    for i in range(1, len(lines), 4):
        times = lines[i].split('-->')
        start_time = times[0]
        end_time = times[1].strip('\n')
        start_times = start_time.split(":")
        hours = start_times[0]
        minutes = start_times[1]
        seconds = start_times[2].split(",")[0]
        start_time_seconds = float(hours)*3600 + float(minutes)*60 + float(seconds)
        end_times = end_time.split(':')
        hours = end_times[0]
        minutes = end_times[1]
        seconds = end_times[2].split(",")[0]
        end_time_seconds = float(hours) * 3600 + float(minutes * 60) + float(seconds)
        caption_time = end_time_seconds - start_time_seconds
        subs.append([start_time, end_time, caption_time, lines[i+1].strip('\n')])
    return subs