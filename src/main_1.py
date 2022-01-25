'''
    @file       lab1main.py
    @brief      Main file is designed to give tasks.
    @details    This file does not deal with the hardware directly but 
                assigns task to the task_user.py and task_encoder.py files. 
                Task to individual encoders can be assigned here and parameters
                like period, the rate at which the encoder responds, can
                be controlled here as well.

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: January 10, 2022
'''

import task_encoder, task_user, shares, pyb


def main():
    ''' 
    @brief      The main program
    @details    Tasks for the individual motors, encoders, and the user interface
                is established here, as well as the data that these tasks 
                collectively share.
    ''' 
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_1 =  shares.Share(0)
    delta_pos_1 =shares.Share(0)
    enc_zero_1 = shares.Share(False)
    enc_duty_1=  shares.Share(0)
    
    #Shares for Motor 1: position, delta, zero, and duty
    enc_pos_2 = shares.Share(0)
    delta_pos_2 = shares.Share(0)
    enc_zero_2 = shares.Share(False)
    enc_duty_2=shares.Share(0)
    
    ## @brief   A variable enable that is true whenever there is not a fault.
    ## @details This variable is written in task_user.py and is set to True
    ##          if the 'c' key is pressed to reset the fault condition.
    enable = shares.Share()
    
    ## @brief   A variable fault_found that triggers during a fault.
    ## @details This variable is written in DRV8847.py and is set to True
    ##          if a fault is detected.
    
    
    fault_found = shares.Share(False)

#     motor_drv = DRV8847.DRV8847(pyb.Pin.cpu.A15, pyb.Pin.cpu.B2, fault_found)
#     motor_drv.enable()  # Enable the motor driver
#     
#     motor_1 = motor_drv.motor(1,2, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5,3) #Motor Object 1
#     motor_2 = motor_drv.motor(3,4, pyb.Pin.cpu.B0, pyb.Pin.cpu.B1,3) #Motor object 2

    task1 = task_user.Task_User(100000,enc_pos_1,enc_pos_2, delta_pos_1,delta_pos_2, enc_zero_1, enc_zero_2,enc_duty_1, enc_duty_2,enable, fault_found)
    task2 = task_encoder.Task_Encoder(65535,4,enc_pos_1, delta_pos_1,enc_zero_1, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)
    #task3 = task_encoder.Task_Encoder(65535,8,enc_pos_2, delta_pos_2,enc_zero_2, pyb.Pin.cpu.C6, pyb.Pin.cpu.C7)
    #task4 = task_motor.Task_Motor(motor_1,motor_drv,enable)
    #task5 = task_motor.Task_Motor(motor_2,motor_drv,enable)
    
    while(True):

        task1.run()
        task2.run()
        #task3.run()
        #task4.run(float(enc_duty_1.read()))
        #task5.run(float(enc_duty_2.read()))
        
if __name__ == '__main__':
    main()