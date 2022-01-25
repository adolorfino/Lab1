class MotorDriver:
    '''!
    This class will drive a motor from the ME 405 kit.
    '''
    
    def __init__(self, enable_pin, in1pin, in2pin, timer):
        '''!
        Creates a motor driver by initializing GPIO pins and turns the motor off for safety.
        
        @param enable_pin A pyb.Pin object that enables or disables the motor using the PULL_UP mode.
        @param in1pin A pyb.Pin object that defines the pin to control motor channel 1.
        @param in1pin A pyb.Pin object that defines the pin to control motor channel 2.
        @param timer A pyb.Timer object with a set frequency and timer number.
        '''
        print('Initializing motor.')
        self.pin1 = pyb.Pin(in1pin, mode = pyb.Pin.OUT_PP)
        self.pin2 = pyb.Pin(in2pin, mode = pyb.Pin.OUT_PP)
        self.pin_enable = pyb.Pin(enable_pin, pyb.Pin.PULL_UP)
        self.tim = timer
        self.tim_chan1 = self.tim.channel(1, mode = pyb.Timer.PWM, pin = self.pin1)
        self.tim_chan2 = self.tim.channel(2, mode = pyb.Timer.PWM, pin = self.pin2)
        self.pin_enable.high()
        self.tim_chan1.pulse_width_percent(0)
        self.tim_chan2.pulse_width_percent(0)
        
    def set_pwm(self, duty_cycle):
        '''!
        Sets the duty cycle and direction of the motor.
        
        @param duty_cycle A numeric value between -100 and 100 to define the duty cycle of the motor. Positive is clockwise.
        '''
        print('Duty Cycle is set to {:}'.format(duty_cycle))
        if duty_cycle > 100:
            duty_cycle = 100
        elif duty_cycle < -100:
            duty_cycle = -100
            
        if duty_cycle > 0:
            self.tim_chan1.pulse_width_percent(duty_cycle)
            self.tim_chan2.pulse_width_percent(0)
        else:
            self.tim_chan1.pulse_width_percent(0)
            self.tim_chan2.pulse_width_percent(abs(duty_cycle))
            
import pyb      
if __name__ == '__main__':

    pin1 = pyb.Pin.board.PB4
    pin2 = pyb.Pin.board.PB5
    pin_enable = pyb.Pin.board.PA10
    timer = pyb.Timer(3, freq = 20000)
    moe = MotorDriver(pin_enable, pin1, pin2, timer)