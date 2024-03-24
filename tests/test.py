import time

def test(func):
    def wrapper(*args, **kwargs):
        print("=" * 50)
        print(f"Testing {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Test finished {func.__name__} in {end - start:.6f} seconds")
        print("=" * 50)
        return result
    return wrapper
