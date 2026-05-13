import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import qos_profile_sensor_data
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import sys

class AcademicLatencyMonitor(Node):
    def __init__(self):
        super().__init__('academic_latency_monitor')
        # QoS Profili Eklendi
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            qos_profile_sensor_data)
        
        self.latencies = []
        self.max_samples = 100
        self.first_msg = True
        self.get_logger().info('🔍 [AKADEMIK] Gecikme (Latency) Olcumu Basladi...')

    def listener_callback(self, msg):
        now = self.get_clock().now()
        msg_time = rclpy.time.Time.from_msg(msg.header.stamp)
        
        # Farkı hesapla (Mutlak değer kullanıyoruz)
        latency_ms = abs((now.nanoseconds - msg_time.nanoseconds) / 1e6)
        
        if self.first_msg:
            print("\n")
            self.get_logger().info(f'✅ ILK PAKET YAKALANDI! (Ham Gecikme: {latency_ms:.2f} ms)')
            self.first_msg = False
            
        self.latencies.append(latency_ms)
        sys.stdout.write(f"\r[Veri Toplaniyor... {len(self.latencies)}/{self.max_samples}] Son Gecikme: {latency_ms:.2f} ms")
        sys.stdout.flush()
        
        if len(self.latencies) == self.max_samples:
            print("\n")
            self.get_logger().info('✅ Veri toplama tamamlandi. Gelismis grafikler hazirlaniyor...')
            self.analyze_and_plot()
            raise SystemExit

    def analyze_and_plot(self):
        data = np.array(self.latencies)
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)
        std_err = stats.sem(data) if np.std(data) > 0 else 0.0001
        ci = stats.t.interval(0.95, df=len(data)-1, loc=mean, scale=std_err)
        
        print("\n📊 --- LATENCY (GECIKME) METRIKLERI ---")
        print(f"Olcum Metodu        : Header Timestamp Farki (/joint_states)")
        print(f"Orneklem Sayisi (n) : {len(data)}")
        print(f"Ortalama (Mean)     : {mean:.3f} ms")
        print(f"Medyan (Median)     : {median:.3f} ms")
        print(f"Standart Sapma      : {std_dev:.3f} ms")
        print(f"%95 Guven Araligi   : {ci[0]:.3f} - {ci[1]:.3f} ms\n")
        
        # --- YENİ GELİŞMİŞ GRAFİK ÇİZİMİ ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # 1. Grafik: Zaman Serisi (Her bir paketin gecikmesi)
        ax1.plot(range(1, len(data)+1), data, marker='o', linestyle='-', color='royalblue', alpha=0.7, markersize=4)
        ax1.axhline(y=mean, color='red', linestyle='--', linewidth=2, label=f'Ortalama: {mean:.2f} ms')
        ax1.set_title('Paket Bazli Gecikme Zaman Serisi', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Paket Numarasi (Sira)', fontsize=12)
        ax1.set_ylabel('Gecikme Suresi (ms)', fontsize=12)
        ax1.legend(loc='upper right')
        ax1.grid(True, linestyle=':', alpha=0.8)
        
        # 2. Grafik: Histogram (Dağılım ve Yığılma)
        ax2.hist(data, bins=15, color='lightseagreen', edgecolor='black', alpha=0.7)
        ax2.axvline(x=mean, color='red', linestyle='--', linewidth=2, label=f'Ortalama: {mean:.2f} ms')
        ax2.axvline(x=median, color='darkorange', linestyle='-.', linewidth=2, label=f'Medyan: {median:.2f} ms')
        ax2.set_title('Gecikme Dagilimi (Histogram)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Gecikme Suresi (ms)', fontsize=12)
        ax2.set_ylabel('Frekans (Paket Sayisi)', fontsize=12)
        ax2.legend(loc='upper right')
        ax2.grid(True, linestyle=':', alpha=0.8)
        
        plt.tight_layout()
        
        # Kaydet
        save_path = os.path.expanduser('~/a9_ws/docs/latency_advanced_plot.png')
        plt.savefig(save_path, dpi=300)
        print(f"📈 Akademik Gelismis Grafik basariyla kaydedildi: {save_path}")

def main(args=None):
    rclpy.init(args=args)
    node = AcademicLatencyMonitor()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
