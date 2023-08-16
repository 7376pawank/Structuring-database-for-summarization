import re
import nltk
from nltk.corpus import wordnet
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# List to store the file contents
file_contents = []

# List of abbreviations
abbreviations_list = {
    "adv.":"Advocate",
    "Adv.": "Advocate",
    "S.C.R.":	"Supreme Court Reporter",
    "S. C. R.": "Supreme Court Reporter",
    "ANR.":	"Another",
    "ORS.":	"Others",
    "Cr. P. C.":"Criminal Procedure Code",
    "Smt.":	"Shrimati",
    "Co.":	"Company",
    "Art.": "Article",
    "art.": "article",
    "s." :	"Section",
    "Sec.":	"Section",
    "sec.": "Section",
    "sub-s.":"Sub Section",
    "viz.":	"videlicet",
    "ltd.":	"limited",
    "a.i.r." : "All India Reporter",
    "f.i.r." :	"First Information Report",
    "i.p.c." :	"Indian Penal Code",
    "p.w.":	"Procecuted Witness",
    "cl.":	"Clauses",
    "cls.":	"Clauses",
    "ex.":	"exhibit",
    "Ex.": "Exhibit",
    "schs.": "schedules",
    "No." : "number",
    "no." : "number",
    "num.": "number",
    "M/s.": "Messrs",
    "Lt." : "Lieutenant",
    "etc.": "etcetera",
    "Prof.": "Professor",
    "Ave.": "Avenue",
    "Corp.": "Corporation",
    "Gov.": "Government",
    "Inc.": "Incorporated",
    "Sr.": "Senior",
    "Jr.": "Junior",
    "qtls.": "quintals",
    "a." : "article",
    "as.": "assize",
    "C.P.C.":"Code of Civil Procedure",
    "C. P. C.":"Code of Civil Procedure",
    "Ch.": "Chapter",
    "Asstt.": "Assistant",
    "C.A.": "Civil Appeal"
}

def replace_abbreviations(document, abbreviations):
    words = document.split()
    replaced_words = []

    for word in words:
        if word in abbreviations:
            replaced_words.append(abbreviations[word])
        else:
            replaced_words.append(word)

    replaced_document = ' '.join(replaced_words)
    return replaced_document

