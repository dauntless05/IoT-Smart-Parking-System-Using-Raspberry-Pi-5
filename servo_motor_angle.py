
import gpiod
import time

# Define the GPIO pin for the servo
SERVO_PIN = 20  # GPIO number

# Constants for pulse width calculation
MIN_PULSE_WIDTH = 0.0006  # Minimum pulse width (0 degrees)
MAX_PULSE_WIDTH = 0.0023  # Maximum pulse width (180 degrees)
FREQUENCY = 50  # Frequency in Hz (typical for servos)

# Initialize the GPIO
chip = gpiod.Chip('gpiochip0')  # 'gpiochip0' is typically the correct chip for the main GPIOs
line = chip.get_line(SERVO_PIN)
line.request(consumer='servo', type=gpiod.LINE_REQ_DIR_OUT)

def set_servo_angle(angle):
    # Calculate the pulse width for the given angle
    pulse_width = MIN_PULSE_WIDTH + (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) * (angle + 90) / 180
    period = 1.0 / FREQUENCY
    duty_cycle = pulse_width / period

    # Generate the PWM signal
    for _ in range(int(FREQUENCY * 2)):  # Run for 2 seconds (2 * frequency)
        line.set_value(1)
        time.sleep(pulse_width)
        line.set_value(0)
        time.sleep(period - pulse_width)

try:
    while True:
        # Set servo to 90 degrees
        print("Setting angle to 90")
        set_servo_angle(90)
        time.sleep(2)

        # Set servo to 0 degrees
        print("Setting angle to 0")
        set_servo_angle(0)
        time.sleep(2)

        # Set servo to -90 degrees
        print("Setting angle to -90")
        set_servo_angle(-90)
        time.sleep(2)

except KeyboardInterrupt:
    # Clean up when the user interrupts the script
    line.release()
    chip.close()
