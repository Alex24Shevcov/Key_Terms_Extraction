# Write your code here
import string
from lxml import etree
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer



class KeyTerms:
    def head_and_text_1_2(self, xml_file: str) -> dict:
        root = etree.parse(xml_file).getroot()[0]
        dictionary = dict()
        for i in range(len(root)):
            news = root[i]
            tmp_key = ""
            for new in news:
                if new.get("name") == "head":
                    tmp_key = new.text
                    dictionary[new.text] = ""
                elif new.get("name") == "text":
                    dictionary[tmp_key] = new.text
        return dictionary

    def tokenize_dict_3_4_5(self, dictionari: dict) -> dict:

        lemmatizer = WordNetLemmatizer()
        stopword_arr = stopwords.words('english')
        tmp_dict = dict()
        for head, text in dictionari.items():
            tmp_arr_words = word_tokenize(text.lower())
            tmp_arr_words = [lemmatizer.lemmatize(word) for word in tmp_arr_words]
            tmp_arr_words = [word for word in tmp_arr_words if word not in list(string.punctuation) and word not in stopword_arr]
            tmp_arr_nouns_words = [word for word in tmp_arr_words if pos_tag([word])[0][1] == "NN"]
            tmp_dict[head] = tmp_arr_nouns_words
        return tmp_dict

    def max_identical_words(self, dictionari: dict) -> dict:
        vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1, 1), stop_words=['ha', 'wa', 'u', 'a'])
        final_dict = dict()
        list_of_stings = [" ".join(arr) for arr in list(dictionari.values())]

        tfidf_matrix = vectorizer.fit_transform(list_of_stings)
        terms = vectorizer.get_feature_names_out()

        i = 0
        for head in dictionari.keys():
            tmp_arr_of_dicts_terms_and_metrics = []
            tmp_arr_of_dicts_terms_and_metrics.append(dict())

            for term, metr in zip(terms, tfidf_matrix.toarray()[i]):
                if metr != 0.0:
                    tmp_arr_of_dicts_terms_and_metrics[0][term] = metr

            arr_sorted_tuples = sorted(tmp_arr_of_dicts_terms_and_metrics[0].items(), key=lambda item: item[0],
                                       reverse=True)
            arr_sorted_tuples = sorted(arr_sorted_tuples, key=lambda item: item[1], reverse=True)
            tmp_arr_of_dicts_terms_and_metrics[0] = arr_sorted_tuples

            final_dict[head] = [tupl[0] for tupl in tmp_arr_of_dicts_terms_and_metrics[0][:5]]

            i += 1
        return final_dict



if __name__ == '__main__':
    key_term = KeyTerms()
    head_and_text_dict = key_term.head_and_text_1_2("news.xml")
    tokenize_dict = key_term.tokenize_dict_3_4_5(head_and_text_dict)
    max_identical_words_dict = key_term.max_identical_words(tokenize_dict)
    for head, arr_words in max_identical_words_dict.items():
        print(f"{head}:")
        print(*arr_words)


