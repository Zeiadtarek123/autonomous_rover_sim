# ASU ROAR Autonomous Rover

## Overview
Autonomous rover navigation and control system developed by the ASU ROAR Racing Team. Engineered for the ERC Marsyard environment using ROS 2 Humble and Gazebo Ignition.

## System Architecture
*   **Perception:** ArUco marker detection via OpenCV.
*   **Localization:** Fuzz-IESKF (fusing IMU, wheel odometry, and visual data).
*   **Path Planning:** $A^*$ for Global routing; Artificial Potential Fields (APF) for Local obstacle avoidance.
*   **Control:** Adaptive Pure Pursuit algorithm.
*   **Hardware Communication:** micro-ROS bridge to STM32.
*   **Environmental Hardening:** Configured for ERC Marsyard simulation constraints and terrain dynamics.

## Prerequisites
*   Ubuntu 22.04 LTS
*   ROS 2 Humble
*   Gazebo Ignition
*   OpenCV 4.x
*   micro-ROS agent

## Build Instructions
```bash
# Navigate to workspace
cd ~/roar_ws

# Install dependencies
rosdep install --from-paths src -y --ignore-src

# Build the workspace
colcon build --symlink-install

## Run Instructions
```bash
# Source the workspace
source ~/roar_ws/install/setup.bash

# Launch the ERC Marsyard simulation environment
ros2 launch roar_simulation marsyard_ignition.launch.py

# Launch the autonomy stack
ros2 launch roar_autonomy core_navigation.launch.py

### 3. File Creation and Editing Instructions

**Via Terminal:**
1. Navigate to your local Git repository root.
2. Create the file: `touch README.md`
3. Open with an editor: `nano README.md`
4. Paste the Markdown text above. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
5. Stage, commit, and push the file:
   ```bash
   git add README.md
   git commit -m "docs: add project README.md"
   git push origin main


## 📺 Media & Demonstrations
To view the full-resolution screen recordings of the rover's autonomous missions, including Gazebo simulations and RViz sensor visualizations, visit the project media folder:

[Direct Link to Simulation Recordings](https://drive.google.com/drive/folders/1N9CdFV8Soqyi_3aVkCv9rnb599V9wYIa?usp=sharing)

### Key Visualizations:
* **Autonomous Navigation**: Rover traversing the Marsyard using $A^*$ and APF planners.
* **Perception Pipeline**: Real-time ArUco marker detection and coordinate frame estimation.
* **Sensor Fusion**: RViz visualization of IMU and wheel odometry data streams.
