# 2D Fluid Simulator

![baundary_condition_2_dye](./images/bc2_res1600_cip_dye.jpg)
![baundary_condition_2_norm](./images/bc2_res1600_cip_norm.jpg)

## Features

- Finite Difference Method (MAC Method)
- Advection Scheme
  - Upwind Differencing
  - Kawamura-Kuwahara
  - CIP (Constrained Interpolation Profile)
- Flow Visualization
  - Norm (Velocity) and Pressure
  - Pressure
  - Vorticity
  - Dye
- Vorticity Confinement
- Customizable Initial Velocity (for boundary condition 1)

## Requirements

- Python 3.11
- Taichi 1.7

GeForce GTX 1080 or higher recommended.

## Usage

- Boundary Condition 1, ReynoldsNumber = 1000, dt = 0.0005, VorticityConfinement is Disable
  ```bash
  python main.py -re 1000 -dt 0.0005 -vc 0.0
  ```
  Press `V` key switches the flow visualization method.
  `dt` is automatically determined even if not specified, but should be small for divergence.

- Boundary Condition 1 with custom initial velocity
  ```bash
  # Default velocity (1.0, 0.0) - flow from left to right
  python main.py -bc 1

  # Custom velocity (e.g., 0.5, 0.2) - flow at an angle
  python main.py -bc 1 -init_v 0.5 0.2

  # Zero velocity
  python main.py -bc 1 -init_v 0 0

  # Example with other parameters
  python main.py -re 1000 -dt 0.0005 -vc 0.0 -bc 1 --save_every 5 --output_path data_bc1 --initial_velocity 1.0 0
  ```
  The initial velocity components are:
  - First value: x-component (horizontal velocity)
  - Second value: y-component (vertical velocity)
  Note: Provide the velocity components as separate numbers without brackets or commas.

- Boundary Condition 2, resolution = 800
  ```bash
  python main.py -bc 2 -res 800
  ```
  Boundary conditions can be specified from 1 to 6
- Boundary Condition 3, ReynoldsNumber = 10^8, resolution = 800, VorticityConfinement = 10
  ```bash
  python main.py -bc 3 -re 100000000 -res 800 -vc 10
  ```
- Help
  ```bash
  python main.py -h
  ```
- for CPU
  ```bash
  python main.py -dt 0.0005 -cpu
  ```

## Screenshots

### Flow Visualization

- Norm and Pressure
  ![norm_and_pressure](./images/bc5_res800_cip_norm.jpg)
- Pressure
  ![pressure](./images/bc5_res800_cip_pressure.jpg)
- Vorticity
  ![vorticity](./images/bc5_res800_cip_vorticity.jpg)
- Dye
  ![dye](./images/bc5_res800_cip_dye.jpg)

### Vorticity Confinement

- Disable
  ![no_vorticity_confinement](./images/bc3_res800_cip_dye_novc.jpg)
- Enable
  ![vorticity_confinement](./images/bc3_res800_cip_dye_vc.jpg)


### Generate image sequence
To generate an image sequence, you can use the generate_graph.py
- example, if the .npz files are in the `output` folder and you want to save images in `image_out_bc1` folder:
  ```bash
  python generate_graph.py --dataset_folder output --output_folder image_out_bc1
  ```

## References

- [移流法](https://pbcglab.jp/cgi-bin/wiki/index.php?%E7%A7%BB%E6%B5%81%E6%B3%95)
- [2 次元 CIP 法による移流項の計算](https://i-ric.org/yasu/nbook2/04_Chapt04.html#cip)
- [GPU Gems Chapter 38. Fast Fluid Dynamics Simulation on the GPU
  ](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu)
- [Ronald Fedkiw, Jos Stam, Henrik Wann Jensen. Visual Simulation of Smoke.](https://web.stanford.edu/class/cs237d/smoke.pdf)
