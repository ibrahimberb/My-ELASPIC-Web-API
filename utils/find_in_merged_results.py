import pandas as pd
import glob

MERGED_INTERFACE_DATASETS_PATH = r"../Elaspic_Results/Merged_Results/*"


def get_interface_datasets(folder_path):
    file_paths = [file for file in glob.glob(folder_path) if "Interface" in file]
    return file_paths


def get_available_interface_data(dataset_paths):
    datasets = []
    for dataset_path in dataset_paths:
        print(dataset_path)
        data = pd.read_csv(dataset_path, sep='\t', low_memory=False)
        datasets.append(data)

    concated_data = pd.concat(datasets)

    return concated_data


def get_query_items():
    with open("find_test.txt") as fin:
        lines = [line.strip() for line in fin.readlines()]

    return lines


def query(pair, available_data):
    protein, mutation = pair.split('.')
    # print(f"PROTEIN: {protein} MUTATION: {mutation}")

    query_data = available_data[
        (available_data["UniProt_ID"] == protein) &
        (available_data["Mutation"] == mutation)
    ]

    return query_data


def query_protein(protein, available_data):
    # print(f"PROTEIN: {protein}")

    query_data = available_data[
        (available_data["UniProt_ID"] == protein)
    ]

    return query_data


interface_file_paths = get_interface_datasets(MERGED_INTERFACE_DATASETS_PATH)
available_interface_data = get_available_interface_data(interface_file_paths)

print(available_interface_data.shape)

items = get_query_items()


# print(query("P01112.G12D", available_interface_data)[["UniProt_ID", "Mutation"]])
#
#


print(items)
print(len(items))

# for item in items:
#     print(f"ITEM: {item}")
#     query_data = query(item, available_interface_data)
#     if query_data.empty:
#         print("COULD NOT FIND RESULTS!")
#
#     print("========================================")

print('- - - - - - ')
print(query_protein("P42336", available_interface_data).shape)
print(query_protein("P42336", available_interface_data)[["UniProt_ID", "Mutation"]])
print("duplicated entries: {}".format(
    query_protein("P42336", available_interface_data)[
        query_protein("P42336", available_interface_data).duplicated()
    ].shape
))
