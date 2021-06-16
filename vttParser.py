import webvtt
def get_captions(name):
    subs =[]
    language = "en"
    suffix= "en.us"
    for caption in webvtt.read(name):
        print(caption.start)
        print(caption.end)
        print(caption.text)
        duration = caption.end_in_seconds-caption.start_in_seconds
        subs.append((duration,caption.text))
    return subs,suffix,language