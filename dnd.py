import random


def rollCommand(dice):
    if '.' in dice:
        return ('Gimme integers you monster')
    else:
        dice = dice.split('d')
        response = ''
        diceroll=[]

        for i in range(int(dice[0])):
            diceroll.append(random.randrange(1,int(dice[1])+1))
            if int(dice[0]) != 1:
                response += '`' + str(diceroll[i]) + '` '
                if i in range(int(dice[0])-1):
                    response += '+ '
                else:
                    response += '= '
        response += '`'+str(sum(diceroll))+'`'
        return response
