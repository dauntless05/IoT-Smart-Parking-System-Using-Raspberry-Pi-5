
import gpiod
import time

# GPIO Configuration for RGB LEDs
SLOT_PINS = {
    "slot_1": {"red": 14, "green": 15, "blue": 18},  # RGB LED for Slot 1
    "slot_2": {"red": 23, "green": 24, "blue": 25},  # RGB LED for Slot 2
    "slot_3": {"red": 2, "green": 3, "blue": 4},    # RGB LED for Slot 3 (updated pins)
}

# Initialize GPIO chip
def initialize_gpio(chip_name='gpiochip0'):
    chip = gpiod.Chip(chip_name)
    lines = {}
    for slot, colors in SLOT_PINS.items():
        lines[slot] = {}
        for color, pin in colors.items():
            line = chip.get_line(pin)
            line.request(consumer=f'{slot}_{color}', type=gpiod.LINE_REQ_DIR_OUT)
            lines[slot][color] = line
    return chip, lines

# Set RGB LED status for a specific slot
def set_slot_status(lines, slot, status):
    """
    Set the status of a parking slot using RGB LEDs.
    Args:
        lines (dict): GPIO lines for all slots.
        slot (str): Slot identifier (e.g., "slot_1").
        status (str): "occupied" (red), "available" (green), or "reserved" (blue).
    """
    # Turn off all colors initially
    for color in ["red", "green", "blue"]:
        lines[slot][color].set_value(0)
    
    # Turn on the color corresponding to the status
    if status == "occupied":
        lines[slot]["red"].set_value(1)
    elif status == "available":
        lines[slot]["green"].set_value(1)
    elif status == "reserved":
        lines[slot]["blue"].set_value(1)
    else:
        print(f"Unknown status '{status}' for {slot}")

# Clean up GPIO lines
def cleanup_gpio(chip, lines):
    for slot, colors in lines.items():
        for line in colors.values():
            line.set_value(0)  # Turn off all LEDs
            line.release()
    chip.close()
