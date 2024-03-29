
# bot.py
import os
from dotenv import load_dotenv
import importlib
import random
import re
import tweepy
import discord
from discord.ext import commands,tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import roles
import conspiracy as con
import siege
import birthdays
import dnd
import timezones
import urllib
import asyncio
from datetime import date

load_dotenv('token.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
SERVER_ID = os.getenv('SERVER_ID')

random.seed()

LIST_OF_MUSIC_COMMANDS = ['p','s','dc','play','skip','showq','addq','clrq','clearq','disconnect']
LIST_OF_SIEGE_COMMANDS = ['r6op']
LIST_OF_DND_COMMANDS = ['r','roll']
LIST_OF_RUNESCAPE_COMMANDS = ['osrswiki','osrsge','rs3wiki']
LIST_OF_MISC_COMMANDS = ['quote','learn','conspiracy','help']
LIST_OF_ALL_COMMANDS = [*LIST_OF_MUSIC_COMMANDS,*LIST_OF_SIEGE_COMMANDS,*LIST_OF_DND_COMMANDS,*LIST_OF_RUNESCAPE_COMMANDS,*LIST_OF_MISC_COMMANDS]


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search' : 'ytsearch'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} #idk what these are

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
    tyjbnhop = KomediBot.get_channel(400109334182494210)       
    birthday.start()
    #await tyjbnhop.send('I AM AWAKE NOW. LET THE KOMEDI ENSUE.')                                                                              ########### COMMENT THIS SHIT OUT WHEN TESTING #######################


# BIRTHDAY STUFF ########################################################################################

@tasks.loop(hours=24)
async def birthday():
    #print('called')
    today = str(date.today())
    response=''
    for key in birthdays.birthdayDict.keys():
        if today[5:] in key:
            response = '**HAPPY BIRTHDAY**!!! ~~I remembered because I am a robot and now everyone else can use me to pretend they knew it was your birthday!~~\n'
            response+= '<@'+str(birthdays.birthdayDict[key])+'>'
            tyjbnhop = KomediBot.get_channel(400109334182494210)  
            await tyjbnhop.send(response)
    if response == '':
        print('not a bday today')


# CHAT RESPONSE ########################################################################################

ampm = re.compile('[0-9]?[0-9]:?[0-9]?[0-9]?[\s]?[ap][m]')

@KomediBot.listen()
async def on_message(message):
    if message.author.id == KomediBot.user.id:         #no mirrors allowed
       return

    elif message.content[0] == '~':                     #Game Summons & other custom commands
        for alias in roles.gameSummonAliases:
            if alias == message.content[1:len(alias)+1]:

                gameSummonData = roles.gameSummonDict[alias]
                flavortext = gameSummonData[1] #is this a bug? [0]?
                roleID = gameSummonData[0]

                response = flavortext + '\n' + roleID
                await message.channel.send(response)
                
    elif ampm.search(message.content.lower()) != None: # Timezone converter
        
        authorRoleIDs = [role.id for role in message.author.roles]
        authorTimezone = timezones.timezoneFinder(authorRoleIDs)

        if ampm.search(message.content.lower()) != None:
            allTimesToConvert = re.findall(ampm, message.content.lower())
                
        timeToConvert = allTimesToConvert[0]                            ######## TODO: make it convert all the times --- is this worth the effort? lol
        convertedTimes,dateModifiers = timezones.TimeConverter(timeToConvert,authorTimezone)

        serverTimezones = ['PT','ET','UK','CET','EET','SAMT']
        response = timezones.TimeFormatter(timeToConvert) + ' for ' + message.author.display_name + ' is:\n\n'
        for i in range(len(serverTimezones)):
            response+= '**'+serverTimezones[i]+'** : '+convertedTimes[i]+' ('+str(dateModifiers[i])+') | '
        response = response[:-3]
        response+= "\n\nDon't trust me around daylight savings switch dates"

        await message.channel.send(response)

    LMAOList = ['LMAO','LMFAO','LFMAO','KOMEDI','LOL']       #KOMEDI response
    for LMAO in LMAOList:
        if LMAO in message.content:
            numKomedi = message.content.count('O')
            response = numKomedi*'KOMEDI '
            await message.channel.send(response)
            break

# COMMANDS #############################################################################################

# Music #

musicQueue = []
urlQueue = []

async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(KomediBot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


def yt(search):
    query_string = urllib.parse.urlencode({
        "search_query": search
    })
    html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    return "http://www.youtube.com/watch?v=" + search_results[0]


@KomediBot.command()
async def p(ctx,*,url):
    
    await join(ctx)
    voice = get(KomediBot.voice_clients, guild=ctx.guild)
    #print(url)

    if not ctx.message.author.voice:
        await ctx.send('You are not in a voice channel')
    elif 'http' not in url:    
        query = url
        #print(yt(query))
        await p(ctx,url=yt(query))
    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            title=info.get('title')
            URL = info['url']
            await addq(ctx,url=url)

        if not voice.is_playing():
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: asyncio.run_coroutine_threadsafe(nextCoro(ctx), KomediBot.loop))
async def p_no_addq(ctx,url):
    
    await join(ctx)
    voice = get(KomediBot.voice_clients, guild=ctx.guild)

    if not ctx.message.author.voice:
        await ctx.send('You are not in a voice channel')
    elif 'http' not in url:
        await ctx.send('Need a URL (for now)')
    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            title=info.get('title')
            URL = info['url']

        if not voice.is_playing():
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: asyncio.run_coroutine_threadsafe(nextCoro(ctx), KomediBot.loop))
async def nextCoro(ctx):
    urlQueue.pop(0)
    musicQueue.pop(0)
    if len(urlQueue) > 0:
        url = urlQueue[0]
        print(urlQueue)
        await p_no_addq(ctx,url)
    else:
        await showq(ctx)
        

