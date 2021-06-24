import json
import Dictionary

class Dictionaries:
    def __init__(self,path= "langs.txt"):
        file = open(path, 'r', encoding='utf-8')
        dictionariesarr = []
        if file:
            for line in file.readlines():
                parts = line.split()
                dict = Dictionary.PoseDictionary(parts[0], parts[1], parts[2])
                dictionariesarr.append(dict)
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
                    dic.wordToID[pose["texts"][0]["text"]] = pose["id"]
            file.close()
        else:
            print("Dictionaries: couldn't load word to ID dictionary")
