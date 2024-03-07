from itertools import chain, combinations

# gets the elements of maximum length of a list
# this is twice as faster as two list comprehensions
def max_len_elems(list):
    max_len_elems = []
    n = 0
    for x in list:
        m = len(x)
        if m>n:
            n = m
            max_len_elems = [x]
        else:
            max_len_elems.append(x)
    return max_len_elems

def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s))))