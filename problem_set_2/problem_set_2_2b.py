
import time
import matplotlib.pyplot as plt
import numpy as np
import random


# Original merge sort (for comparison)
def alg2_keyed(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        #split the data to half
        left = iter(alg2_keyed(data[:split]))
        right = iter(alg2_keyed(data[split:]))
        result = []
        
        #first element of left and right, should be a tuple here
        left_top = next(left)
        right_top = next(right)
        
        while True:
            if left_top[0] < right_top[0]: #compare by key
                result.append(left_top)
                try:
                    left_top = next(left)
                except StopIteration:
                    return result + [right_top] + list(right)
            else:
                result.append(right_top)
                try:
                    right_top = next(right)
                except StopIteration:
                    return result + [left_top] + list(left)


import multiprocessing as mp

# Implement a parallel version of your modified merge sort algorithm
# splitting the workload across multiple processing cores

def parallel_alg2_keyed(data, num_cores=16):
    if len(data) <= 1:
        return data
    #use the maximize cores that the pc supports
    if num_cores is None:
        num_cores = mp.cpu_count()
    
    print(num_cores)

    #if #cores larger then #data, no need to parrallel
    if num_cores > len(data):
        return alg2_keyed(data)

    # now we need num_cores data split
    split_size = len(data) // num_cores
    splits = [data[i * split_size:(i + 1) * split_size] for i in range(num_cores - 1)]
    splits.append(data[(num_cores - 1) * split_size:])
    
    # pool

    with mp.Pool(num_cores) as pool:
        sorted_splits = pool.map(alg2_keyed, splits)

            
    while len(sorted_splits) > 1:
        new_sorted_splits = []
        for i in range(0, len(sorted_splits), 2):
            if i + 1 < len(sorted_splits):
                new_sorted_splits.append(merge(sorted_splits[i], sorted_splits[i + 1]))
            else:
                new_sorted_splits.append(sorted_splits[i]) 
        sorted_splits = new_sorted_splits
        print(len(sorted_splits))

    return sorted_splits[0]

# for two splits, how to merge them into big splits
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result





# Utility function to generate random data
def generate_random_data(num_pairs, key_range):
    return [(random.randint(*key_range), f'value_{i}') for i in range(num_pairs)]

# Function to measure the time of execution
def measure_time(func, data):
    start_time = time.time()
    result = func(data)
    end_time = time.time()
    return end_time - start_time, result

# Main function to compare serial and parallel merge sort
if __name__ == '__main__':
    dataset_sizes = [50000, 100000, 500000,1000000,10000000]
    serial_times = []
    parallel_times = []

    for size in dataset_sizes:
        print(f"Dataset size: {size}")
        data = generate_random_data(size, (1, 100000000))

        # Measure serial merge sort time
        serial_time, _ = measure_time(alg2_keyed, data)
        serial_times.append(serial_time)
        print(f"Serial time: {serial_time:.4f} seconds")

        # Measure parallel merge sort time
        parallel_time, _ = measure_time(parallel_alg2_keyed, data)
        parallel_times.append(parallel_time)
        print(f"Parallel time: {parallel_time:.4f} seconds")

    # Visualize the results
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.loglog(dataset_sizes, serial_times, label="Serial Merge Sort", marker='o')
    plt.loglog(dataset_sizes, parallel_times, label="Parallel Merge Sort", marker='o')
    plt.xlabel("Dataset Size")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.show()
