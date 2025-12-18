import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

# Match your sizes
LABEL_FS = 14
TICK_FS  = 14
LEGEND_FS = 15  # not used here, but kept for consistency
TITLE_FS = 16

# Load data
#DATA_PATH = "./ocean_out/telemetry_with_era5_ocean.parquet"
DATA_PATH = "./Final_datasets/telemetry_final_TRAVIATA.parquet"
df = pd.read_parquet(DATA_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])
if df["timestamp"].dt.tz is None:
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
else:
    df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

# Plot: Shaft power vs STW (full dataset)
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(df["SpeedThroughWater_kn"], df["ShaftRev_rpm"], s=10, alpha=0.15)

ax.set_xlabel("Speed Through Water [kn]", fontsize=LABEL_FS)
ax.set_ylabel("Shaft Power [kW]", fontsize=LABEL_FS)
ax.set_title("Shaft Power vs STW (full dataset)", fontsize=TITLE_FS)

ax.tick_params(axis="both", labelsize=TICK_FS)

ax.set_xlim(left=0)  # 0 to automatic max
ax.set_ylim(bottom=0)  # 0 to automatic max

ax.grid(True)
plt.tight_layout()
plt.show()