atkAliases = ['att','atk','attack','attacker','a']
defAliases = ['def','defender','defence','defense','d']

attackerList = ['Sledge','Thatcher', 'Ash','Thermite','Twitch',
                'Montagne', 'Glaz', 'Fuze', 'Blitz', 'IQ', 
                'Buck', 'Blackbeard', 'Capitao', 'Hibana','Jackal',
                'Ying','Zofia','Dokkaebi','Lion','Finka',
                'Maverick','Nomad','Gridlock','Nokk','Amaru',
                'Kali','Iana','Ace','Zero','Flores',
                'Osa','Sens']

defenderList = ['Smoke','Mute','Castle','Pulse','Doc',
                'Rook','Kapkan','Tachanka','Jager','Bandit',
                'Frost','Valkyrie','Caveira','Echo', 'Mira',
                'Lesion','Ela','Vigil','Maestro','Alibi',
                '~~Clash~~','Kaid','Mozzie','Warden','Goyo',
                'Wamai','Oryx','Melusi','Aruni','Thunderbird',
                'Thorn','Azami']

organizations = ['Amazon','NASA','FedEx','Disney','Fox','Netflix',
                'Google','Facebook','Snapchat','the Church', 
                'Government of North Korea','NATO','Ubisoft',
                'the Illuminati','Antifa','QAnon','the Ku Klux Klan', 'Grubhub',
                'Doordash','Instacart','TSA','NSA','US Supreme Court']

firstNames = ['Ryan','Gerald','Abhilash','Biswajit','Xaofan',
              'Hideshi','Tom','Richard','Harry','Martin','Anton','Kirill',
              'Phil','William','Alen','Max','Jeffery','Stanislav','Vladimir',
              'Nigel','Mohammed','Magnus','Josiah','Ezekiel','Elena','Kyle',
              'Hannah','Hillary','Cooper','Jesse','Tejas','Andrew','Lewis',
              'Shaniqua','Jamal','Tyrone','Wei-Yu','Hitori','Johnathan']

lastNames = ['Biggums','Cox','Sharath','Shekelstein','Chang','Hussein',
            'Imam','bin Laden','Nakamoto','Patel','Kumar','Woods','Shah',
             'Singh','Karlson','Putin','Bezos','Bernstein','Goldstein',
             'Epstein','Clinton','Jameson','Roberts','Hilberts','Einstein',
             'Zhang','Crews','Timonin','Trump','Clinton','Obama']

existingPeopleAlive = ['Jeff Bezos','Elon Musk','Barack Obama','Hillary Clinton',
                  'George Soros','Bill Gates','Mike Pence','Bill Clinton','Donald Trump',
                  'Jair Bolsonaro','Eminem','Boris Johnson','Queen Elizabeth II']

existingPeopleDead = ['Osama bin Laden','Isaac Newton','Tupac','Walt Disney','Adolf Hitler','Anne Frank','Aristotle',
                      'Plato','Abraham Lincoln','Aleister Crowley','Rabbi Menachem Mendel Schneerson','Biggie', 'Julius Caesar',
                      'Emperor Nero']

existingPeopleFictional = ['Jesus Christ','Satan','God','Prophet Mohammed','Moses','Gautama Buddha','Shrek',
                           'King Roald','Abraham','Gilgamesh','Allah']

existingPeopleALL = existingPeopleAlive + existingPeopleDead + existingPeopleFictional

countries = ['India','USA','South Korea','Russia','Norway','Germany','UK',
             'Ireland','Australia','Argentina','Brazil','the Netherlands',
             'Azerbaijan','Austria','Bahrain','Albania','Armenia','Sweden',
             'Thailand','Vietnam','New Zealand','Somalia','Ecuador','Peru',
             'Finland','China','Mongolia','Italy','Chad','Niger','Nigeria',
             'South Africa','Belgium','France','Spain','Uzbekistan','Turkey',
             'Kazakhstan','Turkmenistan','Pakistan','Nepal','Sri Lanka']

places = ['London','Vienna','Dhaka','Moscow','Yerevan','Tamil Nadu','the Moon','Mars',
          'Bangalore','San Francisco','Los Angeles','Glendale','Denver','New York','Antwerp',
          'Amsterdam','Paris','Berlin','Kiev','San Diego','Vancouver','Montreal']

religions = ['Islam','Hinduism','Buddhism','Catholicism','Zoroastrianism','Satanism','Thelema',
             'Judaism','Orthodox Christianity',
             'Atheism',"Baha'i",'Confucianism','Druze','Jainism','Rastafarianism','Sikhism']

events = ['the crucifixion of Jesus Christ','9/11','Uvalde','WW2','the Holocaust','the Trump Presidency']

actions = ['false flags','child sacrifice','public masturbation','mass rape','genocide',
           'selective breeding','Narco-Terrorism','societal degeneracy','Pride Month','circumcision',
           'abortion','racism']

def Conspiracy(organizations,firstNames,lastNames,existingPeopleAlive,existingPeopleDead,existingPeopleFictional,existingPeopleALL,countries,places,religions,events,actions):

    conspiracies = [events[0]+' was caused by '+existingPeopleAlive[0]+' after going back in time using the secret facility in '+countries[0]+', run by '+organizations[0], 
                            existingPeopleAlive[0]+' is dead... replaced by a robot from '+countries[0]+' named '+firstNames[0]+' '+lastNames[0],
                            existingPeopleALL[0]+' burns effigy of '+existingPeopleALL[1]+' for the glory of '+religions[0]+' in '+countries[0],
                            religions[0]+' was actually founded in 1988 by a person named '+firstNames[0]+' '+lastNames[0],
                            existingPeopleAlive[0]+' is secretly funding '+actions[0]+" to appease Moloch's High Priest, "+existingPeopleAlive[1],
                            existingPeopleAlive[0]+' is actively trying to cover up '+events[0]+' with disinformation via main stream media',
                            existingPeopleALL[0]+' was actually born in 49AD, and has been repeatedly cloned by '+existingPeopleALL[1]+', in '+places[0]+', to maintain the bloodline of '+existingPeopleFictional[0],
                            existingPeopleAlive[0]+' is actually dead',
                            existingPeopleDead[0]+' is actually alive',
                            existingPeopleALL[0]+' is actually gay',
                            existingPeopleALL[0]+' and '+existingPeopleALL[1]+' are actually the same person',
                            existingPeopleAlive[0]+' actually won the 2020 election',
                            'Mass surveillance via 5G is being rolled out in '+countries[0]+' at the behest of '+existingPeopleAlive[0]+' because of the events of '+events[0],
                            'In order to counter the spread of '+religions[0]+', '+religions[1]+' has contracted the services of '+organizations[0]+'.',
                            religions[0]+' secretly reveres '+actions[0],
                            'The second coming of '+existingPeopleFictional[0]+' will come when people start to believe in the (clearly falsified) events of '+events[0],
                            organizations[0]+' and '+organizations[1]+' are working closely to disprove the existence of '+existingPeopleFictional[0],
                            countries[0]+' does not actually exist. Come on, do you know anyone from '+countries[1]+'?'
                            ]

    return conspiracies