@KomediBot.command()
async def s(ctx):
    voice = get(KomediBot.voice_clients, guild=ctx.guild)
    voice.pause()
    await nextCoro(ctx)

async def stop(ctx):
    voice = get(KomediBot.voice_clients, guild=ctx.guild)
    voice.stop()

@KomediBot.command()
async def dc(ctx):
    await ctx.guild.voice_client.disconnect() 

@KomediBot.command()
async def showq(ctx):
    if len(musicQueue)==0:
        await ctx.send('Queue is empty!')
    response = 'Now playing: '+str(musicQueue[0])
    numLines=0
    for i in range(len(musicQueue)-1):
        numLines+=1
        if numLines < 3:
            response+= '\n'+str(i+1)+'. '+str(musicQueue[i+1])
        
    if numLines-2 > 0:
        response+='\nAnd '+str(numLines-2)+' more'
    await ctx.send(response)

@KomediBot.command()
async def addq(ctx,*,url):
    if 'http' not in url:    
        query = url
        url=yt(query)
    
    urlQueue.append(url)
    
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        title=info.get('title')

    musicQueue.append(title)
    await ctx.send('Added "'+title+'" to queue')

@KomediBot.command()
async def clrq(ctx):
    musicQueue.clear()
    urlQueue.clear()
    await stop(ctx)
    await ctx.send('Queue cleared')
    

@KomediBot.command()
async def play(ctx,url): ## same as p
    await p(ctx,url)

@KomediBot.command()
async def clearq(ctx): ## same as clrq
    await clrq(ctx)
    
@KomediBot.command()
async def skip(ctx): ## same as s
    await s(ctx)

@KomediBot.command()
async def disconnect(ctx): ## same as dc
    await dc(ctx)

# Siege #

@KomediBot.command()
async def r6op(ctx, team, number=1):
    response = '~r6op syntax is: `~r6op <team> <number>`\n'
    if int(number) not in range(1,6):
        response+= '<number> must be between 1 and 5 (inclusive)'
        await ctx.send(response)
    elif team not in (siege.atkAliases+siege.defAliases):
        response+= '<team> must be attack or defence (or variants of those words)'
        await ctx.send(response)
    else:
        attackerList = siege.attackerList
        defenderList = siege.defenderList
        random.shuffle(attackerList)
        random.shuffle(defenderList)

        response=''

        if team in siege.atkAliases:
            for i in range(number):
                response+=attackerList[i]+' '
            await ctx.send(response)
            
        if team in siege.defAliases:
            for i in range(number):
                response+=defenderList[i]+' '
            if response.find('~~Clash~~') >= 0:
                response+=defenderList[-1]+' '
            await ctx.send(response)

# DND #

@KomediBot.command()
async def r(ctx, dice):
    await ctx.send(dnd.rollCommand(dice))
    
@KomediBot.command()
async def roll(ctx, dice):
    await ctx.send(dnd.rollCommand(dice))

