import socket
import sys
from collections import deque
import json
import ast

trader_to_exchange = [deque() for _ in range(100)]
exchange_to_trader = [deque() for _ in range(100)]
client_counter = 0




class socket:
    AF_INET = 1
    SOCK_STREAM = 2
    SOL_SOCKET = 3
    SO_REUSEADDR = 4
    def __init__(self):
        global client_counter
        self.connected=False
        self.max_connection=0
        self.accepted=False
        self.host = None
        self.port = None
        self.binded = False
        self.issetsockopt = False
        self.id = client_counter
        client_counter+=1
    @staticmethod
    def socket(typeconnection, protocol):
        if socket.AF_INET == typeconnection and \
                socket.SOCK_STREAM == protocol:
            return socket()
        else:
            print("not the right protocol") # check connection type and protocol

    def setsockopt(self,a, b, c):
        if a!=socket.SOL_SOCKET:
            print('not the right arg')
            exit(0)
        if b!=socket.SO_REUSEADDR:
            print('not the right arg')
            exit(0)
        if c!=1:
            print('not the right arg')
            exit(0)
        self.issetsockopt=True # check the parameters

    def connect(self,hostport):# connection
        if hostport[0]!="localhost" and \
                hostport[0] != "127.0.0.1":
            print("the IP address is incorrect")
            sys.exit(0)
        if hostport[1]!= 9999:
            print("server not reachable")
            sys.exit(0)
        self.host = hostport[0]
        self.port = hostport[1]
        self.connected=True 

    def sendall(self,text):
        if not self.connected:
            print('not connected')
            exit(0)
        if type(text)!=bytes:
            print("data incorrect type")
            sys.exit(0)
        trader_to_exchange[self.id].appendleft(text)
        # append the order to trader_to_exchange
        # exchange receive orders from trader
        
    def recv(self, buffersize):
        if not self.connected:
            print('not connected')
            exit(0)
        if exchange_to_trader[self.id]:
            received_message=exchange_to_trader[self.id].pop()
            return received_message
        return None
        # if there are orders in exchange, that order can be sent back to trader, so it's poped
        # return the poped order
    
    def close(self):
        self.connected = False
        # close the connection
        
    def listen(self,number):
        self.max_connection=number
        # max time of signal receiving times
        
    def accept(self):
        if not self.max_connection:
            print("you need to define listen before")
            exit(0)
        if not self.binded:
            print("a server must bind a host and a port")
            exit(0)
        if client_counter>self.max_connection:
            print("too many open connections")
            exit(0)
        return exchange_to_trader,trader_to_exchange
    # return 2 lists
    
    def bind(self,hostport):
        self.binded = True
        self.host=hostport[0]
        self.port = hostport[1]
       # bind the nost and port locations 
        
#%%

class Exchange:
    HOST, PORT = '127.0.0.1', 9999

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connection
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sock.bind((Exchange.HOST, Exchange.PORT)) # bind in server
        self.sock.listen(5) # set the maximum receiving numbers
        self.list_traders = None
        self.list_orders = []
    def update_traders(self):
        self.list_traders=self.sock.accept()
    def handle_traders(self):
        count = 0
        for trader in self.list_traders[1]: # trader who sell stocks
            if trader:
                received_message= trader.pop().decode("utf-8")
                received_message = json.dumps(ast.literal_eval(received_message))
                # pop selling-order's info
                a=json.loads(received_message)
                # transfer
                self.list_orders.append(a)
                ct=0
                for t in self.list_traders[0]:
                    if ct!=count:
                        t.appendleft(received_message)
                    ct+=1 # sell out
            count+=1 # trader's number

#%%


# Enter your code here. Read input from STDIN. Print output to STDOUT

class Trader:
    def __init__(self,i):
        HOST, PORT = "127.0.0.1", 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connection
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.id = i
        self.sock.connect((HOST, PORT))
        
    def send_order(self,side):
        self.sock.sendall(bytes(str({'price' : 1, 'quantity' : 100, 'side' : side , 'id' : self.id}),"utf-8"))
    def listen_market(self):
        a = self.sock.recv(1024)
        return str(a)
        
    def trade(self):
        if self.id == 0:
            self.send_order('sell')
            if self.sock.recv(1024) != None:
                self.send_order('buy')
            
        else:
            self.send_order('buy')
         
           
            
    

#%%
def test1():
    ex1=Exchange()
    traders=[]
    for i in range(3):
        traders.append(Trader(i))
    ex1.update_traders() # list the trader

    for t in traders:
        t.trade()
        ex1.handle_traders()

    print(ex1.list_orders)


def test2():
    ex1 = Exchange()
    traders = []
    for i in range(3):
        traders.append(Trader(i))
    ex1.update_traders()

    for t in traders:
        t.trade()
        ex1.handle_traders()

    for t in traders:
        t.trade()
        ex1.handle_traders()

    print(ex1.list_orders)


if __name__ == '__main__':
    test_number = 2
    globals()['test'+str(test_number)]()
    
    
    # [{'price': 1, 'quantity': 100, 'side': 'sell', 'id': 0},
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 1}, 
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 2}]
    
    
    # [{'price': 1, 'quantity': 100, 'side': 'sell', 'id': 0}, 
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 1},
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 2}, 
    #  {'price': 1, 'quantity': 100, 'side': 'sell', 'id': 0},
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 0}, 
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 1}, 
    #  {'price': 1, 'quantity': 100, 'side': 'buy', 'id': 2}]