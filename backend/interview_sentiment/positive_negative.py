
import nltk
import pandas as pd
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.corpus import sentiwordnet as swn

# nltk.download('sentiwordnet')


# class positive_negative():
#     def __init__(self):
#         self.output

class Sentiment():
    def get_output(self,company):
        if company=="google":
            return "../backend/interview_sentiment/resurces/pos_neg_google.JPG"
        elif company=="apple":
            return "../backend/interview_sentiment/resurces/pos_neg_apple.JPG"
        elif company == "microsoft":
            return "../backend/interview_sentiment/resurces/pos_neg_microsoft.JPG"



    def pre_processing(self,df):
        # tokenize
        data = []
        for row in df.values:
            tokenize_text = nltk.word_tokenize(row[0])
            data.append(tokenize_text)

        # convert to lower case
        data_after_lower = []
        for content in data:
            lower_content = list(map(lambda word: word.lower(), content))
            data_after_lower.append(lower_content)

        # stopwords removel
        data_without_stop_words = []
        stop_words = set(stopwords.words('english'))
        for word in [".", ",", "(", ")", "<", ">", "br", "!", "/", "--", "n't", "'s", "''", "?", "...", "``", ":", "-", "'",
                     "would", ";", "*"]:
            stop_words.add(word)
        for content in data_after_lower:
            filtered_content = [w for w in content if not w in stop_words]
            data_without_stop_words.append(filtered_content)

        # lemmatization
        wnl = nltk.WordNetLemmatizer()
        clean_data = []
        for content in data_without_stop_words:
            lemmatize_content = [wnl.lemmatize(w) for w in content]
            clean_data.append(lemmatize_content)

        return clean_data


    def classify_data(self,clean_data):
        tagged_list = []
        final_docs_score = []
        score_list = []

        # Create POS tagging for each token in each doc
        tagged_list = []
        for content in clean_data:
            tagged_list.append(nltk.pos_tag(content))

        for idx, doc in enumerate(tagged_list):
            score_list.append([])
            for idx2, t in enumerate(doc):  # t[0] word, t[1] pos tag
                newtag = ''
                if t[1].startswith('NN'):
                    newtag = 'n'
                elif t[1].startswith('JJ'):
                    newtag = 'a'
                elif t[1].startswith('V'):
                    newtag = 'v'
                elif t[1].startswith('R'):
                    newtag = 'r'
                else:
                    newtag = ''
                if (newtag != ''):
                    synsets = list(swn.senti_synsets(t[0], newtag))
                    score = 0
                    if (len(synsets) > 0):
                        for syn in synsets:
                            score += syn.pos_score() - syn.neg_score()
                        score_list[idx].append(score / len(synsets))  # add score of each term in doc

        # Create final score to each doc(positive or negative)
        for score_sent in score_list:
            final_docs_score.append(sum([word_score for word_score in score_sent]) / len(score_sent))
        return final_docs_score


    # call functions
    def plot_pie_chart(self,num_positive, num_negative):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Positive reviews', 'Negative reviews'
        sizes = [num_positive, num_negative]
        explode = (0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()


    def percentage(self,part, whole):
        return 100 * float(part) / float(whole)


    def summarize_reviews(self,reviews_score):
        positive = 0
        negative = 0
        for score in reviews_score:
            if score > 0:
                positive += 1
            else:
                negative += 1
        print("The number of positive reviews is: " + str(positive) + "/" + str(len(reviews_score)))
        print("The number of negative reviews is: " + str(negative) + "/" + str(len(reviews_score)))

        print('\n')

        print(("The positive percentage number is: " + str(round(self.percentage(positive, len(reviews_score)), 2)) + '%'))
        print(("The negative percentage number is: " + str(round(self.percentage(negative, len(reviews_score)), 2)) + '%'))

        self.plot_pie_chart(positive, negative)

if __name__ == '__main__':
    path=r'../scrape_interviews/scraper_output/Google_softwareJobs_interviews.csv'

    interview_questions = pd.read_csv(path)
    reviews = interview_questions[['Interview']]
    reviews = reviews.dropna()
    sentiment = Sentiment()
    clean_data = sentiment.pre_processing(reviews)
    docs_score = sentiment.classify_data(clean_data)
    print(docs_score)
    sentiment.summarize_reviews(docs_score)

