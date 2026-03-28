#!/bin/bash
# A9 Projesi - Starter Kit Otomatik Baslatici
source /opt/ros/humble/setup.bash
source ~/a9_ws/install/setup.bash

echo "Gazebo ve UR5e yukleniyor..."
ros2 launch ur_simulation_gazebo ur_sim_control.launch.py ur_type:=ur5e &

sleep 10 # Gazebo'nun tamamen acilmasi icin bekleme suresi

echo "MoveIt2 ve RViz aciliyor..."
ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5e launch_rviz:=true use_sim_time:=true
