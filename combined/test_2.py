import StepModule
import threading

def read_serial_from_module():
    while True:
        while True:
            if StepModule.SerialArduino.in_waiting > 0:
                message = StepModule.SerialArduino.readline().decode()
                print(message)
        
serial_thread = threading.Thread(target=read_serial_from_module)
serial_thread.start()

StepModule.init_serial()
# print("test2: homing")
# StepModule.homing()
print("test2: step")
StepModule.step(0, 25)
# while True:
#     try:
#         StepModule.step_loop()
# 
#     except StepModule.StepperError as e:
#         print(f"Stepper Error: {e}")
#         StepModule.step(1, 20)
#         print("recallibrating")
#         StepModule.homing()
# 
    # except KeyboardInterrupt:
        print('Stopping.')
        break
