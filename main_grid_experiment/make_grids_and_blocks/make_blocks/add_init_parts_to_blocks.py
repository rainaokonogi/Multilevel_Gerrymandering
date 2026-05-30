from gerrychain import Partition, Graph, updaters
from gerrychain.tree import recursive_tree_part
import random
import os
from networkx.readwrite import json_graph
from pathlib import Path
import json

SCRIPT_FILE_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_FILE_PATH)

random_seed_num = 8749
random.seed(random_seed_num)

def main():
    """
    For each neutral building block graph, finds three initial partitions
    (assignments of blocks to districts).
    Overwrites the block graph with a new graph where these initial partition are saved as
    node attributes "init_part_1", "init_part_2", and "init_part_3".
    """

    neutral_blocks_dir = (
            f"{SCRIPT_DIR}/../syn_files/syn_extra_building_blocks/neutral"
        )

    # file_count = 0

    # # Iterate over neutral building block graphs
    # for json_file in Path(neutral_blocks_dir).rglob("*.json"):
    #     file_count += 1

    #     if file_count % 100 == 0:
    #         print(f"Processed {file_count} files (out of 400)")

    #    level_1 = json_file.parent.name
    for name in [2795, 415, 4191, 4567, 5593, 8217, 841, 9458, 9604, 1596, 165, 2526, 3773, 6083, 6370, 6920, 7266, 8916, 8932, 9082, 9200, 9378, 1157, 1159, 1328, 2245, 3006, 5643, 5687, 6622, 8398, 8480, 8851, 9226, 9281, 9334, 2183, 4564, 4620, 486, 5057, 5458, 6343, 7963, 807, 8302, 9087, 9102, 9305, 2498, 3163, 4167, 4759, 5444, 6525, 7217, 9788, 2692, 5154, 5615, 5809, 6741, 6951, 7327, 812, 952, 9546, 1629, 1697, 2080, 3502, 5137, 6558, 8158, 9025, 9283, 2193, 2619, 3103, 4848, 6433, 666, 8387, 1836, 2242, 2259, 357, 4616, 5826, 8460, 1200, 1669, 1680, 2105, 3697, 5528, 6394, 7165, 8806, 2181, 2885, 3469, 3845, 3951, 4326, 4588, 5315, 6145, 6165, 7382, 1507, 17, 2243, 3221, 3459, 4329, 5040, 6425, 8448, 8677, 4497, 4571, 5242, 58, 7094, 7544, 7785, 9337, 9939, 1395, 1659, 3288, 4714, 5248, 5506, 605, 7091, 7783, 790, 8278, 8306, 1007, 323, 4546, 504, 5577, 6704, 6957, 7607, 7631, 8292, 9900, 9928, 3661, 3991, 434, 5400, 5831, 6219, 676, 6768, 7863, 8971, 8990, 9647, 9983, 2111, 4701, 6425, 7792, 846, 8850, 9555, 1497, 1644, 185, 2193, 3029, 32, 4689, 5327, 7376, 7502, 959, 9687, 1203, 174, 213, 4497, 6067, 6630, 7478, 8142, 3233, 7604, 7932, 8001, 861, 883, 8990, 956, 2604, 2727, 2881, 2928, 316, 4636, 4723, 6373, 8195, 9920, 1640, 2585, 2721, 3364, 3887, 4674, 4691, 5996, 7109, 7914, 8284, 8421, 9161, 118, 2491, 383, 3976, 7081, 7197, 7205, 7573, 7766, 813, 8331, 8962, 9573, 3183, 3356, 3578, 376, 5349, 5966, 6471, 6719, 8154, 9019]:
        file_name = f"{neutral_blocks_dir}/block_size_2/sample_{name}.json"

        graph = Graph.from_json(file_name)

        my_updaters = {
            "population": updaters.Tally("population",alias="population"),
            "R_tally": updaters.Tally("R",alias="R_tally"),
            "D_tally": updaters.Tally("D",alias="D_tally")
            }

        # Find three initial partitions
        for i in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
            n_found = 0
            while n_found < 1:
                try:
                    init_part_i = Partition.from_random_assignment(
                        graph=graph,
                        n_parts=12,
                        pop_col='population',
                        updaters = my_updaters,
                        epsilon = 0.00001,
                        method = recursive_tree_part
                    )
                    n_found += 1
                except Exception:
                    pass
            
            assignment_i = init_part_i.assignment

            for block, district in assignment_i.items():
                graph.nodes[block][f"init_part_{i}"] = district

        # Overwrite file with graph with initial partitions added
        with open(file_name, "w") as f:
            json.dump(json_graph.adjacency_data(graph), f)

main()