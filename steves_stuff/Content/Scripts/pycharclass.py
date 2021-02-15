import unreal_engine as ue

import threading
import queue
import zmq
import time
from datetime import datetime
import os.path


import sys
import struct
import io
import socket
import json


ue.log('Hello i am a PyCharClass module')

port = "5555"

current_command = 'XXX'

cmd_body_rotate = 0



char_data = {
  'command': 'RUN',
  'head_roll': 16,
  'head_yaw': 16,
  'head_pitch': 16,
  'body_yaw': 16,
  'play_animation': 'walking',
  'mouth_pos': 16,
  'left_eye_pos': 16,
  'right_eye_pos': 16
  
}



class ZMQ_REQ_Task:

    def __init__(self): 
        self._running = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:%s" % port)
        self.data = None
        
    def terminate(self): 
        self._running = False

    def set_data(self,data):
        self.data = data
          
    def run(self,args):
        global char_data
   
        while self._running:
              self.socket.send('CMD_GET'.encode())
              char_data = json.loads(self.socket.recv())
              time.sleep(.1)            
            
        print('Shut down')
        return


class PyCharClass:

    def __init__(self):
        self.zmq_thread = ''
        self.zmq_req_task = ''
        

    def pre_initialize_components(self):
        ue.log('Begin pre_initialize_components')
        
                
        
    # this is called on game start
    def begin_play(self):
        self.zmq_req_task = ZMQ_REQ_Task() 
        self.zmq_thread = threading.Thread(target = self.zmq_req_task.run, args =(10, ))
        self.zmq_thread.start()
        ue.log('Begin Play on PyCharClass class')

                        
    def end_play(self,blah):
        self.zmq_req_task.terminate()
        self.zmq_thread.join()   
        ue.log('End Play on PyCharClass class')
                
    # this is called at every 'tick'    
    def tick(self, delta_time):
        #pass

        # get current rotation
        rotation = self.uobject.get_actor_rotation()

        #Pitch Yaw Roll
        #rotation.yaw += 10 * delta_time
        rotation.yaw = char_data['head_yaw']

        # set new location
        self.uobject.set_actor_rotation(rotation)

        
    def CurrentCommand(self):
        return char_data['command']

    def BodyRotation(self):
        return float(char_data['body_yaw'])

    def HeadYaw(self):
        return float(char_data['head_yaw'])

    def HeadPitch(self):
        return float(char_data['head_pitch'])

    def HeadRoll(self):
        return float(char_data['head_roll'])

    def MouthPos(self):
        return float(char_data['mouth_pos'])
        


    