#!/bin/python3

import math
import os
import random
import re
import sys
import json
import unittest





# you will need to pass the test cases below. test_D will be called 4 different times to test that orders are
# handled properly. test_B, C, and D will each be called once to ensure that all handle methods are impelemented.

class OrderBook:
    def __init__(self):
        self.list_asks = []
        self.list_bids = []
        # the list of bids and offers is self explanatory. 
        # the orders attribute keeps a record of all the orders where they key is the order id and the
        # value is the order. If used correctly, this should help you implement the handle methods below.
        self.orders = {}
    def handle_order(self,o):
        if o['action']=='new':
            self.handle_new(o)
        elif o['action']=='modify':
            self.handle_modify(o)
        elif o['action']=='delete':
            self.handle_delete(o)
        else:
            print('Error-Cannot handle this action')
            
    def handle_new(self,o):
        self.orders[o['id']] = o
        if o['side'] == 'bid':
            self.list_bids.append(o)
            self.list_bids.sort(key = lambda x: x['price'],reverse = True)
        elif o['side'] == 'ask':
            self.list_asks.append(o)
            self.list_asks.sort(key = lambda x: x['price'],reverse = False)
        
        

    def handle_modify(self,o):
        if self.orders[o['id']]['side']=='bid':
            for i in self.list_bids:
                if i['id'] == o['id']:
                    i['quantity'] = o['quantity']
                    break
        elif self.orders[o['id']]['side']=='ask':
            for i in self.list_asks:
                if i['id'] == o['id']:
                    i['quantity'] = o['quantity']
                    break


    def handle_delete(self,o):
        if self.orders[o['id']]['side']=='bid':
            for i in self.list_bids:
                if i['id'] == o['id']:
                    self.list_bids.remove(i)
                    del self.orders[o['id']]
                    break
        elif self.orders[o['id']]['side']=='ask':
            for i in self.list_asks:
                if i['id'] == o['id']:
                    self.list_asks.remove(i)
                    del self.orders[o['id']]
                    break
        

    def find_order_in_a_list(self,o,lookup_list = None):
        pass

    def display_content(self,fptr):
    # you certainly don't need to touch this part
        fptr.write('BIDS\n')
        for o in self.list_bids:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))
        fptr.write('OFFERS\n')
        for o in self.list_asks:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))
            




        
def test_A():
    ob = OrderBook()
    orders = json.loads(input().strip())
    for o in orders:
        ob.handle_new(o)
    if (orders[0]['id'] in ob.orders.keys()) and (orders[0] in ob.list_bids):
        print(f"Implemented handle_new: True")
    else: print(f"Implemented handle_new: False")
    

def test_B():
    ob = OrderBook()
    mod_orderid = None
    orders = json.loads(input().strip())
    while True:
        for order in orders:
            if order['action'] == 'modify':
                ob.handle_modify(order)
                mod_orderid = order['id']
                break
            ob.handle_order(order)
        break
    mod_order = ob.orders.get(mod_orderid, None)
    if (ob.orders[mod_orderid]['quantity'] == 20) and (mod_order in ob.list_bids):
            print(f"Implemented handle_modify: True")
    else: print(f"Implemented handle_modify: False")
    
    
def test_C():
    ob = OrderBook()
    del_orderid = None
    orders = json.loads(input().strip())
    while True:
        for order in orders:
            if order['action'] == 'delete':
                ob.handle_delete(order)
                del_orderid = order['id']
                break
            ob.handle_order(order)
        break
    del_order = ob.orders.get(del_orderid, None)
    if (not del_order) and (del_order not in ob.list_bids):
            print(f"Implemented handle_delete: True")
    else: print(f"Implemented handle_delete: False")
    
    
def test_D():
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    order_book = OrderBook()

    order_list_from_file = input().strip()

    json_order_list=json.loads(order_list_from_file)
    for order in json_order_list:
        order_book.handle_order(order)
        
    order_book.display_content(fptr)

    fptr.close()
    
# def test_B():
#     orderbook_test = unittest.TestLoader().loadTestsFromTestCase(OrderBookTest)
#     unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(orderbook_test)
    



if __name__ == '__main__':
    letter = sys.stdin.readline().strip()
    globals()['test_' + letter]()

    
