from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        #here is where you start using api
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        self.reqMktData(1101, contract, "", False, False, None)

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price)
        #this will disconnect and end this program because loop finishes
        self.done = True

def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 3)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()
