import time
import numpy as np
from statistics import mean, stdev
from functools import wraps

class LongTimeDecorator:
    def __init__(self):
        self.times = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            self.times.append(end - start)
            return result
        return wrapper

    def stats(self):
        return {
            "sum": sum(self.times),
            "min": min(self.times),
            "max": max(self.times),
            "mean": mean(self.times),
            "stdev": stdev(self.times)
        }
    
decorator = LongTimeDecorator()

@decorator
def long_time_function(n):
    size=n
    matrixa = np.random.rand(size, size)
    matrixb = np.random.rand(size, size)
    return np.dot(matrixa, matrixb)

for _ in range(10):
    long_time_function(4000)

print("Statystyki czasów wykonania:")
print(decorator.stats())