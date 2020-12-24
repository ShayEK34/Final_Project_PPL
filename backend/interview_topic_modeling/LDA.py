
class LDA():
    def clean(self, doc, stop, lemma, exclude):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized


    def process_data(self, interview_list):
        sentence_list = []
        for question_inter in interview_list:
            a = nltk.word_tokenize(question_inter)
            remove_token_list = ['.', '(', ')', ' )', ' (', '!', '+', '-', '?', ',', '1', '2', '3', '4', '5', '6', '7', '8',
                                 '9', '0']
            sentence = ''
            for token in a:
                if token not in remove_token_list:
                    sentence = sentence + ' ' + token
            sentence_list.append(sentence)
        df = pd.DataFrame(sentence_list, columns=['Interview Questions'])
        return df


    def dic_words_per_topic(self, topics):
        final_list = {}
        for elemnet in topics:
            topic_num = -1
            for value in elemnet:
                if type(value) == int:
                    topic_num = value
                else:
                    a = value.split()
                    tmp_list = []
                    for i in a:
                        if i == '+':
                            continue
                        else:
                            b = i.split('*')
                            word = b[1].replace('"', '')
                            tmp_list.append(word)
            final_list[topic_num] = tmp_list
        return final_list


    def get_topics_words(self, num_topic, num_words, data):
        question = data[['Interview Questions']]
        question = question.dropna()
        interview_list = question['Interview Questions'].tolist()

        stop = (stopwords.words('english'))
        stop.extend(
            ['it.', 'answers', 'questions', 'answer', 'question', 'it', 'asked', 'user.', 'question.', 'problem', 'time', 'would'])
        stop = set(stop)
        exclude = set(string.punctuation)
        lemma = WordNetLemmatizer()
        interview_list = self.process_data(interview_list)
        interview_list = interview_list['Interview Questions'].tolist()
        question_clean = [self.clean(ques, stop, lemma, exclude).split() for ques in interview_list]

        # Creating the term dictionary of our courpus, where every unique term is assigned an index.
        dictionary = corpora.Dictionary(question_clean)

        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        doc_term_matrix = [dictionary.doc2bow(ques) for ques in question_clean]

        # Creating the object for LDA model using gensim library
        Lda = gensim.models.ldamodel.LdaModel

        # Running and Trainign LDA model on the document term matrix.
        ldamodel = Lda(doc_term_matrix, num_topics=num_topic, id2word=dictionary, passes=50)
        topics = ldamodel.print_topics(num_topics=num_topic, num_words=num_words)
        topics_dictionary = self.dic_words_per_topic(topics)
        return topics_dictionary



    def get_words(self, comapny):
        if comapny=="google":
            return ['array','list','projects','sum','threads']
        elif comapny=="microsoft":
            return ['list','array','threads','sum','projects']
        else:
            return ['threads','list','projects','sum','java']





if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk.tokenize import TweetTokenizer
    import string
    import gensim
    from gensim import corpora

    # nltk.download()
    lda= LDA()
    path= r'backend/scrape_interviews/scraper_output/Google_softwareJobs_interviews.csv'
    interview_questions = pd.read_csv(path)
    dict_topic_words = lda.get_topics_words(1, 10, interview_questions)
    print(dict_topic_words)

