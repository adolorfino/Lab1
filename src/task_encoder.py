'''
@file       task_encoder.py
@brief      This file is responsible for the logic and decision making of the encoder.
@details    The main function of this file is to import encoder data collected 
            from the driver encoder.py. Checks if the encoder timer has changed 
            if it has then it updates position, delta, and current time. 
'''

"""

@author: Chloe, Aleya, and Christian
"""

import utime,encoder

class Task_Encoder:
    '''@brief   A standard variable for assigning tasks to encoder. 
       @details Tasked can be assigned from the main script. Position,
       delta, and time can be updated and returned depending on the task assigned. 
    '''
    def __init__ (self,period,timNum, enc_pos, delta_pos, enc_zero, pin1, pin2):
        '''
        @brief  Constructs shared variables 
        @param timNum is the channel number corresponding to the encoder doing the task 
               period controls the frequency at which the encoder returns data 
               enc_pos  Returns the encoder position
               delta_pos returns the delta of the encoder over a period 
               enc_zero  Zeros the encoder postion using a datum value
        '''
        self.enc_pos = enc_pos
        self.delta_pos = delta_pos
        self.enc_zero = enc_zero
        self.period = period
        
        self.next_time = utime.ticks_add(utime.ticks_us(), period)
        self.encode = encoder.Encoder(timNum, pin1, pin2)
        
    def run(self):
        '''
        @brief Runs and called for the defined functions in the encoder. 
        @details Checks if a period has passed, if it has then the encoded is updated 
                if new position, delta, and timer values. 
        Returns
        -------
        None.

        '''
        current_time = utime.ticks_us()
        if (utime.ticks_diff(current_time, self.next_time) >= 0):
            self.encode.update()
            if(self.enc_zero.read() == True):
                self.encode.zero()
                
            self.enc_pos.write(self.encode.get_position())
            self.delta_pos.write(self.encode.get_delta())
            print(self.enc_pos.read())
            self.next_time = utime.ticks_add(self.next_time, self.period)