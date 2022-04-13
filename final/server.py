from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import json

#=========================== Classe Call =============================    

class Call:
        def __init__(self, id):
            self.id = id
            self.operator = ""
            self.state = "calling"
        def callMade(self):
            ret = ("Call "+ self.id +" received\n")
            return(ret)
        def callReceived(self, operator):
            self.operator = operator
            ret = ("Call " + self.id + " ringing for operator " + self.operator + "\n")
            return(ret)
        def callAnswered(self):
            self.state = "answered"
        def callFinished(self):
            if (self.state == "calling"):
                ret = ("Call " + self.id + " missed\n")
                return(ret)
            return "True"  
        def callWaiting(self):
            ret = ("Call "+ self.id +" waiting in queue\n")
            return(ret)
        def callIgnored(self):
            self.state = "ignored"
            ret = ("Call "+ self.id +" ignored by operator " + self.operator+ "\n")
            return(ret)
            
##=========================== Classe Operator =============================                
            
class Operator:
        def __init__(self, id):
            self.id = id
            self.state = "available"
            self.call = ""
        def callReceived(self, call):
            self.state = "ringing"
            self.call = call
        def callAnswered(self):
            self.state = "busy"
            ret = ("Call " + self.call + " answered by operator " + self.id+"\n")
            return(ret)
        def callRejected(self):
            self.state = "available"
            ret = ("Call " + self.call + " rejected by operator " + self.id+"\n")
            return(ret)
        def callFinished(self):
            self.state = "available"
            ret = ("Call " + self.call + " finished and operator " + self.id + " available\n")
            return(ret)
        def callHangUp(self):
            self.state = "available"
            self.call = ""

class CallProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        msg = []
        data = data.decode("utf-8")
        arg = json.loads(data)
        if(arg["command"] == "call"):
            self.call(arg["id"], msg)        
        elif(arg["command"] == "answer"):
           self.answer(arg["id"], msg)        
        elif(arg["command"] == "reject"):
            self.reject(arg["id"], msg)
        elif(arg["command"] == "hangup"):
            self.hangup(arg["id"], msg)
        elif(arg["command"] == "ignored"):
            self.ignored(arg["id"], msg)
        message = ""
        for i in msg:
            message += i
        ret = (json.dumps({"message" : message})).encode("utf-8")
        self.transport.write(ret)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def ignored(self, id, msg):
        arg = self.findCall(id)
        if(arg.state == "calling"):
            msg.append(arg.callIgnored())
            for operator in self.factory.operators:
                if (operator.call == arg.id):
                    operator.callHangUp()
            if(len(self.factory.queue) > 0):
                for i in range(len(self.factory.queue)-1):
                    if(self.factory.queue[i].id == arg.id):
                        self.factory.queue.pop(i)
            return 
        
    def call(self, id, msg): 
        call = Call(id)
        msg.append(call.callMade())
        self.factory.calls.append(call)
        self.receive(call, msg)
        return

    def answer(self, id, msg):
        for operator in self.factory.operators:
            if (operator.id == id):
                msg.append(operator.callAnswered())
                c = self.findCall(operator.call)
                c.callAnswered()
                return

    def reject(self, id, msg):
        for operator in self.factory.operators:
            if (operator.id == id):
                c = self.findCall(operator.call)
                msg.append(operator.callRejected())
                self.receive(c, msg)  
                return

    def hangup(self, call, msg):
        c = self.findCall(call)
        var = c.callFinished()
        if(var == "True"):
            for operator in self.factory.operators:
                if (operator.call == call):
                    msg.append(operator.callFinished())
                    if(len(self.factory.queue) > 0):
                        self.receive(self.factory.queue[0], msg)
                        self.factory.queue.pop(0)
                    return
        else:
            msg.append(var)
            for q in range(len(self.factory.queue)):
                if (self.factory.queue[q] == c):
                    self.factory.queue.pop(q)
            for operator in self.factory.operators:
                if (operator.call == call):
                    operator.callHangUp() 
                    if(len(self.factory.queue) > 0):
                        self.receive(self.factory.queue[0], msg)
                        self.factory.queue.pop(0)
                    return

    def receive(self, call, msg):
        for operator in self.factory.operators:
            if (operator.state == "available"):
                msg.append(call.callReceived(operator.id))
                operator.callReceived(call.id)
                return
        msg.append(call.callWaiting())
        self.factory.queue.append(call)
        return

    def findCall(self, arg):
        for c in self.factory.calls:
            if(arg == c.id):
                return c
                  
class CallFactory(Factory):
    numConnections = 0
    calls = []
    operators = []
    queue = []
    A = Operator("A")
    B = Operator("B")
    operators.append(A)
    operators.append(B)

    def buildProtocol(self, addr):
        return CallProtocol(self)

reactor.listenTCP(5678, CallFactory())
reactor.run()