import numpy as np
import random

def get_realistic_task_duration():
    duration_days = np.random.lognormal(mean=0.5, sigma=0.8)
    return max(0.1, min(60, duration_days))

