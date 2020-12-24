import spacy
import os

all_list = []
basic_words = []

nlp = spacy.load("en_core_web_sm")

doc = nlp("I loved pizza very much ""     " " . / :")

for token in doc:
    # Ignore punctuations : / ' . , and so on
    if not token.is_punct and not token.is_space:
        # For some reason, PRON needed to specify on his own
        if token.lemma_ == "-PRON-":
            basic_words.append(token.orth_)
            all_list.append(token.text + "_" + token.orth_ + "_" + token.pos_)
        else:
            basic_words.append(token.lemma_)
            all_list.append(token.text + "_" + token.lemma_ + "_" + token.pos_)
print(all_list)

#my directory conatins only I.pose love.pose and pizza.pose
for i in basic_words:
    if os.path.isfile("/home/israelk/Desktop/examples/" + i + ".pose"):
        print("true")
    else:
        print("fales")

