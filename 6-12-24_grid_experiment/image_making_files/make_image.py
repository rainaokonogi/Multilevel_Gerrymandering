import numpy as np
import matplotlib.pyplot as plt
import json
from collections import Counter
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.legend_handler import HandlerBase
import seaborn as sns
import os


for map_type in ["med"]:
    for num_r_units in ["18", "21"]:
        for map_number in ["1"]:

            print(map_type + num_r_units + map_number)

            colors = ["#C777DB", "#76C0D8", "#FFC787"]

            one_data = np.load(f"/share/duchin/raina/6-12-24_grid_exp/6_results_updaters/NN_hists/{map_type}_BR_r_units_{num_r_units}_map_{map_number}__block_size_1.jsonl_histogram.npy", allow_pickle=True)
            two_data = np.load(f"/share/duchin/raina/6-12-24_grid_exp/6_results_updaters/NN_hists/{map_type}_BR_r_units_{num_r_units}_map_{map_number}__block_size_2.jsonl_histogram.npy", allow_pickle=True)
            four_data = np.load(f"/share/duchin/raina/6-12-24_grid_exp/6_results_updaters/NN_hists/{map_type}_BR_r_units_{num_r_units}_map_{map_number}__block_size_3.jsonl_histogram.npy", allow_pickle=True)

            N = len(one_data)
            x = np.linspace(0, 6, N)

            print(one_data)
            print(two_data)
            print(four_data)

            # fig, ax = plt.subplots(figsize=(6, 4))

            # plt.bar(x, one_data, align='edge', width=0.5, alpha=0.5, label="1", color=colors[0])
            # plt.bar(x, two_data, align='edge', width=0.5, alpha=0.5, label="2", color=colors[1])
            # plt.bar(x, four_data, align='edge', width=0.5, alpha=0.5, label="3", color=colors[2])

            # ax.set_xlim(0, 6)
            # ax.set_xticks(np.arange(0, 7, 1))
            # to_save = f"/share/duchin/raina/6-12-24_grid_exp/images/hist_images/6_{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_no_label_combined_NN_NG_combined_size.png"
            # os.makedirs(os.path.dirname(to_save), exist_ok=True)
            # fig.savefig(to_save,bbox_inches=None)

            # one_density = one_data / np.sum(one_data)
            # two_density = two_data / np.sum(two_data)
            # four_density = four_data / np.sum(four_data)

            # print(one_density)
            # print(two_density)
            # print(four_density)

            # N = len(one_data)
            # x = np.linspace(0, 6, N)

            rng = np.random.default_rng(seed=35)
            delta = 0.2
            delta_neg = -0.2

            def jitter_x(size):
                return rng.uniform(delta_neg, delta, size=size) * (6 / (N - 1))

            # fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
            fig, ax = plt.subplots(figsize=(6, 4))

            def minmax(data):
                nonzero_indices_in_data = np.nonzero(data)[0]
                return x[nonzero_indices_in_data.min()], x[nonzero_indices_in_data.max()]

            xmin_1, xmax_1 = minmax(one_data)
            xmin_2, xmax_2 = minmax(two_data)
            xmin_4, xmax_4 = minmax(four_data)

            for i, block_size in enumerate([1,2,3]):
                with open(f"/share/duchin/raina/6-12-24_grid_exp/6_results_updaters/NG_maximums/{map_type}_BR_r_units_{num_r_units}_map_{map_number}.jsonl", 'r') as f:
                    for k, line in enumerate(f):
                        data = json.loads(line)
                        if data["block_size"] == f"block_size_{block_size}":
                            counts = Counter(data["max_Seats_won_D_values"])
                            x_vals = np.array(sorted(counts.keys()))
                            sizes = np.array([counts[x] for x in x_vals])
                            expanded = np.repeat(x_vals, sizes)

                            ax.vlines(
                                expanded + jitter_x(len(expanded)),
                                0,
                                1,
                                linewidth=0.2,
                                alpha=0.2,
                                color=colors[i]
                            )

                with open(f"/share/duchin/raina/6-12-24_grid_exp/6_results_updaters/NG_minimums/{map_type}_BR_r_units_{num_r_units}_map_{map_number}.jsonl", 'r') as fi:
                    for j, line in enumerate(fi):
                        data = json.loads(line)
                        if data["block_size"] == f"block_size_{block_size}":
                            counts = Counter(data["min_Seats_won_D_values"])

                            x_vals = np.array(sorted(counts.keys()))
                            sizes = np.array([counts[x] for x in x_vals])
                            expanded = np.repeat(x_vals, sizes)

                            ax.vlines(
                                expanded + jitter_x(len(expanded)),
                                0,
                                1,
                                linewidth=0.2,
                                alpha=0.3,
                                color=colors[i]
                            )

                        if block_size == 1:
                            # plt.bar(x - 0.5, one_data, align='edge', alpha=0.5, label="1", color=colors[0])
                            sns.kdeplot(
                                x=np.linspace(0, 6, len(one_data)),
                                weights=one_data,
                                bw_adjust=0.8,
                                color=colors[0],
                                ax=ax
                            )
                        elif block_size == 2:
                            # plt.bar(x - 0.5, two_data, align='edge', alpha=0.5, label="1", color=colors[1])
                            sns.kdeplot(
                                x=np.linspace(0, 6, len(two_data)),
                                weights=two_data,
                                bw_adjust=0.8,
                                color=colors[1],
                                ax=ax
                            )

                        elif block_size == 3:
                            # plt.bar(x - 0.5, four_data, align='edge', alpha=0.5, label="1", color=colors[2])
                            sns.kdeplot(
                                x=np.linspace(0, 6, len(four_data)),
                                weights=four_data,
                                bw_adjust=0.8,
                                color=colors[2],
                                ax=ax
                            )

                        if num_r_units == "18":
                            ax.vlines(3,0, 1, color='black', linewidth=3)
                        elif num_r_units == "21":
                            ax.vlines(2.46, 0, 1, color='black', linewidth=3)

                    # jitter = jitter_x(10)

                    # def vline_pair(xmin, xmax, color, i, j):
                    #     ax.axvline(xmin + jitter[i], color=color, linewidth=1.5, linestyle='--')
                    #     ax.axvline(xmax + jitter[j], color=color, linewidth=1.5, linestyle='--')

                    # vline_pair(xmin_1, xmax_1, colors[0], 0, 1)
                    # vline_pair(xmin_2, xmax_2, colors[1], 2, 3)
                    # vline_pair(xmin_3, xmax_3, colors[2], 4, 5)
                    # vline_pair(xmin_4, xmax_4, colors[3], 6, 7)
                    # vline_pair(xmin_6, xmax_6, colors[4], 8, 9)

                    # Make legend
                    y = np.exp(-((x - 0.5) ** 2) / 0.02)  # bell-shaped "curve"

                    class BellCurveHandle:
                        def __init__(self, color='black', label='Distribution of \n number of \n blue seats \n across neutral searches'):
                            self.color = color
                            self._label = label

                        def get_label(self):
                            return self._label

                    class HandlerBellCurve(HandlerBase):
                        def create_artists(self, legend, orig_handle,
                                        xdescent, ydescent, width, height,
                                        fontsize, trans):

                            x = np.linspace(0, width, 50)

                            y = height * np.exp(-((x - width/2) ** 2) / (2 * (width/6)**2))

                            line = Line2D(
                                x - xdescent,
                                y - ydescent,
                                color=orig_handle.color,
                                linewidth=2
                            )
                            line.set_transform(trans)
                            return [line]

                    bell = BellCurveHandle(color='black')

                    straight_line_max = Line2D(
                        [0], [0],
                        color='black',
                        linewidth=3,
                        label='Maximum/minimum \n number of blue seats \n from optimized searches'
                    )

                    straight_line_min = Line2D(
                        [0], [0],
                        color='black',
                        linewidth=3,
                        linestyle='--',
                        label='Maximum/minimum \n number of blue seats \n from neutral ensemble'
                    )

                    legend_elements = [
                        Patch(facecolor=colors[0], edgecolor=colors[0], label='Size 1'),
                        Patch(facecolor=colors[1], edgecolor=colors[1], label='Size 2'),
                        Patch(facecolor=colors[2], edgecolor=colors[2], label='Size 3'),
                        # Patch(facecolor=colors[3], edgecolor=colors[3], label='Size 4'),
                        # Patch(facecolor=colors[4], edgecolor=colors[4], label='Size 6'),
                        Patch(facecolor="black", edgecolor="black", label='Blue vote share'),
                        # Patch(facecolor='gray', edgecolor='gray', label='Distribution'),
                        bell,
                        straight_line_min,
                        straight_line_max
                    ]


                ax.set_ylabel("")
                # ax.tick_params(axis='y', labelsize=14)
                ax.set_xlim(0, 6)
                ax.set_xticks(np.arange(0, 7, 1))
                ax.tick_params(axis='x')
                ax.set_ylim(0, 1)
                ax.set_yticks([])
                to_save = f"/share/duchin/raina/6-12-24_grid_exp/images/only_search_maxes_and_mins/by_color/6_{map_type}_BR_score_r_units_{num_r_units}_map_{map_number}_no_label_combined_NN_NG_combined_size_{block_size}.png"
                os.makedirs(os.path.dirname(to_save), exist_ok=True)
                plt.tight_layout()
                fig.savefig(to_save,bbox_inches=None)
                ax.clear()


                                    # ax.legend(handles=legend_elements,handler_map={BellCurveHandle: HandlerBellCurve()},loc='upper left', bbox_to_anchor=(1, 1))
                        # ax.set_xlabel("Number of blue seats \n (12 possible)")
                        # ax.set_ylabel("Count of plans")
                        # if map_type == "low":
                        #     ax.set_title("Comparing performance of different building block sizes to neutral ensemble \n on 12-by-12 grid (low number of blue-red edges)")
                        # elif map_type == "high":
                        #     ax.set_title("Comparing performance of different building block sizes to neutral ensemble \n on 12-by-12 grid (high number of blue-red edges)")
                        # elif map_type == "med":
                        #     ax.set_title("Comparing performance of different building block sizes to neutral ensemble \n on 12-by-12 grid (about half blue-red edges)")