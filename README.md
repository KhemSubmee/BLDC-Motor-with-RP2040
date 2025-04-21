# BLDC-Motor-with-RP2040

In recent years, brushless DC (BLDC) motors have become increasingly popular in industrial applications due to their numerous advantages, including longer lifespan, lower maintenance requirements, and quieter operation compared to traditional brushed motors.

However, adopting BLDC motors also introduces certain challenges. These include more complex wiring setups, higher costs associated with positional sensors, and the added expense of dedicated motor drivers capable of precise control.

The objective of this project is to develop a simple closed-loop position control system for a BLDC motor using only a Raspberry Pi RP2040 microcontroller and a SimpleFOCMini driver board, with all control logic written in MicroPython. A key focus is to achieve field-oriented control (FOC) via the SimpleFOCMini, providing smooth and efficient motor operation while minimizing system complexity and cost.

# Hardware used in this project:

Brushless Motor (Actuators and sensors): [RCL-SA3L](https://www.intelligentactuator.com/partsearch/robocylinder/pg377_RCL-SA3L.pdf)

![blmotor](https://github.com/user-attachments/assets/fc343e00-95d5-48ac-8157-d7e5acdf2d0b)

Controller: [Raspberry Pi RP2040](https://th.cytron.io/p-maker-pi-rp2040-simplifying-robotics-with-raspberry-pi-rp2040?srsltid=AfmBOooaFu4PSIIAP_ADe4ZNodhzwVvPOSK_TfrufLAQRjbY8dDoTbOJ)

![maker-pi-rp2040-top-1x1-logo-800x800](https://github.com/user-attachments/assets/9762d11e-d657-4267-8187-a30518a011ea)

BL Motor Driver: [SimpleFOCMini](https://docs.simplefoc.com/simplefocmini)

![image](https://github.com/user-attachments/assets/271b9bf5-c83c-45d8-a902-9e2e8704391a)

# Wiring Diagram:

![image](https://github.com/user-attachments/assets/195b803b-a6f1-4b0c-97e5-06cac3390f5c)

# Experiment Setup:

![image](https://github.com/user-attachments/assets/7c91ea1a-cb7d-4bbd-af64-5f29b3134677)

# How to Control a Brushless DC (BLDC) Motor

Controlling a BLDC motor typically involves two key components: 
_**positional sensing**_ and _**a control method**_ to drive the motor phases based on that position. 

![Rotating_field-compact](https://github.com/user-attachments/assets/5ddb5d96-c1f6-4ffd-aad6-fc284ba02ffe)

## Positional Sensors for BLDC Motors

To properly control a BLDC motor, it’s essential to know the rotor’s position. Several types of sensors are commonly used for this purpose, each with its own advantages and drawbacks:

### 1. [Hall Element](https://www.haydonkerkpittman.com/learningzone/whitepapers/connecting-brushless-dc-motors-to-electronic-controllers)
Hall sensors are the most basic and widely used position sensors for BLDC motors. They work by detecting the magnetic field from the rotor’s magnets and providing a digital signal when the field crosses certain thresholds.

How it works:
Three sensors are placed 120° apart, providing a 3-bit signal indicating the rotor position.

![image](https://github.com/user-attachments/assets/eb96b654-5c32-4096-aa3b-0f8aa9921a05)

### 2. Optical Encoder
An encoder is a sensor that converts the position, speed, or direction of a rotating shaft into an electrical signal. It provides feedback to the control system, allowing for precise control of motors in position, speed, and motion applications.
Encoders are typically classified into two main types:

### 2.1 [Incremental Encoder](https://micronor.com/products/em-incremental-encoders/)
An incremental encoder provides pulses as the shaft rotates but does not inherently track absolute position. The position is determined by counting pulses from a known reference point.

How it works:
It has a disc with equally spaced lines and optical or magnetic sensors that detect changes as the disc rotates. Two output signals (A and B channels) in quadrature allow determination of both position and direction.

![image](https://github.com/user-attachments/assets/fce8c0e7-84db-48f8-9ebc-a55e4f707f67)

### 2.2 [Absolute Encoder](https://www.linearmotiontips.com/when-is-encoder-resolution-specified-in-bits-and-what-does-that-tell-us/)
An absolute encoder provides a unique digital code or position value for each shaft position. Unlike incremental encoders, it retains the position information even when power is lost.

How it works:
The encoder disc has multiple concentric tracks, each representing a binary value. Light passing through the disc is detected by sensors, generating a digital position code.

![image](https://github.com/user-attachments/assets/9c809978-14d8-4246-ba3f-bb0250c558c6)

### 3. [Resolver](https://www.celeramotion.com/inductive-sensors/resolvers/)
A resolver is an analog electromechanical device that provides continuous position feedback over 360° using sine and cosine signals.

How it works:
It consists of a rotor winding and two stator windings placed at 90° to each other. As the rotor turns, it induces sinusoidal voltages in the stator windings proportional to the rotor’s position. These signals are then converted to digital position data using a resolver-to-digital converter.

![image](https://github.com/user-attachments/assets/6c89b816-18af-40e3-a27e-d97d9903b7f6)

### In this project, an _**incremental encoder**_ is used for position feedback because it is already built into the given BLDC motor.

## [Brushless Motor Controlling Method](https://www.renesas.com/en/support/engineer-school/brushless-dc-motor-02-inverter-pmw?srsltid=AfmBOooy_e6pUcm3HEjqYTa10uTOkbG9XOpBEfvfKHw1DI-_ry2SbONa)

### 1. Controlling the Magnetic Field
To rotate a BLDC motor, we must control both the direction and timing of current through the stator coils. A BLDC motor typically uses three coils (phases U, V, and W) spaced 120° apart. When current flows through a coil, it generates a magnetic field.

By selectively energizing different combinations of these coils, a rotating magnetic field is produced inside the stator. The rotor's permanent magnets are pulled by this rotating field, causing the rotor to turn.

For example:

Energizing phase U→W creates a resultant magnetic flux in one direction.

The rotor aligns itself with this flux.

By continuously switching the energized phases in a specific sequence (known as 6-mode or 120° conduction control), the resultant flux vector rotates, pulling the rotor along with it.

The speed of rotation is controlled by adjusting how quickly the phases switch, while the direction is determined by the order of switching. This is the fundamental principle behind BLDC motor operation.

![fig3-the-changing-resultant-en](https://github.com/user-attachments/assets/2cfa1081-9dd2-4c6f-b80a-7c1bf239c3c9)

The changing resultant flux continually pulls the rotor magnet, causing the rotor to turn.

### 2. Sinusoidal Control Delivers Smooth Rotation
In 120-degree conduction control, the motor switches between six fixed flux directions, each separated by 60°, pulling the rotor in steps. While effective, this creates jerky motion, vibrations, and audible noise.

A better alternative is sinusoidal control, where the current in each phase is varied smoothly in the shape of a sine wave. This produces a continuously rotating magnetic field, resulting in smoother, quieter, and more efficient motor operation.

The most advanced form of sinusoidal control is Field-Oriented Control (FOC). In FOC, the three-phase motor currents are mathematically transformed into two perpendicular components which are torque-producing (Iq) and flux-producing (Id).

By controlling these components separately, FOC allows for precise torque and speed control, minimized torque ripple, and higher efficiency at all speeds.

FOC continuously adjusts the magnitude and angle of the stator’s magnetic field to follow the rotor position smoothly — typically using an encoder for position feedback. It’s widely used in robotics, drones, electric vehicles, and high-performance industrial drives.

![fig4-sinusoidal-control-en](https://github.com/user-attachments/assets/2529c508-919e-44d7-88f1-5012babb13e6)

By controlling the current into all three phases, resultant flux magnitude and direction can be controlled more precisely that with 120-degree conducting control, so as to achieve smoother rotation. Resultant flux is no longer limited to six discrete directions.

### 2.1 [FOC (Field Oriented Control)](https://www.pmdcorp.com/resources/type/articles/get/field-oriented-control-foc-a-deep-dive-article)
Field Oriented Control (FOC) is an advanced technique for controlling BLDC or PMSM motors by regulating the stator magnetic field in relation to the rotor position. It uses continuous, smoothly rotating magnetic fields generated by sinusoidal phase currents — effectively aligning the stator’s magnetic vector with the rotor’s permanent magnet vector for maximum torque efficiency at all positions.

![image](https://github.com/user-attachments/assets/491a6950-2a38-44da-bc32-929c37ec8741)

### 2.2 [SimpleFOCMini](https://docs.simplefoc.com/simplefocmini)
SimpleFOCMini is a small, affordable, and highly capable open-source motor controller board designed specifically for brushless DC (BLDC) and gimbal motors. It runs the SimpleFOC (Field Oriented Control) firmware — a popular Arduino-based open-source library and control platform for BLDC motor control.

It’s essentially a compact inverter (3-phase driver) paired with an MCU, designed to implement FOC algorithms easily for precise, quiet, and efficient motor control.

SimpleFOCMini acts as both:

1.) Inverter - switching the 3-phase voltages applied to the BLDC motor windings

2.) Controller - reading position feedback (from encoder/hall sensors), calculating the FOC control algorithm, and generating appropriate PWM signals for the inverter.

The board uses Field Oriented Control (FOC) - an advanced control method where motor currents are transformed into a rotating reference frame, allowing precise independent control of torque and magnetic flux.

![connection_mini](https://github.com/user-attachments/assets/129f200b-2329-4a45-941d-219ccba65d40)

### 3. Control by Inverter
In a BLDC motor, controlling the direction and timing of current through the three motor phases (U, V, W) is essential for generating a rotating magnetic field. Unlike brushed DC motors, which use brushes and a commutator for switching current direction, BLDC motors rely on inverter circuits made of electronic switches (typically MOSFETs).

The inverter sequentially switches current between different phase pairs (e.g. U→W, U→V) based on the control method used. In 120-degree conduction control, only two phases are active at a time, while in sinusoidal control and FOC, all three phases are modulated continuously.

To regulate the magnitude of the current, inverters use Pulse Width Modulation (PWM). By adjusting the duty cycle (the ratio of ON time to total period), the effective voltage, and therefore the phase current is controlled. Increasing the duty cycle raises the current, while decreasing it lowers the current.

120-degree control uses simpler two-phase PWM switching.

Sinusoidal control and FOC require precise, continuous three-phase PWM control for smooth torque and speed regulation.

Modern microcontrollers with built-in PWM modules and external inverter circuits make it possible to efficiently drive BLDC motors across a range of applications, from fans to electric vehicles.

![image](https://github.com/user-attachments/assets/7f683b61-1e93-4827-b6a8-d09e4f1a62ad)

Varying the duty cycle (the ON time within each switching period) changes the effective voltage.

### For motor control, this project uses a semi-sinusoidal control method together with inverter-based switching.

In this project's code we are not doing full FOC, but we are applying a semi-sinusoidal commutation strategy by dividing the electrical angle into 8 sectors and modulating the duty cycles of each phase per sector using a floating-point value "t" to smoothly adjust the phase currents.

This is a simplified, software-controlled approximation of sinusoidal commutation which produces smoother operation than 6-step control and mimics the idea of continuous rotating flux vectors by gradually varying duty cycles in each sector.

To conclude, this system’s approach is closer to sinusoidal commutation via inverter control than classic FOC, but based on similar principles.

# [PID control](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller)

PID (Proportional-Integral-Derivative) control is a widely used feedback control technique that continuously calculates an error value as the difference between a desired target (setpoint) and a measured value, then applies corrections based on proportional (P), integral (I), and derivative (D) terms. The Proportional term reacts to the current error, the Integral term accounts for the accumulated past error, and the Derivative term predicts future error based on its rate of change. In our code, we've implemented a simple _**Proportional control (P-only) loop**_, where the duty cycle applied to the motor is proportional to the position error between the desired encoder count and the actual encoder reading. 

For example:
```
error = desired_position - encoder_value
duty_float = clamp(Kp * abs(error), 0.0, 1.0)
scaled_duty = int(MAX_DUTY * duty_float)
```

This part of the codecalculates the error, multiplies it by the proportional gain Kp, clamps it between 0 and 1 to keep it within safe limits, and then scales it to the maximum PWM duty cycle. This duty value is then used to control the motor phases, making the motor correct its position proportionally to how far off it is from the target.

![image](https://github.com/user-attachments/assets/29bfbcb2-0b3c-41f1-9441-453684447874)

# Close loop control method:

This project implements a simple closed-loop position control for a BLDC motor using the following approach:

**1.) 6-Mode Control via Electrical Angle Sectors:**

The electrical rotation (0–360°) is divided into 8 equal sectors based on the encoder position. Each sector is assigned a specific duty cycle pattern to drive the motor phases, effectively creating a 6-mode control system for commutation.

**2.) Dynamic Duty Cycle Adjustment:**

The duty cycle for each active phase is controlled using a floating-point variable (ranging from 0.0 to 1.0) to increase or decrease the power delivered to the motor phases, providing smoother and more precise movement.

**3.) Position and Direction Control via Encoder Feedback:**

The system continuously reads the current position from the motor’s encoder and compares it to the target position. Based on the difference, the control logic determines the movement direction and activates the appropriate sectors to drive the motor toward the desired position.

![image](https://github.com/user-attachments/assets/aff13df5-f0c2-4c33-9e7b-c8980bb5a688)

This diagram illustrates a concept of the code for closed-loop position control (forward movement)

## Code example
```
if sector == 0:
 return (0, 10000, 0) # minimum initial duty cycle at 10000
 elif sector == 1:
 return (0, d, int(d * t)) # u = 0, v = 15000, w = 0 -> 15000
 elif sector == 2:
 return (0, int(d * (1 - t)), d) # u = 0, v = 15000 -> 0, w = 15000
 elif sector == 3:
 return (int(d * t), 0, d) # u = 0 -> 15000, v = 0, w = 15000
```
This code segment implements a semi-sinusoidal control method for a BLDC motor by assigning PWM duty cycles to each of the three motor phases (U, V, W) based on the current electrical sector. Using a constant maximum duty cycle d = 15000 and a float t ranging from 0 to 1 (representing the rotor’s progress within a sector), the duty cycles are smoothly varied to create stepped transitions between phases, reducing torque ripple and enabling smoother motor rotation. This approach simplifies sinusoidal control by approximating sinusoidal phase currents without requiring complex calculations, offering a practical balance between performance and implementation ease on hardware like the RP2040.

# Results:

https://github.com/user-attachments/assets/88a1d1a9-b69e-4c54-ac2b-c14129728297

From testing, the maximum positioning error observed was less than 15 pulses out of 1578 pulses per motor's full rotation, which corresponds to an error of approximately 0.95%. This indicates that the closed-loop position control system is able to track the desired position with very high accuracy, given the simple control method and limited hardware.

# References

## [PIO Pin](https://tutoduino.fr/en/pio-rp2040-en/)

PIO stands for Programmable I/O which is unique to the RP2040 chip (used in Raspberry Pi Pico), it’s a hardware feature that allows you to create custom digital interfaces and protocols in hardware, without burdening the main CPU cores allowing you to create custom hardware-level protocols and I/O control that runs independently of the main CPU cores.

Every GPIO pin on the RP2040 can be controlled either by the CPU directly, or by a PIO state machine. When we say a "PIO pin," we’re referring to a GPIO pin that’s currently assigned to be controlled by a PIO state machine rather than being a regular GPIO pin handled by the CPU.

![image](https://github.com/user-attachments/assets/15071387-1583-4ab4-8479-58333b4f116a)

## Libraries used

### 1. Built-in Micropython libraries
time → Used for time management functions such as sleep() to create delays or manage loop timing during motor control operations.

machine → Provides access to hardware-related functions on the RP2040, such as configuring GPIO pins (Pin) and generating PWM signals (PWM) for motor phase control.

### 2. Custom Quadrature encoder reading using _**PIO**_
QEnc_Pio_4 → A custom Python module for reading incremental (quadrature) encoders using the RP2040's PIO (Programmable I/O) hardware. It enables precise, high-speed position feedback by decoding the encoder’s A and B channels in hardware without CPU overhead, ensuring accurate and responsive closed-loop position control.

### 3. [Arduino SimpleFOClibrary](https://docs.simplefoc.com/arduino_simplefoc_library_showcase)
While this project references the Arduino SimpleFOC library conceptually (as it traditionally provides Field-Oriented Control functions for BLDC motors on Arduino platforms), in this project, its control strategy was manually recreated in MicroPython using custom code for motor commutation and duty cycle management, inspired by SimpleFOC’s methodology.
