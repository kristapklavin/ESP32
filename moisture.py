# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(36))
pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

def read_moisture():
   # Read analog value from the sensor
    moisture_value = pot.read()

    # Check if moisture value is within valid range
    moisture_percentage = ((moisture_value - 2800) / (1000 - 2800)) * 100

    return moisture_percentage


while True:
    # Read moisture level
    moisture = read_moisture()

    # Check if reading is valid
    if moisture != -1:
        # Print moisture level
        print("Moisture level: {:.2f}%".format(moisture))
    else:
        print("Error: Moisture reading out of range")

    # Wait for some time before taking the next reading (adjust as necessary)
    sleep(0.1)
# while True:
#     print(pot.read())
#     sleep(0.1)

# import os
# from machine import Pin, SoftSPI
# from sdcard import SDCard

# Pin assignment:
# MISO -> GPIO 13
# MOSI -> GPIO 12
# SCK  -> GPIO 14
# CS   -> GPIO 27
# spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
# sd = SDCard(spisd, Pin(2))


# print('Root directory:{}'.format(os.listdir()))
# vfs = os.VfsFat(sd)
# os.mount(vfs, '/sd')
# print('Root directory:{}'.format(os.listdir()))
# os.chdir('sd')
# print('SD Card contains:{}'.format(os.listdir()))


# 1. To read file from the root directory:
# f = open('jsonfile.json', 'r')
# print(f.read())
# f.close()

# 2. To create a new file for writing:
# f = open('sample2.txt', 'w')
# f.write('Some text for sample 2')
# f.close()

# 3. To append some text in existing file:
# f = open('sample3.txt', 'a')
# f.write('Some text for sample 3')
# f.close()

# 4. To delete a file:
# os.remove('file to delete')

# 5. To list all directories and files:
# os.listdir()

# 6. To create a new folder:
# os.mkdir('sample folder')

# 7. To change directory:
# os.chdir('directory you want to open')

# 8. To delete a folder:
# os.rmdir('folder to delete')

# 9.  To rename a file or a folder:
# os.rename('current name', 'desired name')