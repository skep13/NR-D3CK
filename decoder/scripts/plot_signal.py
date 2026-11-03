import numpy as np
import matplotlib.pylot as plt

path = "data/recordings/modes1.bin"

raw = np.fromfile(path, dtype=np.uint8)

print("Bytes loaded:", len(raw))
print("First 10 values:", raw[:10])
