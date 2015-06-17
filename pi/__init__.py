import RPi.GPIO as GPIO
from coin_acceptor import CoinAcceptor
from rfid_reader import RfidReader
from pop_machine import PopMachine
from web import WebService
from config import Configuration
from services.member.db_member_service import DbMemberService as MemberService

rfid = None
acceptor = None
memberService = None
popMachine = None
webService = None
conf = Configuration()
try:
    GPIO.setmode(GPIO.BOARD)
    rfid = RfidReader()
    acceptor = CoinAcceptor()
    memberService = MemberService(conf)
    popMachine = PopMachine()
    webService = WebService()

    while 1:
        acceptor.inhibit(True)

        card = rfid.readCard()
        print "Got card: " + str(card)

        member = memberService.getMember(card)
        if member is None:
            webService.onNotFound()
            print("Member does not exist")
        else:
            credit = member.getCredit()
            required = popMachine.getPopCost()
            webService.onSwipe(credit, required)
            inserted = 0
            print("Member needs to supply " + str(required - credit) + " cents")
            while credit + inserted < required:
                acceptor.inhibit(False)
                coin = acceptor.readCoin()
                print("Member entered " + str(coin) + " cents")
                webService.onDeposit(coin)
                inserted += coin
            acceptor.inhibit(True)
            newCredit = (credit + inserted) - required
            memberService.setCredit(card, newCredit)
            print("Member's new credit is " + str(newCredit) + " cents")
            webService.onPaid(newCredit)
            popMachine.awardPop()
            print("Pop awarded to member")
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
