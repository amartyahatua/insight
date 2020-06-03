import tweepy
import json
CONSUMER_KEY = 'fgF5FcWZ1R84ToNw8oQcySMLH'
CONSUMER_SECRET = 'DBs7EWyhUVw96eCI7wVzLVNi49K2ONPoT2fPDQ2dY1dI0ilDB5'
ACCESS_KEY = '813832637383053318-azj59CPBrpkdkj2f7mo0H2CVvPvoVXo'
ACCESS_SECRET = 'U6LvaiNoaShfrX7EcU5hZcS1fcSdhofESFz1KEhfNONoF'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

import csv


########################################################################################################
########## I/P : The input file contains list of HashTags in hashtags_part2.csv. We want to downloaded##
#################    tweets of that particular HashTag  ################################################
############ O/P : .json file corresponds to each HashTag containing the tweets ########################
########################################################################################################




with open('C:\\Users\\Dime\\Desktop\\Insight project\\insight\\data\\data.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #nTweet = 0
    #flag = 1
    for row in spamreader:
        print(row[0])
        nTweet = 0
        #flag = 1
        with open('C:\\Users\\Dime\\Desktop\\Insight project\\insight\\download\\'+row[0]+'.json', 'w') as outfile:
            outfile.write('[')
            for page in tweepy.Cursor(api.search, q='#'+row[0], count=1000).pages():
                #print(page)
                #ids.extend(page)
                for tweet in page:
                    nTweet = nTweet + 1
                    if(nTweet > 1):
                        outfile.write(',')
                    outfile.write(json.dumps(tweet._json))
                    #print(count)
                if(nTweet >= 100000):   #### 100000 is the maximum tweets can be downloaded using this code. To change the limit change the number
                    #print(nTweet)
                    #flag = -1
                    break
                #if (flag == -1):
                #    #ids.clear
                #    break
            print(row[0], ' => ', nTweet, ' tweets downloaded')
            outfile.write(']')