import StepModule
# import threading

# def read_serial_from_module():
#     message = StepModule.read_serial()
#     print("Received from module:", message)
#     if message == "LimitSwitchPressed":
#         raise StepModule.StepperError("Limit switch pressed on Arduino")

# serial_thread = threading.Thread(target=read_serial_from_module)
# serial_thread.start()

StepModule.init_serial()
StepModule.Homing()
StepModule.step(0, 25)
while True:
    try:
        StepModule.stepLoop()
    
    except StepModule.StepperError as e:
        print(f"Stepper Error: {e}")
        StepModule.step(1, 20)
        print("recallibrating")
        StepModule.Homing()

    except KeyboardInterrupt:
        print('Stopping.')
        break
