# Pioneer Project 
#!/usr/bin/env python
# -*- coding: utf8 -*-
# code by MTMoore and Fcowell(1-dinomite59) 
#With Thanks to the creators of the MFRC522 Libary 
#
#


import RPi.GPIO as GPIO
import MFRC522
import signal
import time

# Define GPIO to LCD mapping
# set these to BOARD type pin numbers and not BCM

LCD_RS = 37
LCD_E  = 35
LCD_D4 = 33
LCD_D5 = 31
LCD_D6 = 29
LCD_D7 = 40

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
# Capture SIGINT for cleanup when the script is aborted
continue_reading = True
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522



def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_init()
  
    
  # Welcome message
  lcd_string("Don't get lost!",LCD_LINE_1)
  MIFAREReader = MFRC522.MFRC522()
    
  # This loop keeps checking for chips. If one is near it will get the UID and authenticate
  while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        uidread=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        print uidread
        
        # tag 1
        if uidread=="21324516196":
            lcd_string("Goal we won!",LCD_LINE_1)
        # tag 2
        if uidread=="3714217435":
            lcd_string("What a view!",LCD_LINE_1)
        # tag 3
        if uidread=="1017919196":
            lcd_string("Kick Flip?",LCD_LINE_1)
        # tag 4
        if uidread=="10115017435":
            lcd_string("The band",LCD_LINE_1)
        # tag 5
        if uidread=="569139195":
            lcd_string("Nice plants!",LCD_LINE_1)
        # tag 6
        if uidread=="521324196":
            lcd_string("You did it!",LCD_LINE_1)

        # tag 7 - this our restart tag, will start from tag 1 again
        if uidread=="16519914196":
            lcd_string("Don't get lost!",LCD_LINE_1)

        
            
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
  
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
    message = message.ljust(LCD_WIDTH," ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

  
if __name__ == '__main__':
    main()
