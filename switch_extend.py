import RPi.GPIO as GPIO
import time
import uinput
import os

GPIO.setmode(GPIO.BCM)
#activate the pins ready for button inputs
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#set keyboard mapping
device = uinput.Device([
    uinput.KEY_P,
    uinput.KEY_N,
	uinput.KEY_F5,
	uinput.KEY_M,
	uinput.KEY_A,
    uinput.KEY_W
        ])

view = 'w'

while True:
    input_state_multi = GPIO.input(12)
    input_state_back = GPIO.input(19)
    input_state_forward = GPIO.input(26)
    input_state_week = GPIO.input(16)
    input_state_month = GPIO.input(20)
    input_state_agenda = GPIO.input(21)

#'action buttons'
# map input/gpio variables to uinput keys to control the calendar dates visible based on the display mode (week/month/agenda) 
    ##Go to the previous time period in the calendar
    if input_state_back == False:
        print('Previous')
        device.emit_click(uinput.KEY_P)
        time.sleep(0.5)
    ##Go to the next time period in the calendar    
    if input_state_forward == False:
        print('Next')
        device.emit_click(uinput.KEY_N)
        time.sleep(0.5)    
    ##Go to the week view in the calendar    
    if input_state_week == False:
        print('Week View')
        device.emit_click(uinput.KEY_W)
        time.sleep(0.5)
    ##Go to the month view in the calendar    
    if input_state_month == False:
        print('Month View')
        device.emit_click(uinput.KEY_M)
        time.sleep(0.5)
    ##Go to the agenda view in the calendar    
    if input_state_agenda == False:
        print('Agenda View')
        device.emit_click(uinput.KEY_A)
        time.sleep(0.5)

#refresh the page if all 'action buttons' are pressed        
    if input_state_agenda == False and input_state_back == False and input_state_forward == False:
        	print('Refresh Page')
            device.emit_click(uinput.KEY_F5)

#set power button and restart PI 'multi button'   
    if input_state_multi == False:
	start = time.time()
	time.sleep(0.01)
	while input_state_multi == False:
		time.sleep(0.01)
		print('Multibutton is pressed')
		end = time.time()
		multi_press_time = end-start
		input_state_multi = GPIO.input(12)

		if input_state_multi ==  True or multi_press_time > 5.5:
			print('Button press in', multi_press_time)
			break

	if multi_press_time < 5:
        print('Restarting the Calendar')
        os.system('sudo reboot')
		time.sleep(0.5)
	else:
		print('Powerering Off')
		os.system("sudo shutdown -h now")
		time.sleep(0.5)
