
import gpiod
import time

# Define the GPIO pin for the LED
RED_LED_PIN = 14  # This is the GPIO number, not the physical pin number
GREEN_LED_PIN = 15
BLUE_LED_PIN = 18

# Initialize the GPIO
chip = gpiod.Chip('gpiochip4')  # 'gpiochip0' is typically the correct chip for the main GPIOs

red_line = chip.get_line(RED_LED_PIN)
red_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

green_line = chip.get_line(GREEN_LED_PIN)
green_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

blue_line = chip.get_line(BLUE_LED_PIN)
blue_line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        # Turn the LED on
        print("Turning LED on")
        red_line.set_value(1)
        time.sleep(1)  # Wait for 1 second

        # Turn the LED off
        print("Turning LED off")
        red_line.set_value(0)
        time.sleep(1)  # Wait for 1 second

        print("Turning LED on")
        blue_line.set_value(1)
        time.sleep(1)  # Wait for 1 second

        # Turn the LED off
        print("Turning LED off")
        blue_line.set_value(0)
        time.sleep(1)  # Wait for 1 second

        print("Turning LED on")
        green_line.set_value(1)
        time.sleep(1)  # Wait for 1 second

        # Turn the LED off
        print("Turning LED off")
        green_line.set_value(0)
        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    # Clean up when the user interrupts the script
    red_line.release()
    blue_line.release()
    green_line.release()
    chip.close()
