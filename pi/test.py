from coin_acceptor import CoinAcceptor

acceptor = CoinAcceptor()
while 1:
    cents = acceptor.readCoin()
    print "Got cents: " + str(cents)
