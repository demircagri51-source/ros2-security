import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class LatencyMonitor(Node):
    def __init__(self):
        super().__init__('latency_monitor')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.latencies = []
        self.get_logger().info("Gecikme (Latency) ölçümü basladi. Lutfen 10-15 saniye bekleyin...")

    def listener_callback(self, msg):
        # Paketin uretildigi zaman
        msg_time = msg.header.stamp.sec + (msg.header.stamp.nanosec / 1e9)
        # Su anki zaman
        current_time = self.get_clock().now().nanoseconds / 1e9
        
        # Gecikmeyi milisaniye (ms) cinsinden hesapla
        latency_ms = (current_time - msg_time) * 1000 
        
        # 0'dan buyuk mantikli degerleri listeye ekle
        if latency_ms > 0 and latency_ms < 1000:
            self.latencies.append(latency_ms)

    def print_stats(self):
        if self.latencies:
            avg_latency = sum(self.latencies) / len(self.latencies)
            max_latency = max(self.latencies)
            min_latency = min(self.latencies)
            print("\n" + "="*40)
            print("📊 PERFORMANS TEST SONUCLARI (LATENCY)")
            print("="*40)
            print(f"Toplanan Veri Paketi: {len(self.latencies)} adet")
            print(f"Ortalama Gecikme  : {avg_latency:.2f} ms")
            print(f"Minimum Gecikme   : {min_latency:.2f} ms")
            print(f"Maksimum Gecikme  : {max_latency:.2f} ms")
            print("="*40 + "\n")
        else:
            print("Yeterli veri toplanamadi!")

def main(args=None):
    rclpy.init(args=args)
    monitor = LatencyMonitor()
    
    try:
        # 30 saniye boyunca veri topla
        timeout = time.time() + 30
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
