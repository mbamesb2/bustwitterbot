#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TEST VERSION


import tweepy, time, sys, urllib2, urllib, json, requests, datetime, pytz
 
CONSUMER_KEY = 'consumer key'
CONSUMER_SECRET = 'consumer secret'
ACCESS_KEY = 'access key'
ACCESS_SECRET = 'access secret'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
 
url = 'http://developer.trimet.org/ws/V1/arrivals?'
values = {
    'locIDs' : '718',
    'appID' : 'your developer id',
    'json' : 'true'
    
}

data = urllib.urlencode(values)
fullURL = url + data

tz= pytz.timezone('US/Pacific')

while True:
    response = urllib2.urlopen(fullURL)
    jsonResponse = json.loads(response.read())
    status_list = []
        
    #for i in jsonResponse["resultSet"]["arrival"]:
    #    print i["fullSign"]
    for i in range(0, 2):

        bus = jsonResponse["resultSet"]["arrival"][i]["fullSign"]
        bustime = jsonResponse["resultSet"]["arrival"][i]["estimated"]

        bustime = bustime[:-5]
        busDate = datetime.datetime.strptime(str(bustime), '%Y-%m-%dT%H:%M:%S.%f')
            
        exactTime = datetime.datetime.now(tz)
        exactTime = exactTime.replace(tzinfo=None)
        
           
        finalTime = ((busDate - exactTime).total_seconds())/60
        finalTime = str(finalTime).split('.', 1)
       
        busNumber = bus.split(" ", 1)
        print "The " + busNumber[0] + " bus is arriving in " + finalTime[0] + " minutes. "

        status_list.append("The " + busNumber[0] + " bus is arriving in " + finalTime[0] + " minutes. ")

        #api.update_status("The " + busNumber[0] + " bus is arriving in " + finalTime[0] + " minutes.")
    api.update_status(status_list[0] + status_list[1])
    time.sleep(2000)

if __name__=="__main__":
    tweetThis() 
