# profiling.py
from time import time
from functools import wraps

# Global statistics dictionary to track function statistics
stats = {}

def audit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global stats

        # Initialize the stat entry for the function if it doesn't exist
        if func.__name__ not in stats:
            stats[func.__name__] = [0, 0.0]  # Initialize the stat as [run_count, avg_time]

        # Get the stat for the current function
        stat = stats[func.__name__]

        # Start timing
        pstart = time()

        # Execute the actual function
        result = func(*args, **kwargs)

        # End timing
        pend = time()

        # Update statistics
        elapsed_time = pend - pstart
        stat[1] = stat[1] + ((elapsed_time) - stat[1]) / (stat[0] + 1)
        stat[0] += 1

        # Print the profiling result
        print(func.__name__ + f" runs: {stat[0]}, avg: {stat[1]:.10f} seconds")

        return result

    return wrapper
