#RaspberryPi screen with weather etch information visible, by Alpo van der Knaap. Started in 2024.

import os
from datetime import datetime
import time

def fullScreenRenderer(time: datetime, weather, location: str):
  width = os.get_terminal_size().columns
  height = os.get_terminal_size().lines
  widthArr = []
  for i in range(width):
    widthArr.append('-')
  widthArr = ''.join(str(i) for i in widthArr)

  #screen construction:
  print(str(widthArr))
  for i in range(height - 3):
    print(time)
  print(str(widthArr))

  return None

def getWeather():

  return None

def main():
  #longSeq = [None, None, None, None, None, None, None, None, None, None]  #instructions for 6min steps in 1h loop
  #shortSeq = [None, None, None, None, None, None, None, None, None, None] #instructions for 6s steps in 1min loop
  location = 'Helsinki'

  runnig = True

  shortTime = time.time()
  longTime = time.time()
  while runnig:
    if time.time() > 6 + shortTime:
      fullScreenRenderer(datetime.now(), None, None)
      shortTime = time.time()
    if time.time() > 1200 + longTime:
      getWeather()
    time.sleep(1)
  return None

main()
