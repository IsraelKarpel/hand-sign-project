import spacy
#
# class Word:
#     def __init__(self,word):
#         self.original_word = word
#         self.basic_word =
#         self.pos = None
class LanguageParser:
    def parse_sentence(self, txt):
        pass

    def remove_punctuation(self, txt):
        # define punctuation
        punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
        # remove punctuation from the string
        newtxt = ""
        for char in txt:
            if char not in punctuations:
                newtxt = newtxt + char
        return newtxt


class EnglishParser(LanguageParser):
    def parse_captions(self, txt):
        txt = self.remove_punctuation(txt)
        correct_dict = "en_core_web_sm"  # get the currect file of language syntax according to the syntax of the video
        nlp = spacy.load(correct_dict)
        sentence = nlp(txt)
        all_list = []  # For every word we save the original word, the basic word and its POS in the sentence
        basic_words = []  # Only the words in their basic format
        for token in sentence:
            # Ignore punctuations : / ' . , and so on
            if token.lemma_ == "be":
                continue
            if not token.is_punct and not token.is_space:
                # For some reason, PRON needed to specify on his own
                if token.lemma_ == "-PRON-":
                    basic_words.append(token.orth_)
                    all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
                else:
                    basic_words.append(token.lemma_)
                    all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
            # print(all_list)
        return basic_words, all_list
