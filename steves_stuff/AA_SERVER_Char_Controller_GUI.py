import tkinter as tk
import io
import threading
import queue
import zmq
import time
import sys
import json

# Global vars
port = "5555"
zmq_thread = ''
zmq_rep_task = ''

w1 = ''
w2 = ''
button = ''

#cmd_foo = 'CMD_BODY_ROTATE 30'
#val = int(cmd_foo.split()[1])
#print(val)
#exit(0)

char_data = {
  'command': 'RUN',
  'head_roll': 16,
  'head_yaw': 16,
  'head_pitch': 16,
  'blink': 10,
  'play_animation': 'walking',
  'mouth_pos': 10,
  'left_eye_pos': 16,
  'right_eye_pos': 16
  
}


#----- Our ZMQ SERVER "REP" Lister Task
class ZMQ_REP_Task:

    
    def __init__(self): 
        self._running = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)
        
    def terminate(self): 
        self._running = False
          
    def run(self,args):
        #This is GLOBAL , outside thread, has to be here
        global char_data
        
        while self._running:
            
            #  Wait for next request from client
            message = self.socket.recv()
            print("RECV CMD: ", message)
            self.socket.send_string(json.dumps(char_data))
            
            
        print('Shut down')
        return

#-------------------------------------------------------------------
def send_quit_cmd():
    global char_data
    char_data['command'] = 'QUIT'

#-------------------------------------------------------------------
def send_value(event):
    global char_data
    char_data['blink'] = 1 / w1.get()
    char_data['head_yaw'] = w2.get()
    char_data['head_pitch'] = w3.get()
    char_data['mouth_pos'] = 1 / w4.get()
    
#-------------------------------------------------------------------
#---- Set up ----------------
gui = tk.Tk()

#set window size
gui.geometry('640x480') 

#orient=tk.HORIZONTAL,
w1 = tk.Scale(gui,
              label='Blink',
              orient=tk.HORIZONTAL,
              from_=1,
              to=10,
              tickinterval=1,
              command=send_value)

w1.set(20)
w1.pack() #anchor=tk.CENTER)


w2 = tk.Scale(gui,
              label='Head Yaw',
              orient=tk.HORIZONTAL,
              from_=-30,
              to=30,
              tickinterval=1,
              command=send_value)
w2.set(20)
w2.pack()

w3 = tk.Scale(gui,
              label='Head Pitch',
              orient=tk.HORIZONTAL,
              from_=-30,
              to=30,
              tickinterval=1,
              command=send_value)

w3.set(20)
w3.pack()

w4 = tk.Scale(gui,
              label='Mouth Position',
              orient=tk.HORIZONTAL,
              from_=1,
              to=10,
              tickinterval=1,
              command=send_value)
w4.set(20)
w4.pack()




button = tk.Button(gui, text='Quit Cmd', command=send_quit_cmd).pack()


#--------------------------------------------------------------
print('Server Listening')

zmq_rep_task = ZMQ_REP_Task() 
zmq_thread = threading.Thread(target = zmq_rep_task.run, args =(10, ))
zmq_thread.start()

tk.mainloop()



