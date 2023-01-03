import hashlib
import os

# stm: member state
def unwind(stm) -> bytes:
    _stm = hashlib.sha1(stm)
    return _stm.digest()

class PublisherState:
    def __init__(self, mw):
        self.i = 0
        self.stms = [None] * mw
        self.stms[-1] = os.urandom(20) # 160 bit

        for i in reversed(list(range(0, mw-1))):
            self.stms[i] = unwind(self.stms[i+1])

    # stp: publisher state
    # returns new publisher state and a member state
    def wind(self):
        self.i += 1
        return (self, self.stms[self.i])

def keyder(stm: bytes):
    sha1 = hashlib.sha1(bytes([0]*8) + stm)
    return sha1.digest()

if __name__ == "__main__":
    stp = PublisherState(5)
    last_stm = None

    for i in range(4):
        (stp_next, stm) = stp.wind()
        last_stm = stm
        stp = stp_next
        key = keyder(stm)
        print(key)

    assert unwind(last_stm) == stp.stms[3]
    assert unwind(unwind(last_stm)) == stp.stms[2]
    assert unwind(unwind(unwind(last_stm))) == stp.stms[1]