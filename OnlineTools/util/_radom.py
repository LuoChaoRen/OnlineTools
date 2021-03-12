import random
def get_radom(stri,num):
    if len(stri)>num:
        return ''.join(random.sample(stri, num))
    else:
        return ''.join(str(random.choice(stri)) for _ in range(num))
