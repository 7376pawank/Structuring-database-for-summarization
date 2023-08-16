import json
from sklearn.feature_extraction.text import TfidfVectorizer

with open("data.json", "r") as json_file:
    dictionaries = json.load(json_file)

headnote_sentences = []
judgement_sentences = []
for i in range(0,10000):
    print(i)
    first_dic = dictionaries[i]
    first_dictionary = json.loads(first_dic)
    print(first_dictionary)
    headnote_sentences.extend(first_dictionary['headnote_refined'])
    judgement_sentences.extend(first_dictionary['judgement_refined'])

tfidf_vectorizer = TfidfVectorizer()
headnote_tfidf = tfidf_vectorizer.fit_transform(headnote_sentences)
judgement_tfidf = tfidf_vectorizer.fit_transform(judgement_sentences)

#TF-IDF REPRESENTATION FOR HEADNOTES
for i, sentence in enumerate(headnote_sentences):
    print(f"Headnote Sentence {i+1}: {sentence}")
    print(f"TF-IDF Representation: {headnote_tfidf[i]}")
    print()

#TF-IDF REPRESENTATION FOR JUDGEMENTS
for i, sentence in enumerate(judgement_sentences):
    print(f"Judgement Sentence {i+1}: {sentence}")
    print(f"TF-IDF Representation: {judgement_tfidf[i]}")
    print()
