import csv
import collections
import re

tweet = open("all_tweets.txt", "rU")

tweetcontent = open("all_tweet_content.csv", "w")

# convert all tweets into a csv file, in order to further read tweets in dictionary
tweetcontent_Writable = csv.writer(tweetcontent)
try:
    tweetcontent_Writable.writerow(["Location", "Date", "Content"])
    for line in tweet:
        s = line.split()
        location = ["".join(s[:2])]
        Date = [" ".join(s[3:5])]
        content = [" ".join(s[5:])]
        list = []
        list += location + Date + content

        tweetcontent_Writable.writerow(list)
finally:
    tweet.close()

tweet.close()


source = open("all_tweet_content.csv", "rU")
# DictReader is built-in function of csv package
sourceFile = csv.DictReader(source) # a single tweet in sourceFile is a dictionary

sentiment = open("sentiments.csv", "rU")
sentimentFile = csv.DictReader(sentiment)

def makedictionaries(sentimentFile):
    dict = collections.OrderedDict()# define an ordered dictionary
    for item in sentimentFile:
        dict[item['key']] = item[' value']
    return dict

def add_sentiment(dict_sentiment, dict_a_tweet):
    # remove common punctuations
    content_split = re.split('[;_,|/()#!?.@"$\s]\s*',dict_a_tweet["Content"].lower())
    count = 0
    # count the number of sentiment words in a tweet
    score = 0
    # in order to record sentiment score
    for item in content_split:
        # check sentiment words
        if item in dict_sentiment.keys():
            count += 1
            score += float(dict_sentiment[item])
    if count != 0.0:
        # caculate average score
        sentimentscore = score / count
    else:
        sentimentscore = 0
    return sentimentscore

#convert sentiment file into dictionary
sentimentDictionary = makedictionaries(sentimentFile)

# add a column to store scores and make a new csv file
score_output = open("all_score_output.csv", "w")
score_File = csv.writer(score_output)

# in order to check their average sentiment in following steps
Alreadywithheader = False
for each_tweet in sourceFile:
    if Alreadywithheader == False: # add column name
        score_File.writerow([item for item in each_tweet] + ["Sentiment Score"])
        Alreadywithheader = True
    else:
        l = [each_tweet[item] for item in each_tweet]
        score_File.writerow(l + [add_sentiment(sentimentDictionary, each_tweet)])

source.close()
sentiment.close()
score_output.close()


tweet_with_score = open("all_score_output.csv", "rU")
tweet_with_score_file = csv.DictReader(tweet_with_score)

tweet_filtered_out = open("all_filtered_out_tweets.csv", "w")
tweet_filtered_out_file = csv.writer(tweet_filtered_out)

# creat filter
def tweet_filter(tweet_with_score_file, word_list):
    for tweet in tweet_with_score_file:
        add = True
        for word in word_list:
            lower_word = word.lower()
            if lower_word not in re.split('[;_,|/()#!?.@"$\s]\s*',tweet["Content"].lower()):
                add = False
                break
        if add == True:
            tweet_filtered_out_file.writerow(tweet.values())

tweet_filter(tweet_with_score_file, ["a", "is","i"])
tweet_with_score.close()
tweet_filtered_out.close()
