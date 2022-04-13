import cmd
import json
from twisted.internet import reactor, protocol


class Commands(cmd.Cmd):
    
    def do_call(self, arg):
        a = json.dumps({"command" : "call" , "id" : arg})
        a = a.encode("utf-8")
        return call(a)
    def do_answer(self, arg):
        a = json.dumps({"command" : "answer" , "id" : arg})
        a = a.encode("utf-8")
        return answer(a)
    def do_reject(self, arg):
        a = json.dumps({"command" : "reject" , "id" : arg})
        a = a.encode("utf-8")
        return reject(a)
    def do_hangup(self, arg):
        a = json.dumps({"command" : "hangup" , "id" : arg})
        a = a.encode("utf-8")
        return hangup(a)
            
 
def call(a):
    return a
def answer(a):
    return a
def reject(a):
    return a
def hangup(a):
    return a

class callProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        self.transport.write(self.factory.quote)

    def dataReceived(self, data):
        aux = json.loads(data.decode("utf-8"))
        print(aux["message"])
        line = input()
        command = Commands()
        a = command.onecmd(line)
        reactor.connectTCP('localhost', 5678, callClientFactory(a))
        self.transport.loseConnection()
        

class callClientFactory(protocol.ClientFactory):
    def __init__(self, quote):
        self.quote = quote
        
    def buildProtocol(self, addr):
        return callProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())

reactor.connectTCP('localhost', 5678, callClientFactory("Start"))
reactor.run()