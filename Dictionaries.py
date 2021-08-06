import json
import Dictionary
from codecs import encode


class Dictionaries:
    def __init__(self, path="langs.txt"):
        file = open(path, 'r', encoding='utf-8')
        dictionariesarr = []
        if file:
            for line in file.readlines():
                parts = line.split()
                dict = Dictionary.PoseDictionary(parts[0], parts[1], parts[2])
                dictionariesarr.append(dict)
                print("loaded " + str(dict.lang))
            file.close()
            self.dictionaries = dictionariesarr
        else:
            print("Wrong path, couldn't load languages")
            exit(-1)

    def add_dictionary(self, dict):
        if dict:
            self.dictionaries.append(dict)
        else:
            print("Dictionaries: couldn't add dictionary")

    def getdictionarybysuffix(self, suffix):
        for dict in self.dictionaries:
            if dict.suffix == suffix:
                return dict

    def createAllWordToID(self, path="index.jsonl"):
        file = open(path, 'r', encoding='utf-8')
        if file:
            for line in file.readlines():
                pose = json.loads(line)
                dic = self.getdictionarybysuffix(pose["sign_language"])
                if dic:
                    word = encode(pose["texts"][0]["text"].encode().decode('unicode_escape'), "raw_unicode_escape").decode('utf-8')
                    dic.wordToID[word] = pose["id"]
                    if pose["id"][0]=='$':
                        pose_id=-1
                    else:
                        pose_id = int(pose["id"].split('_')[0])
                    dic.IdToWord[pose_id]=word
            file.close()
        else:
            print("Dictionaries: couldn't load word to ID dictionary")
