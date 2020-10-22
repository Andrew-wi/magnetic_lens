# ----------------------------------------------------------------------------
# Function Timing
# ----------------------------------------------------------------------------
from helpers import *
import timeit

# is_not_dead timer

is_not_dead_setup = '''
pos_test = [0.0023423094, 0.009834284823, 0.3289385938]
'''

is_not_dead_stmt = '''
def is_not_dead(pos):
    if ((pos[0] ** 2 + pos[1] ** 2) ** (1/2)) > 0.003:
        return False
    else:
        return True
'''

is_not_dead_time = timeit.timeit(setup=is_not_dead_setup,
                                 stmt=is_not_dead_stmt,
                                 number=1000000)

print('Execution time of is_not_dead: {} seconds'.format(is_not_dead_time))
