from member import Member

class DbMember(Member):
    def __init__(self, balance):
        self.__balance = balance

    def getCredit(self):
        return self.__balance
