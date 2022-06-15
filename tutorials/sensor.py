#!/usr/bin/env python
import rospy                     # Import the ROS Python library 
from std_msgs.msg import Bool    # Import Bool message type from standard messages
import brickpi3                  # Import the BrickPi3 drivers

'''A class for handling sensor(s).'''  
class Sensor:
    def __init__(self): # Class constructor

        # Create a publisher 
        self.pub = rospy.Publisher('/touch/reading', Bool, queue_size=10)
        
        # Create BrickPi3 instance  
        self.BP = brickpi3.BrickPi3()
        
        # Configure for a touch sensor on connector S1
        self.BP.set_sensor_type(self.BP.PORT_1, self.BP.SENSOR_TYPE.TOUCH)
         
    # Method for reading and publishing sensor values
    def read(self):
        try:
            value = self.BP.get_sensor(self.BP.PORT_1)
            self.pub.publish(value)
        except brickpi3.SensorError:
            pass
            
    # Method for "unconfigure" all sensors and motors
    def reset(self):
        self.BP.reset_all() 
    
# Main function
if __name__ == '__main__':

    # Init the connection with the ROS system
    rospy.init_node('sensor', anonymous=True)
    
    # Create Sensor instance
    s = Sensor()
    try:
    
        # Start the ROS main loop, running with a frequency of 10Hz
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            s.read()     # Call sensor read method 
            rate.sleep() # Call sleep to maintain the desired rate
            
    except rospy.ROSInterruptException:
        s.reset() # Call sensor reset method
