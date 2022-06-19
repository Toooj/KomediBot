
# bot.py
import os
import discord
from dotenv import load_dotenv
import tweepy
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
        atkAliases = ['att','atk','attack','attacker','a']
        defAliases = ['def','defender','defence','defense','d']

        attackerList = ['Sledge','Thatcher','Ash','Thermite','Twitch','Montagne','Glaz','Fuze','Blitz','IQ','Buck','Blackbeard','Capitao','Hibana','Jackal','Ying','Zofia','Dokkaebi','Lion','Finka','Maverick','Nomad','Gridlock','Nokk','Amaru','Kali','Iana','Ace','Zero','Flores','Osa','Sens']
        defenderList = ['Smoke','Mute','Castle','Pulse','Doc','Rook','Kapkan','Tachanka','Jager','Bandit','Frost','Valkyrie','Caveira','Echo','Mira','Lesion','Ela','Vigil','Maestro','Alibi','~~Clash~~','Kaid','Mozzie','Warden','Goyo','Wamai','Oryx','Melusi','Aruni','Thunderbird','Thorn','Azami']

        I=1
        if message.content[-1].isnumeric() == True:
            if int(message.content[-1]) < 1 or int(message.content[-1]) > 5:
                await message.channel.send('Must be 0 < n <= 5')
            I = int(message.content[-1])
 
        random.shuffle(attackerList)
        random.shuffle(defenderList)

        response=''
        for item in atkAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=attackerList[i]+' '
                await message.channel.send(response)
                break
            
        for item in defAliases:
            if message.content.find(item) >= 0:
                for i in range(I):
                    response+=defenderList[i]+' '
                if response.find('~~Clash~~') >= 0:
                    response+=defenderList[-1]+' '
                await message.channel.send(response)
                break

    elif message.content == '~conspiracy':
        organizations = ['Amazon','NASA','FedEx','Disney','Fox','Netflix','Google','Facebook','Snapchat','the Church',
                         'Government of North Korea','NATO','Ubisoft','the Illuminati','Antifa','QAnon']
        firstNames = ['Ryan','Gerald','Abhilash','Biswajit','Xaofan','Hideshi','Tom','Richard','Harry','Martin','Anton','Kirill',
                      'Phil','William','Alen','Max','Jeffery','Nigel','Mohammed','Magnus','Josiah','Ezekiel','Hannah','Hillary',
                      'Shaniqua','Jamal','Tyrone']
        lastNames = ['Biggums','Cox','Sharath','Shekelstein','Chang','Hussein','Imam','bin Laden','Nakamoto','Patel','Kumar',
                     'Singh','Karlson','Putin','Bezos','Bernstein','Epstein','Clinton','Jameson','Roberts','Hilberts']
        existingPeople = ['Jeff Bezos','Elon Musk','Barack Obama','Osama bin Laden','Hillary Clinton','George Soros','Walt Disney',
                          'Adolf Hitler','Anne Frank','Bill Gates','Hermes Trismegistus','Aristotle','Bill Clinton','Donald Trump',
                          'Mike Pence','Plato','Abraham Lincoln','Satan','Jesus','Aleister Crowley','Rabbi Menachem Mendel Schneerson']
        countries = ['India','USA','South Korea','Russia','Norway','Germany','UK','Ireland','Australia','Argentina','Brazil',
                     'Azerbaijan','Austria','Bahrain','Albania','Armenia']
        places = ['London','Vienna','Dhaka','Moscow','Yerevan','Tamil Nadu','the Moon','Mars']
        religions = ['Islam','Hinduism','Buddhism','Catholicism','Zoroastrianism','Satanism','Thelema','Judaism','Orthodox Christianity',
                     'Atheism',"Baha'i",'Confucianism','Druze','Jainism','Rastafarianism','Sikhism']
        events = ['the crucifixion of Jesus','9/11','Uvalde','WW2','The Holocaust']
        actions = ['False Flags','Child Sacrifice','Public Masturbation','Mass Rape','Genocide','Selective Breeding','Narco-Terrorism','Societal Degeneracy']

        random.shuffle(organizations)
        random.shuffle(firstNames)
        random.shuffle(lastNames)
        random.shuffle(existingPeople)  
        random.shuffle(countries)
        random.shuffle(places)
        random.shuffle(religions)
        random.shuffle(events)
        random.shuffle(actions)

        conspiracies = [events[0]+' was caused by '+existingPeople[0]+' after going back in time using the secret facility in '+countries[0]+', run by '+organizations[0], 
                       existingPeople[0]+' is dead... replaced by a robot from '+countries[0]+' named '+firstNames[0]+' '+lastNames[0],
                       existingPeople[0]+' burns effigy of '+existingPeople[1]+' for glory of '+religions[0]+' in '+countries[0],
                       religions[0]+' was actually founded in 1988 by '+firstNames[0]+' '+lastNames[0],
                       existingPeople[0]+' is secretly funding '+actions[0]+" to appease Moloch's High Priest, "+existingPeople[1],
                       existingPeople[0]+' is actively trying to cover up '+events[0]+' with disinformation via main stream media',
                       existingPeople[0]+' was actually born in 49AD, and has been repeatedly cloned by '+existingPeople[1]+', in '+places[0]+', to maintain the bloodline of Jesus Christ',
                       existingPeople[0]+' is actually dead',
                       existingPeople[0]+' is actually alive',
                       existingPeople[0]+' and '+existingPeople[1]+' are actually the same person'
                       ]

        random.shuffle(conspiracies)
        
        conspiracies[0].capitalize()
        await message.channel.send(conspiracies[0])
        



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