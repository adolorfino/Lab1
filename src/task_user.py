'''
    @file       task_user.py
    @brief      This file is responsible for the user interface of the motor commands.
    @details    Depending on the input of the user the task_user.py will zero the
                motor encoder, print the motor encoder position, print the motor
                encoder delta, collect data for 30 seconds and print as a list,
                and enter duty cycles. This can be done with either Motor 1 or 
                Motor 2 as specified by capital/lowercase letters.
                
    @image html SStask_user.jpg "State Space Diagram:Task Diagram" width=600px
    @image html lab2task.png "Task Diagram" width=600px

    @author: Chloe Chou
    @author: Aleya Dolorfino
    @author: Christian Roberts
    @date: January 10, 2022
'''
import utime,pyb,math

S0_INIT = 0
S1_WAIT_FOR_CHAR = 1
S2_COLLECT_DATA = 2
S3_PRINT_DATA = 3
S4_SET_DUTY = 4
S5_FAULT = 5

class Task_User:
    '''
    @brief
    @details
    '''
    def __init__ (self,period, enc_pos_1,enc_pos_2, delta_pos_1,delta_pos_2, enc_zero_1, enc_zero_2, enc_duty_1, enc_duty_2, enable, fault_found):
        '''
        @brief Initializes and returns a task_user object.
        @param period controls the frequency at which the encoder returns data 
               enc_pos_1    Contains the encoder position of Motor 1
               enc_pos_2    Contains the encoder position of Motor 2
               delta_pos_1  Contains the delta of Motor 1 encoder over a period 
               delta_pos_2  Contains the delta of Motor 2 encoder over a period  
               enc_zero_1   Contains information to zero the postion of Motor 1
               enc_zero_2   Contains information to zero the postion of Motor 3
               enc_duty_1   Contains the duty cycle of Motor 1
               enc_duty_2   Contains the duty cycle of Motor 2
               enable       Contains information to re-enable motors
               fault_found  Contains information if a fault was detected.
        '''
        self.enc_pos_1 = enc_pos_1
        self.delta_pos_1 = delta_pos_1
        self.enc_zero_1 = enc_zero_1
        self.enc_duty_1 = enc_duty_1
        
        
        self.enc_pos_2 = enc_pos_2
        self.delta_pos_2 = delta_pos_2
        self.enc_zero_2 = enc_zero_2
        self.enc_duty_2 = enc_duty_2
        
        
        self.period = period
        self.next_time = utime.ticks_add(utime.ticks_us(), period)
        self.next_time_collect = utime.ticks_add(utime.ticks_us(), period)
        self.state = S0_INIT
        self.interrupt = False
        
        self.my_list_runs = []
        self.my_list_position= []
        self.my_list_velocity = []
        
        self.runs = 1
        self.motor_number = 0
        self.num_st = ""

        self.ser_port = pyb.USB_VCP()
        
        self.enable = enable
        self.enable.write(False)
        
        self.fault_found = fault_found
        
    def run(self):
        '''
        @brief      This function runs different states in the task_user command.
        @details    This function waits for input of the user to call different
                    states of the motor as printed on the screen for the user. 
                    It will leave the user input command phase if collecting 
                    data, printing data, taking data input for duty cycles, or 
                    if a fault is triggered.
        '''
        self.current_time = utime.ticks_us()
        if (utime.ticks_diff(self.current_time, self.next_time) >= 0):
            if self.state == S0_INIT:
                print("__________________________________________________________________________________________")
                print("|Welcome, here are a list of commands for this device.                                    |")
                print("|z-Zero the position of Motor 1                                                           |")
                print("|Z-Zero the position of Motor 2                                                           |")
                print("|p-Print out the position of Motor 1                                                      |")
                print("|P-Print out the position of Motor 2                                                      |")
                print("|d-Print out the delta for Motor 1                                                        |")
                print("|D-Print out the delta for Motor 2                                                        |")
                print("|g-Collect Motor 1 data for 30 seconds and print it to PuTTY as a comma separated list    |")
                print("|G-Collect Motor 2 data for 30 seconds and print it to PuTTY as a comma separated list    |")
                print("|m-Prompt the user to enter a duty cycle for Motor 1                                      |")
                print("|M-Prompt the user to enter a duty cycle for Motor 2                                      |")
                print("|s-End data collection prematurely                                                        |")
                print("|_________________________________________________________________________________________|")
                self.state = S1_WAIT_FOR_CHAR
                
            elif self.state == S1_WAIT_FOR_CHAR:
                
                if(self.enc_zero_1.read() == True):
                    self.enc_zero_1.write(False)
                if(self.enc_zero_2.read() == True):
                    self.enc_zero_2.write(False)
                
                if(self.fault_found.read()):
                        self.state = S5_FAULT
                        
                if(self.ser_port.any()):
                    char_decoded = self.ser_port.read(1).decode()
                    
                    if(char_decoded == 'z'):
                        print ("Zeroing position. Motor 1 is now at 0.")
                        self.enc_zero_1.write(True)
                    
                    elif(char_decoded == 'Z'):
                        print ("Zeroing position. Motor 2 is now at 0.")
                        self.enc_zero_2.write(True)
                        
                    elif(char_decoded == 'p'):
                        print('Motor 1 position is {:}.'.format(self.enc_pos_1.read()))
                    elif(char_decoded == 'P'):
                        print('Motor 2 position is {:}.'.format(self.enc_pos_2.read()))
                         
                    elif(char_decoded == 'd'):
                        print ('Motor 1 delta is {:}.'.format(self.delta_pos_1.read()))
                    elif(char_decoded == 'D'):
                        print ('Motor 2 delta is {:}.'.format(self.delta_pos_2.read()))
                        
                    elif(char_decoded == 'g'):
                        self.state = S2_COLLECT_DATA
                        print("Collecting data for Motor 1.")
                        self.motor_number = 1
                        self.interrupt = False
                        
                    elif(char_decoded == 'G'):
                        self.state = S2_COLLECT_DATA
                        print("Collecting data for Motor 2.")
                        self.motor_number = 2
                        self.interrupt = False
                        
                    elif(char_decoded == 'm'):
                        print("Please enter duty cycle for motor 1:")
                        self.state = S4_SET_DUTY
                        self.motor_number = 1
                        self.num_st = ""
                        
                    elif(char_decoded == 'M'):
                        print("Please enter duty cycle for motor 2:")
                        self.state = S4_SET_DUTY
                        self.motor_number = 2
                        self.num_st = ""
                    
            elif self.state == S2_COLLECT_DATA:
                self.current_time_collect = utime.ticks_us()
                if (utime.ticks_diff(self.current_time_collect, self.next_time_collect) >= 0):
                    if self.motor_number == 1:
                        self.my_list_position.append(self.enc_pos_1.read()*(2*math.pi/4000))
                        self.my_list_velocity.append(self.delta_pos_1.read()*(2*math.pi/4000)*self.period/65535.3)
                        self.my_list_runs.append(self.runs)
                        self.runs = self.runs + 1
                    if self.motor_number == 2:
                        self.my_list_position.append(self.enc_pos_2.read()*(2*math.pi/4000))
                        self.my_list_velocity.append(self.delta_pos_2.read()*(2*math.pi/4000)*self.period/65535.3)
                        self.my_list_runs.append(self.runs)
                        self.runs = self.runs + 1
                    if(self.ser_port.any()): #breaks loop if s input
                        char_in = self.ser_port.read(1)
                        char_decoded = char_in.decode()
                        if(char_decoded == 's' or char_decoded == 'S'):
                            self.interrupt = True
                            print('End data collection.')
                            self.runs = 1
                            self.state = S3_PRINT_DATA
                    if(self.runs >= 65):
                        self.interrupt = True
                        print('End data collection.')
                        self.state = S3_PRINT_DATA
                    self.next_time_collect = utime.ticks_add(self.next_time_collect, 500000)
            
            elif self.state == S3_PRINT_DATA:
                print('Printing data.')
                print('Motor {:} over {:} points:'.format(self.motor_number, len(self.my_list_runs)))
                for x in range(len(self.my_list_position)):
                    print('At point {:} position is {:} radians and velocty is {:} rad/sec'.format(self.my_list_runs[x], self.my_list_position[x], self.my_list_velocity[x] ))
                self.my_list_position.clear()
                self.my_list_velocity.clear()
                self.my_list_runs.clear()
                self.runs = 1
                self.state = S1_WAIT_FOR_CHAR
            
            elif self.state == S4_SET_DUTY:
                if(self.ser_port.any()):
                        char_in = self.ser_port.read(1).decode()
                        
                        if(char_in.isdigit()): # Adds to string only if the number is a digit
                            self.num_st = self.num_st + char_in
                            self.ser_port.write(char_in)
                        
                        elif (char_in == '-'): # Only adds to string if the minus sign is the first character entered
                            if (len(self.num_st)==0):
                                self.num_st = self.num_st + char_in
                                self.ser_port.write(char_in)
                        
                        elif (char_in == '\x7F'): # Backspaces last key and changes num_st appropriately
                            if (len(self.num_st)!=0):
                                self.num_st = self.num_st[:-1]
                                self.ser_port.write(char_in)
                        
                        elif (char_in == '.'): # If the string does not already have a decimal, add one
                            if self.num_st.find(char_in) == -1:
                                self.num_st = self.num_st + char_in
                                self.ser_port.write(char_in)
                        elif (char_in == '\r'or char_in == '\n'): # Submit entered duty
                            if (len(self.num_st)==0):
                                self.num_st = "0.0"
                            print ("")
                            num_doub = float (self.num_st)
                            if self.motor_number == 1:
                                print('Motor 1 will run at {:}'.format(num_doub))
                                self.enc_duty_1.write(self.num_st)
                                self.state = S1_WAIT_FOR_CHAR
                            elif self.motor_number == 2:
                                print('Motor 2 will run at {:}'.format(num_doub))
                                self.enc_duty_2.write(self.num_st)
                                self.state = S1_WAIT_FOR_CHAR
            elif self.state == S5_FAULT:
                self.enc_duty_1.write(0)
                self.enc_duty_2.write(0)
                if(self.ser_port.any()):
                    char_decoded = self.ser_port.read(1).decode()
                    if(char_decoded=='c'or char_decoded=='C'):
                        self.enable.write(True)
                        print("Fault is cleared.")
                        self.state = S1_WAIT_FOR_CHAR
            else:
                raise ValueError('Invalid State') 
            self.next_time = utime.ticks_add(self.next_time, self.period)