
# bot.py
import os
import discord
from dotenv import load_dotenv
import tweepy
import komedi
import random

load_dotenv('token.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')

client = discord.Client()
random.seed()

# INITIALIZATION CONFIRMATION ########################################################################

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# TWITTER FUCKERY # don't ask how this works, i have no idea #########################################
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
new_tweets = tweepy.Cursor(api.user_timeline, screen_name="bbbquotes1", tweet_mode='extended').items(200) #make sure the argument of items() is >= the number of tweets that exist on @bbbquotes1
list = []
for tweet in new_tweets:
    text = tweet._json["full_text"]

    refined_tweet = {'text' : text,
                    'favorite_count' : tweet.favorite_count,
                    'retweet_count' : tweet.retweet_count,
                    'created_at' : tweet.created_at}
    
    list.append(refined_tweet)                                  

# Actual stuff ########################################################################################

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
#####################

# Fun stuff

#####################



    if message.content == '~quote':
        rng = random.randrange(0,len(list))
        response = list[rng]['text']
        await message.channel.send(response)

    elif message.content.find('LMAO')>=0:
        numKomedi = message.content.count('O')
        response = numKomedi*'KOMEDI '
        await message.channel.send(response)
       
    elif message.content[0:5] == '~r6op':
        I=1
        if message.content[-1].isnumeric() == True:
            if int(message.content[-1]) < 1 or int(message.content[-1]) > 5:
                await message.channel.send('Must be 0 < n <= 5')
            I = int(message.content[-1])
 
        random.shuffle(komedi.attackerList)
        random.shuffle(komedi.defenderList)

        response=''
        for item in komedi.atkAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=komedi.attackerList[i]+' '
                await message.channel.send(response)
                break
            
        for item in komedi.defAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=komedi.defenderList[i]+' '
                if response.find('~~Clash~~') >= 0:
                    response+=komedi.defenderList[-1]+' '
                await message.channel.send(response)
                break

    elif message.content == '~conspiracy':
        #not actually sure if this will work, but it shouldn't be hard to find a replacement
        #just random a number and use that as the var
        #might need to move the conspiracies list back to this file
        random.shuffle(komedi.organizations)
        random.shuffle(komedi.firstNames)
        random.shuffle(komedi.lastNames)
        random.shuffle(komedi.existingPeople)  
        random.shuffle(komedi.countries)
        random.shuffle(komedi.places)
        random.shuffle(komedi.religions)
        random.shuffle(komedi.events)
        random.shuffle(komedi.actions)

        random.shuffle(komedi.conspiracies)
        
        komedi.conspiracies[0].capitalize()
        await message.channel.send(komedi.conspiracies[0])
        



    ### clean this shit up with functions or something


#####################

# Game Stuff

#####################

    elif message.content[0:9] == '~osrswiki':

        await message.channel.send('https:// ill finish this later lol') ### do this 
    

    elif message.content[0:8] == '~rs3wiki':

        await message.channel.send('https:// ill finish this later lol') ### do this 
    


#####################

# Game Summons

#####################

    elif message.content == '~siege':
        await message.channel.send('Do not attempt to board the helicopter. إنشالله الله أكبر أستغفرلله. أنت قرد غبي وستأكل حذائي. @Rainbow 6: Siege') #figure out how to tag people lmfao
                                        

#####################

# Help

#####################

    elif message.content == '~help':
        await message.channel.send('fuck you (for now) ill fill this in later lol')


#######################################################################################################

client.run(DISCORD_TOKEN)