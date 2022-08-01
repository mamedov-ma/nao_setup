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
        self.publisher_jointpositions = self.create_publisher(JointPositions, 'effectors/joint_positions', 10)
        #self.poses = np.load(r'poses.npy')
        self.poses = [[-9, 0, 8, 9, 0, -8], [-9, 0, -1, -40, 30, 8], [9, 0, -8, -9, 0, 8], [-40, 30, 8, -9, 0, -1]]
    '''
    def one_poses_cycle(self, msg):
        for position in self.poses:
            positions_msg = JointPositions()
            positions_msg.indexes = [9, 10, 11, 14, 15, 16]
            positions_msg.positions = list(map(np.deg2rad, position))
            print('send:', positions_msg)
            self.publisher_jointpositions.publish(positions_msg)
            time.sleep(0.08)
    '''
    def listener_callback(self, msg):
        '''
        if (str(input()) = 'go'):
            walk_act == 1
        if (str(input()) = 'stop'):    
            walk_act == 0 
        if (walk_act == 1):  
        '''
       
        if msg.head_middle:
            
            if(self.count == 0):
                joint_msg = JointStiffnesses()
                joint_msg.indexes = range(25)
                joint_msg.stiffnesses = [1.0] * 25
                print(joint_msg)
                self.publisher_jointstiffnesses.publish(joint_msg)
            
            chestled_color = ChestLed()
            chestled_color.color.r = 1.0 if self.count % 3 == 0 else 0.0
            chestled_color.color.g = 1.0 if self.count % 3 == 1 else 0.0
            chestled_color.color.b = 1.0 if self.count % 3 == 2 else 0.0
            self.publisher_chest_led.publish(chestled_color)       
            #one_poses_cycle(self, msg)
            for position in self.poses:
                positions_msg = JointPositions()
                positions_msg.indexes = [9, 10, 11, 14, 15, 16]
                positions_msg.positions = list(map(np.deg2rad, position))
                print('send:', positions_msg)
                self.publisher_jointpositions.publish(positions_msg)
                time.sleep(0.5)
            #time.sleep(0.08)
            self.count += 1
  
     
    

                                           
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
