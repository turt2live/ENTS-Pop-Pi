from coin_acceptor import CoinAcceptor
from rfid_reader import RfidReader

rfid = RfidReader()
while 1:
    card = rfid.readCard()
    print "Got card: " + str(card)

acceptor = CoinAcceptor()
while 1:
    cents = acceptor.readCoin()
    print "Got cents: " + str(cents)
