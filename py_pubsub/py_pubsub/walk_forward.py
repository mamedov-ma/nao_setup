
import rclpy
from rclpy.logging import LoggingSeverity
from rclpy.node import Node
import time
import numpy as np
from std_msgs.msg import String
from nao_sensor_msgs.msg import Touch
from std_msgs.msg import ColorRGBA
from nao_command_msgs.msg import ChestLed
from nao_command_msgs.msg import JointStiffnesses
from nao_command_msgs.msg import JointPositions



class MyNode(Node):
    def __init__(self):
        super().__init__('walk_forward')
        self.count = 0
        self.subscription = self.create_subscription(Touch, 'sensors/touch', self.listener_callback, 10)
        self.publisher_chest_led = self.create_publisher(ChestLed, 'effectors/chest_led', 10)
        self.publisher_jointstiffnesses = self.create_publisher(JointStiffnesses, 'effectors/joint_stiffnesses', 10)
        self.publisher_jointpositions = self.create_publisher(JointStiffnesses, 'effectors/joint_positions', 10)
        self.poses = np.load(r'poses.npy')

    def listener_callback(self, msg):
        '''
        if (str(input()) = 'go'):
            walk_act == 1
        if (str(input()) = 'stop'):    
            walk_act == 0 
        if (walk_act == 1):  
        '''
        if msg.head_middle:
            chestled_color = ChestLed()
            chestled_color.color.r = 1.0 if self.count % 3 == 0 else 0.0
            chestled_color.color.g = 1.0 if self.count % 3 == 1 else 0.0
            chestled_color.color.b = 1.0 if self.count % 3 == 2 else 0.0
            self.publisher_chest_led.publish(chestled_color)       
            one_poses_cicle(self)
            #self.count = (self.count + 1) % (self.poses.shape[0] - 1)
            
     def one_poses_cicle(self):
        for position in self.poses:
            positions_msg = JointPositions()
            positions_msg.indexes = range(25)
            positions_msg.positions = list(map(np.deg2rad, position)
            print('send:', positions_msg)
            self.publisher_jointpositions.publish(positions_msg)
            time.sleep(0.02)

                                           
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

