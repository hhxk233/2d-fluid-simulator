import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pydmd import DMD
import argparse

def analyze_and_plot(dataset_folder, output_folder, field_name='v_mag', svd_rank=10):
    """
    Performs DMD analysis on the specified field from the dataset and saves plots.

    Args:
        dataset_folder (str): Path to the folder containing .npz files.
        output_folder (str): Path to the folder to save output plots.
        field_name (str): The field to analyze. Options: 'v_mag', 'vx', 'vy', 'p', 'dye'.
        svd_rank (int): The rank for SVD truncation in DMD.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Get sorted list of .npz files
    npz_files = sorted(glob.glob(os.path.join(dataset_folder, "*.npz")))
    if not npz_files:
        print(f"No .npz files found in {dataset_folder}")
        return

    snapshots = []
    snapshot_shape = None

    print(f"Loading data from {dataset_folder}...")
    for npz_file in npz_files:
        data = np.load(npz_file)
        
        if field_name == 'v_mag':
            vx, vy = data["v"][:,:,0], data["v"][:,:,1]
            snapshot = np.sqrt(vx**2 + vy**2)
        elif field_name == 'vx':
            snapshot = data["v"][:,:,0]
        elif field_name == 'vy':
            snapshot = data["v"][:,:,1]
        elif field_name == 'p':
            snapshot = data["p"]
        elif field_name == 'dye' and 'dye' in data:
            snapshot = data['dye']
        elif field_name == 'dye' and 'dye' not in data:
            print("Dye field not found in data. Skipping.")
            return
        else:
            raise ValueError(f"Unknown field name: {field_name}")

        if snapshot_shape is None:
            snapshot_shape = snapshot.shape

        snapshots.append(snapshot.flatten())

    if not snapshots:
        print("No snapshots were loaded.")
        return
        
    snapshots_matrix = np.array(snapshots).T
    print(f"Snapshots matrix shape: {snapshots_matrix.shape}")

    # Perform DMD
    dmd = DMD(svd_rank=svd_rank)
    dmd.fit(snapshots_matrix)

    # --- Plotting ---
    analysis_output_folder = os.path.join(output_folder, f"dmd_analysis_{field_name}")
    os.makedirs(analysis_output_folder, exist_ok=True)
    
    # Plot eigenvalues
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(dmd.eigs.real, dmd.eigs.imag)
    # unit circle
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(t), np.sin(t), 'r-')
    ax.set_aspect('equal')
    ax.set_title('DMD Eigenvalues')
    fig.savefig(os.path.join(analysis_output_folder, 'eigenvalues.png'))
    plt.close(fig)

    # Plot modes
    for i, mode in enumerate(dmd.modes.T):
        fig, ax = plt.subplots()
        im = ax.imshow(np.rot90(mode.reshape(snapshot_shape).real), cmap='viridis')
        ax.set_title(f'DMD Mode {i}')
        fig.colorbar(im, ax=ax)
        ax.axis('off')
        fig.savefig(os.path.join(analysis_output_folder, f'mode_{i}.png'))
        plt.close(fig)

    # Plot dynamics
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, dynamic in enumerate(dmd.dynamics):
        ax.plot(dynamic.real, label=f'Mode {i}')
    ax.set_title('DMD Mode Dynamics')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Amplitude')
    ax.legend()
    fig.savefig(os.path.join(analysis_output_folder, 'dynamics.png'))
    plt.close(fig)
    
    print(f"DMD analysis plots for '{field_name}' saved in {analysis_output_folder}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PyDMD Analysis on fluid simulation data.")
    parser.add_argument("--dataset_folder", type=str, required=True, help="Folder with .npz data files.")
    parser.add_argument("--output_folder", type=str, default="dmd_results", help="Folder to save analysis results.")
    parser.add_argument("--field", type=str, default="v_mag", help="Field to analyze ('v_mag', 'vx', 'vy', 'p', 'dye').")
    parser.add_argument("--svd_rank", type=int, default=10, help="SVD rank for DMD (0 for full rank).")
    
    args = parser.parse_args()

    analyze_and_plot(args.dataset_folder, args.output_folder, args.field, args.svd_rank) 