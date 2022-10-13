import random
import string


def id_generator(prefix='', len_id=6, suffix='', chars=string.ascii_lowercase):
    return prefix + ''.join(random.choice(chars) for _ in range(len_id)) + suffix
