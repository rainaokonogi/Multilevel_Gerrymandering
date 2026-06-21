from math import comb, factorial, floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

CURRENT_WORKING_DIRECTORY = Path.cwd()

N = 18

def compute_best_GN_comps(red_pts):
    """Returns the number of blue-blue dominos in the best composition (i.e. best expected value under our score function)
    for gerry-neutral case.
    
    Args:
        red_pts: the number of red units (out of 144) in the underlying grid.
    """
    blue_pts = N*N - red_pts

    max_val_wins = 0
    bbs_in_best_comp_wins = 0
    max_val_ties = 0
    bbs_in_best_comp_ties = 0

    if red_pts < (((N*N)//2) + 1):
        for num_red_doms in range(0,floor(red_pts/2)+1):
            num_blue_doms = num_red_doms + (blue_pts - ((N*N)//2))

            num_purple_doms = ((N*N)//2) - num_blue_doms - num_red_doms

            win_score = 0
            tie_score = 0

            for b in range(1,int((N//2)+1)):
                for r in range(0,min(b,int((N//2)+1-b))):
                    p = (N//2) - b - r
                    # wins = ((comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) / comb(((N*N)//2),(N//2)))
                    wins = (comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) 
                    win_score = win_score + wins

            # for i in range(0,floor((N/4)+1)):
            #     ties = ((comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,(N//2)-2*i)) / comb(((N*N)//2),(N//2)))
            #     tie_score = tie_score + ties

            # By linearity of expectation, gives expected value of a random plan from this composition
            score_fnc_1 = N * win_score
            # score_fnc_2 = N * (win_score + 0.2 * tie_score)

            # Keep track of what composition has best expected value
            if score_fnc_1 > max_val_wins:
                max_val_wins = score_fnc_1
                bbs_in_best_comp_wins = num_blue_doms

            # if score_fnc_2 > max_val_ties:
            #     max_val_ties = score_fnc_2
            #     bbs_in_best_comp_ties = num_blue_doms

        # return bbs_in_best_comp_wins, bbs_in_best_comp_ties
        return bbs_in_best_comp_wins


    elif red_pts > ((N*N)//2):
        for num_blue_doms in range(0,floor(blue_pts/2)+1):
            num_red_doms = num_blue_doms + ((N*N)//2) - blue_pts
        
            num_purple_doms = ((N*N)//2) - num_blue_doms - num_red_doms

            win_score = 0
            tie_score = 0

            for b in range(1,int((N//2)+1)):
                for r in range(0,min(b,int((N//2)+1-b))):
                    p = (N//2) - b - r
                    wins = ((comb(num_blue_doms,b) * comb(num_red_doms,r) * comb(num_purple_doms,p)) / comb(((N*N)//2),(N//2)))
                    win_score = win_score + wins

            # for i in range(0,floor((N/4)+1)):
            #     ties = ((comb(num_blue_doms,i) * comb(num_red_doms,i) * comb(num_purple_doms,(N//2)-2*i)) / comb(((N*N)//2),(N//2)))
            #     tie_score = tie_score + ties

            # By linearity of expectation, gives expected value of a random plan from this composition
            score_fnc_1 = N * win_score
            # score_fnc_2 = N * (win_score + 0.2 * tie_score)

            # Keep track of what composition has best expected value
            if score_fnc_1 > max_val_wins:
                max_val_wins = score_fnc_1
                bbs_in_best_comp_wins = num_blue_doms

            # if score_fnc_2 > max_val_ties:
            #     max_val_ties = score_fnc_2
            #     bbs_in_best_comp_ties = num_blue_doms

        # return bbs_in_best_comp_wins, bbs_in_best_comp_ties
        return bbs_in_best_comp_wins


def C(n, k):
    if k < 0 or k > n:
        return 0
    return comb(n, k)


def win_count_for_composition(B, P, R):
    """
    Exact integer count of blue-winning labeled districts.
    B = BB blocks, P = BR blocks, R = RR blocks.
    A district has N//2 dominoes.
    Blue wins iff b > r.
    """
    k = N // 2
    total = 0

    for b in range(1, k + 1):
        for r in range(0, min(b, k + 1 - b)):
            p = k - b - r
            total += C(B, b) * C(P, p) * C(R, r)

    return total


def compare_R0_to_best_exact(blue_units, verbose=True):
    """
    Exact comparison of the R=0 composition against all valid compositions
    for a fixed number of blue units.
    """
    M = (N * N) // 2

    B0 = blue_units - M
    P0 = N * N - blue_units
    R0 = 0

    if B0 < 0 or P0 < 0:
        if verbose:
            print(f"R=0 composition invalid for t={blue_units}")
        return False, None, None, []

    R0_score = win_count_for_composition(B0, P0, R0)

    best_score = None
    best_comps = []

    min_B = max(0, blue_units - M)
    max_B = blue_units // 2

    for B in range(min_B, max_B + 1):
        R = M - blue_units + B
        P = blue_units - 2 * B

        if B < 0 or P < 0 or R < 0:
            continue

        score = win_count_for_composition(B, P, R)

        if best_score is None or score > best_score:
            best_score = score
            best_comps = [(B, P, R)]
        elif score == best_score:
            best_comps.append((B, P, R))

    R0_is_best = (R0_score == best_score)

    if verbose:
        print(f"\nN={N}, t={blue_units}")
        print(f"R=0 comp: {(B0, P0, R0)}")
        print(f"R=0 exact win count: {R0_score}")
        print(f"Best exact win count: {best_score}")
        print(f"R=0 is maximizer? {R0_is_best}")
        print(f"Best comps: {best_comps[:20]}")

    return R0_is_best, R0_score, best_score, best_comps


def make_GN_best_image():
    x_values_wins = []
    y_values_wins = []
    x_values_ties = []
    y_values_ties = []

    for red_pts in range((N//2)+1, N*N-(N//2)):
        # best_comp_wins, best_comp_ties = compute_best_GN_comps(red_pts)
        best_comp_wins = compute_best_GN_comps(red_pts)
        x_values_wins.append(N*N - red_pts)
        # x_values_ties.append(N*N - red_pts)
        y_values_wins.append(best_comp_wins)
       # y_values_ties.append(best_comp_ties)
    print(list(zip(x_values_wins,y_values_wins)))

    baseline_dict = {
    i: i - (N*N//2)
    for i in range((N*N//2), N*N)
    }

    first_intersection_x = None

    for x, y in reversed(list(zip(x_values_wins, y_values_wins))):
        if x in baseline_dict and y == baseline_dict[x]:
            first_intersection_x = x
            break

    print(f"First intersection x-value: {first_intersection_x}")

    first_stop_intersection_x = None
    first_stop_intersection_y = None
    seen_first_intersection = False

    for x, y in reversed(list(zip(x_values_wins, y_values_wins))):
        intersects = (x in baseline_dict and y == baseline_dict[x])

        if not seen_first_intersection:
            if intersects:
                seen_first_intersection = True
            continue

        if not intersects:
            first_stop_intersection_x = x
            first_stop_intersection_y = y
            break

    print(
        f"First x after first intersection where green stops intersecting purple: "
        f"({first_stop_intersection_x}, {first_stop_intersection_y})"
    )

    if first_stop_intersection_x is not None:
        compare_R0_to_best_exact(first_stop_intersection_x)
        compare_R0_to_best_exact(first_stop_intersection_x - 1)
        compare_R0_to_best_exact(first_stop_intersection_x + 1)

    first_ineq_x = None

    for blue_units in range(0, N*N + 1):
        if (blue_units - (N*N)//2) >= floor(blue_units / ((N//2) + 1)):
            first_ineq_x = blue_units
            break

    print(f"First integer satisfying inequality: {first_ineq_x}")

    first_strict_ineq_x = None

    for blue_units in range(0, N*N + 1):
        if (blue_units - (N*N)//2) > floor(blue_units / ((N//2) + 1)):
            first_strict_ineq_x = blue_units
            break

    first_lower_bound_x = None
    n = N // 2
    denom = floor((n - 1) / 2)

    if denom == 0:
        raise ValueError("Denominator floor((n - 1) / 2) is 0.")

    for blue_units in range((N*N)//2, N*N + 1):
        lhs = blue_units - (N*N)/2
        rhs = (N*N - blue_units - n + 1) / denom

        if lhs >= rhs:
            first_lower_bound_x = blue_units
            break

    print(f"First t satisfying lower-bound condition: {first_lower_bound_x}")

    plt.figure(figsize=(10, 7))
    plt.plot(list(range((N*N//2), N*N - (N//2) + 1)), [i - (N*N//2) for i in list(range((N*N//2), N*N - (N//2) + 1))], alpha=0.8, color="#C9DC87",linewidth=5,label="Smallest number of blue-blue dominos possible")
    plt.plot(x_values_wins, y_values_wins,marker='o',linestyle='None',markersize=5,color="#BB3385",label="Number of blue-blue dominos in best composition",alpha=0.8)
    # plt.plot(x_values_ties, y_values_ties,marker='o',linestyle='None',markersize=5,color="#7B68EE",label="Number of blue-blue dominos in best composition",alpha=0.8)
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
    # if first_ineq_x is not None:
    #     plt.axvline(
    #         x=first_ineq_x,
    #         color="blue",
    #         linewidth=2,
    #         alpha=0.5,
    #         label=f"First integer satisfying inequality: x={first_ineq_x}"
    #     )

    #     plt.text(
    #         first_ineq_x,
    #         plt.ylim()[1] * 0.85,
    #         f"x = {first_ineq_x}",
    #         fontsize=14,
    #         color="blue",
    #         ha="center",
    #         va="bottom"
    #     )
    if first_strict_ineq_x is not None:
        plt.axvline(
            x=first_strict_ineq_x,
            color="red",
            linestyle="--",
            alpha=0.5,
            linewidth=2,
            label=f"First strict inequality: x={first_strict_ineq_x}"
        )

        plt.text(
            first_strict_ineq_x,
            plt.ylim()[1] * 0.75,
            f"x = {first_strict_ineq_x}",
            fontsize=14,
            color="red",
            ha="center",
            va="bottom"
        )
    if first_stop_intersection_x is not None:
        plt.axvline(
            x=first_stop_intersection_x,
            color="green",
            linestyle=":",
            linewidth=3,
            alpha=0.8,
            label=f"Green stops intersecting purple: x={first_stop_intersection_x}"
        )

        plt.text(
            first_stop_intersection_x,
            first_stop_intersection_y,
            f"({first_stop_intersection_x}, {first_stop_intersection_y})",
            fontsize=14,
            color="green",
            ha="left",
            va="bottom"
        )

    # x_br0 = [0, (N*N)//2]
    # y_br0 = [0, (N*N)//4]

    # plt.plot(
    #     x_br0,
    #     y_br0,
    #     color="black",
    #     linestyle="--",
    #     linewidth=2,
    #     alpha=0.8,
    # )
    x_test = np.linspace(0, (N*N)//2, 1000)
    y_test = (5/11) * x_test

    # plt.plot(
    #     x_test,
    #     y_test,
    #     color="black",
    #     linestyle="--",
    #     linewidth=2,
    #     alpha=0.8,
    #     label=r"$BB=\frac{5}{11}t$"
    # )

    if first_lower_bound_x is not None:
        plt.axvline(
            x=first_lower_bound_x,
            color="orange",
            linestyle="-.",
            linewidth=3,
            alpha=0.8,
            label=(
                r"First $t$ satisfying "
                r"$(t-\frac{N^2}{2}) \geq "
                r"\frac{N^2-t-n+1}{\lfloor (n-1)/2 \rfloor}$"
                rf": $t={first_lower_bound_x}$"
            )
        )

        plt.text(
            first_lower_bound_x,
            plt.ylim()[1] * 0.65,
            f"x = {first_lower_bound_x}",
            fontsize=14,
            color="orange",
            ha="center",
            va="bottom"
        )

    plt.axvline(
        x=(N*N)//2,
        color="black",
        linewidth=3,
        alpha=0.8
        )

    # plt.text(
    #     (N*N)//2,
    #     plt.ylim()[1] * 0.65,
    #     f"x = (N^2)/2",
    #     fontsize=14,
    #     color="black",
    #     ha="center",
    #     va="bottom"
    # )

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend([handles[1], handles[0]], [labels[1], labels[0]], fontsize=14)
    # plt.title(f"N = {N}, {N*N} units into districts of size {N}", fontsize=18)
    # plt.xlabel("Number of blue units", fontsize=16)
    # plt.ylabel("Number of blue-blue pairs in best composition (GN)", fontsize=16)
    plt.savefig(f"{CURRENT_WORKING_DIRECTORY}/theoretical_grid_files/MEETING_best_GN_comps_wins_N_{N}.png",bbox_inches="tight",dpi=600)


make_GN_best_image()