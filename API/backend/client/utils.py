import math
import numpy as np

def calculate_reorder_point(units_sold_list, lead_time_days, z_score=1.65):
    """
    Calculates Reorder Point using statistical safety stock formula:
    ROP = (Average Daily Usage * Lead Time) + Safety Stock

    Safety Stock = Z * σ_d * sqrt(L)
    """
    if not units_sold_list:
        avg_daily = 1
        std_dev = 0
    else:
        avg_daily = np.mean(units_sold_list)
        std_dev = np.std(units_sold_list)

    safety_stock = z_score * std_dev * math.sqrt(lead_time_days)
    reorder_point = (avg_daily * lead_time_days) + safety_stock

    return int(round(reorder_point))
