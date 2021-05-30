import json


class Dictionaries:
    def __init__(self):
        self.dictionaries = []

    def add_dictionary(self, dict):
        self.dictionaries.append(dict)

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
