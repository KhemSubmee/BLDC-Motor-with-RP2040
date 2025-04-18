from time import sleep
from machine import Pin, PWM
from QEnc_Pio_4 import QEnc_Pio_4

# === Setup ===
encoder = QEnc_Pio_4((Pin(0, Pin.IN), Pin(1, Pin.IN)), sm_id=7, freq=100_000_000)
enable_pin = Pin(5, Pin.OUT, value=1)
pins = [PWM(Pin(i, Pin.OUT), freq=20000) for i in range(2, 5)]

MAX_DUTY = 15000
DELAY_TIME = 0.01
Kp = 0.02 #Proportional gain
ENCODER_FULL_ROTATION = 1271  # Encoder counts per 360 degrees
SECTOR_SIZE = 45  # Degrees per commutation sector

desired_position = 790  # Target encoder reading (in counts)

# === Functions ===

def get_sector_and_position(angle_deg):
    sector = int(angle_deg // SECTOR_SIZE) % 8
    pos_in_sector = (angle_deg % SECTOR_SIZE) / SECTOR_SIZE
    return sector, pos_in_sector

def compute_pwm_forward(sector, t, d):
    if sector == 0:
        return (0, 10000, 0)
    elif sector == 1:
        return (0, d, int(d * t))
    elif sector == 2:
        return (0, int(d * (1 - t)), d)
    elif sector == 3:
        return (int(d * t), 0, d)
    elif sector == 4:
        return (d, 0, int(d * (1 - t)))
    elif sector == 5:
        return (d, int(d * t), 0)
    elif sector == 6:
        return (int(d * (1 - t)), d, 0)
    elif sector == 7:
        return (0, d, int(d * t))

def compute_pwm_backward(sector, t, d):
    if sector == 1:
        return (10000, 0, 0)
    elif sector == 0:
        return (d, 0, int(d * t))
    elif sector == 7:
        return (int(d * (1 - t)), 0, d)
    elif sector == 6:
        return (0, int(d * t), d)
    elif sector == 5:
        return (0, d, int(d * (1 - t)))
    elif sector == 4:
        return (int(d * t), d, 0)
    elif sector == 3:
        return (d, int(d * (1 - t)), 0)
    elif sector == 2:
        return (d, 0, int(d * t))

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

# === Main Loop ===
try:
    while True:
        encoder_value = encoder.read()
        current_angle = (encoder_value * 360) / ENCODER_FULL_ROTATION  # still used for sector logic

        error = desired_position - encoder_value
        direction = 1 if error >= 0 else -1
        duty_float = clamp(Kp * abs(error), 0.0, 1.0)
        scaled_duty = int(MAX_DUTY * duty_float)

        sector, t = get_sector_and_position(current_angle)

        if direction == 1:
            u, v, w = compute_pwm_forward(sector, t, scaled_duty)
        else:
            u, v, w = compute_pwm_backward(sector, t, scaled_duty)

        for pin, val in zip(pins, (u, v, w)):
            pin.duty_u16(val)

        print(f"Encoder: {encoder_value}, Error: {error}, PWM: {(u,v,w)}")
        sleep(DELAY_TIME)

except KeyboardInterrupt:
    print("\nStopping motor...")
    for pin in pins:
        pin.duty_u16(0)
    enable_pin.low()
    print("Motor stopped.")

