import re
import nltk
# nltk.download('punkt')
from nltk.corpus import wordnet
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# List to store the file contents
file_contents = []

# List of abbreviations
abbreviations_list = {
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "Ms.": "Miss",
    "adv.":"Advocate",
    "Adv.": "Advocate",
    "sub.":"sub",
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
    "se.":"Section",
    "viz.":	"videlicet",
    "ltd.":	"limited",
    "Ltd.": "Limited",
    "co.": "Company",
    "a.i.r." : "All India Reporter",
    "f.i.r." :	"First Information Report",
    "i.p.c." :	"Indian Penal Code",
    "p.w.":	"Procecuted Witness",
    "cl.":	"Clauses",
    "cls.":	"Clauses",
    "ex.":	"exhibit",
    "Ex.": "Exhibit",
    "schs.": "schedules",
    "P. W.":"Prosecution Witness",
    "P.W.": "Prosecution Witness",
    "No." : "number",
    "no." : "number",
    "Nos.":"numbers",
    "Petns.":"Petitions",
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
    "Proviso.": "provided that",
    "qtls.": "quintals",
    "Ms. Number":"Manuscript Number",
    "Ms. number": "Manuscript Number",
    "S.C.C.":"Supreme Court Cases",
    "J.T.": "Judgement Today",
    "a." : "article",
    "as.": "assize",
    "v.": "verses",
    "C.P.C.":"Code of Civil Procedure",
    "C. P. C.":"Code of Civil Procedure",
    "Ch.": "Chapter",
    "Asstt.": "Assistant",
    "C.A.": "Civil Appeal",
    "s.l.p.": "special leave petitions",
    "w.e.f.": "with effect from",
    "slp": "special leave petitions",
    "nos.": "numbers",
    "fir": "first information report ",
    "ngt": "National Green Tribunal",
    "s. c. r.":	"Supreme Court Reporter",
    "anr.":	"Another",
    "Ors.":	"Others",
    "cr. p. c.":	"Criminal Procedure Code",
    "smt.":	"Shrimati",
    "p.": "Page number if followed by number",
    "pwd.": "Public Works Department",
    "ss.": "Sub Section",
    "crm.": "client relationship management",
    "…………..........................j.": "judge name",
    "………….........................j.": "judge name",
    "lrs.": "legal representatives",
    "ors.": 'others',
    "aor.": 'advocate on record',
    "crm-m": 'criminal main',
    "cr.": "civil revision",
    "rsa.": "regular second appeal",
    "crr.": "criminal revision",
    "o&m.": "operation and maintenance",
    "o&m": "operation and maintenance",
    "dlf": "Delhi Land & Finance",
    "vs.": "verses",
    "para.":"paragraph",
    "w.a.": "writ appeal",
    "a.s." : "FIRST APPEAL",
    "s.a.": "SECOND APPEAL",
    "o.s.a.": "ORIGINAL SIDE APPEAL" ,
    "s.t.a.": "SPECIAL TRIBUNAL APPEAL" ,
    "c.m.a.": "CIVIL MISCELLANEOUS APPEAL",
    "c.m.s.a": "CIVIL MIS.SECOND APPEAL" ,
    "l.p.a.": "LETTERS PATENT APPEAL" ,
    "s.t.p.": "SPECIAL TRIBUNAL PETITION",
    "S. R. O.": "STATUTORY RULES AND ORDERS",
    "cont. a.": "CONTEMPT APPEAL",
    "cross. obj.": "CROSS OBJECTION" ,
    "t.m.a.": "TRADE MARKS APPEAL",
    "t.m.s.a.": "TRADE MARKS SECOND APPEAL" ,
    "Rs.": "Rupees",
    "t.c.": "TAX CASES" ,
    "t.c.a.": "TAX CASE APPEAL"  ,
    "t.c.r.": "TAX CASE REVISION",
    "r.c.p.": "REFERRED CASE PETITION" ,
    "c.r.p.": "CIVIL REVISION PETITION",
    "c.r.p. (pd)": "CIVIL REVISION PETITION (PD)",
    "mc": "MATRIMONIAL CAUSES" ,
    "rev. appl.": "REVIEW APPLICATION",
    "m.p.": "MISCELLANEOUS PETITION" ,
    "caveat" : "CAVEAT",
    "h.c.p.": "HABEAS CORPUS PETITION",
    "crl. r.c.": "CRL. REVISION CASE",
    "crl. a.": "CRIMINAL APPEAL",
    "r.t.":  "REFERRED TRIAL",
    "crl. o.p.": "CRIMINAL ORIGINAL PETITION",
    "r.c.": "REFERENCE CASE",
    "C. A.":"CIVIL APPEAL",
    "atty": "Attorney",
    "BFP":"Bona fide purchaser",
    "DOA": "Court of Appeals",
    "EE":  "Employee",
    "ain't": "am / are not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "i.e.":"that is",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / would",
    "he'd've": "he would have",
    "he'll": "he shall / will",
    "he'll've": "he shall / will have",
    "he's": "he has / is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / is",
    "i'd": "I had / would",
    "i'd've": "I would have",
    "i'll": "I shall / will",
    "i'll've": "I shall / will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had / would",
    "it'd've": "it would have",
    "it'll": "it shall / will",
    "it'll've": "it shall / will have",
    "it's": "it has / is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / would",
    "she'd've": "she would have",
    "she'll": "she shall / will",
    "she'll've": "she shall / will have",
    "she's": "she has / is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / is",
    "that'd": "that would / had",
    "that'd've": "that would have",
    "that's": "that has / is",
    "there'd": "there had / would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / would",
    "they'd've": "they would have",
    "they'll": "they shall / will",
    "they'll've": "they shall / will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / will",
    "what'll've": "what shall / will have",
    "what're": "what are",
    "what's": "what has / is",
    "what've": "what have",
    "when's": "when has / is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / is",
    "where've": "where have",
    "who'll": "who shall / will",
    "who'll've": "who shall / will have",
    "who's": "who has / is",
    "who've": "who have",
    "why's": "why has / is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / would",
    "you'd've": "you would have",
    "you'll": "you shall / will",
    "you'll've": "you shall / will have",
    "you're": "you are",
    "you've": "you have"
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
            combined_tokens.append(current_token + ' percent')
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

        elif is_valid_acronym(current_sentence.split()[-1]) and is_valid_acronym(next_sentence.split()[0] )and not dictionary.check(next_sentence.split()[0]):
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


    #EXTRACT CASEID
    case_id=""
    id_pattern = r"\[(\d{4})\] INSC (\d+)"
    matched = re.search(id_pattern, title)
    if matched:
        year, case_number = matched.groups()
        case_id = f"{year}_{case_number}"


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
    act = re.sub(r"\s+", " ", act)


    # EXTRACT HEADNOTES
    match1 = re.search(r'HEADNOTE:(.*?)(APPEAL|APPELLATE|OR[I|l]G[I|l]NAL|APPELLANT|CRIMINAL|CIVIL|REVIEW|Civil\sAppella|Criminal\sAppella|Original\sJurisdiction|EXTRA\sORDINARY)', judgement, re.DOTALL )
    match2 = re.search(r'HEADNOTE:(.*?)(Civil\sAppeal\sNo\.)', judgement, re.DOTALL )
    if(match1):
        headnotes = match1.group(1).strip()
    else:
        headnotes = match2.group(1).strip()

    headnote = re.sub(r"\n", " ", headnotes)
    headnote = re.sub(r"\"", " ", headnote)
    headnote = re.sub(r"\s+", " ", headnote)
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
    judgments = re.sub(r"\s+", " ", judgments)
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

            match4 = re.search(r'^(.*?J\.)', judgename)
            if match4:
                judgename= match4.group(1).strip()

            # dash_pattern = re.search("\-",judgename)
            # if(dash_pattern):
            #     name1 = judgename.split(", J.-")
            #     judgename=name1[0]
        else:
            judgename=convert_name_format(cleaned_text)

    judgename = remove_extraspace_and_title_from_name(judgename)
    if(len(judgename.split(" ")) >= 5):
        pattern1 = r"RANGNATH MISRA"
        pattern2 = r"KULDIP SINGH"
        pattern3 = r"K.J. YOGESHWAR DAYAL"
        matches1 = re.findall(pattern1, judgename)
        matches2 = re.findall(pattern2, judgename)
        matches3 = re.findall(pattern3, judgename)
        if (matches1):
            judgename = matches1[0]
        if matches2:
            judgename = matches2[0]
        if matches3:
            judgename = matches3[0]


    sentences = post_process_of_sentences(sent_tokenize(headnote))

    sentence_judge = post_process_of_sentences(sent_tokenize(judgments))

    judgement_data = {
        'title': title,
        "case_id":case_id,
        'date_of_judgement' : date,
        'plaintiff': plaintiff,
        'defendant': defendant,
        'act': act,
        'judge': judgename,
        'citations': citations,
        "headnote_sent": sentences,
        # "headnote_refined":refined_text(sentences),
        "judgement_sent": sentence_judge,
        # "judgement_refined" : refined_text(sentence_judge)
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