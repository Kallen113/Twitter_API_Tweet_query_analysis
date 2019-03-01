"""specifies what enables the app to login with twitter"""
import constants
import oauth2
import urllib.parse as urlparse
import json

"""Specify the needed API keys to identify the app
:"""
#I.e., create a consumer class, which uses the CONSUMER_KEY and CONSUMER_secret to uniquely identify the app
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

"""Enable the app to make API requests to Twitter"""
client = oauth2.Client(consumer)

#have client variable do request to Twitter API:
#use the REQUEST_TOKEN_URL as the first argument:

#The 2nd argument is 'POST': i.e.. the app will extract/analyze a Twitter post
# use the client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

"""implement for loop to print an error message if a user request via the app fails
or another error occurs while trying to use the app:
"""
if response.status != 200:
    print("An error occurred with getting the request token from Twitter.")

#dGet th request token for parsing the query to return string
#use .decode('utf-8') so the data for making requests will be converted to strings, instead of bytes
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

"""Tell the user to go to the Twitter site in order for user to authorize the app,
and provide us with the PIN code"""

print("Go to the following site in your web browser:")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL,
                                 request_token['oauth_token']))

#after prompting the user to go the specific URL, the program will prompt the user to copy the PIN
# and then, ask the user to ask what the PIN is
oauth_verifier = input("What is the PIN?")

#create a token object that contains the request token and verifier
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
#set the token as the oauth verifier
token.set_verifier(oauth_verifier)

#create a client with the consumer (i.e., our app) and the newly verified token
#use client to get the access token
client = oauth2.Client(consumer, token)

#Ask Twitter to get an access token, having clready verified the request token
response, content =  client.request(constants.ACCESS_TOKEN_URL, 'POST')

access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)



#Create an authorized_token object and use it to perform Twitter API calls for the app user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
#whenever a request is sent to the Twitter API, the user will be  gained authorization to the app
authorized_client = oauth2.Client(consumer, authorized_token)

'''Having gained access to the Twitter API, 
let's start making requests/calls to the Twitter API:'''

#for starters, make request to Twitter to query on Tweets pertaining to images
#do a GET request for this query
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=economics', 'GET')

#warn the App user if an error occurs while making the Twiiter API request
if response.status!= 200:
    print("An errror occurred when searching for Tweets on the Twitter API")


#convert bytes to strings so the query output is a list of Tweets with string elements
#this will print out the content of the query output, parsing the JSON code to strings

tweets = json.loads(content.decode('utf-8'))

"""Iterate over each Tweet, and print only the text of each of them
:"""

for tweet in tweets['statuses']:
    #i.e.., iterate over each tweet stored in the tweets list
    print(tweet['text'])
    #print the text of the tweet
