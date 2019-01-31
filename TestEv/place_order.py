from ibapi.contract import *
from ContractSamples import ContractSamples
from ibapi.order import *
from ibapi.order_state import *
from ibapi.order_condition import *
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.ticktype import *
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
        self.reqOpenOrders()


    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)


    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        print("OpenOrder. ID:", orderId, "Symbol:", contract.symbol, "SecType:", contract.secType,
              "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
              "TotalQuantity:", order.totalQuantity, "Status:", orderState.status)

        if order.whatIf and orderState is not None:
            print("WhatIf. OrderId: ", orderId, "initMarginBefore:", orderState.initMarginBefore, "maintMarginBefore:", orderState.maintMarginBefore,
             "equityWithLoanBefore:", orderState.equityWithLoanBefore, "initMarginChange:", orderState.initMarginChange, "maintMarginChange:", orderState.maintMarginChange,
             "equityWithLoanChange:", orderState.equityWithLoanChange, "initMarginAfter:", orderState.initMarginAfter, "maintMarginAfter:", orderState.maintMarginAfter,
             "equityWithLoanAfter:", orderState.equityWithLoanAfter)

        order.contract = contract
        self.permId2ord[order.permId] = order
    # ! [openorder]

    @iswrapper
    # ! [openorderend]
    def openOrderEnd(self):
        super().openOrderEnd()
        print("OpenOrderEnd")

    # ! [openorderend]

    @iswrapper
    # ! [orderstatus]
    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
              "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
              "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
              lastFillPrice, "ClientId:", clientId, "WhyHeld:",
              whyHeld, "MktCapPrice:", mktCapPrice)
    # ! [orderstatus]

def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 4)
    app.run()

if __name__ == "__main__":
    main()
