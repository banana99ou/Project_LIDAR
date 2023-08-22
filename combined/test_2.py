import StepModule
import threading

def read_serial_from_module():
    message = StepModule.read_serial()
    print("Received from module:", message)
    if message == "LimitSwitchPressed":
        raise StepModule.StepperError("Limit switch pressed on Arduino")

serial_thread = threading.Thread(target=read_serial_from_module)
serial_thread.start()

StepModule.Homing()
while True:
    try:
        StepModule.StepLoop()
    
    except StepModule.StepperError as e:
        print(f"Stepper Error: {e}")
        StepModule.step(1, 20)
        print("recallibration")
        StepModule.Homing()
        
    except KeyboardInterrupt:
        print('Stopping.')
        break