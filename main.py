#RaspberryPi screen with weather etch information visible, by Alpo van der Knaap. Started in 2024.

import os
from datetime import datetime
import time
import asyncio
import python_weather


def screenRenderer(timeNow: datetime, weather, location: str):
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 3

    widthArr = []
    for i in range(width):
      widthArr.append('-')
    widthArr = ''.join(str(i) for i in widthArr)
    
    clockWidth = 8 + 8 + 5 + 8 + 8
    fillerLen = width - clockWidth - width//6
    widthFiller = []
    for i in range(fillerLen):
      widthFiller.append(' ')
    widthFiller = ''.join(str(i) for i in widthFiller)

    if width < 3*clockWidth//2:
      print(timeNow.date(), timeNow.time())
      print('Can not properly display information due to small terminal!')
      return None
    if weather == None:
      print(timeNow.date(), timeNow.time())
      print('Can not reach weather services!')
      return None

    tStr = timeSymbols(timeNow)

    hour1 = getSymbol('numbers.txt', tStr[0])
    hour2 = getSymbol('numbers.txt', tStr[1])
    min1 = getSymbol('numbers.txt', tStr[2])
    min2 = getSymbol('numbers.txt', tStr[3])

    #symLines = [getSymbol('numbers.txt', '0')[0], getSymbol('numbers.txt', '0')[1], getSymbol('numbers.txt', '0')[2], getSymbol('numbers.txt', '0')[3], getSymbol('numbers.txt', '0')[4]]

    #screen construction:
    print(str(widthArr))
    print('')

    for i in range(5):
      print('%s %-8s %-8s %-5s %-8s %-8s' % (widthFiller, hour1[i], hour2[i], getSymbol('numbers.txt', ':')[i], min1[i], min2[i]))
    print('%s  %s' % (widthFiller, str(timeNow.date())))
    print('')

    todayWeather = ''
    weatherLines = 0

    for daily in weather:
      if daily.date == timeNow.date():
        for hourly in daily.hourly_forecasts:
          if hourly.time.hour > timeNow.hour:
            todayWeather = todayWeather + '  ' + str(hourly.time)[0:2] + ': ' + str(hourly.temperature) + 'C '
        print('%s  Weather in %s today:' % (widthFiller, location))
        print('%s%s\n' % (widthFiller, todayWeather))
        weatherLines += 2
      else:
        print(widthFiller + '  ' + str(daily.date) + ' ' + str(daily.lowest_temperature) + 'C / ' + str(daily.highest_temperature) + 'C')
        weatherLines += 1
        
  
    for i in range((height - 8 - weatherLines)):
      print('')
    
    print(str(widthArr))
    return None
    #end screen construction


def timeSymbols(timeNow: datetime):
    hours = str(timeNow.hour)
    minutes = str(timeNow.minute)
    if len(hours) == 1:
      hours = '0' + hours
    if len(minutes) == 1:
      minutes = '0' + minutes
    return [hours[0], hours[1], minutes[0], minutes[1]]


def getSymbol(fileName, symbol):
    font = open(fileName, 'r')
    bigSym = []
    symStart = False
    height = 5
    for lines in font.readlines():
      if symStart == True and height != 0:
        bigSym.append(lines.replace('\n', ''))
        height -= 1
      elif '[' + symbol + ']' in lines:
        symStart = True
    font.close()
    return bigSym


async def main():
    location = 'Helsinki'

    runnig = True

    dailyWeather = None
    checkTime = time.time()
    lastTime = 0
    while runnig:
      if time.time() > 1200 + checkTime or dailyWeather == None:            #only run this every 20min
        try:
          async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(location)
            dailyWeather = []
            for daily in weather.daily_forecasts:
              dailyWeather = dailyWeather + [daily]
        except:
          dailyWeather = None

      if time.time() - lastTime >= 60:
        screenRenderer(datetime.now(), dailyWeather, location)
        lastTime = time.time()
      time.sleep(1)

    return None

if __name__ == "__main__":
  asyncio.run(main())
