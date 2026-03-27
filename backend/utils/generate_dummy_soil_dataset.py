import pandas as pd
import numpy as np

np.random.seed(42)

num_samples = 300

data = []

for _ in range(num_samples):

    # Generate realistic RGB values (soil colors)
    mean_r = np.random.randint(60, 180)
    mean_g = np.random.randint(50, 160)
    mean_b = np.random.randint(40, 140)

    # HSV values
    mean_h = np.random.randint(5, 35)
    mean_s = np.random.randint(20, 80)
    mean_v = np.random.randint(60, 180)

    # --- Create realistic NPK relationships ---
    # Darker soil (lower brightness) → higher Nitrogen
    brightness = (mean_r + mean_g + mean_b) / 3

    N = max(20, 120 - brightness + np.random.randint(-10, 10))
    P = max(10, (mean_r * 0.4) + np.random.randint(-15, 15))
    K = max(20, (mean_g * 0.5) + np.random.randint(-15, 15))

    data.append([
        mean_r, mean_g, mean_b,
        mean_h, mean_s, mean_v,
        round(N,2), round(P,2), round(K,2)
    ])

columns = [
    'mean_r','mean_g','mean_b',
    'mean_h','mean_s','mean_v',
    'N','P','K'
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("soil_dataset.csv", index=False)

print("soil_dataset.csv created successfully with 300 samples!")
