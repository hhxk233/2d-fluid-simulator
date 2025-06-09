import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_folder", type=str, default="dataset")
parser.add_argument("--output_folder",   type=str, default="output")
args = parser.parse_args()

dataset_folder = args.dataset_folder
output_folder  = args.output_folder

# make subfolders
subdirs = ["velocity_x", "velocity_y", "pressure", "dye", "velocity_field"]
for sd in subdirs:
    os.makedirs(os.path.join(output_folder, sd), exist_ok=True)

# process each .npz
for npz_file in glob.glob(os.path.join(dataset_folder, "*.npz")):
    data = np.load(npz_file)
    base = os.path.splitext(os.path.basename(npz_file))[0]   # e.g. "step_003700"

    # X‐component
    fig, ax = plt.subplots()
    im = ax.imshow(np.rot90(data["v"][:,:,0]), cmap="viridis")
    ax.set_title("Velocity Field (X Component)")
    fig.colorbar(im, ax=ax)
    ax.axis("off")
    out = os.path.join(output_folder, "velocity_x", f"{base}_v_x.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)

    # Y‐component
    fig, ax = plt.subplots()
    im = ax.imshow(np.rot90(data["v"][:,:,1]), cmap="viridis")
    ax.set_title("Velocity Field (Y Component)")
    fig.colorbar(im, ax=ax)
    ax.axis("off")
    out = os.path.join(output_folder, "velocity_y", f"{base}_v_y.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)

    # Pressure
    fig, ax = plt.subplots()
    im = ax.imshow(np.rot90(data["p"]), cmap="viridis")
    ax.set_title("Pressure Field")
    fig.colorbar(im, ax=ax)
    ax.axis("off")
    out = os.path.join(output_folder, "pressure", f"{base}_pressure.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)

    # Dye (if present)
    if "dye" in data:
        fig, ax = plt.subplots()
        im = ax.imshow(np.rot90(data["dye"]), cmap="viridis")
        ax.set_title("Dye Field")
        fig.colorbar(im, ax=ax)
        ax.axis("off")
        out = os.path.join(output_folder, "dye", f"{base}_dye.png")
        fig.savefig(out, bbox_inches="tight")
        plt.close(fig)

    # Whole velocity magnitude (optional)
    vx, vy = data["v"][:,:,0], data["v"][:,:,1]
    mag = np.sqrt(vx**2 + vy**2)
    fig, ax = plt.subplots()
    im = ax.imshow(np.rot90(mag), cmap="viridis")
    ax.set_title("Velocity Magnitude")
    fig.colorbar(im, ax=ax)
    ax.axis("off")
    out = os.path.join(output_folder, "velocity_field", f"{base}_velocity_mag.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