def get_wordnet_pos(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('R'):
        return wordnet.ADV
    elif tag.startswith('J'):
        return wordnet.ADJ
    else:
        return wordnet.NOUN

def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    tagged_words = nltk.pos_tag(tokens)  # Perform POS tagging
    lemmas = []
    for word, tag in tagged_words:
        pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(word, pos=pos)
        lemmas.append(lemma)
    return lemmas

def combine_hyphenated_words(document):
    hyphenated_words = re.findall(r"\b(\w+)-\s*\n?\s(\w+)\b", document)
    for hyphenated_word in hyphenated_words:
        combined_word = hyphenated_word[0] + hyphenated_word[1]
        document = document.replace('- '.join(hyphenated_word), combined_word)
    return document

def convert_name_format(name):
    parts = name.split(",")  # Split the name by comma
    if len(parts) == 2:
        surname = parts[0].strip()  # Remove leading/trailing whitespaces
        firstname = parts[1].strip()  # Remove leading/trailing whitespaces
        converted_name = f"{firstname} {surname}"  # Combine firstname and surname
        # print(converted_name)
        return converted_name
    else:
        return name

def remove_extraspace_and_title_from_name(name):
    name = re.sub(r"\(J\)|\(CJ\)", "", name)  # Remove (J) or (CJ) using regex substitution
    name = re.sub(r"\s+", " ", name)  # Replace multiple spaces with a single space
    name = re.sub(r"\(","", name)
    name = name.strip()  # Remove leading/trailing whitespaces
    return name

def remove_punctuations_stopwords(tokens):
    import string
    from nltk.corpus import stopwords
    punctuation = set(string.punctuation)
    stopwords = set(stopwords.words('english'))
    tokens_no_punct = [token for token in tokens if token not in string.punctuation]
    tokens_no_stop = [token for token in tokens_no_punct if token.lower() not in stopwords]
    return tokens_no_stop


def combine_percentages(tokens):
    combined_tokens = []
    i = 0
    while i < len(tokens):
        current_token = tokens[i]

        # Check if the current token is a percentage value
        if re.match(r'\d+(\.\d+)?$', current_token) and i + 1 < len(tokens) and tokens[i + 1] == '%':
            combined_tokens.append(current_token + '%')
            i += 1

        elif re.match(r'\w+$', current_token) and i+1 < len(tokens) and tokens[i+1] == "'s":
            combined_tokens.append(current_token + tokens[i+1])
            i += 1

        else:
            combined_tokens.append(current_token)
        i += 1
    return combined_tokens


def remove_unwanted_words(sentence):
    pattern = r"\[[^\]]*\]|\d+\."
    return re.sub(pattern, "", sentence)


def post_process_of_sentences(sentences):
    import enchant
    dictionary = enchant.Dict("en_US")
    def is_valid_acronym(s):
        return re.match(r'\b(?:[A-Z][a-z]{0,3}\.|[a-z]{0,4}\.)+', s)

    merged_sentences = []
    current_sentence = sentences[0]

    for next_sentence in sentences[1:]:
        if is_valid_acronym(current_sentence.split()[-1]) and not dictionary.check(current_sentence.split()[-1]):
            current_sentence += " " + next_sentence

        elif is_valid_acronym(current_sentence.split()[-1]) and is_valid_acronym(next_sentence.split()[0]):
            current_sentence += " "+next_sentence

        elif re.match( r"\d{4}",current_sentence.split()[-1]) and re.match(r"[A-Za-z]+\s\d{1,2}", next_sentence):
            current_sentence += " "+next_sentence

        elif not next_sentence[0].isupper():
            current_sentence += " "+ next_sentence

        elif len(current_sentence.split()) == 1 :
            current_sentence += " " + next_sentence

        else:
            merged_sentences.append(current_sentence)
            current_sentence = next_sentence

    merged_sentences.append(current_sentence)
    return merged_sentences

def remove_multiple_punctuations(tokens):
    filtered_tokens = []
    for token in tokens:
        if not re.match(r'^\W+$', token):
            filtered_tokens.append(token)
    return filtered_tokens

def json_data_func(judgement):

    # EXTRACT TITLE
    title_pattern = r"(.+)\n"
    title = re.search(title_pattern, judgement).group(1).strip()


    #EXTRACT DATE
    date_pattern = r'\((\d+\s[A-Za-z]+\s\d+)\)'
    dates = re.search(date_pattern, title)
    date = dates.group(1)


    #EXTRACT ACT
    act_regex = r'ACT:\n(.*?)\nHEADNOTE'
    act_match = re.search(act_regex, judgement, re.DOTALL)
    act = act_match.group(1).strip()
    act=replace_abbreviations(act, abbreviations_list)
    act = re.sub(r"\n", " ", act)


    # EXTRACT HEADNOTES
    match1 = re.search(r'HEADNOTE:(.*?)(APPEAL|APPELLATE|OR[I|l]G[I|l]NAL|APPELLANT|CRIMINAL|CIVIL|REVIEW|Civil\sAppella|Criminal\sAppella|Original\sJurisdiction|EXTRA\sORDINARY)', judgement, re.DOTALL )
    match2 = re.search(r'HEADNOTE:(.*?)(Civil\sAppeal\sNo\.)', judgement, re.DOTALL )
    if(match1):
        headnotes = match1.group(1).strip()
    else:
        headnotes = match2.group(1).strip()

    headnote = re.sub(r"\n", " ", headnotes)
    headnote = re.sub(r"\"", " ", headnote)
    headnote=replace_abbreviations(headnote, abbreviations_list)


    # EXTRACT MAIN JUDGEMENT
    judgments_pattern = r'(JUR[I|l|i]SD[I|l|i]CT[I|l|i]ON)\s?\.?\:?(.+):?\.?\:?\s?(.+)'
    judgments_pattern1 = r'Jurisdiction\s?\.?\:?(.+):?\.?\:?\s?(.+)'
    judgments_pattern3 =  r'jurisdiction\s?\.?\:?(.+):?\.?\:?\s?(.+)'
    judgments_pattern2 = r'APPEAL(.+):'
    judgments_match = re.search(judgments_pattern, judgement, re.MULTILINE | re.DOTALL )
    judgments_match2 = re.search(judgments_pattern2, judgement, re.MULTILINE | re.DOTALL)
    judgments_match1 = re.search(judgments_pattern1, judgement, re.MULTILINE | re.DOTALL)
    judgments_match3 = re.search(judgments_pattern3, judgement, re.MULTILINE | re.DOTALL)
    if judgments_match:
        judgments = judgments_match.group(2).strip()
    elif judgments_match2:
        judgments = judgments_match2.group(1).strip()
    elif judgments_match1:
        judgments = judgments_match1.group(1).strip()
    elif judgments_match3:
        judgments = judgments_match3.group(1).strip()
    judgments = re.sub(r"\"", " ", judgments)
    judgments = re.sub(r"\n", " ", judgments)
    judgments = replace_abbreviations(judgments, abbreviations_list)


    # EXTRACT CITATIONS
    citation_pattern = r"\[(.*?)\(\d+\s+\w+\s+\d+\)"
    citation_match = re.search(citation_pattern, title)
    cita = citation_match.group(1)
    cita = "[" + cita
    citations = cita.split("; ")


    # EXTRACT PLAINTIFF AND DEFENDANT
    plain_def = re.search(r'(.+?) (V\.|v\.) (.+)', title)
    if plain_def:
        plaintiff = plain_def.group(1)
        defendant = plain_def.group(3)

        # Remove "& ors" or "& anr" from plaintiff or defendant if present
        plaintiff = re.sub(r'\s+(& ors|& anr)\b', '', plaintiff, flags=re.IGNORECASE)
        defendant = re.sub(r'\s+(& ors|& anr)\b', '', defendant, flags=re.IGNORECASE)
        defendants_match = re.search(r'(.+?) \[', defendant)
        defendant = defendants_match.group(1)

    # EXTRACT MAIN JUDGE
    judgename=""
    match = re.search(r'\n(.+?)\n', judgement)  #SECOND LINE
    if match:
        extracted_text = match.group(1)
        cleaned_text = re.sub(r'\d{2}/\d{2}/\d{4}\n?\s\n?','', extracted_text) #REMOVE DATE, IF IT HAS
        match_text2= re.search(r', (.+?)\,', cleaned_text) # EXTRACT JUDGENAME BETWEEN FIRST ABD SECOND COMMA
        if(match_text2):
            judgename=match_text2.group(1)
        elif(re.search(r'\d{2}/\d{2}/\d{4}\s?', cleaned_text) or cleaned_text=="ACT:"):
            match3 = re.search(r'WAS DELIVERED BY\,?\:?\s(.+),?\s?C?\.?J\.\-?',judgments.upper())
            judgename=match3.group(1).upper()
            dash_pattern = re.search("\-",judgename)
            if(dash_pattern):
                name = judgename.split(", J.-")
                judgename=name[0]
        else:
            judgename=convert_name_format(cleaned_text)

    judgename = remove_extraspace_and_title_from_name(judgename)
    if(len(judgename.split(" ")) >= 5):
        pattern1 = r"RANGNATH MISRA"
        pattern2 = r"KULDIP SINGH"
        matches1 = re.findall(pattern1, judgename)
        matches2 = re.findall(pattern2, judgename)
        if (matches1):
            judgename = matches1[0]
        if matches2:
            judgename = matches2[0]


    sentences = post_process_of_sentences(sent_tokenize(headnote))

    sentence_judge = post_process_of_sentences(sent_tokenize(judgments))

    judgement_data = {
        'title': title,
        'date_of_judgement' : date,
        'plaintiff': plaintiff,
        'defendant': defendant,
        'act': act,
        'judge': judgename,
        'citations': citations,
        "headnote_sent": sentences,
        "headnote_refined":refined_text(sentences),
        "judgement_sent": sentence_judge,
        "judgement_refined" : refined_text(sentence_judge)
    }
    return judgement_data, len(sentences), len(sentence_judge)

def refined_text(sentences):
    cleaned_sentences = [remove_unwanted_words(sentence) for sentence in sentences]
    cleared_sentences = post_process_of_sentences(cleaned_sentences)
    new_headnotes =[]
    for each in cleared_sentences:
        words = word_tokenize(each)
        words = combine_percentages(words)
        words = remove_punctuations_stopwords(words)
        words = lemmatization(words)
        words = remove_multiple_punctuations(words)
        new_headnotes.append(" ".join(words))
    return new_headnotes