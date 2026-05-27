from math import comb, factorial, floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import Counter
from tqdm import tqdm
from functools import lru_cache

CURRENT_WORKING_DIRECTORY = Path.cwd()

building_block_size = 6

# Create a list of the combinations of blue-blue, blue-red, and red-red dominos that can go into a blue-winning, size-12 district
valid_winning_districts = []
for bb in range(0, building_block_size + 1):
    for br in range(0, building_block_size + 1 - bb):
        rr = building_block_size - bb - br
        if 2 * bb + br >= 7:   # majority blue units
            valid_winning_districts.append((bb, br, rr))

print(len(valid_winning_districts))

quit()

def count_ways_achieve_max_districts(bb_total, br_total, rr_total, sets_needed):

    memo = {}

    district_types = list(valid_winning_districts)

    m = len(district_types)

    @lru_cache(None)
    def search(i, bb, br, rr, k):

        if k == 0:
            return 1
        if i == m:
            return 0

        xbb, xbr, xrr = district_types[i]

        total = 0

        # try using this type t times
        max_t = k

        # resource-limited upper bound (important pruning)
        if xbb > 0:
            max_t = min(max_t, bb // xbb)
        if xbr > 0:
            max_t = min(max_t, br // xbr)
        if xrr > 0:
            max_t = min(max_t, rr // xrr)

        for t in range(max_t + 1):

            need_bb = t * xbb
            need_br = t * xbr
            need_rr = t * xrr

            ways = (
                comb(bb, need_bb) *
                comb(br, need_br) *
                comb(rr, need_rr)
            )

            total += ways * search(
                i + 1,
                bb - need_bb,
                br - need_br,
                rr - need_rr,
                k - t
            )

        return total

    result = search(0, bb_total, br_total, rr_total, sets_needed)

    # number_ways_unordered_districts = number_ways_ordered_districts // factorial(sets_needed)

    # convert to unordered districts
    return result



# def count_ways_achieve_max_districts(bb_total, br_total, rr_total, sets_needed):

#     memo = {}

#     def search(bb, br, rr, k):
#         key = (bb, br, rr, k)
#         if key in memo:
#             return memo[key]

#         if k == 0:
#             memo[key] = 1
#             return 1

#         if bb < 0 or br < 0 or rr < 0:
#             memo[key] = 0
#             return 0

#         total = 0

#         # Search over all ways to make a winning district
#         for xbb, xbr, xrr in valid_winning_districts:

#             # If you have enough "allowance" to make a type of winning district, sum all ways possible using labeled blocks
#             if bb >= xbb and br >= xbr and rr >= xrr:
#                 ways_choose_blocks = (
#                     comb(bb, xbb) *
#                     comb(br, xbr) *
#                     comb(rr, xrr)
#                 )

#                 # Continue searching for the rest of the districts
#                 total += ways_choose_blocks * search(
#                     bb - xbb,
#                     br - xbr,
#                     rr - xrr,
#                     k - 1
#                 )

#         memo[key] = total
#         return total

#     number_ways_ordered_districts = search(bb_total, br_total, rr_total, sets_needed)

#     number_ways_unordered_districts = number_ways_ordered_districts // factorial(sets_needed)

#     # convert to unordered districts
#     return number_ways_unordered_districts

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
        if bb + br + rr < 6 * (target - made):
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

    print(nBB)
    print(search(nBB, nBR, nRR, 0))
    return search(nBB, nBR, nRR, 0)

    with open("GG_72R_72D_size_2.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Blue-Blue","Blue-Red","Red-Red","Max Districts (10) Achievable?"])
        
        for B in range(37):
            R = B
            P = 72 - 2*B
            writer.writerow([B,P,R,can_make_target_num_blue_districts(B, P, R, 10)])

def compute_best_GG_comps(red_pts):

    max_val = 0
    bbs_in_best_comp = 0

    blue_pts = 144 - red_pts
    max_districts = min(12,floor(blue_pts/7))
     
    with open(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/theoretical_grid_files/compositions_for_which_max_district_is_achievable/GG_{red_pts}R_{blue_pts}D_size_2.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header row

        for row in reader:
            if row[3] == "True":
                bb, br, rr = int(row[0]), int(row[1]), int(row[2])

                num_ways = count_ways_achieve_max_districts(bb, br, rr, sets_needed=max_districts)
                if num_ways > max_val:
                    max_val = num_ways
                    bbs_in_best_comp = bb
                    
        return bbs_in_best_comp

def make_GG_best_image():

    x_values = []
    y_values = []

    for red_pts in range(7,138):
        best_comp = compute_best_GG_comps(red_pts)
        x_values.append(144 - red_pts)
        y_values.append(best_comp)

    plt.figure(figsize=(10, 7))
    plt.plot(list(range(72, 145)), [i - 72 for i in list(range(72, 145))], alpha=0.8, linewidth=5, color="#C9DC87",label="Smallest number of blue-blue dominos possible")
    plt.plot(x_values, y_values,marker='o',linestyle='None',markersize=5,color="#3CB371",label="Number of blue-blue dominos in best composition",alpha=0.8)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=14)
    plt.savefig(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/theoretical_grid_files/best_GG_comps_size_2.png",bbox_inches="tight",dpi=600)

make_GG_best_image()




# x = np.arange(7, 137)
# y = np.floor(x / 7)
# y2 = np.maximum(0, x - 72)
# y3 = (3/7)*x -0.4






# for red_pts in range(73,138):
# # for red_pts in range(73,138):

#     max_val = 0
#     max_at = 0

#     blue_pts = 144 - red_pts
#     max_districts = min(12,floor(blue_pts/7))

#     with open(f"/share/duchin/raina/find_GG_best/{red_pts}R_size_2.csv", "w", newline="") as csvfile:

#         writer = csv.writer(csvfile)
#         writer.writerow(["Blue-Blue","Blue-Red","Red-Red","Number Ways Achieve Max Districts {max_districts}"])

#         with open(f"/share/duchin/raina/GG_max_districts_achievable_by_comp/GG_{red_pts}R_{blue_pts}D_size_2.csv", newline="") as f:
#             reader = csv.reader(f)
#             header = next(reader)  # skip header row

#             for row in reader:
#                 if row[3] == "True":
#                     bb, br, rr = int(row[0]), int(row[1]), int(row[2])

#                     num_ways = count_ways_achieve_max_districts(bb, br, rr, sets_needed=max_districts)
#                     if num_ways > max_val:
#                         max_val = num_ways
#                         max_at = bb
                    
#                     writer.writerow([bb,br,rr,num_ways])

#         x_1_values.append(blue_pts)
#         y_1_values.append(max_at)
#         # print("Red pts: ", red_pts)
#         # print("maximized at: ", max_at)