# 🛡️ A9 Project: ROS2 Humble Security Risk Analysis & SROS2 Mitigation

This repository contains the complete security analysis, penetration testing (exploitation), cryptographic mitigation, and performance evaluation for a robotic manipulator (UR5e) running on ROS2 Humble. 

**Author:** Çağrı Demir  
**Advisor:** Dr. Yunus Emre ÇOĞURCU  
**Environment:** Ubuntu 22.04, ROS2 Humble, Gazebo Classic, MoveIt2  

## 🎯 Project Objectives
1. **Vulnerability Discovery:** Prove that default ROS2 DDS traffic is transmitted in plain text.
2. **Exploitation:** Execute a "Rogue Node" attack to achieve Command Injection and cause State Inconsistency.
3. **Mitigation:** Implement SROS2 (DDS-Security) with a "Zero Trust" Enforce strategy.
4. **Performance Evaluation:** Measure the cryptographic overhead (CPU, RAM, Latency) introduced by AES-256-GCM encryption using custom Python monitors.

---

## 📂 Repository Structure
* `/scripts`: Contains the system launch scripts, malicious exploitation bash scripts, and python-based performance measurement tools.
* `/src`: The workspace source code for the UR5e simulation and controllers.
* `/a9_keystore`: Contains the DDS-Security governance, permissions, and cryptographic keys (Enclaves).
* `/docs`: Contains advanced plots and Wireshark traffic analysis captures.

---

## 🛠️ Prerequisites & Installation
Ensure you have ROS2 Humble and the necessary security packages installed:
```bash
sudo apt update
sudo apt install ros-humble-sros2 python3-psutil wireshark -y
```
**Build the Workspace:**
```bash
cd ~/a9_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```
**🔓 Phase 1: Baseline Setup (Vulnerable State)**

To run the simulation in its default, unencrypted state:
```bash
1. Open a terminal and launch the robot simulation:
cd ~/a9_ws
export ROS_SECURITY_ENABLE=false
./scripts/starter_kit_baslat.sh
```
---

## ⚔️ Phase 2: Attack Reproduction (Exploitation)

With the baseline system running, we simulate an "Insider Threat" injecting malicious trajectories directly into the low-level controllers, bypassing the MoveIt2 planner.

1. Open a new terminal and execute the rogue node script:
```bash
cd ~/a9_ws
./scripts/rogue_node_attack.sh
```

**Impact:** The physical robot in Gazebo will flail erratically, while the RViz operator interface will falsely display the robot in a secure home state. This demonstrates critical State Inconsistency and Loss of Control.



**🔐 Phase 3:SROS2-Enabled Defense (Mitigation)**

To neutralize the Rogue Node, we establish a Root Certificate Authority (CA) and distribute Enclaves to enforce a "Zero Trust" architecture.

Close all previous terminals. Open a new terminal and apply the strict security environment variables before launching:
```bash
cd ~/a9_ws
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
export ROS_SECURITY_KEYSTORE=~/a9_ws/a9_keystore
export ROS_SECURITY_ENCLAVE_OVERRIDE=/a9_master_enclave
./scripts/starter_kit_baslat.sh
```
**Verification:** Running the rogue_node_attack.sh in an unauthorized terminal will now fail completely. Wireshark analysis will confirm all traffic payload is now AES-256-GCM encrypted (SEC_BODY).

**📊 Phase 4: Performance Evaluation**

To measure the cryptographic overhead introduced by SROS2, we run custom python monitors.
1. **Baseline Performance (Unencrypted)**

Ensure the system is running in the vulnerable state (ROS_SECURITY_ENABLE=false), then run:
```bash
# Measure Baseline Latency (100 packets):
python3 ~/a9_ws/scripts/latency_monitor.py --ros-args -p use_sim_time:=true

# Measure Baseline CPU & RAM (30 seconds):
python3 ~/a9_ws/scripts/cpu_monitor_baseline.py
```
2. **SROS2 Performance (Encrypted)**

Ensure the system is running in the mitigated state (ROS_SECURITY_ENABLE=true), then run:
```bash
# Measure SROS2 Steady-State Latency & Initialization Blocking:
python3 ~/a9_ws/scripts/latency_monitor_sros2.py --ros-args -p use_sim_time:=true

# Measure SROS2 CPU & RAM:
python3 ~/a9_ws/scripts/cpu_monitor_sros2.py
```
**Conclusion:** The empirical data conclusively proves that while SROS2 enforces strict Zero-Trust initialization (causing an initial packet block), the steady-state performance impact is virtually non-existent. AES-256-GCM provides absolute network confidentiality and access control with a negligible CPU overhead (+1.02%) and RAM increase (+0.44%), proving highly viable for real-time industrial robotics.

| Metric | Baseline (Unencrypted) | SROS2 (Enforced) | Overhead / Impact |
| :--- | :--- | :--- | :--- |
| **Communication Latency** | 50.08 ms | 44.55 ms | Negligible (Lost in natural variance) |
| **Average CPU Load** | 59.75 % | 60.77 % | **+ 1.02 %** |
| **Average RAM Load** | 25.75 % | 26.19 % | **+ 0.44 %** |
| **Connection Startup** | 0.040 Seconds | 0.127 Seconds | **+ 0.087 Seconds** |
