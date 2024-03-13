from random import choice, randint

#       WE SHOULD CONNECT TO DATABASE AND HAVE ACCOUNTS TO STORE WORKOUTS ETC.

#   GETS USER RESPONSES AND CHECKS FOR COMMANDS THEN GIVES OUTPUTS
#   I THINK MOST OF OUR CODE WILL GO HERE

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '': 
        return 'Well you\'re awfully silent...'
    elif '!hello' in lowered:
        return 'Sup Tiny Bitch!'
    elif '!roll dice' in lowered:
        return f'You Rolled: {randint(1,6)}'
    elif '!flip coin' in lowered:
        if randint(0,100) <= 50: 
            return f'Heads!'
        else:
            return f'Tails!'