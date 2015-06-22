import threading
import RPi.GPIO as GPIO
from time import sleep
from observable import Observable
from coin_acceptor import CoinAcceptor
from rfid_reader import RfidReader
from pop_machine import PopMachine
from web import WebService
from config import Configuration
from member_service import MemberService

class PopPi:
    # Main application for pop machine

    # State information
    __acceptingFob = False
    __acceptingFunds = False
    __memberFob = None
    __memberCredit = None
    __deposited = None
    __popCost = None

    def __init__(self):
        self.__obs = Observable()
        conf = Configuration()
        self.__rfid = RfidReader(conf.rfid.serialPort)
        self.__acceptor = CoinAcceptor(conf.coinAcceptor.serialPort, conf.coinAcceptor.inhibitPin, conf.coinMap)
        self.__memberService = MemberService(conf.db.username, conf.db.password, conf.db.hostname, conf.db.port, conf.db.database)
        self.__popMachine = PopMachine(conf.popMachine.relayPin)
        self.__webService = WebService(conf.web.bindAddress, conf.web.port)
        self.__acceptor.inhibit(True)
        self.__popCost = self.__popMachine.getPopCost()
        self.__obs.on("CardSwiped", self.__onCardRead)
        self.__obs.on("CoinAccepted", self.__onCoinAccepted)
        self.__obs.on("MemberNotFound", self.__onMemberNotFound)
        self.__obs.on("PopPaid", self.__onPopPaid)
        self.__creditOnlyPin = conf.general.creditOnlyPin

    def start(self):
        self.__fobThread = threading.Thread(target=self.__readCardThread)
        self.__fobThread.daemon = True
        self.__fobThread.start()
        self.__coinThread = threading.Thread(target=self.__readCoinThread)
        self.__coinThread.daemon = True
        self.__coinThread.start()
        self.__resetStates()
        self.__acceptingFob = True

    def stop(self):
        if not self.__rfid is None:
            self.__rfid.shutdown()
        if not self.__acceptor is None:
            self.__acceptor.shutdown()
        if not self.__memberService is None:
            self.__memberService.shutdown()
        if not self.__popMachine is None:
            self.__popMachine.shutdown()
        if not self.__webService is None:
            self.__webService.shutdown()

    def __onCardRead(self, card):
        if not self.__acceptingFob:
            print("Fob swiped while not accepting fobs: Ignoring fob " + str(card))
            return
        self.__acceptingFob = False
        print("Fob " + str(card) + " swiped. Finding member...")
        self.__memberCredit = self.__memberService.getCredit(card)
        if self.__memberCredit is None:
            self.__obs.trigger("MemberNotFound", card)
            return
        self.__memberFob = card
        print("Member " + str(card) + " has " + str(self.__memberCredit) + " cents credit")
        self.__acceptingFunds = True
        self.__deposited = 0
        self.__acceptor.inhibit(False)
        self.__webService.onSwipe(self.__memberCredit, self.__popCost)
        requiredFunds = self.__getRequiredFunds()
        print("Member " + str(card) + " needs to supply " + str(requiredFunds) + " cents")

    def __onCoinAccepted(self, coin):
        if not self.__acceptingFunds:
            print("Coin accepted while not accepting coins: Ignoring " + str(coin) + " cents")
            return
        self.__deposited += coin
        self.__webService.onDeposit(coin)
        print("Member inserted " + str(coin) + " cents")
        if self.__getRequiredFunds() <= 0:
            self.__obs.trigger("PopPaid")

    def __onPopPaid(self):
        self.__acceptor.inhibit(True)
        self.__acceptingFunds = False
        newCredit = (self.__memberCredit + self.__deposited) - self.__popCost
        self.__memberService.setCredit(self.__memberFob, newCredit)
        print("Member's new credit is " + str(newCredit) + " cents")
        self.__webService.onPaid(newCredit)
        self.__popMachine.awardPop()
        print("Pop awarded to member")
        self.__resetStates()

    def __onMemberNotFound(self, card):
        print("Member not found: " + str(card))
        self.__resetStates()
        self.__webService.onNotFound()

    def __resetStates(self):
        self.__acceptingFob = True
        self.__acceptingFunds = False
        self.__memberFob = None
        self.__memberCredit = None
        self.__deposited = None
        self.__acceptor.inhibit(True)
        print("Waiting for member")

    def __getRequiredFunds(self):
        totalDeposit = self.__memberCredit + self.__deposited
        return self.__popCost - totalDeposit

    def __readCardThread(self):
        while True:
            if self.__rfid is None:
                sleep(1)
                continue
            card = self.__rfid.readCard()
            self.__obs.trigger("CardSwiped", card)

    def __readCoinThread(self):
        while True:
            if self.__acceptor is None:
                sleep(1)
                continue
            coin = self.__acceptor.readCoin()
            self.__obs.trigger("CoinAccepted", coin)
