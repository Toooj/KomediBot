import datetime
from dateutil import tz

rolePT = 984741133403967518
roleET = 984741340174757908
roleUK = 984741431065329704
roleCET = 984741645218115584
roleEET = 984742011078860810
roleSAMT = 984742205916864523

def timezoneFinder(authorRoleIDs):
    if rolePT in authorRoleIDs:
        return rolePT
    elif roleET in authorRoleIDs:
        return roleET
    elif roleUK in authorRoleIDs:
        return roleUK
    elif roleCET in authorRoleIDs:
        return roleCET
    elif roleEET in authorRoleIDs:
        return roleEET
    elif roleSAMT in authorRoleIDs:
        return roleSAMT

PT = tz.gettz('America/Los_Angeles')
ET = tz.gettz('America/New_York')
UK = tz.gettz('Europe/London')
CET = tz.gettz('Europe/Amsterdam')
EET = tz.gettz('Europe/Kiev')
SAMT = tz.gettz('Europe/Samara')

timezonesDict = {
    rolePT : PT,
    roleET : ET,
    roleUK : UK,
    roleCET : CET,
    roleEET : EET,
    roleSAMT : SAMT,
    }

dayDict = {
    'Sunday' : 0,
    'Monday' : 1,
    'Tuesday' : 2,
    'Wednesday' : 3,
    'Thursday' : 4,
    'Friday' : 5,
    'Saturday' : 6
    }

def TimeFormatter(time):

    if ' ' in time:
        time = time.replace(' ','') #remove space if there is one
    if ':' not in time:
        time = time[0:-2] + ':00' + time[-2:] #standardize format
    if len(time) == 6:
        time = '0'+time #standardize length

    if 'pm' in time and time[0:2] != '12':
        hh = int(time[0:2])
        hh = hh+12
        if hh == 24:
            hh = '00' #failsafe for 12pm but i dont think this needs to be here
        time = str(hh) + time[2:]
    elif 'am' in time and time[0:2] == '12':
        time = '00' + time[2:]
    time = time[:-2] #remove am/pm

    return time

def TimeConverter(timeToConvert,authorTimezone):

    convertedTimes=[]
    dateModifiers=[]

    fromZone = timezonesDict[authorTimezone]

    for toZone in [*timezonesDict.values()]:
        
        time = timeToConvert
        time = TimeFormatter(time)

        timeNowObject = datetime.datetime.now() # for up to date timezone conventions (daylight, timezone boundaries, etc)
        timeNowString = timeNowObject.strftime('%H:%M %d %B %Y')
        time = time+timeNowString[5:] #replace the actual current time with the time to be converted

        timeObject = datetime.datetime.strptime(time, '%H:%M %d %B %Y')
        timeObject = timeObject.replace(tzinfo=fromZone)
        timeObject = timeObject.astimezone(toZone) #convert time

        timeString = timeObject.strftime('%H:%M')

        day = dayDict[timeNowObject.strftime('%A')]
        convertedDay = dayDict[timeObject.strftime('%A')] #for if the day changes upon conversion

        dayChange = convertedDay - day
        
        if dayChange > 1:
            dayChange -= 7
        elif dayChange < -1:
            dayChange += 7

        convertedTimes.append(timeString)
        dateModifiers.append(f'{dayChange:+}')

    return convertedTimes,dateModifiers
