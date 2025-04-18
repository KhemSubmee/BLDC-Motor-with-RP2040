# BLDC-Motor-with-RP2040
A mechatronics project to control a BLDC motor with microPython, using only RP2040 and SimpleFOCMini.

In present days brushless motors are becoming more popular in the industry field due to its many advantages for example long lifespan, lower maintenance and less noise.

However, there are some drawbacks to choosing a brushless motor over brushed motor such as complex wiring, high cost for the motor's positional sensor and the motor's driver.

The objective for this project is to create a simple close-loop position control system by using only the RP2040 and SimpleFOCMini via microPython code.

Hardware used in this project:

Brushless Motor: https://www.intelligentactuator.com/partsearch/robocylinder/pg377_RCL-SA3L.pdf

Pi RP2040 Board: https://th.cytron.io/p-maker-pi-rp2040-simplifying-robotics-with-raspberry-pi-rp2040?srsltid=AfmBOooaFu4PSIIAP_ADe4ZNodhzwVvPOSK_TfrufLAQRjbY8dDoTbOJ

SimpleFOCMini: https://docs.simplefoc.com/simplefocmini

Wiring Diagram:

![wiring](https://github.com/user-attachments/assets/f3facea5-4eb7-4758-b5a8-80edeec504bc)

Experiment Setup:

![setup](https://github.com/user-attachments/assets/02b8943c-c706-4682-b500-1060c3043a9b)


Close loop control method:

1.) Create a 6-mode control method by dividing electrical degree (encoder position) into 8 sector for choosing duty cycle 
2.) Vary duty cycles by using float variable (0 - 1) to increase or decrease duty cycles
3.) Using encoder to control movement section and direction by comparing desired position to current position read by encoder

Results:


https://github.com/user-attachments/assets/88a1d1a9-b69e-4c54-ac2b-c14129728297

From the results, the maximum error is approximately less than 15 pulses from 1578 pulse or about 0.95%
