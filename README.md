# BLDC-Motor-with-RP2040

In recent years, brushless DC (BLDC) motors have become increasingly popular in industrial applications due to their numerous advantages, including longer lifespan, lower maintenance requirements, and quieter operation compared to traditional brushed motors.

However, adopting BLDC motors also introduces certain challenges. These include more complex wiring setups, higher costs associated with positional sensors, and the added expense of dedicated motor drivers capable of precise control.

The objective of this project is to develop a simple closed-loop position control system for a BLDC motor using only a Raspberry Pi RP2040 microcontroller and a SimpleFOCMini driver board, with all control logic written in MicroPython. A key focus is to achieve field-oriented control (FOC) via the SimpleFOCMini, providing smooth and efficient motor operation while minimizing system complexity and cost.
# Hardware used in this project:

Brushless Motor: https://www.intelligentactuator.com/partsearch/robocylinder/pg377_RCL-SA3L.pdf

Pi RP2040 Board: https://th.cytron.io/p-maker-pi-rp2040-simplifying-robotics-with-raspberry-pi-rp2040?srsltid=AfmBOooaFu4PSIIAP_ADe4ZNodhzwVvPOSK_TfrufLAQRjbY8dDoTbOJ

SimpleFOCMini: https://docs.simplefoc.com/simplefocmini

# Wiring Diagram:

![wiring](https://github.com/user-attachments/assets/f3facea5-4eb7-4758-b5a8-80edeec504bc)

# Experiment Setup:

![setup](https://github.com/user-attachments/assets/02b8943c-c706-4682-b500-1060c3043a9b)


# Close loop control method:

This project implements a simple closed-loop position control for a BLDC motor using the following approach:

1.) 6-Mode Control via Electrical Angle Sectors:

The electrical rotation (0–360°) is divided into 8 equal sectors based on the encoder position. Each sector is assigned a specific duty cycle pattern to drive the motor phases, effectively creating a 6-mode control system for commutation.

2.) Dynamic Duty Cycle Adjustment:

The duty cycle for each active phase is controlled using a floating-point variable (ranging from 0.0 to 1.0) to increase or decrease the power delivered to the motor phases, providing smoother and more precise movement.

3.) Position and Direction Control via Encoder Feedback:

The system continuously reads the current position from the motor’s encoder and compares it to the target position. Based on the difference, the control logic determines the movement direction and activates the appropriate sectors to drive the motor toward the desired position.

# Results:


https://github.com/user-attachments/assets/88a1d1a9-b69e-4c54-ac2b-c14129728297

From testing, the maximum positioning error observed was less than 15 pulses out of 1578 pulses per motor's full rotation, which corresponds to an error of approximately 0.95%. This indicates that the closed-loop position control system is able to track the desired position with very high accuracy, given the simple control method and limited hardware.
