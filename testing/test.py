import requests

def test_sentences1():
    print("Sentences API Test")
    count_success = 0
    counttests = 0
    with open("sentence_requests.txt", "r") as file:
        #d: simple word,s:test,slang:en,dlang:es,fps:30
        # extracting each data row one by one
        for row in file:
            counttests += 1
            parts = row.split(',')
            description = parts[0].split(':')[1]
            sentence = parts[1].split(':')[1].replace(" ","+")
            slang = parts[2].split(':')[1]
            dlang = parts[3].split(':')[1]
            fps = parts[4].split(':')[1]
            url ="https://nlp.biu.ac.il/~ccohenya8/sign/sentence/?slang={0}&dlang={1}&sentence={2}&fps={3}".format(slang,dlang,sentence,fps)
            print(url)
            r = requests.get(url)
            if r.status_code == 200:
                count_success += 1
                print("✔ succeeded")
            else:
                print("failed")
    print("{0}% tests succeeded".format(str(count_success / counttests * 100)))


def test_youtube():
    print("Youtube API Test")
    count_success=0
    counttests = 0
    with open("youtube_requests.txt", "r") as file:
        for row in file:
            counttests +=1
            parts = row.split(',')
            vidid = parts[0]
            lang = parts[1][:5]
            url ="https://nlp.biu.ac.il/~ccohenya8/sign/youtube/?v={0}&lang={1}".format(vidid,lang)
            print(url)
            r = requests.get(url)
            if r.status_code == 200:
                count_success+=1
                print("✔ succeeded")
            else:
                print("failed")
    print("{0}% tests succeeded\n".format(str(count_success/counttests*100)))

test_youtube()
test_sentences1()