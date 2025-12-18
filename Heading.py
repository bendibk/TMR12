#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TRAVIATA – Single time series plot with three separate y-axes
(ShaftRev_rpm / SpeedThroughWater_kn / ShaftPower_kW) for a 1-hour window
Larger fonts for thesis-quality readability.
"""

import pandas as pd
import matplotlib.pyplot as plt


def main():
    plt.style.use("seaborn-v0_8-whitegrid")

    # -----------------------------
    # Font sizes (tune here)
    # -----------------------------
    LABEL_FS = 14
    TICK_FS  = 14
    LEGEND_FS = 15

    # -----------------------------
    # Load data
    # -----------------------------
    DATA_PATH = "./ocean_out/telemetry_with_era5_ocean.parquet"
    df = pd.read_parquet(DATA_PATH)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    df = df.sort_values("timestamp").reset_index(drop=True)

    # -----------------------------
    # Filter to the requested time window (UTC)
    # -----------------------------
    t0 = pd.Timestamp("2023-06-17 18:50", tz="UTC")
    t1 = pd.Timestamp("2023-06-17 21:50", tz="UTC")
    dfw = df[(df["timestamp"] >= t0) & (df["timestamp"] <= t1)].copy()

    print("Windowed data shape:", dfw.shape)

    # Colors
    c_rpm = "tab:blue"
    c_stw = "red"
    c_pwr = "orange"

    # Thicker grid linewidths
    lw_grid_y = 1.4
    lw_grid_x = 1.2

    # -----------------------------
    # Plot with 3 y-axes
    # -----------------------------
    fig, ax1 = plt.subplots(figsize=(16, 6))

    # Axis 1 (left): RPM
    l1, = ax1.plot(dfw["timestamp"], dfw["HeadingTrue_deg"], lw=2, color=c_rpm, label="HeadingTrue_deg")
    ax1.set_ylabel("Heading Degree", color=c_rpm, fontsize=LABEL_FS)
    ax1.tick_params(axis="y", colors=c_rpm, labelsize=TICK_FS)
    ax1.spines["left"].set_color(c_rpm)

    # Disable default grid; add colored grids explicitly
    ax1.grid(False)
    ax1.yaxis.grid(True, color=c_rpm, alpha=0.20, linewidth=lw_grid_y)
    ax1.xaxis.grid(True, color=c_rpm, alpha=0.10, linewidth=lw_grid_x)

    # Axis 2 (right): STW
    ax2 = ax1.twinx()
    l2, = ax2.plot(dfw["timestamp"], dfw["SpeedThroughWater_kn"], lw=2, color=c_stw, label="SpeedThroughWater_kn")
    ax2.set_ylabel("STW [kn]", color=c_stw, fontsize=LABEL_FS)
    ax2.tick_params(axis="y", colors=c_stw, labelsize=TICK_FS)
    ax2.spines["right"].set_color(c_stw)
    ax2.grid(False)
    ax2.yaxis.grid(True, color=c_stw, alpha=0.15, linewidth=lw_grid_y)

    # Axis 3 (right, offset outward): Shaft Power
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 70))
    ax3.spines["right"].set_color(c_pwr)
    l3, = ax3.plot(dfw["timestamp"], dfw["ShaftPower_kW"], lw=2, color=c_pwr, label="ShaftPower_kW")
    ax3.set_ylabel("Shaft Power [kW]", color=c_pwr, fontsize=LABEL_FS)
    ax3.tick_params(axis="y", colors=c_pwr, labelsize=TICK_FS)
    ax3.grid(False)
    ax3.yaxis.grid(True, color=c_pwr, alpha=0.12, linewidth=lw_grid_y)

    # X-axis formatting
    ax1.set_xlabel("Time (UTC)", fontsize=LABEL_FS)
    ax1.tick_params(axis="x", labelsize=TICK_FS)

    # Combined legend
    lines = [l1, l2, l3]
    labels = [ln.get_label() for ln in lines]
    ax1.legend(lines, labels, loc="lower left", fontsize=LEGEND_FS)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
