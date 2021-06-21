import concurrent.futures, os

WORKERS = 5 * os.cpu_count()

def function_name(parameter):
    return parameter

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    futures = []

    # Add To Processing Queue
    for element in elements:
        futures.append(executor.submit(function_name, parameter))

    # Print Results
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
