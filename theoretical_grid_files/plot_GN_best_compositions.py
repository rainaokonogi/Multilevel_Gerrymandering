from math import comb, factorial, floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

# Toggle these values to change the situation!
# The number of units is N^2. They will be combined into N/2 pairs which will be aggregated into N districts.
# ties_worth is the score awarded to a tied district according to our score function. Wins are always worth 1.
# In the paper, we look at N=12 with ties_worth=0 and ties_worth=0.5
N = 12
ties_worth = 0

def compute_best_GN_comps(red_pts):
    """Returns the number of blue-blue pairs in a best composition for the gerry-neutral case
    (i.e. a composition that maximizes the expected value of a random districting plan).
    Will always return the first best composition that is found; based on the order in which we
    check the EVs of each composition, this will be the best composition with the highest number of blue-red pairs.
    
    Args:
        red_pts: the number of red units (out of N^2) in the underlying grid.
    """
    blue_pts = N*N - red_pts

    max_val_EV = 0
    bbs_in_best_comp = 0

    # First we look at what happens when there are fewer red units than blue units.
    if red_pts < (((N*N)//2) + 1):

        # We look at each possible composition, starting from the one that minimizes red-red pairs.
        # This is equivalent to maximizing blue-red pairs.
        for num_red_doms in range(0,floor(red_pts/2)+1):

            num_blue_doms = num_red_doms + (blue_pts - ((N*N)//2))
            num_purple_doms = ((N*N)//2) - num_blue_doms - num_red_doms

            # We keep track of the contribution to EV of blue-winning districts and tied districts.
            win_score = 0
            tie_score = 0

            # With the composition fixed, we look at every way of forming a blue-winning district.
            for b in range(1,int((N//2)+1)):
                for r in range(0,min(b,int((N//2)+1-b))):
                    p = (N//2) - b - r
                    
                    # Note that in the formal expected value computations we would turn these into probabilties by dividing by (N^2/2 choose N/2).
                    # We skip this step to avoid floating-point errors.
                    # Since we only care about comparing compositions, not the raw expected values, this doesn't change our results.
                    wins = (comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) 
                    win_score = win_score + wins

            # We look at every way of forming a tied district and do an equivalent computation as above.
            for i in range(0,floor((N/4)+1)):
                ties = (comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,(N//2)-2*i))
                tie_score = tie_score + ties

            # Compute final EV of the composition according to the score function.
            # Again, we neglect the shared scalar; to get the true EV of a random plan, we would apply linearity of expectation and multiply by N.
            score_fnc = win_score + (ties_worth * tie_score)

            # Keep track of composition with highest EV seen so far.
            # Composition only changes if a new composition has a strictly higher EV.
            if score_fnc > max_val_EV:
                max_val_EV = score_fnc
                bbs_in_best_comp = num_blue_doms

        return bbs_in_best_comp


    # Repeat the process for the cases where there are more red units than blue units.
    elif red_pts > ((N*N)//2):

        # Again, we look at each possible composition, starting from the one that minimizes blue-blue pairs.
        # This is equivalent to maximizing blue-red pairs.
        for num_blue_doms in range(0,floor(blue_pts/2)+1):

            num_red_doms = num_blue_doms + ((N*N)//2) - blue_pts
            num_purple_doms = ((N*N)//2) - num_blue_doms - num_red_doms

            win_score = 0
            tie_score = 0

            for b in range(1,int((N//2)+1)):
                for r in range(0,min(b,int((N//2)+1-b))):
                    p = (N//2) - b - r
                    wins = (comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p))
                    win_score = win_score + wins

            for i in range(0,floor((N/4)+1)):
                ties = (comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,(N//2)-2*i))
                tie_score = tie_score + ties

            score_fnc = win_score + (ties_worth * tie_score)

            if score_fnc > max_val_EV:
                max_val_EV = score_fnc
                bbs_in_best_comp = num_blue_doms

        return bbs_in_best_comp

def make_GN_best_image():
    """Plots the number of blue units (x-axis) against the number of blue-blue pairs in the best composition
    with the highest number of blue-red pairs.
    Also plots the line showing the compositions with the maximum number of blue-red pairs
    when there are more blue units than red.
    """
    x_values = []
    y_values = []

    for red_pts in range((N//2)+1, N*N-(N//2)):
        best_comp = compute_best_GN_comps(red_pts)
        x_values_wins.append(N*N - red_pts)
        y_values_wins.append(best_comp)

    plt.figure(figsize=(10, 7))

    # Plot the compositions with the maximum number of blue-red pairs when there are more blue units than red.
    plt.plot(list(range((N*N//2), N*N - (N//2) + 1)), [i - (N*N//2) for i in list(range((N*N//2), N*N - (N//2) + 1))], alpha=0.8, color="#C9DC87",linewidth=5,label="Smallest number of blue-blue dominos possible")

    # Plot best compositions for blue against number of blue units
    plt.plot(x_values, y_values,marker='o',linestyle='None',markersize=5,color="#7B68EE",label="Number of blue-blue dominos in best composition",alpha=0.8)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=14)
    # plt.title(f"N = {N}, {N*N} units into districts of size {N}", fontsize=18)
    # plt.xlabel("Number of blue units", fontsize=16)
    # plt.ylabel("Number of blue-blue pairs in best composition (GN)", fontsize=16)
    save_location = f"{CURRENT_WORKING_DIRECTORY}/image_replication/game_theoretic_images/best_GN_comp_N_{N}_ties_worth_{ties_worth}.png"
    os.makedirs(os.path.dirname(save_location), exist_ok=True)
    plt.savefig(save_location,bbox_inches="tight",dpi=600)

make_GN_best_image()