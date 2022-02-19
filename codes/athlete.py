import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class athlete:
    def __init__(self,athlete_args) -> None:
        self.E_remain,self.recover_index, = athlete_args

    def P_out(self,h,curv):
        return 1