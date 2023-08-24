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
print("homing")
StepModule.homing()
StepModule.step(0, 25)
# while True:
#     try:
#         StepModule.step_loop()
    
#     except StepModule.StepperError as e:
#         print(f"Stepper Error: {e}")
#         StepModule.step(1, 20)
#         print("recallibrating")
#         StepModule.homing()

#     except KeyboardInterrupt:
#         print('Stopping.')
#         break
