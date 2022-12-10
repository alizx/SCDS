import hashlib
import os

def unwind(stm):
    _stm = hashlib.sha1(stm)
    return _stm.digest()

class PublisherState:
  def __init__(self, mw):
    self.i = 0
    self.stms = [None] * mw
    self.stms[mw-1] = os.urandom(20) # 160 bit

    for i in reversed(list(range(0,mw-1))):
        self.stms[i] = unwind(self.stms[i+1])
    

def wind(stp: PublisherState):
    i = stp.i
    stp.i += 1
    return (stp,stp.stms[i])

def keyder(stm):
    sha1 = hashlib.sha1(bytes([0]*8) + stm)
    return sha1.digest()

stp = PublisherState(5)

last_stm = None
for i in range(2):
    (stp_next, stm) = wind(stp)
    last_stm = stm
    stp = stp_next
    key = keyder(stm)
    print(key)

assert unwind(last_stm) == stp.stms[1]
assert stp.i == 1

