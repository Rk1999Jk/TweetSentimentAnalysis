from tkinter import *
import sys,tweepy,csv,re
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from textblob import TextBlob




def main_screen():
    global screen
    screen = Tk();
    screen.geometry("250x200")
    screen.title("Sentiment Analysis")

    global NoOf
    global search
    NoOf = IntVar()
    search=StringVar()

    Label().pack()
    Label(text="Enter Keyword/Tag to search about",font=("Times New Roman",13)).pack()
    Entry(textvariable=search).pack()
    Label(text="Enter how many tweets to search",font=("Times New Roman",13)).pack()
    Entry(textvariable=NoOf).pack()
    Label().pack()
    Button(text="OK",bg="grey",width=50, height=3, command=analysis_screen).pack()

    screen.mainloop()


def analysis_screen():
    screen1 = Toplevel(screen)
    screen1.geometry("500x520")
    NoOfTerms = NoOf.get()
    searchTerm = search.get()
    tweets = []
    tweetText = []
    now = datetime.now()

    Label(screen1,text="").pack()
    Label(screen1,text="How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.",font=("Times New Roman",13)).pack()

    consumerKey = 'vDcmvsXjrQRGOJJhOrJgbzv4C'
    consumerSecret = '8L9V3Rj4px6WSoBCFhuCz0EZMQAZ7AmmgxCs6uTzbSTS8hmwLU'
    accessToken = '1199276490593992704-0QB456dIAVcoIH0zzrUw9kIJmuefNP'
    accessTokenSecret = 'Mtl85cC3D8WM1xE87n4ro47WxDW9xwY9u5ShhlQ8Adkbz'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)

    # Open/create a file to append data to
    csvFile = open('result.csv', 'a')

    # Use csv writer
    csvWriter = csv.writer(csvFile)

    # creating some variables to store info
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    for tweet in tweets:
        # Append to temp so that we can store in csv later. I use encode UTF-8
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        # print(analysis.sentiment)  # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1

            # Write to csv and close csv file
    csvWriter.writerow(tweetText)
    csvFile.close()

    positive = percentage(positive, NoOfTerms)
    wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

         #finding average reaction
    polarity = polarity / NoOfTerms
    Label(screen1, text="").pack()
    Label(screen1, text="General Report :", font=("Times New Roman", 13)).pack()

    if (polarity == 0):
         Label(screen1, text="Neutral", font=("Times New Roman", 13)).pack()
    elif (polarity > 0 and polarity <= 0.3):
         Label(screen1, text="Weakly Positive", font=("Times New Roman", 13)).pack()
    elif (polarity > 0.3 and polarity <= 0.6):
         Label(screen1, text="Positive", font=("Times New Roman", 13)).pack()
    elif (polarity > 0.6 and polarity <= 1):
         Label(screen1, text="Strongly Positive", font=("Times New Roman", 13)).pack()
    elif (polarity > -0.3 and polarity <= 0):
         Label(screen1, text="Weakly Negative", font=("Times New Roman", 13)).pack()
    elif (polarity > -0.6 and polarity <= -0.3):
         Label(screen1, text="Negative", font=("Times New Roman", 13)).pack()
    elif (polarity > -1 and polarity <= -0.6):
         Label(screen1, text="Strongly Negative", font=("Times New Roman", 13)).pack()

    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text="Detailed Report", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=positive+" people thought it was positive", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=wpositive + " people thought it was weakly positive", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=spositive + " people thought it was strongly positive", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=negative + " people thought it was negative", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=wnegative + " people thought it was weakly negative", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=snegative + " people thought it was strongly negative", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()
    Label(screen1, text=neutral + " people thought it was neutral", font=("Times New Roman", 13)).pack()
    Label(screen1, text="", font=("Times New Roman", 13)).pack()

    plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)

    conn=sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS analysis(
                    searchTerm text ,
                    NoOfTerms integer ,
                    DateTime text ,
                    positive real ,
                    wpositive real ,
                    spositive real ,
                    negative real ,
                    wnegative real ,
                    snegative real ,
                    neutral real
    )""")
    cur.execute('''INSERT INTO analysis(searchTerm,NoOfTerms,DateTime,positive,wpositive,spositive,negative,wnegative,snegative,neutral)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',(searchTerm,NoOfTerms,now,positive,wpositive,spositive,negative,wnegative,snegative,neutral))

    conn.commit()
    conn.close()





def cleanTweet(tweet):
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')


def plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


main_screen()