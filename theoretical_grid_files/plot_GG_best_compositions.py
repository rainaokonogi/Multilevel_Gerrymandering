from math import comb, factorial, floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import Counter
from tqdm import tqdm
from functools import lru_cache
import os

CURRENT_WORKING_DIRECTORY = Path.cwd()

N = 18

number_of_building_blocks_in_district = N // 2

# Create a list of the combinations of blue-blue, blue-red, and red-red dominos that can go into a blue-winning, size-12 district
valid_winning_districts = []
for bb in range(0, number_of_building_blocks_in_district + 1):
    for br in range(0, number_of_building_blocks_in_district + 1 - bb):
        rr = number_of_building_blocks_in_district - bb - br
        if 2 * bb + br >= ((N // 2) + 1):   # majority blue units
            valid_winning_districts.append((bb, br, rr))

def can_make_target_num_blue_districts(nBB, nBR, nRR, target):
    PAT = tuple(valid_winning_districts)

    memo = {}

    def search(bb, br, rr, made):
        key = (bb, br, rr, made)
        if key in memo:
            return memo[key]

        # success
        if made == target:
            memo[key] = True
            return True

        # prune: not enough groups left to fill remaining districts
        if bb + br + rr < number_of_building_blocks_in_district * (target - made):
            memo[key] = False
            return False

        # try each blue-majority pattern
        for num_blues, num_purples, num_reds in PAT:
            if num_blues <= bb and num_purples <= br and num_reds <= rr:
                if search(bb-num_blues, br-num_purples, rr-num_reds, made+1):
                    memo[key] = True
                    return True

        memo[key] = False
        return False

    return search(nBB, nBR, nRR, 0)

def can_make_target_all_t():
    for blue_units in range(N*N + 1):
        target_blue_dists = min(N,floor(blue_units / (number_of_building_blocks_in_district + 1)))
        output_file = f"{CURRENT_WORKING_DIRECTORY}/theoretical_grid_files/new_compositions_for_which_max_dists_achievable/grid_size_{N}/GG_t_{blue_units}.csv"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)
            writer.writerow(["Blue-Blue","Blue-Red","Red-Red","Max Districts Achievable?"])
            
            min_B = max(0, blue_units - (N*N)//2)
            max_B = blue_units // 2

            for B in range(min_B, max_B + 1):
                R = (N*N)//2 - blue_units + B
                P = blue_units - 2*B
                writer.writerow([B,P,R,can_make_target_num_blue_districts(B, P, R, target_blue_dists)])


def count_ways_achieve_max_districts(bb_total, br_total, rr_total, sets_needed):

    memo = {}

    def search(bb, br, rr, k):
        key = (bb, br, rr, k)
        if key in memo:
            return memo[key]

        if k == 0:
            memo[key] = 1
            return 1

        if bb < 0 or br < 0 or rr < 0:
            memo[key] = 0
            return 0

        total = 0

        # Search over all ways to make a winning district
        for xbb, xbr, xrr in valid_winning_districts:

            # If you have enough "allowance" to make a type of winning district, sum all ways possible using labeled blocks
            if bb >= xbb and br >= xbr and rr >= xrr:
                ways_choose_blocks = (
                    comb(bb, xbb) *
                    comb(br, xbr) *
                    comb(rr, xrr)
                )

                # Continue searching for the rest of the districts
                total += ways_choose_blocks * search(
                    bb - xbb,
                    br - xbr,
                    rr - xrr,
                    k - 1
                )

        memo[key] = total
        return total

    number_ways_ordered_districts = search(bb_total, br_total, rr_total, sets_needed)
    number_ways_unordered_districts = number_ways_ordered_districts // factorial(sets_needed)
    return number_ways_unordered_districts

def compute_best_GG_comps(blue_pts):

    max_val = 0
    bbs_in_best_comp = 0
     
    with open(f"{CURRENT_WORKING_DIRECTORY}/theoretical_grid_files/new_compositions_for_which_max_dists_achievable/grid_size_{N}/GG_t_{blue_pts}.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header row
        target_blue_dists = min(N,floor(blue_pts / (number_of_building_blocks_in_district + 1)))
        for row in reader:
            if row[3] == "True":
                bb, br, rr = int(row[0]), int(row[1]), int(row[2])

                num_ways = count_ways_achieve_max_districts(bb, br, rr, sets_needed=target_blue_dists)
                if num_ways > max_val:
                    max_val = num_ways
                    bbs_in_best_comp = bb
        
        return bbs_in_best_comp

def make_GG_best_image():

    x_values = []
    y_values = []

    for blue_pts in range((N//2)+1, N*N-(N//2)):
        best_comp = compute_best_GG_comps(blue_pts)
        x_values.append(blue_pts)
        y_values.append(best_comp)
    print(list(zip(x_values,y_values)))

    baseline_dict = {
        i: i - (N*N//2)
        for i in range((N*N//2), N*N)
    }

    first_intersection_x = None

    for x, y in list(zip(x_values, y_values)):
        if x in baseline_dict and y == baseline_dict[x]:
            first_intersection_x = x
            break


    plt.figure(figsize=(10, 7))
    plt.plot(list(range((N*N//2), N*N - (N//2) + 1)), [i - (N*N//2) for i in list(range((N*N//2), N*N - (N//2) + 1))], alpha=0.8, color="#C9DC87",linewidth=5,label="Smallest number of blue-blue dominos possible")
    plt.plot(x_values, y_values,marker='o',linestyle='None',markersize=5,color="#3CB371",label="Number of blue-blue dominos in best composition",alpha=0.8)
    # if first_intersection_x is not None:
    #     plt.axvline(
    #         x=first_intersection_x,
    #         color="black",
    #         linestyle="--",
    #         linewidth=2,
    #         alpha=0.8,
    #         label=f"First intersection: x={first_intersection_x}"
    #     )
    # if first_intersection_x is not None:
    #     plt.text(
    #         first_intersection_x,
    #         plt.ylim()[1] * 0.95,
    #         f"x = {first_intersection_x}",
    #         fontsize=14,
    #         ha="center",
    #         va="bottom"
    #     )
    plt.axvline(
        x=(N*N)//2,
        color="black",
        linewidth=2,
        alpha=0.8
    )
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=14)
    plt.savefig(f"{CURRENT_WORKING_DIRECTORY}/theoretical_grid_files/MEETING_best_GG_comps_N_{N}.png",bbox_inches="tight",dpi=600)


make_GG_best_image()


