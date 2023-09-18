import StepModule
import threading

angleNow = 125
prev_angle = 0

StepModule.init_serial()
# def read_serial_from_module():
#     while True:
#         while True:
#             if StepModule.SerialArduino.in_waiting > 0:
#                 message = StepModule.SerialArduino.readline().decode()
#                 print("arduino serial: " + message)
        
# serial_thread = threading.Thread(target=read_serial_from_module)
# serial_thread.start()

StepModule.homing()

while True:
    try:
        angleNow, prev_angle = StepModule.step_loop(resolution="fine", angleNow=angleNow, prev_angle=prev_angle)

    except StepModule.StepperError as e:
        print(f"Stepper Error: {e}")
        StepModule.step(1, 20)
        print("recallibrating")
        StepModule.homing()

    except KeyboardInterrupt:
        print('Stopping.')
        break