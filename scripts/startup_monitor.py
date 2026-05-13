import rclpy
import time
from rclpy.node import Node
from sensor_msgs.msg import JointState

class StartupMonitor(Node):
    def __init__(self):
        super().__init__('startup_monitor')
        # Node başlatıldığı an kronometreyi başlat!
        self.start_time = time.time()
        self.get_logger().info('Kronometre basladi. Ilk paket bekleniyor...')
        
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        # İlk paketi gördüğümüz an kronometreyi durdur!
        elapsed_time = time.time() - self.start_time
        print(f"\n✅ BAGLANTI KURULDU! (Handshake & Keşif Süresi: {elapsed_time:.3f} saniye)\n")
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    node = StartupMonitor()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
