# Israel
import spacy
# class CapParser:
#     def parse_captions(self,txt):
#         """Parse the captions file into POSE list.
#          Making it easier to map between raw words and how they'll appear in our dictionary ."""
#         pass
# # class Israelparserversion(Parser):
#

def parse_captions1(txt):
    all_list = []  # For every word we save the original word, the basic word and its POS in the sentence
    basic_words = []  # Only the words in their basic format
    nlp = spacy.load("en_core_web_sm")

    sentence = nlp(txt)

    for token in sentence:
        # Ignore punctuations : / ' . , and so on
        if not token.is_punct and not token.is_space:
            # For some reason, PRON needed to specify on his own
            if token.lemma_ == "-PRON-":
                basic_words.append(token.orth_)
                all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
            else:
                basic_words.append(token.lemma_)
                all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
        # print(all_list)
    return basic_words,all_list





