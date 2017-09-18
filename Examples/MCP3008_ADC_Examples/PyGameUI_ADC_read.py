#!/usr/bin/python2.7
'''
Description: This PyGameUI program allows you to switch between any ADC inputs and view the voltage being
             applied to that input.

Created on Jul 26, 2014

@author: jeremyblythe
'''
import sys
import pygame
import os
import pygameui as ui
import logging
import signal
import threading
import time

# Import SPI library (for hardware SPI) and the MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Hardware SPI configuration:
SPI_PORT = 1
SPI_DEVICE = 0

mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE))


log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


MARGIN = 20


class PotReader():
    def __init__(self, pitft):
        self.pitft = pitft
        self.terminated = False
        
    def terminate(self):
        self.terminated = True
        
    def __call__(self):
        while not self.terminated:
            time.sleep(0.1)  # Only poll the voltage once every 100ms
            volts = mcp.read_adc(self.pitft.chan) / 1024.0 * 3.3  # Read the ADC count from the selected channel and convert it to a voltage
            self.pitft.set_chan_label(self.pitft.chan)
            self.pitft.set_volts_label(volts)
            self.pitft.set_progress(volts / 3.3)

class PiTft(ui.Scene):

    def __init__(self):

        self.chan = 0

        ui.Scene.__init__(self)

        self.previousChan_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'Previous Chan')
        self.previousChan_button.on_clicked.connect(self.gpi_button)
        self.add_child(self.previousChan_button)

        self.nextChan_button = ui.Button(ui.Rect(170, MARGIN, 130, 60), 'Next Chan')
        self.nextChan_button.on_clicked.connect(self.gpi_button)
        self.add_child(self.nextChan_button)

        self.chan_value = ui.Label(ui.Rect(MARGIN, 170, 100, 30), '')
        self.add_child(self.chan_value)

        self.progress_view = ui.ProgressView(ui.Rect(MARGIN, 200, 280, 40))
        self.add_child(self.progress_view)

        self.volts_value = ui.Label(ui.Rect(170, 170, 50, 30), '')
        self.add_child(self.volts_value)

    def gpi_button(self, btn, mbtn):
        logger.info(btn.text)
        
        if btn.text == 'Previous Chan':
            if self.chan > 0:
                self.chan -= 1
            else:
                self.chan = 7
        elif btn.text == 'Next Chan':
            if self.chan < 7:
                self.chan += 1
            else:
                self.chan = 0

    def set_progress(self, percent):
        self.progress_view.progress = percent
        
    def set_volts_label(self, volts):
        self.volts_value.text = '%.2f V' % volts

    def set_chan_label(self, chan_in):
        self.chan_value.text = 'Channel: %d' % chan_in

    def update(self, dt):
        ui.Scene.update(self, dt)


ui.init('Raspberry Pi UI', (320, 240), True)

pitft = PiTft()

# Start the thread running the callable
potreader = PotReader(pitft)
threading.Thread(target=potreader).start()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    potreader.terminate()
    sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)

ui.scene.push(pitft)
ui.run()


