
import gpiod
import time

# Define the GPIO pins
INPUT_PIN = 1  # GPIO 3

# Initialize the GPIO chip
chip = gpiod.Chip('gpiochip0')

# Configure the input pin
input_line = chip.get_line(INPUT_PIN)
input_line.request(consumer='INPUT', type=gpiod.LINE_REQ_DIR_IN)

try:
    while True:
        # Read the value from the input pin
        val = input_line.get_value()
        print(val)
        time.sleep(1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    # Clean up on exit
    input_line.release()
    chip.close()
