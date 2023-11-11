# Imports
from argparse import ArgumentParser
from os import path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LogNorm

# Parse execution arguments
parser = ArgumentParser(description="Create graphics from the experiments data.")
parser.add_argument(
    "input_files",
    help="CSV files to be read and processed. Should be outputs of launcher.py, from different machines",
    nargs="+",
)
parser.add_argument(
    "-o", "--out", help="Folder where the images will be saved", required=True
)
args = parser.parse_args()
input_files = args.input_files
out_folder = args.out

# Read the data in every csv input and combine into single dataframe
data = []
for input_file in input_files:
    partial_data = pd.read_csv(input_file)
    partial_data["Machine"] = input_file.split(".")[0]
    data.append(partial_data)
data = pd.concat(data, ignore_index=True)

# Transform time from microseconds to seconds
data["Time (secs)"] = data["Time"] * 10**-6
# Fix machine names to agree with aws documentation
data["Machine"] = data.apply(lambda x: x["Machine"].replace("_", "."), axis=1)
# Obtain list of unique machines and algorithms
machines = data["Machine"].unique()
algorithms = data["Algorithm"].unique()
num_machines = len(machines)
num_algorithms = len(algorithms)

# Create matplotlib figure to plot time heatmap
fig, ax = plt.subplots(num_machines, num_algorithms)
fig_width = 12
fig.set_size_inches(fig_width, 3 * fig_width // 2)
ax_idx = 0
# Iterate over every machine and algorithm combination
for machine in machines:
    for algorithm in algorithms:
        # Obtain axis position in figure
        position = divmod(ax_idx, num_algorithms)
        # Create time heatmap, with matrix vs threads dimensions
        heatmap = data.query(f"Algorithm == '{algorithm}' and Machine == '{machine}'")
        heatmap = heatmap.pivot_table(
            values="Time (secs)",
            index="Matrix_Size",
            columns="N_Threads",
            aggfunc="mean",
        )
        sns.heatmap(heatmap, norm=LogNorm(), ax=ax[*position])
        ax[*position].set_title(f"Machine={machine} | Algorithm={algorithm}")
        ax_idx += 1
fig.suptitle(
    "Time (secs) for every threads-size combination", fontsize="xx-large", x=0.5, y=0.92
)
# Save figure
plt.savefig(path.join(out_folder, "size-threads-time.png"))
# Clear figure
plt.clf()
plt.cla()

# Define data subset with max number of threads and matrix size
data_size2k_threads20 = data.query("Matrix_Size == 2000 and N_Threads == 20")
# Create matplotlib figure to plot time heatmap
fig, ax = plt.subplots(num_machines, num_algorithms)
fig_width = 12
fig.set_size_inches(fig_width, 3 * fig_width // 2)
ax_idx = 0
# Iterate over every machine and algorithm combination
for machine in machines:
    for algorithm in algorithms:
        # Obtain axis position in figure
        position = divmod(ax_idx, num_algorithms)
        # Create time distribution plot as violinplot
        dist = data_size2k_threads20.query(
            f"Algorithm == '{algorithm}' and Machine == '{machine}'"
        )
        sns.violinplot(dist, y="Time (secs)", inner="quart", ax=ax[*position])
        ax[*position].set_title(f"Machine={machine} | Algorithm={algorithm}")
        ax_idx += 1
fig.suptitle(
    "Time (secs) distribution for Matrix_Size=2000, N_Threads=20",
    fontsize="xx-large",
    x=0.5,
    y=0.92,
)
# Save figure
plt.savefig(path.join(out_folder, "distribution.png"))
# Clear figure
plt.clf()
plt.cla()

# Plot threads vs time lineplots
ax = sns.relplot(
    data,
    x="N_Threads",
    y="Time (secs)",
    hue="Matrix_Size",
    row="Machine",
    col="Algorithm",
    palette="plasma",
    kind="line",
)
# Save figure
plt.savefig(path.join(out_folder, "threads-time.png"))
# Clear figure
plt.clf()
plt.cla()

# Plot matrix_size vs time lineplots
data["N_Threads"] = data["N_Threads"].astype(str)
ax = sns.relplot(
    data,
    x="Matrix_Size",
    y="Time (secs)",
    hue="N_Threads",
    row="Machine",
    col="Algorithm",
    palette="plasma",
    kind="line",
)
# Save figure
plt.savefig(path.join(out_folder, "size-time.png"))
# Program end
