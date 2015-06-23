typedef struct {
  volatile int count;
  volatile unsigned long buffer;
  volatile unsigned long lastRead;
}
rfidInterface;
rfidInterface rfidData;

/* Tests whether the given Wiegand data has correct parity information.
 * First bit in Wiegand26 message is an Even parity bit on first 13 bits of message.
 * Last bit in Wiegand26 message is an Odd parity bit on the last 13 bits of message.
 */
boolean checkWiegandParity(long wiegandData) {
  // Check parity
  byte parity = 0;

  // XOR lower 13 bits to test odd parity
  for (int i = 0; i < 13; i++) {
    parity ^= wiegandData & 1;  // Bitwise AND by 1 to mask lowest bit
    wiegandData = wiegandData >> 1;
  }
  // Lower parity bit should make result odd
  if (parity != 1) {
    return false;
  }

  // XOR upper 13 bits to test even parity
  for (int i = 0; i < 13; i++) {
    parity ^= wiegandData & 1;  // Bitwise AND by 1 to mask lowest bit
    wiegandData = wiegandData >> 1;
  }
  // Upper parity bit should make result even
  if (parity != 0) {
    return false;
  }

  return true;
}

void readBit(int nextBit){
  rfidData.count++;
  rfidData.buffer = rfidData.buffer << 1;
  rfidData.buffer |= nextBit;
  rfidData.lastRead = millis();
}

void readD0(){
  readBit(0);
}
void readD1(){
  readBit(1);
}

void configureRfid(){
  pinMode(5, INPUT_PULLUP); // 5 = D0 (Green)
  attachInterrupt(5, readD0, FALLING);
  pinMode(6, INPUT_PULLUP); // 6 = D1 (White)
  attachInterrupt(6, readD1, FALLING);
}

// The time before RFID data is purged
unsigned long readTimeout = 1000;

void setup(){
  Serial.begin(9600);
  //Serial.println("OK");

  configureRfid();

  rfidData.count = 0;
  rfidData.buffer = 0;
  rfidData.lastRead = 0;
}

void loop(){
  if (rfidData.count == 26) {
    // We have a full read - attempt to parse the data
    long cardNum = rfidData.buffer;
    if (checkWiegandParity(cardNum)) {
      // Failed: Invalid parity from RFID reader
      Serial.println("E:Failed to check parity");
    }
    else {
      cardNum = (cardNum >> 1) & 0xFFFFFF;
      Serial.println(String(cardNum, 10));
    }

    rfidData.count = 0;
    rfidData.buffer = 0;
  }
  else if (rfidData.count > 0 && (millis() - rfidData.lastRead) > readTimeout) {
    // Error: Failed to read from RFID reader
    Serial.println("E:Failed to read from RFID reader");
    rfidData.count = 0;
    rfidData.buffer = 0;
  }
}
