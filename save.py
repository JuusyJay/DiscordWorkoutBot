def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    # IF COMMAND: RETURN OUTPUT
    if lowered == '': 
        return 'Well you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Sup Tiny Bitch!'
    elif 'rd' or 'roll' or 'roll dice' in lowered:
        return f'You Rolled: {randint(1,6)}'
    elif 'fc' or 'flip' or 'flip coin' in lowered:
        flip = {randint(1,2)}
        if flip == 1: 
            return 'Heads!'
        else:
            return 'Tails!'