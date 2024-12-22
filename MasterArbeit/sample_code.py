import os
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt


# Dimension reduction and clustering libraries
import umap

import sklearn.cluster as cluster
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import tsfel
from tqdm import tqdm
import umap
import seaborn as sns
import sklearn.cluster as cluster


MBN_SAMPL_FREQ = 4_000_000.0


def get_measurement_number(file_name):
    print("pattern match")
    pattern = r"(?P<meas_idx>.*?)_sliced"
    measurement_idx = re.search(pattern, file_name)
    if measurement_idx is not None:
        measurement_idx = measurement_idx.group("meas_idx")
        print("measurement_idx:", measurement_idx)
        return measurement_idx
    else:
        print(f"Failed to match pattern in filename: {file_name}")
        return None

def load_mbn_file(file_path, nrows=30_000):
    print("load files")
    df_signal = pd.read_csv(
        file_path,
        # sep=";",
        decimal=",",
        names=["time", "mbn"],
        skiprows=1,
        nrows=nrows
    )
    return df_signal
def extract_features(df_signal):
    print("extract features")
    cfg_file = tsfel.get_features_by_domain()
    features = tsfel.time_series_features_extractor(
        cfg_file, df_signal, fs=MBN_SAMPL_FREQ)
    return features


def scale_data(df_features_all):
    print("scale_data")
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(df_features_all)
    df_features_scaled = pd.DataFrame(
        features_scaled,
        index=df_features_all.index,
        columns=df_features_all.columns
    )
    return df_features_scaled

#
# def preprocess_data(data_root_dir, features_root_dir, path_final_dataset):
#     # Create empty list and DataFrame variable to store data and measurement
#     # indices
#     indices = []
#     df_features_all = None
#
#     for file_name in tqdm(os.listdir(data_root_dir)):
#         # Get measurement number from file name and store in indices list
#         measurement_idx = get_measurement_number(file_name)
#         indices.append(measurement_idx)
#
#         # Load single Barkhausen measurement
#         file_path = os.path.join(data_root_dir, file_name)
#         df_signal = load_mbn_file(file_path)
#
#         # # # Uncomment to plot Barkhausen signal
#         # df_signal["mbn"].plot()
#         # plt.show()
#
#         # Extract features
#         df_features = extract_features(df_signal["mbn"])
#
#         # Save features
#         path_features = os.path.join(
#             features_root_dir, f"{measurement_idx}.csv")
#         df_features.to_csv(path_features)
#
#         # Aggregate features from different signals to a single table
#         if df_features_all is None:
#             df_features_all = df_features
#         else:
#             df_features_all = pd.concat(
#                 [df_features_all, df_features],
#                 ignore_index=True
#             )
#
#     # Set measurement indices from file names as indices in DataFrame
#     df_features_all.index = indices
#
#     # Scale features
#     df_features_scaled = scale_data(df_features_all)
#     print("sacled df features:", df_features_scaled)
#
#     # Save scaled dataset
#     df_features_scaled.to_csv(path_final_dataset)
#
#     return df_features_scaled


def get_2d_umap_projection(df_features_scaled, n_neighbors=15, min_dist=0.1):
    print("umap projection")
    print("dataset size : ", df_features_scaled.shape)
    reducer = umap.UMAP(n_components=2, n_neighbors=n_neighbors, min_dist=min_dist, metric='correlation')
    features_scaled = df_features_scaled[
        [
            "0_Absolute energy",
    "0_Area under the curve",
#features removed
    "0_Zero crossing rate",
        ]
    ].values
    # np.random.seed(99)

    embedding = reducer.fit_transform(features_scaled)
    df_embedding = pd.DataFrame(
        embedding,
        columns=["Component 1", "Component 2"],
        index=df_features_scaled.index
    )
    print("shape of embedding: ", embedding.shape)

    kmeans_labels = cluster.KMeans(n_clusters=3, n_init=3).fit_predict(features_scaled)
    print("unique labels assigned by k-means : ", np.unique(kmeans_labels))

    custom_colors = {
        0: (0 / 255, 84 / 255, 159 / 255),  # The specific shade of blue you mentioned
        1: (64 / 255, 127 / 255, 183 / 255),  # Just another color as an example
        2: (142 / 255, 186 / 255, 229 / 255),  # Just another color as an example
    }
    colors = [custom_colors[label] for label in kmeans_labels]

    plt.scatter(df_embedding['Component 1'], df_embedding['Component 2'], s=20, color = colors);
    plt.xlabel("Component_1", fontsize=10)
    plt.ylabel("Component_2", fontsize=10)
    plt.title('k-means clustering of mbn data', fontsize=10)

    plt.show()

    return df_embedding


def plot_projection(df_embedding, features_scaled=None):
    print("plot umap")

    # # Create a new variable to hold the mapped batch values as integers
    # batch_numbers = df_features_scaled['batch'].map(
    #     {"b1": 0, "b2": 1, "b3": 2, "b4": 3, "b5": 4, "b6": 5, "b7": 6, "b8": 7, "b9": 8})

    # Create a scatter plot using batch_numbers for color mapping
    scatter = plt.scatter(
        df_embedding['Component 1'],
        df_embedding['Component 2'],
        s=29
        # c=batch_numbers,  # Use batch_numbers for color mapping
        # cmap='Blues',  # Set a colormap
    )

    # Create a colorbar
    # cbar = plt.colorbar(scatter, boundaries=np.arange(11)-0.5)
    # cbar.set_ticks(np.arange(10))

    # Add the batch_numbers as a new column to df_embedding
    # df_embedding['Batch_Numbers'] = batch_numbers.values

    # Get the colors from the scatter plot and add them as a new column to df_embedding
    # colors = scatter.to_rgba(batch_numbers)
    # df_embedding['Color'] = [','.join(map(str, color)) for color in colors]

    # Save the batch_numbers to a new CSV file
    df_embedding.to_csv('color_labels.csv', index=False)

    plt.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.6)

    plt.gca().set_aspect('equal', 'datalim')
    plt.xlabel("Component 1", fontsize=10)
    plt.ylabel("Component 2", fontsize=10)
    plt.title('UMAP projection of mbn data', fontsize=10)
    plt.show()



# Remember to add 'batch' column to df_embedding before calling the function


if __name__ == "__main__":
    ROOT_RAW_DATA = r"Fixed_Length_MMA/"
    ROOT_FEATURES = r"data/processed"
    PATH_SCALED_DATASET = r"data/scaled_mbn_features.csv"

    # print("Starting to load data.")
    # df_features_scaled = preprocess_data(
    #     ROOT_RAW_DATA, ROOT_FEATURES, PATH_SCALED_DATASET)

    # Read scaled features (if already processed)
    df_features_scaled = pd.read_csv(PATH_SCALED_DATASET)
    print(df_features_scaled)

    print("Starting to apply UMAP")
    df_embedding = get_2d_umap_projection(df_features_scaled)

    print("Plotting UMAP results")
    plot_projection(df_embedding)
