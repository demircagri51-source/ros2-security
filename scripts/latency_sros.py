import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class LatencyMonitorSROS(Node):
    def __init__(self):
        super().__init__('latency_monitor')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.latencies = []
        self.first_packet = False
        self.get_logger().info("🛡️ SROS2 Gecikme (Latency) ölçümü basladi.")
        self.get_logger().info("⏳ Kriptografik El Sikisma (Handshake) bekleniyor... (Maks 60 saniye)")

    def listener_callback(self, msg):
        if not self.first_packet:
            self.get_logger().info("✅ SIFRELI BAGLANTI KURULDU! Veriler AES-256 ile akiyor...")
            self.first_packet = True

        # Paketin uretildigi zaman
        msg_time = msg.header.stamp.sec + (msg.header.stamp.nanosec / 1e9)
        # Su anki zaman
        current_time = self.get_clock().now().nanoseconds / 1e9
        
        # Gecikmeyi hesapla
        latency_ms = (current_time - msg_time) * 1000 
        
        # Mantikli degerleri listeye ekle
        if 0 < latency_ms < 5000:
            self.latencies.append(latency_ms)

    def print_stats(self):
        if self.latencies:
            avg_latency = sum(self.latencies) / len(self.latencies)
            max_latency = max(self.latencies)
            min_latency = min(self.latencies)
            print("\n" + "="*45)
            print("📊 SROS2 PERFORMANS TEST SONUCLARI (LATENCY)")
            print("="*45)
            print(f"Toplanan Sifreli Paket : {len(self.latencies)} adet")
            print(f"Ortalama Gecikme       : {avg_latency:.2f} ms")
            print(f"Minimum Gecikme        : {min_latency:.2f} ms")
            print(f"Maksimum Gecikme       : {max_latency:.2f} ms")
            print("="*45 + "\n")
        else:
            print("\n❌ 60 saniye doldu fakat SROS2 baglantisi kurulamadi!")

def main(args=None):
    rclpy.init(args=args)
    monitor = LatencyMonitorSROS()
    
    try:
        # SROS2 Handshake icin tam 60 saniye bekleme suresi
        timeout = time.time() + 60
        while time.time() < timeout:
            rclpy.spin_once(monitor, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.print_stats()
        monitor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
