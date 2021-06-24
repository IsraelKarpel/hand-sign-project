# Israel and
import spacy
import fr_core_news_sm


# class CapParser:
#     def parse_captions(self,txt):
#         """Parse the captions file into POSE list.
#          Making it easier to map between raw words and how they'll appear in our dictionary ."""
#         pass
# # class Israelparserversion(Parser):
#


def LoadDictionaryAccordingToLanguage(language):
    if language == "zh":  # Chinese
        # python -m spacy download zh_core_web_sm
        return "zh_core_web_sm"
    if language == "da":  # Danish
        # python -m spacy download da_core_news_sm
        return "da_core_news_sm"
    if language == "nl":  # Dutch
        # python -m spacy download nl_core_news_sm
        return "nl_core_news_sm"
    if language == "en":  # English
        # python -m spacy download en_core_web_sm
        return "en_core_web_sm"
    if language == "fr":  # French
        # python -m spacy download fr_core_news_sm
        return "fr_core_news_sm"
    if language == "de":  # German
        # python -m spacy download de_core_news_sm
        return "de_core_news_sm"
    if language == "el":  # Greek
        # python -m spacy download el_core_news_sm
        return "el_core_news_sm"
    if language == "it":  # Italian
        # python -m spacy download it_core_news_sm
        return "it_core_news_sm"
    if language == "ja":  # Japanese
        # python -m spacy download ja_core_news_sm
        return "ja_core_news_sm"
    if language == "lt":  # Lithuanian
        # python -m spacy download lt_core_news_sm
        return "lt_core_news_sm"
    if language == "nb":  # Norwegian
        # python -m spacy download nb_core_news_sm
        return "nb_core_news_sm"
    if language == "pl":  # Polish
        # python -m spacy download pl_core_news_sm
        return "pl_core_news_sm"
    if language == "pt":  # Portuguese
        # python -m spacy download pt_core_news_sm
        return "pt_core_news_sm"
    if language == "ro":  # Romanian
        # python -m spacy download ro_core_news_sm
        return "ro_core_news_sm"
    if language == "re":  # Russian
        # python -m spacy download re_core_news_sm
        return "re_core_news_sm"
    if language == "es":  # Spanish
        # python -m spacy download es_core_news_sm
        return "es_core_news_sm"
    # multi_language
    # python -m spacy download xx_ent_wiki_sm
    return "xx_ent_wiki_sm"


def remove_punctuation(txt):
    # define punctuation
    punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    # remove punctuation from the string
    newtxt = ""
    for char in txt:
        if char not in punctuations:
            newtxt = newtxt + char
    return newtxt


def spellWord(word):
    word = word.upper()
    newWord = []
    for char in word:
        newWord.append('$' + char + '$')
    return newWord


def parse_captions(language, suffix,txt, dict):
    if suffix == "en.us":
        return english_parser(language, txt, dict)
    else:
        return universal_parser(language, txt, dict)


def english_parser(language, txt, dict):
    txt = remove_punctuation(txt)
    all_list = []  # For every word we save the original word, the basic word and its POS in the sentence
    basic_words = []  # Only the words in their basic format
    # get the current file of language syntax according to the syntax of the video
    correct_dict = LoadDictionaryAccordingToLanguage(language)
    nlp = dict.nlp_module
    sentence = nlp(txt)
    for token in sentence:
        # Ignore punctuations : / ' . , and so on
        if token.is_space or token.is_punct or token.lemma_ == "be" or token.text == "a" or token.text.lower() == "an" or token.text.lower() == "the":
            continue
        else:
            # For some reason, PRON needed to specify on his own
            if token.lemma_ == "-PRON-":
                if (dict.check_if_word_exist(token.orth_)):
                    basic_words.append(token.orth_)
                    all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
                else:
                    basic_words.extend(spellWord(token.orth_))
                    all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
            else:
                if (dict.check_if_word_exist(token.lemma_)):
                    basic_words.append(token.lemma_)
                    all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
                else:
                    basic_words.extend(spellWord(token.lemma_))
                    all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
        # print(all_list)
    print(basic_words)
    return basic_words, all_list


def universal_parser(language, txt, dict):
    txt = remove_punctuation(txt)
    all_list = []  # For every word we save the original word, the basic word and its POS in the sentence
    basic_words = []  # Only the words in their basic format
    # get the current file of language syntax according to the syntax of the video
    nlp = dict.nlp_module
    sentence = nlp(txt)
    for token in sentence:
        word = token.text
        # Ignore punctuations : / ' . , and so on
        if token.is_space or token.is_punct or token.lemma_ == "be" or token.text == "a" or token.text.lower() == "an" or token.text.lower() == "the":
            continue
        else:
            # For some reason, PRON needed to specify on his own
            if token.lemma_ == "-PRON-":
                basic_words.append(token.orth_)
                all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
            else:
                # if (dict.check_if_word_exist(token.lemma_)):
                basic_words.append(token.lemma_)
                all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
    print(basic_words)
    return basic_words, all_list
