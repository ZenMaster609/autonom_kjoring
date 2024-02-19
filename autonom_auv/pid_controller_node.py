import numpy as np
import time
from scipy.signal import TransferFunction, tf2ss
import numpy as np


class PidControllerNode: 
     def __init__(self,Pre_offset=None,Pre_time=None,Pre_I=None,Pre_D=None):
            self.Pre_offset = Pre_offset
            self.Pre_time = Pre_time
            self.Pre_I = Pre_I
            self.Pre_D = Pre_D
    
     @staticmethod
     def calculate_parameters(Center_X,set_point):
         Offset_x = set_point-Center_X     
         return Offset_x 
    
    
     def PID_controller(self,Offset,P=0,I=0,D=0,scale_devide=1):
          time_now = time.time()
          P = P/scale_devide
          I = I/scale_devide
          D = D/scale_devide
          if self.Pre_time is None:
               Output = P*Offset
               u_I = 0
               u_D = 0
          else:
               u_I=self.Pre_I+I*Offset*(time_now-self.Pre_time)
               u_D = D*(Offset-self.Pre_offset)
               Output = P*Offset+u_I+u_D

          self.Pre_offset = Offset
          self.Pre_time = time_now
          self.Pre_I = u_I
          self.Pre_D = u_D


          return Output


class transfer_funtion_class: 
    def __init__(self,numerator,denominator): 
        self.numerator = numerator
        self.denominator = denominator
        self.A, self.B, self.C, self.D = tf2ss(numerator, denominator)
        self.x = np.zeros((self.A.shape[0],))
        self.pre_time = None


    def impliment_transfer_function(self,input): 
        time_now = time.time()
        t_s = time_now-self.pre_time
        # State update equation: x(k+1) = Ax(k) + Bu(k)      
        self.x = self.A.dot(self.x) * t_s + self.B * input * t_s
        # Output equation: y(k) = Cx(k) + Du(k)
        output = self.C.dot(self.x) + self.D * input

        self.pre_time=time_now
        return output
    