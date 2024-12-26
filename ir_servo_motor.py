
import gpiod
import time

# Define the GPIO pins for the IR sensors (Input pins)
INPUT_PIN_1 =1  # GPIO 3
INPUT_PIN_2 = 7 # GPIO 4
INPUT_PIN_3 = 8 # GPIO 5

# Define the GPIO pin for the servo motor (Output pin)
SERVO_PIN = 20


# Constants for pulse width calculation
MIN_PULSE_WIDTH = 0.0006  # Minimum pulse width (0 degrees)
MAX_PULSE_WIDTH = 0.0023  # Maximum pulse width (180 degrees)
FREQUENCY = 50  # Frequency in Hz (typical for servos)

# Initialize the GPIO chip
chip = gpiod.Chip('gpiochip0')

# Configure the input pins for the IR sensors
input_line_1 = chip.get_line(INPUT_PIN_1)
input_line_1.request(consumer='INPUT', type=gpiod.LINE_REQ_DIR_IN)

input_line_2 = chip.get_line(INPUT_PIN_2)
input_line_2.request(consumer='INPUT', type=gpiod.LINE_REQ_DIR_IN)

input_line_3 = chip.get_line(INPUT_PIN_3)
input_line_3.request(consumer='INPUT', type=gpiod.LINE_REQ_DIR_IN)

# Configure the servo pin
servo_line = chip.get_line(SERVO_PIN)
servo_line.request(consumer='Servo', type=gpiod.LINE_REQ_DIR_OUT)

def set_servo_angle(angle):
    # Calculate the pulse width for the given angle
    pulse_width = MIN_PULSE_WIDTH + (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) * (angle + 90) / 180
    period = 1.0 / FREQUENCY
    duty_cycle = pulse_width / period
    
    # Generate the PWM signal
    for _ in range(int(FREQUENCY * 2)):  # Run for 2 seconds (2 * frequency)
        servo_line.set_value(1)
        time.sleep(pulse_width)
        servo_line.set_value(0)
        time.sleep(period - pulse_width)

try:
    while True:
        # Read the values from the input pins (IR sensors)
        val_1 = input_line_1.get_value()
        val_2 = input_line_2.get_value()
        val_3 = input_line_3.get_value()

        # Print the values of all three sensors
        print(f"Sensor 1: {val_1}, Sensor 2: {val_2}, Sensor 3: {val_3}")

        # If any sensor detects something (i.e., any value is 1), open the gate
        if val_1 == 1 or val_2 == 1 or val_3 == 1:
            print("IR Sensor triggered: Opening the gate to 90 degrees.")
            set_servo_angle(90)  # Open the gate to 90 degrees if any sensor is triggered
        else:
            print("No sensor detected: Closing the gate to 0 degrees.")
            set_servo_angle(0)  # Close the gate to 0 degrees if no sensor is triggered

        time.sleep(1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    # Clean up on exit
    input_line_1.release()
    input_line_2.release()
    input_line_3.release()
    servo_line.release()
    chip.close()
