from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
import inspect

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        print("Account list:", accountsList)
        self.account = accountsList.split(",")[0]

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        self.reqAccountSummary(2, "All", "$LEDGER")

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        print("Acct Summary. ReqId:" , reqId , "Acct:", account, 
            "Tag: ", tag, "Value:", value, "Currency:", currency)

    @iswrapper
    def accountSummaryEnd(self, reqId:int):
        print("AccountSummaryEnd. Req Id: ", reqId)
        # now we can disconnect
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 123)
    app.run()

if __name__ == "__main__":
    main()
