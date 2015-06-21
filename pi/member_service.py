from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, subqueryload, relationship, backref

class MemberService():
    # Provides member information from a MySQL database

    def __init__(self, username, password, hostname, port, database):
        connectionString = 'mysql+mysqldb://' + username + ':' + password + '@' + hostname + ':' + port + '/' + database
        engine = create_engine(connectionString)
        self.session = sessionmaker(bind=engine)()

    def __findWallet__(self, memberId):
        dbMember = self.session.query(OrmMember).\
            options(subqueryload(OrmMember.wallets)).\
            filter_by(fob_field=str(memberId)).first()
        if dbMember is None:
            return None
        newWallet = OrmWallet(name='pop', balance=0)
        if not dbMember.wallets is None:
            for wallet in dbMember.wallets:
                if wallet.name == 'pop':
                    return wallet # Already added
        dbMember.wallets.append(newWallet)
        self.session.commit() # Save changes
        return newWallet

    def getCredit(self, memberId):
        wallet = self.__findWallet__(memberId)
        if wallet is None:
            return None
        return wallet.balance

    def awardCredit(self, memberId, cents):
        wallet = self.__findWallet__(memberId)
        if not wallet is None:
            wallet.balance += cents
            self.session.commit()
        else:
            raise Error("Could not find wallet for member %s" % str(memberId))

    def setCredit(self, memberId, cents):
        wallet = self.__findWallet__(memberId)
        if not wallet is None:
            wallet.balance = cents
            self.session.commit()
        else:
            raise Error("Could not find wallet for member %s" % str(memberId))

    def shutdown(self):
        return # Nothing to do?

# TODO: Are these best placed here?
Base = declarative_base()
class OrmWallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    balance = Column(Integer)

    def __repr__(self):
        return "<Wallet(name='%s', balance='%i')>" % (self.name, self.balance)

class OrmMember(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    fob_field = Column(String)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))

    wallets = relationship("OrmWallet", backref=backref('wallets', order_by=id), uselist=True)

    def __repr__(self):
        return "<User(nickname='%s', fob='%s')>" % (self.nickname, self.fob_field)
