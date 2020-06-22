# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from typing import Text, List, Dict, Any
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
import mysql.connector
      
class ActionAskInfo(Action):
    def name(self) -> Text:
        return "action_ask_info"

    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        slots = {}
        for key in ['brand','tel_name','category','addition']:
            value = tracker.get_slot(key)
            if(value is not None):
                slots[key] = str(value)
            else:
                slots[key] = ''
                
        brand = slots['brand']
        telName = slots['tel_name']
        category = slots['category']
        addition = slots['addition']
        mess = "Sorry we dont have"
        sql_query = "SELECT detail from info where (info.phoneName = '" + telName + "')"
        if(brand != ''):
            sql_query = sql_query + "and (info.brand = '" + brand + "')"
            mess = mess + " " + brand
        if(category != ''):
            sql_query = sql_query + "and (info.category = '" + category + "')"
            mess = mess + " " + category
        if(telName != ''):
            mess = mess + " " + telName
        if(addition != ''):
            sql_query = sql_query + "and (info.addition = '" + addition + "')"
            mess = mess + " " + addition
        
        myconn = mysql.connector.connect(host = "localhost",user = "root", passwd="ngonhatminh000.",database = "data")
        print(myconn)
        cur = myconn.cursor()
        result = ""
        try:
            cur.execute(sql_query)
            result = cur.fetchall()[0][0]
        except:
            myconn.rollback()
            
        myconn.close()
        if(result == ""):
            mess = mess + " by now"
        else:
            mess = "Click link below for more info\n"+result
        dispatcher.utter_message(text = mess)
        return [AllSlotsReset()]
        
class ActionAskTime(Action):
    def name(self) -> Text:
        return "action_ask_time"
    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        weekday = tracker.get_slot('weekday')
        weekend = tracker.get_slot('weekend')
        if(weekday is not None):
            mess = "yes we open in " + weekday + " from 7AM to 10PM"
            weekday = None
        elif(weekend is not None):
            mess = "Sorry we dont open in " + weekend
            weekday = None
        else:
            mess = " "
        dispatcher.utter_message(text = mess)
        return [AllSlotsReset()]

class ActionAskByPrice(Action):
    def name(self) -> Text:
        return "action_ask_by_price"
    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        value = int(tracker.get_slot("price"))
        
        myconn = mysql.connector.connect(host = "localhost",user = "root", passwd="ngonhatminh000.",database = "data")
        print(myconn)
        cur = myconn.cursor()
        sql_query = cur.execute("SELECT detail from info where (info.price > "+str(value*0.8)+") and (info.price <"+str(value*1.2)+")")
        result = ""
        try:
            cur.execute(sql_query)
            result = cur.fetchall()
        except:
            myconn.rollback()
            
        myconn.close()
        if(len(result)==0):
            mess = "Sorry we dont have anything in that price"
        else:
            mess = "By price " + str(value)+ " $ we have something here for u.\n"
            for i in result:
                mess = mess + i[0] +"\n"
        dispatcher.utter_message(text = mess)
        return [AllSlotsReset()]
