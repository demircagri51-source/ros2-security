import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import qos_profile_sensor_data
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import sys

class SROS2LatencyMonitor(Node):
    def __init__(self):
        super().__init__('sros2_latency_monitor')
        self.subscription = self.create_subscription(
            JointState, '/joint_states', self.listener_callback, qos_profile_sensor_data)
        self.latencies = []
        self.max_samples = 100
        self.first_msg = True
        self.get_logger().info('🛡️ [SROS2] Kararli Durum (Steady-State) Olcumu Basladi...')

    def listener_callback(self, msg):
        now = self.get_clock().now()
        msg_time = rclpy.time.Time.from_msg(msg.header.stamp)
        latency_ms = abs((now.nanoseconds - msg_time.nanoseconds) / 1e6)
        
        if self.first_msg:
            print("\n")
            self.get_logger().info(f'⚠️ ILK PAKET BLOKAJI YAKALANDI: {latency_ms:.2f} ms')
            self.first_msg = False
            
        self.latencies.append(latency_ms)
        sys.stdout.write(f"\r[Veri Toplaniyor... {len(self.latencies)}/{self.max_samples}] Son Gecikme: {latency_ms:.2f} ms")
        sys.stdout.flush()
        
        if len(self.latencies) == self.max_samples:
            print("\n")
            self.analyze_and_plot()
            raise SystemExit

    def analyze_and_plot(self):
        data = np.array(self.latencies)
        initial_block_ms = data[0]
        steady_data = data[1:] 
        
        mean = np.mean(steady_data)
        median = np.median(steady_data)
        std_dev = np.std(steady_data)
        std_err = stats.sem(steady_data) if np.std(steady_data) > 0 else 0.0001
        ci = stats.t.interval(0.95, df=len(steady_data)-1, loc=mean, scale=std_err)
        
        print("\n📊 --- SROS2 STEADY-STATE (KARARLI DURUM) METRIKLERI ---")
        print(f"Ilk Paket Blokaji   : {initial_block_ms:.2f} ms")
        print(f"Ortalama (Mean)     : {mean:.3f} ms")
        print(f"Medyan (Median)     : {median:.3f} ms")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        ax1.plot(range(2, len(data)+1), steady_data, marker='o', linestyle='-', color='crimson', alpha=0.7)
        ax1.axhline(y=mean, color='black', linestyle='--', linewidth=2, label=f'Kararli Ortalama: {mean:.2f} ms')
        ax1.set_title('SROS2 Kararli Durum (Steady-State) Zaman Serisi', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Paket Numarasi')
        ax1.set_ylabel('Gecikme Suresi (ms)')
        ax1.legend(loc='upper right')
        ax1.grid(True, linestyle=':')
        
        bbox_props = dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="darkred", lw=1.5)
        ax1.text(0.02, 0.90, f"⚠️ NOT: Ilk pakette SROS2 Enclave \ndogrulamasi nedeniyle {initial_block_ms:.1f} ms\nbaslatma blokajı yasanmistir.", 
                 transform=ax1.transAxes, fontsize=10, verticalalignment='top', bbox=bbox_props)
        
        ax2.hist(steady_data, bins=15, color='coral', edgecolor='black', alpha=0.7)
        ax2.axvline(x=mean, color='black', linestyle='--', linewidth=2, label=f'Ortalama: {mean:.2f} ms')
        ax2.axvline(x=median, color='darkblue', linestyle='-.', linewidth=2, label=f'Medyan: {median:.2f} ms')
        ax2.set_title('SROS2 Gecikme Dagilimi (Histogram)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Gecikme Suresi (ms)')
        ax2.set_ylabel('Frekans')
        ax2.legend(loc='upper right')
        ax2.grid(True, linestyle=':')
        plt.tight_layout()
        
        save_path = os.path.expanduser('~/a9_ws/docs/latency_sros2_plot.png')
        plt.savefig(save_path, dpi=300)
        print(f"📈 SROS2 Savunma Grafigi kaydedildi: {save_path}")

def main(args=None):
    rclpy.init(args=args)
    node = SROS2LatencyMonitor()
    try: rclpy.spin(node)
    except SystemExit: pass
    finally: node.destroy_node(); rclpy.shutdown()

if __name__ == '__main__': main()
