# Raspberry Pi screen

Should be made to run at start up in foreground. Shows and regularly updates information like the weather.

Uses simply the terminal view, nothing fancy.

## Requirements

Requires python-weather package and an config.xml file in the program directory with the following format:

'''xml
<?xml version="1.0"?>
<conf>
    <units>metric</units>
    <location>Helsinki</location>
    <screen_update>59</screen_update>
</conf>
'''