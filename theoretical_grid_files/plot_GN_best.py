from math import comb, factorial, floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

def compute_best_GN_comps(red_pts):
    """Returns the number of blue-blue dominos in the best composition (i.e. best expected value under our score function)
    for gerry-neutral case.
    
    Args:
        red_pts: the number of red units (out of 144) in the underlying grid.
    """
    blue_pts = 144 - red_pts

    max_val_wins = 0
    bbs_in_best_comp_wins = 0
    max_val_ties = 0
    bbs_in_best_comp_ties = 0

    if red_pts < 73:
        for num_red_doms in range(0,floor(red_pts/2)+1):
            num_blue_doms = num_red_doms + 72 - red_pts

            num_purple_doms = 72 - num_blue_doms - num_red_doms

            win_score = 0
            tie_score = 0

            for b in range(0,7):
                for r in range(0,min(b,7-b)):
                    p = 6 - b - r
                    wins = ((comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) / comb(72,6))
                    win_score = win_score + wins

            for i in range(0,4):
                ties = ((comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,6-2*i)) / comb(72,6))
                tie_score = tie_score + ties

            # By linearity of expectation, gives expected value of a random plan from this composition
            score_fnc_1 = 12 * win_score
            score_fnc_2 = 12 * (win_score + 0.5 * tie_score)

            # Keep track of what composition has best expected value
            if score_fnc_1 > max_val_wins:
                max_val_wins = score_fnc_1
                bbs_in_best_comp_wins = num_blue_doms

            if score_fnc_2 > max_val_ties:
                max_val_ties = score_fnc_1
                bbs_in_best_comp_ties = num_blue_doms

        return bbs_in_best_comp_wins, bbs_in_best_comp_ties


    elif red_pts > 72:
        for num_blue_doms in range(0,floor(blue_pts/2)+1):
            num_red_doms = num_blue_doms + 72 - blue_pts
        
            num_purple_doms = 72 - num_blue_doms - num_red_doms

            win_score = 0
            tie_score = 0

            for b in range(0,7):
                for r in range(0,min(b,7-b)):
                    p = 6 - b - r
                    wins = ((comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) / comb(72,6))
                    win_score = win_score + wins

            for i in range(0,4):
                ties = ((comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,6-2*i)) / comb(72,6))
                tie_score = tie_score + ties

            # By linearity of expectation, gives expected value of a random plan from this composition
            score_fnc_1 = 12 * win_score
            score_fnc_2 = 12 * (win_score + 0.5 * tie_score)

            # Keep track of what composition has best expected value
            if score_fnc_1 > max_val_wins:
                max_val_wins = score_fnc_1
                bbs_in_best_comp_wins = num_blue_doms

            if score_fnc_2 > max_val_ties:
                max_val_ties = score_fnc_1
                bbs_in_best_comp_ties = num_blue_doms

        return bbs_in_best_comp_wins, bbs_in_best_comp_ties


def make_GN_best_image():
    x_values_wins = []
    y_values_wins = []
    x_values_ties = []
    y_values_ties = []

    for red_pts in range(7,138):
        best_comp_wins, best_comp_ties = compute_best_GN_comps(red_pts)
        x_values_wins.append(144 - red_pts)
        x_values_ties.append(144 - red_pts)
        y_values_wins.append(best_comp_wins)
        y_values_ties.append(best_comp_ties)

    plt.figure(figsize=(10, 7))
    plt.plot(list(range(72, 145)), [i - 72 for i in list(range(72, 145))], alpha=0.8, color="#C9DC87",linewidth=5,label="Smallest number of blue-blue dominos possible")
    plt.plot(x_values_wins, y_values_wins,marker='o',linestyle='None',markersize=5,color="#BB3385",label="Number of blue-blue dominos in best composition",alpha=0.8)
    # plt.plot(x_values_ties, y_values_ties,marker='o',linestyle='None',markersize=5,color="#7B68EE",label="Number of blue-blue dominos in best composition",alpha=0.8)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=14)
    plt.savefig(f"{CURRENT_WORKING_DIRECTORY}/REPLICATION_REPO/theoretical_grid_files/best_GN_comps_wins_size_2.png",bbox_inches="tight",dpi=600)


make_GN_best_image()