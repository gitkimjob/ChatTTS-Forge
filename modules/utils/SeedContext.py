import torch
import random
import numpy as np


def deterministic(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def is_numeric(obj):
    if isinstance(obj, str):
        try:
            float(obj)
            return True
        except ValueError:
            return False
    elif isinstance(obj, (np.integer, np.signedinteger, np.unsignedinteger)):
        return True
    elif isinstance(obj, np.floating):
        return True
    elif isinstance(obj, (int, float)):
        return True
    else:
        return False


class SeedContext:
    def __init__(self, seed):
        assert is_numeric(seed), "Seed must be an number."

        try:
            self.seed = int(np.clip(int(seed), -1, 2**32 - 1))
        except Exception as e:
            raise ValueError("Seed must be an integer.")

        self.seed = seed
        self.state = None

        if isinstance(seed, str) and seed.isdigit():
            self.seed = int(seed)

        if isinstance(self.seed, float):
            self.seed = int(self.seed)

        if self.seed == -1:
            self.seed = random.randint(0, 2**32 - 1)

    def __enter__(self):
        self.state = (torch.get_rng_state(), random.getstate(), np.random.get_state())

        deterministic(self.seed)

    def __exit__(self, exc_type, exc_value, traceback):
        torch.set_rng_state(self.state[0])
        random.setstate(self.state[1])
        np.random.set_state(self.state[2])


if __name__ == "__main__":
    print(is_numeric("1234"))  # True
    print(is_numeric("12.34"))  # True
    print(is_numeric("-1234"))  # True
    print(is_numeric("abc123"))  # False
    print(is_numeric(np.int32(10)))  # True
    print(is_numeric(np.float64(10.5)))  # True
    print(is_numeric(10))  # True
    print(is_numeric(10.5))  # True
    print(is_numeric(np.int8(10)))  # True
    print(is_numeric(np.uint64(10)))  # True
    print(is_numeric(np.float16(10.5)))  # True
    print(is_numeric([1, 2, 3]))  # False
