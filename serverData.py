from ibapi import order_condition
from ibapi.message import IN
from ibapi.order import OrderComboLeg
from ibapi.contract import ContractDescription
from ibapi.contract import ComboLeg
from ibapi.server_versions import * # @UnusedWildImport
from ibapi.softdollartier import SoftDollarTier
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue
from ibapi.scanner import ScanData
from ibapi.errors import BAD_MESSAGE
from ibapi.common import * # @UnusedWildImport
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
import inspect
import time
import sys
import os

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    @iswrapper
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        print("Account list:", accountsList)
        # ! [managedaccounts]

        self.account = accountsList.split(",")[0]

    @iswrapper
    def nextValidId(self, orderId:int):
        print("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # here is where you start using api
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
    def interpret(fields):
        if len(fields) == 0:
            return
        
        sMsgId = fields[0]
        nMsgId = int(sMsgId)
        print(nMsgId)

    
    app = TestApp()
    app.connect("127.0.0.1", 4002, 31)
    time.sleep(30)
    while not app.reader.msg_queue.empty():
        interpret(app.reader.msg_queue.get())
    app.run()

if __name__ == "__main__":
    main()
