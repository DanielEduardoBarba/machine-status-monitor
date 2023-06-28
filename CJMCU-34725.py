import smbus2
import time

# Define the I2C address of the TCS34725 sensor
SENSOR_ADDRESS = 0x29

# Define the register addresses for the sensor
COMMAND_BIT = 0x80
ENABLE_REGISTER = 0x00
ATIME_REGISTER = 0x01
CONTROL_REGISTER = 0x0F
CDATAL_REGISTER = 0x14
RDATAL_REGISTER = 0x16
GDATAL_REGISTER = 0x18
BDATAL_REGISTER = 0x1A

# Enable the sensor
bus = smbus2.SMBus(2)
bus.write_byte_data(SENSOR_ADDRESS, COMMAND_BIT | ENABLE_REGISTER, 0x03)

# Set the integration time (ATIME) and gain (CONTROL) for the sensor
bus.write_byte_data(SENSOR_ADDRESS, COMMAND_BIT | ATIME_REGISTER, 0xEB)  # 410 ms integration time
bus.write_byte_data(SENSOR_ADDRESS, COMMAND_BIT | CONTROL_REGISTER, 0x00)  # 1x gain

# Function to read the color values
def read_color():
    r = bus.read_word_data(SENSOR_ADDRESS, COMMAND_BIT | RDATAL_REGISTER)
    g = bus.read_word_data(SENSOR_ADDRESS, COMMAND_BIT | GDATAL_REGISTER)
    b = bus.read_word_data(SENSOR_ADDRESS, COMMAND_BIT | BDATAL_REGISTER)
    return r, g, b

# Main loop to continuously read and display color values
while True:
    try:
        red, green, blue = read_color()
        print("Red: {}, Green: {}, Blue: {}".format(red, green, blue))
        time.sleep(1)  # Delay for 1 second
    except KeyboardInterrupt:
        break

# Disable the sensor before exiting
bus.write_byte_data(SENSOR_ADDRESS, COMMAND_BIT | ENABLE_REGISTER, 0x00)
