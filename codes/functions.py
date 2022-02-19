import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def power_dissipation(velocity,athlete_inf,track_inf,wind_inf): # 功耗函数
    weight, drag_coefficient,_,_ = athlete_inf
    slope, curvatue, road_direction = track_inf
    speed, wind_direction = wind_inf

    # 在此得出能量消耗
    power_comsumpthon = 0

    return power_comsumpthon

def power_strategy(velocity,athlete_inf,track_inf,wind_inf):
    weight, drag_coefficient, remain_energy, peak_power = athlete_inf
    slope, curvatue, road_direction = track_inf
    speed, wind_direction = wind_inf

    # 在此决断输出功率，或是设定速度
    power_output = 0

    return power_output

def physical_recovery(power_output,athlete_inf):
    weight, drag_coefficient, remain_energy, peak_power = athlete_inf

    # 在此算得恢复功率
    power_recovery = 0

    return power_recovery