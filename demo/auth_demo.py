# -*- coding: utf-8 -*-
import thosttraderapi as api
'''
穿透式版本认证及报单demo，用于6.3.13及以上版本API
'''
#Addr
FrontAddr="tcp://180.168.146.187:10101"
#LoginInfo
BROKERID="9999"
USERID="070624"
PASSWORD="070624"
#OrderInfo
EXCHANGEID="SHFE"
INSTRUMENTID="rb1909"
PRICE=3200
VOLUME=1
DIRECTION=api.THOST_FTDC_D_Sell
#DIRECTION=api.THOST_FTDC_D_Buy
#open
OFFSET="0"
#close
#OFFSET="1"

#USERID="148#865#Trim"
#PASSWORD="Af8236CTP#Trim"
'''
Testing on 2019/08/03
注册账号：137~3417
用户昵称：YF
investorId：148865
brokerId：9999
挂靠会员：SimNow 

'''

def ReqorderfieldInsert(tradeapi):
	print ("ReqOrderInsert Start")
	orderfield=api.CThostFtdcInputOrderField()
	orderfield.BrokerID=BROKERID
	orderfield.ExchangeID=EXCHANGEID
	orderfield.InstrumentID=INSTRUMENTID
	orderfield.UserID=USERID
	orderfield.InvestorID=USERID
	orderfield.Direction=DIRECTION
	orderfield.LimitPrice=PRICE
	orderfield.VolumeTotalOriginal=VOLUME
	orderfield.OrderPriceType=api.THOST_FTDC_OPT_LimitPrice
	orderfield.ContingentCondition = api.THOST_FTDC_CC_Immediately
	orderfield.TimeCondition = api.THOST_FTDC_TC_GFD
	orderfield.VolumeCondition = api.THOST_FTDC_VC_AV
	orderfield.CombHedgeFlag="1"
	orderfield.CombOffsetFlag=OFFSET
	orderfield.GTDDate=""
	orderfield.orderfieldRef="1"
	orderfield.MinVolume = 0
	orderfield.ForceCloseReason = api.THOST_FTDC_FCC_NotForceClose
	orderfield.IsAutoSuspend = 0
	tradeapi.ReqOrderInsert(orderfield,0)
	print ("ReqOrderInsert End")
	

class CTradeSpi(api.CThostFtdcTraderSpi):
	tapi=''
	def __init__(self,tapi):
		api.CThostFtdcTraderSpi.__init__(self)
		self.tapi=tapi
		
	def OnFrontConnected(self) -> "void":
		print ("OnFrontConnected")
		authfield = api.CThostFtdcReqAuthenticateField();
		authfield.BrokerID=BROKERID
		authfield.UserID=USERID
		authfield.AppID="simnow_client_test"
		authfield.AuthCode="0000000000000000"
		self.tapi.ReqAuthenticate(authfield,0)
		print ("send ReqAuthenticate ok")
		
	def OnRspAuthenticate(self, pRspAuthenticateField: 'CThostFtdcRspAuthenticateField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":	
		print ("BrokerID=",pRspAuthenticateField.BrokerID)
		print ("UserID=",pRspAuthenticateField.UserID)
		print ("AppID=",pRspAuthenticateField.AppID)
		print ("AppType=",pRspAuthenticateField.AppType)		
		print ("ErrorID=",pRspInfo.ErrorID)
		print ("ErrorMsg=",pRspInfo.ErrorMsg)
		if not pRspInfo.ErrorID :
			loginfield = api.CThostFtdcReqUserLoginField()
			loginfield.BrokerID=BROKERID
			loginfield.UserID=USERID
			loginfield.Password=PASSWORD
			loginfield.UserProductInfo="python dll"
			self.tapi.ReqUserLogin(loginfield,0)
			print ("send login ok")
		
	def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		print ("OnRspUserLogin")
		print ("TradingDay=",pRspUserLogin.TradingDay)
		print ("SessionID=",pRspUserLogin.SessionID)
		print ("ErrorID=",pRspInfo.ErrorID)
		print ("ErrorMsg=",pRspInfo.ErrorMsg)

		qryinfofield = api.CThostFtdcQrySettlementInfoField()
		qryinfofield.BrokerID=BROKERID
		qryinfofield.InvestorID=USERID
		qryinfofield.TradingDay=pRspUserLogin.TradingDay
		self.tapi.ReqQrySettlementInfo(qryinfofield,0)
		print ("send ReqQrySettlementInfo ok")
		

	def OnRspQrySettlementInfo(self, pSettlementInfo: 'CThostFtdcSettlementInfoField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		print ("OnRspQrySettlementInfo")
		if  pSettlementInfo is not None :
			print ("content:",pSettlementInfo.Content)
		else :
			print ("content null")
		pSettlementInfoConfirm=api.CThostFtdcSettlementInfoConfirmField()
		pSettlementInfoConfirm.BrokerID=BROKERID
		pSettlementInfoConfirm.InvestorID=USERID
		self.tapi.ReqSettlementInfoConfirm(pSettlementInfoConfirm,0)
		print ("send ReqSettlementInfoConfirm ok")
		
	def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm: 'CThostFtdcSettlementInfoConfirmField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		print ("OnRspSettlementInfoConfirm")
		print ("ErrorID=",pRspInfo.ErrorID)
		print ("ErrorMsg=",pRspInfo.ErrorMsg)
		ReqorderfieldInsert(self.tapi)
		print ("send ReqorderfieldInsert ok")


	def OnRtnOrder(self, pOrder: 'CThostFtdcOrderField') -> "void":
		print ("OnRtnOrder")
		print ("OrderStatus=",pOrder.OrderStatus)
		print ("StatusMsg=",pOrder.StatusMsg)
		print ("LimitPrice=",pOrder.LimitPrice)
		
	def OnRspOrderInsert(self, pInputOrder: 'CThostFtdcInputOrderField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
		print ("OnRspOrderInsert")
		print ("ErrorID=",pRspInfo.ErrorID)
		print ("ErrorMsg=",pRspInfo.ErrorMsg)
		
def main():
	tradeapi=api.CThostFtdcTraderApi_CreateFtdcTraderApi()
	tradespi=CTradeSpi(tradeapi)
	tradeapi.RegisterFront(FrontAddr)
	tradeapi.RegisterSpi(tradespi)
	tradeapi.SubscribePrivateTopic(api.THOST_TERT_QUICK)
	tradeapi.SubscribePublicTopic(api.THOST_TERT_QUICK)
	tradeapi.Init()
	tradeapi.Join()
	
if __name__ == '__main__':
	main()