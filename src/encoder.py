'''
    @file    encoder.py
    @brief   Task for collecting data from the hardware. 
    @details This file interacts directly with the hardware of the Nucleo to
             read motor encoders and return information as called.
            
    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: January 10, 2022
'''
import pyb


class Encoder:
    ''' @brief  Interface with quadrature encoders
        @details Creates a class for the encoder to call encoder position, 
        change in encoder position, and datums the motor. 
        
    '''

    def __init__(self, timNum, pin1, pin2):
        ''' @brief Constructs an encoder object
            @param timNum   Corresponds to the timer channel that the
                            encoder is connected to. 
        '''
        self.datumPosition = 0
        self.old_counter = 0
        self.delta = 0
        self.count = 0
        self.position = 0
        self.cap = 65535
        self.oldDelta = -1
        
        self.tim = pyb.Timer(timNum,prescaler = 0, period = 65535)
        TIM4_CH1 = self.tim.channel(1, mode = pyb.Timer.ENC_A, pin = pin1)
        TIM4_CH2 = self.tim.channel(2, mode = pyb.Timer.ENC_B, pin = pin2)
    
    def read(self):
        '''
            @brief   Gets encoder timer  
            @return  The value of the timer encoder
        '''
        return self.tim.counter()
    
    def zero(self):
        '''
            @brief   Gets encoder timer  
            @return  The value of the timer encoder
        '''
        self.datumPosition = 0
    
    def update(self):
        ''' @brief      Updates encoder position and delta
            @details    Updates the encoder postion,delta, and 
                        handles the enconter over and underflow. 
        '''
        
        self.count = self.read()
        self.delta = self.count - self.old_counter
        self.old_counter = self.count
        if (abs(self.delta) >= self.cap/2):
                if(self.delta >= self.cap/2):
                    self.delta-=self.cap
                else:
                    self.delta+=self.cap
        if(self.delta!=self.oldDelta):
            self.datumPosition+= self.delta
            self.oldDelta = self.delta

    def get_position(self): 
        ''' @brief Returns encoder position
            @details
            @return The position of the encoder shaft
        '''
        
        return self.datumPosition
        
    def set_position(self, position):
        ''' @brief Sets encoder position
            @details
            @param position The new position of the encoder shaft
        '''
        
        self.datumPosition = self.position
    
    def get_delta(self):
        ''' @brief Returns encoder delta
            @details
            @return The change in position of the encoder shaft
            between the two most recent updates
        '''
        return self.delta