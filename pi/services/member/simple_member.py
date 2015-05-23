from member import Member

class SimpleMember(Member):
    def __init__(self, memberId):
        self.__memberId = memberId

    def getCredit(self):
        if self.__memberId == 5964780: # TODO: Remove hard-coded value
            return 100
        elif self.__memberId == 5952096:
            return 50
        else:
            return 0
