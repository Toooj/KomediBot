
# bot.py
import os
from dotenv import load_dotenv
import importlib
import random
import tweepy
import discord
from discord.ext import commands

import roles
import komedi

load_dotenv('token.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
SERVER_ID = os.getenv('SERVER_ID')

random.seed()

LIST_OF_COMMANDS = ['quote','r6op','conspiracy','osrswiki','osrsge','rs3wiki','learn','help']

# TWITTER FUCKERY # don't ask how this works, i have no idea ##########################################
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
new_tweets = tweepy.Cursor(api.user_timeline, screen_name="bbbquotes1", tweet_mode='extended').items(200) #make sure the argument of items() is >= the number of tweets that exist on @bbbquotes1
quoteList = []
for tweet in new_tweets:
    text = tweet._json["full_text"]

    refined_tweet = {'text' : text,
                    'favorite_count' : tweet.favorite_count,
                    'retweet_count' : tweet.retweet_count,
                    'created_at' : tweet.created_at}
    
    quoteList.append(refined_tweet)    

# INITIALIZATION ######################################################################################

KomediBot = commands.Bot(command_prefix = '~', help_command=None)

@KomediBot.event
async def on_ready():
    print(f'KomediBot has connected to Discord!')

# Actual stuff ########################################################################################

@KomediBot.listen()
async def on_message(message):

    if message.author.id == KomediBot.user.id:         #no mirrors allowed
       return

    

#####################

# Game Summons

#####################

    elif message.content[0] == '~':
        for alias in roles.gameSummonAliases:
            if alias == message.content[1:len(alias)+1]:

                gameSummonData = roles.gameSummonDict[alias]
                flavortext = gameSummonData[1]
                roleID = gameSummonData[0]

                response = flavortext + '\n' + roleID
                await message.channel.send(response)

    LMAOList = ['LMAO','LMFAO','LFMAO','KOMEDI']       #KOMEDI response
    for LMAO in LMAOList:
        if LMAO in message.content:
            numKomedi = message.content.count('O')
            response = numKomedi*'KOMEDI '
            await message.channel.send(response)
            break


@KomediBot.command()
async def quote(ctx):

    random.shuffle(quoteList)
    await ctx.send(quoteList[0]['text'])

@KomediBot.command()
async def r6op(ctx, team, number=1):
    
    response = '~r6op syntax is: `~r6op <team> <number>`\n'
    if int(number) not in range(1,6):
        response+= '<number> must be between 1 and 5 (inclusive)'
        await ctx.send(response)
    elif team not in (komedi.atkAliases+komedi.defAliases):
        response+= '<team> must be attack or defence (or variants of those words)'
        await ctx.send(response)
    else:
        attackerList = komedi.attackerList
        defenderList = komedi.defenderList
        random.shuffle(attackerList)
        random.shuffle(defenderList)

        response=''

        if team in komedi.atkAliases:
            for i in range(number):
                response+=attackerList[i]+' '
            await ctx.send(response)
            
        if team in komedi.defAliases:
            for i in range(number):
                response+=defenderList[i]+' '
            if response.find('~~Clash~~') >= 0:
                response+=defenderList[-1]+' '
            await ctx.send(response)

@KomediBot.command()
async def conspiracy(ctx):
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

    await ctx.send(conspiracies[0])

#####################

# RuneScape Stuff

#####################

@KomediBot.command()
async def osrswiki(ctx):

    await ctx.send('osrs wiki page for item in ~osrswiki <item>')

@KomediBot.command()
async def osrsge(ctx):

    await ctx.send('osrs ge price/data for item in ~osrswiki <item>')

@KomediBot.command()
async def rs3wiki(ctx):

    await ctx.send('rs3 wiki page for item in ~rs3wiki <item>')
    
#####################

# Misc

#####################

@KomediBot.command()
async def learn(ctx, command, role, flavortext):

    
    

    if command in (LIST_OF_COMMANDS + roles.gameSummonAliases):
        await ctx.send('That command already exists')

    elif role in roles.roleIDs:
        await ctx.send('A command for this role already exists')

    else:

        await ctx.send("I'm a stupid robot who can't figure out how long the flavortext is if you don't put it in quotations")
        
        gameSummonAliases = roles.gameSummonAliases
        roleIDs = roles.roleIDs
        existingflavortext = roles.flavortext

    
        os.rename('roles.py','roles_ifthisexistssomethingwentwrong.py')

        #await ctx.send(role)

        gameSummonAliases.append(str(command))
        roleIDs.append(str(role))
        existingflavortext.append(str(flavortext))

        f = open('roles.py','x')
        f.write('gameSummonAliases = ["' + '", "'.join([str(item) for item in gameSummonAliases]) + '"]')
        f.write('\n\n')
        f.write('roleIDs = ["' + '", "'.join([str(item) for item in roleIDs]) + '"]')
        f.write('\n')
        f.write('flavortext = ["' + '", "'.join([str(item) for item in existingflavortext]) + '"]')
        f.write('\n\n')
        f.write('gameSummonData = list(zip(roleIDs,flavortext))')
        f.write('\n\n')
        f.write('gameSummonDict = dict(zip(gameSummonAliases,gameSummonData))')
        f.close()

        importlib.reload(roles)

        os.remove('roles_old.py')
        os.rename('roles_ifthisexistssomethingwentwrong.py','roles_old.py')

        await ctx.send('Me smart now, me know now what ~'+str(roles.gameSummonAliases[-1]) +' means')

@KomediBot.command()
async def help(ctx,full='0'):

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

    if full.lower() == 'full' or full == '1':
        full = 1

    if full==1:

        response+= '\n\n**PASSIVE FUNCTIONS:**\n\n'
        response+= '- Responds to LMAO variants with "KOMEDI" as many times as there are Os.\n'
        response+= '- Automatically converts and messages timezone based on timezone role of sender. NOT IMPLEMENTED\n'

    await ctx.send('Check your DMs <:fuckboi:988374504168390717>') #fuckboi emoji
    await ctx.author.send(response)

#######################################################################################################

KomediBot.run(DISCORD_TOKEN)

