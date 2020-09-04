from local_search import LS
from copy import deepcopy

class ILS:

    def ils(self, s0, PBL, ILS, iter_max):
        ls = LS()
        s = ls.local_search(s0, 30, iter_max)
        iter = 0
        while iter < iter_max:
            iter = + 1