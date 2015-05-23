from member_service import MemberService
from simple_member import SimpleMember

class SimpleMemberService(MemberService):
    def getMember(self, memberId):
        if memberId == 5971042: # TODO: Remove hard-coded value
            return None
        return SimpleMember(memberId)

    def awardCredit(self, memberId, cents):
        return # TODO: Actually implement?

    def setCredit(self, memberId, cents):
        return # TODO: Actually implement?

    def shutdown(self):
        return # Nothing to do
