__author__ = 'fine'
#info:  This code takes two input files "tweet.txt" and "user.txt" and outputs the tweets made by each user and
#       the people they follow in alphabetical order.
#date:  2015/07/26
import os
import sys
import re
from collections import defaultdict
from collections import OrderedDict
import itertools
import operator
import traceback


#initialize maximum length of tweet:
Lmax = 140
#initialize an empty list for Users
Users = []
#read lines from input file "user.txt"
try:
    arg = os.getcwd() + '/user.txt'
    linesUser=open(arg,'r').readlines()
except IOError:
        print 'cannot open file', arg, '.  Make sure the filename is correct'



#split the read lines at comas and spaces and strip any white spaces

for line in linesUser:Users.append(re.split(',|' ' ',line.strip()))

#create an list of "noise" info in the resulting data
noise = ['follows','']
#remove noise from list of Users, create a set in order to remove duplicates, and recreate list
# (sorted alphabetically)  from that set.
Users = sorted(list(set([item for sublist in Users for item in sublist if item not in noise])))

#initiate the creation of dictionary "d0" that links each user to its followers:
userKey=[]
userVal=[]
d0 = defaultdict(list)
for line in linesUser:
    userKey.append(line.strip().split('follows')[0].strip())
    userVal.append(line.strip().split('follows')[1].strip())

#create a list linking each user to its followers:
data0= zip(userKey,userVal)
#start adding these keys and values to the user-follower dict (d0)
for user,val in data0:
    d0[user].append(val)

    val = val.split(', ')
    #if the user follows more than one person, these folks need to be split:
    if len(val)>1:
        k=[]
        for obj in val:
            k.append(obj.split(', '))
            newk= list(set(list(itertools.chain(*k))))
            d0.update({user:newk})
#add the user itself to its own list of followers:  i.e. user must follow himself, hence see tweets from himself
for u in Users:d0[u].append(u)
#order alphabetically:
d0=OrderedDict(sorted(d0.items(),key=lambda t:t[0]))
# user-follower dictionary (d0) is now done.
########################################################################################################################
#Proceed to create dictionary (d1) linking tweets to tweetees:
#initialize lists for Users and their tweets:
Tweets=[]
Tweeters=[]
#read info from the "tweet.txt" input file and append values to the Tweets and Tweeters lists:
linesTweets=open(os.getcwd()+'/tweet.txt').readlines()
for line in linesTweets:
    Tweeters.append(line.strip().split('>',1)[0])
    Tweets.append(line.strip().split('>',1)[1])

#link each Tweeter with its tweets:
data = zip(Tweeters,Tweets)
#create the dictionary
d1 = defaultdict(list)
for user,tweet in data:
    d1[user].append(tweet)
UserIndexes=[]
UserNames=[]

########################################################################################################################
#create a dictionary (d2) that shows the order in which tweets are made
for u in Users:
    indexes = [i for i,x in enumerate(Tweeters) if x == u]
    UserNames.append(u)
    UserIndexes.append(indexes)
list1 = zip(UserNames,UserIndexes)
list1.sort(key=operator.itemgetter(1))

d2=defaultdict(list)
for user,position in list1:d2[user].append(position)
########################################################################################################################
#Proceed to print output:
for u in Users:
    print u #print the name of each of the users
    #create two empty lists:
    J=[]
    L = []
    #for each of the people that the user "u" follows, create a list of the tweets they see (L)
    #as well as a list that shows the order in which these tweets were made (J)
    for obj in d0[u]:

        for l in d1[obj]:
            L.append(l)

        try:
            for jj in d2[obj][0]:J.append(jj)
        except IndexError:print 'Index out of range:  Check that followers are separated by coma and space'
        #link each tweet to its ordering position and sort it according to this position (i.e. 2 before 5 etc.)
        K = zip(L,J)
        K.sort(key=operator.itemgetter(1))
    #print out the tweets made by each of the users in the correct order:
    for i,j in K:
        # print "\t",'@',Tweeters[j],':',i[0:Lmax+1]
        print "\t@%s:%s" %(Tweeters[j],i[0:Lmax+1])
########################################################################################################################
#END OF CODE.
#Assumptions made in this code:
#1)A user may not be named "follows".  It may be named "Follows" (capital F).  Naming the user "follows" will result in
#the line being read incorrectly.
