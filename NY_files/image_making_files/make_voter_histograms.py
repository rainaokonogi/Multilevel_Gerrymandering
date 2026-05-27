import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

CURRENT_WORKING_DIRECTORY = Path.cwd()

for block_type in ["blockgroups","vtds","tracts"]:
    for election in ["PRES20","SEN22"]:
        with open(f'{CURRENT_WORKING_DIRECTORY}/NY_files/dual_graphs/{block_type}_dual_graph.json') as f:
            data = json.load(f)

        bins = np.linspace(0, 1, 21)

        df = pd.DataFrame(data["nodes"])

        df['total_votes'] = df[f'{election}DEM'] + df[f'{election}REP']
        df['dem_share'] = df[f'{election}DEM'] / df['total_votes']

        # Drop any units with no valid vote data
        df_valid = df.dropna(subset=['dem_share'])

        plt.figure(figsize=(10, 6))
        plt.hist(df_valid['dem_share'], bins=bins, color='#1560BD', edgecolor='black')

        if election == "PRES20":
            plt.vlines(0.617, 0, 1450, color='red', linewidth=2)
        elif election == "SEN20":
            plt.vlines(0.570, 0, 1450, color='red', linewidth=2)


        # plt.title("Distribution of Democratic Vote Share (Sen 2020, Block Groups)")
        # plt.ylabel("Number of Units")
        plt.ylim(0,110)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.yticks(fontsize=20)
        plt.xlim(0,1)
        plt.xticks(np.linspace(0, 1, 11), fontsize=20)
        plt.tight_layout()
        save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/NY_voter_histograms/{block_type}_{election}_dem_votes.png"
        os.makedirs(save_location, exist_ok=True)
        plt.savefig(save_location, dpi=600)
        plt.close()