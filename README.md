ENTS-Pop-Pi
===========

Code for use with the Edmonton New Technology Society's RFID enabled pop vending machine

For details on the project see [the ENTS project page](http://ents.ca/index.php/Projects/RFIDpop).

## Project Structure
- `/RFIDReader` - Arduino code for connecting to the RFID reader (sends values to pi over serial)
- `/pi` - Applicable python code for the Raspberry Pi side (controls vending machine and coordinates devices)
- `/www` - Web static data (hosted by the Pi)

For more technical information such as wiring diagrams, please [click here](https://drive.google.com/folderview?id=0B6JIYSBkLkAnfjJhUDQtY3JvMktOWmdqbkhYcGJKZDdkOUpjM1Nzczl4Um1ENV90UjVzOHM&usp=sharing) or visit the [ENTS project page](http://ents.ca/index.php/Projects/RFIDpop).