# RuneScape #

@KomediBot.command()
async def osrswiki(ctx):
    await ctx.send('osrs wiki page for item in ~osrswiki <item>') ## TODO

@KomediBot.command()
async def osrsge(ctx):
    await ctx.send('osrs ge price/data for item in ~osrswiki <item>') ## TODO

@KomediBot.command()
async def rs3wiki(ctx):
    await ctx.send('rs3 wiki page for item in ~rs3wiki <item>') ## TODO
    
# Misc #

@KomediBot.command()
async def quote(ctx):
    random.shuffle(quoteList)
    await ctx.send(quoteList[0]['text'])


@KomediBot.command()
async def learn(ctx, command, role, flavortext):
    if command in (LIST_OF_ALL_COMMANDS + roles.gameSummonAliases):
        await ctx.send('That command already exists')

    elif role in roles.roleIDs:
        await ctx.send('A command for this role already exists')

    else:
        await ctx.send("I'm a stupid robot who can't figure out how long the flavortext is if you don't put it in quotations")
        
        gameSummonAliases = roles.gameSummonAliases
        roleIDs = roles.roleIDs
        existingflavortext = roles.flavortext

        os.rename('roles.py','roles_ifthisexistssomethingwentwrong.py')

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
async def conspiracy(ctx):
    organizations = con.organizations
    firstNames = con.firstNames
    lastNames = con.lastNames
    existingPeopleAlive = con.existingPeopleAlive
    existingPeopleDead = con.existingPeopleDead
    existingPeopleFictional = con.existingPeopleFictional
    existingPeopleALL = con.existingPeopleALL
    countries = con.countries
    places = con.places
    religions = con.religions
    events = con.events
    actions = con.actions
        
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
    conspiracies=con.Conspiracy(*conspiracyInputs)
    random.shuffle(conspiracies)

    conspiracies[0].capitalize()

    await ctx.send(conspiracies[0])

@KomediBot.command()
async def help(ctx,*,kw=''):

    response = '**AVAILABLE COMMANDS:**\n\n'
    response+= '\n**Music:**\n\n'
    response+= '**~p <link/search item>** : Plays the audio from <link>, or the audio of the first search result for <search item>. Can also use ~play.\n'
    response+= '**~s** : Skips the current item in the queue. Can also use ~skip.\n'
    response+= '**~dc** : Disconnects KomediBot from the voice channel.\n'
    response+= '**~addq <link/search item>** : Adds the audio from <link/search item> to the queue.\n'
    response+= '**~showq** : Shows the current queue.\n'
    response+= '**~clrq** : Clears the current queue except for ongoing audio. Can also use ~clearq.\n'
    if 'games' in kw:
        response+= '\n**Game Specific:**\n\n'
        response+= '**~r6op <team> <number>** : Generates <number> operators from <team> (i.e. attack/defence).\n'
        response+= '**~r <numdice>d<typedice>** : Rolls <numdice>d<typedice> and displays the result (and individual rolls). Can also use ~roll.\n'
        response+= '**~osrswiki <item>** : Returns OSRS wiki page for <item>. NOT IMPLEMENTED\n'
        response+= '**~osrsge <item>** : Returns OSRS GE information from wiki for <item>. NOT IMPLEMENTED\n'
        response+= '**~rs3wiki <item>** : Returns RS3 wiki page for <item>. NOT IMPLEMENTED\n'
    response+= '\n**Misc:**\n\n'
    response+= '**~quote** : Generates a random quote from the BBB Twitter @BBBQuotes1.\n'
    response+= '**~conspiracy** : Generates random conspiracy theory.\n'
    response+= '**~help** : I think you know what it does... <:fuckboi:988374504168390717>'

    if 'passives' in kw:

        response+= '\n\n**PASSIVE FUNCTIONS:**\n\n'
        response+= '- Responds to LMAO variants with "KOMEDI" as many times as there are Os.\n'
        response+= '- Automatically converts and messages timezone based on timezone role of sender.\n'
        
    response+= '\n**Use the keywords "games" and/or "passives" to see more commands**'
    response+= '\n**For example, try replying with "~help games"**'
    await ctx.send('Check your DMs <:fuckboi:988374504168390717>') #fuckboi emoji
    await ctx.author.send(response)

#######################################################################################################

KomediBot.run(DISCORD_TOKEN)