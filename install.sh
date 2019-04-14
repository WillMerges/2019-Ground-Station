#!/bin/bash
"""
Install script for ground station displays
Run on Raspian from raspi
"""
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip python-imaging python-numpy
sudo pip install RPi.GPIO
sudo python setup.py install

echo "enable SPI in interfacing options"
sudo raspi-config
