import RPi.GPIO as GPIO
import threading
from time import sleep
from observable import Observable
from coin_acceptor import CoinAcceptor
from rfid_reader import RfidReader
from pop_machine import PopMachine
from web import WebService
from config import Configuration
from member_service import MemberService

acceptingFob = False
acceptingFunds = False
requestingMemberFob = None
requestingMemberCredit = None
amountDeposited = None
minimumPopCost = None

obs = Observable()
rfid = None
acceptor = None
memberService = None
popMachine = None
webService = None
conf = Configuration()
try:
    GPIO.setmode(GPIO.BOARD)
    rfid = RfidReader(conf.rfid.serialPort)
    acceptor = CoinAcceptor(conf.coinAcceptor.serialPort, conf.coinAcceptor.inhibitPin, conf.coinMap)
    memberService = MemberService(conf.db.username, conf.db.password, conf.db.hostname, conf.db.port, conf.db.database)
    popMachine = PopMachine(conf.popMachine.relayPin)
    webService = WebService(conf.web.bindAddress, conf.web.port)

    acceptor.inhibit(True) # By default we should inhibit the coin acceptor

    # Start thread for card reading
    fobThread = threading.Thread(target=read_card_thread)
    fobThread.daemon = True
    fobThread.start()

    # Start thread for coin acceptor
    coinThread = threading.Thread(target=read_coin_thread)
    coinThread.daemon = True
    coinThread.start()

    minimumPopCost = popMachine.getPopCost()
    reset_states()
    acceptingFob = True

    # TODO: Does anything need to go here?
    # TODO: Do the keyboard interrupts still fire?
except KeyboardInterrupt:
    if not rfid is None:
        rfid.shutdown()
    if not acceptor is None:
        acceptor.shutdown()
    if not memberService is None:
        memberService.shutdown()
    if not popMachine is None:
        popMachine.shutdown()
    if not webService is None:
        webService.shutdown()
    GPIO.cleanup()

# Utility functions
# ==============================================================================

def reset_states():
    requestingMemberFob = None
    requestingMemberCredit = None
    acceptingFunds = False
    acceptingFob = True
    amountDeposited = None
    acceptor.setInhibited(True)

def get_required_funds():
    totalDeposit = requestingMemberCredit + amountDeposited
    return minimumPopCost - totalDeposit

# Event handlers
# ==============================================================================

@obs.on("CardSwiped")
def handle_card_read(card):
    if not acceptingFob:
        print("Fob swiped while not accepting fobs: Ignoring {card}")
        return # Don't care
    acceptingFob = False
    print("Fob {card} swiped. Finding member...")
    requestingMemberCredit = memberService.getCredit(card)
    if requestingMemberCredit is None:
        obs.trigger("MemberNotFound", card)
        return
    requestingMemberFob = card
    print("Member {card} has {requestingMemberCredit} cents credit")
    acceptingFunds = True
    amountDeposited = 0
    acceptor.setInhibited(False)
    webService.onSwipe(requestingMemberCredit, minimumPopCost)
    requiredFunds = get_required_funds()
    print("Member {card} needs to supply {requiredFunds}")

@obs.on("CoinAccepted")
def handle_coin_read(coin):
    if not acceptingFunds:
        print("Coin accepted while not accepting coins: Ignoring {coin} cents")
        return # Don't care
    amountDeposited += coin
    webService.onDeposit(coin)
    print("Member inserted {coin} cents")
    if get_required_funds() <= 0:
        obs.trigger("PopPaid")

@obs.on("PopPaid")
def handle_pop_paid():
    acceptor.setInhibited(True)
    acceptingFunds = False
    newCredit = (requestingMemberCredit + amountDeposited) - minimumPopCost
    memberService.setCredit(requestingMemberFob, newCredit)
    print("Member's new credit is {newCredit} cents")
    webService.onPaid(newCredit)
    popMachine.awardPop()
    print("Pop awarded to member")
    reset_states()

@obs.on("MemberNotFound")
def handle_member_not_found(id):
    print("Member not found: {id}")
    reset_states()
    webService.onNotFound()

# Definitions for threaded methods
# ==============================================================================

def read_card_thread():
    while True:
        if rfid is None:
            sleep(1)
            continue
        card = rfid.readCard()
        obs.trigger("CardSwiped", card)

def read_coin_thread():
    while True:
        if acceptor is None:
            sleep(1)
            continue
        coin = acceptor.readCoin()
        obs.trigger("CoinAccepted", coin)
