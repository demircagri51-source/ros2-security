
# 🛡️ A9 Project: ROS2 Humble Security Risk Analysis & SROS2 Mitigation

This repository contains the complete security analysis, penetration testing (exploitation), cryptographic mitigation, and performance evaluation for a robotic manipulator (UR5e) running on ROS2 Humble. 

**Author:** Çağrı  
**Advisor:** Dr. Yunus Emre ÇOĞURCU  
**Environment:** Ubuntu 22.04, ROS2 Humble, Gazebo Classic, MoveIt2  

## 🎯 Project Objectives
1. **Vulnerability Discovery:** Prove that default ROS2 DDS traffic is transmitted in plain text.
2. **Exploitation:** Execute a "Rogue Node" attack to achieve Command Injection and cause State Inconsistency.
3. **Mitigation:** Implement SROS2 (DDS-Security) with a "Zero Trust" Enforce strategy.
4. **Performance Evaluation:** Measure the cryptographic overhead (CPU, RAM, Latency) introduced by AES-256-GCM encryption.

---

## 📂 Repository Structure
* `/scripts`: Contains the system launch script, malicious exploitation bash scripts, and python-based performance measurement tools.
* `/src`: The workspace source code for the UR5e simulation and controllers.
* `/rosbags`: Saved trajectory and joint state data from various simulation runs.

---

## 🛠️ Prerequisites & Installation
Ensure you have ROS2 Humble and the necessary security packages installed:
```bash
sudo apt update
sudo apt install ros-humble-sros2 python3-psutil wireshark -y

🔓 Phase 1: Baseline Setup (Vulnerable State)

To run the simulation in its default, unencrypted state:

    Open a terminal and source your workspace.

    Launch the robot simulation:

cd ~/a9_ws
./scripts/starter_kit_baslat.sh
Note: At this stage, capturing the loopback (lo) interface traffic via Wireshark will reveal critical joint telemetry (e.g., shoulder_pan_joint) in pure plaintext.


⚔️ Phase 2: Attack Reproduction (Exploitation)

With the baseline system running, we simulate an "Insider Threat" injecting malicious trajectories directly into the low-level controllers, bypassing the MoveIt2 planner.

    Open a new terminal.

    Execute the rogue node script:

Bash

cd ~/a9_ws
./scripts/rogue_node_attack.sh

Impact: The physical robot in Gazebo will flail erratically, while the RViz operator interface will falsely display the robot in a secure home state. This demonstrates critical State Inconsistency and Loss of Control.
🔐 Phase 3: SROS2-Enabled Defense (Mitigation)

To neutralize the Rogue Node, we establish a Root Certificate Authority (CA) and distribute Enclaves to enforce a "Zero Trust" architecture.

1. Generate Keystore and Enclave:
Bash

cd ~/a9_ws
ros2 security create_keystore a9_keystore
ros2 security create_enclave a9_keystore /a9_master_enclave

2. Launch with Security Enforced:
Close all previous terminals. Open a new terminal and apply the strict security environment variables before launching:
Bash

export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
export ROS_SECURITY_KEYSTORE=~/a9_ws/a9_keystore
export ROS_SECURITY_ENCLAVE_OVERRIDE=/a9_master_enclave

./scripts/starter_kit_baslat.sh

Verification: Running the rogue_node_attack.sh in an unauthorized terminal will now fail completely. The DDS-Security Access Control plugin drops all unauthenticated packets at the network layer. Wireshark analysis will confirm all traffic is now AES-256-GCM encrypted (SEC_BODY).
📊 Phase 4: Performance Evaluation

To measure the cryptographic overhead introduced by SROS2, we run custom python monitors. Ensure the system is running in the SROS2 Enforced Mode (Phase 3), then open a new authorized terminal (apply the same export variables as above) and run the monitors:

Measure Latency & Handshake Overhead:
Bash

cd ~/a9_ws
python3 scripts/latency_sros.py --ros-args -p use_sim_time:=true

Measure CPU & RAM Overhead:
Bash

cd ~/a9_ws
python3 scripts/cpu_monitor.py

📈 Results Summary
Metric	Baseline (Unencrypted)	SROS2 (Enforced)	Overhead / Impact
Communication Latency	5.00 ms	6.00 ms	+ 1.00 ms
Average CPU Load	61.31 %	62.60 %	+ 1.29 %
Average RAM Load	25.72 %	26.02 %	+ 0.30 %
Connection Startup	Instant (0s)	~ 1-2 Seconds	Cryptographic Handshake

Conclusion: The AES-256-GCM encryption provides absolute network confidentiality and access control with a negligible CPU overhead (+1.29%) and latency increase (+1.00 ms), proving highly viable for resource-constrained industrial robotics.
