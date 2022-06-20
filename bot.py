
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

# Fun Stuff

#####################

    if message.content == '~quote':
        rng = random.randrange(0,len(list))
        response = list[rng]['text']
        await message.channel.send(response)

    elif message.content.find('LMAO')>=0 or message.content.find('LMFAO')>=0 or message.content.find('LFMAO')>=0:
        numKomedi = message.content.count('O')
        response = numKomedi*'KOMEDI '
        await message.channel.send(response)
       
    elif message.content[0:5] == '~r6op':
        
        attackerList = komedi.attackerList
        defenderList = komedi.defenderList
        random.shuffle(attackerList)
        random.shuffle(defenderList)

        I=1
        if message.content[-1].isnumeric() == True:
            if int(message.content[-1]) < 1 or int(message.content[-1]) > 5:
                await message.channel.send('Must be 0 < n <= 5')
            I = int(message.content[-1])
 
        response=''
        for item in komedi.atkAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=attackerList[i]+' '
                await message.channel.send(response)
                break
            
        for item in komedi.defAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=defenderList[i]+' '
                if response.find('~~Clash~~') >= 0:
                    response+=defenderList[-1]+' '
                await message.channel.send(response)
                break

    elif message.content == '~conspiracy':
        
        organizations = komedi.organizations
        firstNames = komedi.firstNames
        lastNames = komedi.lastNames
        existingPeopleAlive = komedi.existingPeopleAlive
        existingPeopleDead = komedi.existingPeopleDead
        existingPeopleFictional = komedi.existingPeopleFictional
        existingPeopleALL = komedi.existingPeopleALL
        countries = komedi.countries
        places = komedi.places
        religions = komedi.religions
        events = komedi.events
        actions = komedi.actions
        
        random.shuffle(organizations)
        random.shuffle(firstNames)
        random.shuffle(lastNames)
        random.shuffle(existingPeopleAlive)
        random.shuffle(existingPeopleDead)
        random.shuffle(existingPeopleFictional)
        random.shuffle(existingPeopleALL)
        random.shuffle(countries)
        random.shuffle(places)
        random.shuffle(religions)
        random.shuffle(events)
        random.shuffle(actions)
        
        ### these things need to be randomized every time ~conspiracy is said

        conspiracyInputs=[organizations,firstNames,lastNames,existingPeopleAlive,existingPeopleDead,existingPeopleFictional,existingPeopleALL,countries,places,religions,events,actions]
        conspiracies=komedi.Conspiracy(*conspiracyInputs)
        random.shuffle(conspiracies)

        conspiracies[0].capitalize()
        await message.channel.send(conspiracies[0])
        

    ### clean this shit up with functions or something?


#####################

# RuneScape Stuff

#####################

    elif message.content[0:9] == '~osrswiki':

        await message.channel.send('https:// ill finish this later lol') ### do this 

    elif message.content[0:7] == '~osrsge':

        await message.channel.send('https://') ### do this
    

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

    elif message.content[0:5]=='~help':

        response = '**AVAILABLE COMMANDS:**\n\n'
        response+= '\n**Fun Stuff:**\n\n'
        response+= '**~quote** : Generates a random quote from the BBB Twitter @BBBQuotes1.\n'
        response+= '**~conspiracy** : Generates random conspiracy theory.\n'
        response+= '**~r6op <team> <number>** : Generates <number> operators from <team> (i.e. attack/defence).\n'
        response+= '**~roll <numdice><typedice>** : NOT IMPLEMENTED\n' ### maybe in the future might be worth making a dedicated DnD set of commands?
        response+= '\n**RuneScape Things:**\n\n'
        response+= '**~osrswiki <item>** : NOT IMPLEMENTED\n'
        response+= '**~osrsge <item>** : NOT IMPLEMENTED\n'
        response+= '**~rs3wiki <item>** : NOT IMPLEMENTED\n'
        response+= '\n**Game Summons:**\n\n'
        response+= '**~siege** : Tags the Rainbow 6: Siege role.\n'

        if message.content.find('FULL')>=0:

            response+= '\n\n**PASSIVE FUNCTIONS:**\n\n'
            response+= '- Responds to LMAO variants with "KOMEDI" as many times as there are Os.\n'
            response+= '- Automatically converts and messages timezone based on timezone role of sender. NOT IMPLEMENTED\n'

        await message.channel.send('Check your DMs <:fuckboi:988374504168390717>') #fuckboi emoji
        await message.author.send(response)


#######################################################################################################

client.run(DISCORD_TOKEN)