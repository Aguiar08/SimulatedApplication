import cmd

#=========================== Classe Call =============================    

class Call:
        def __init__(self, id):
            self.id = id
            self.operator = ""
            self.state = "calling"
        def callMade(self):
            print("Call "+ self.id +" received")
        def callReceived(self, operator):
            self.operator = operator
            print("Call " + self.id + " ringing for operator " + self.operator)
        def callAnswered(self):
            self.state = "answered"
        def callFinished(self):
            if (self.state == "calling"):
                print("Call " + self.id + " missed")
                return False
            return True  
        def callWaiting(self):
            print("Call "+ self.id +" waiting in queue")
            
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
            print("Call " + self.call + " answered by operator " + self.id)
        def callRejected(self):
            self.state = "available"
            print("Call " + self.call + " rejected by operator " + self.id)
        def callFinished(self):
            self.state = "available"
            print("Call " + self.call + " finished and operator " + self.id + " available")
        def callHangUp(self):
            self.state = "available"
            self.call = ""
            
#=========================== Funções =============================                

calls = []
operators = []
queue = []
A = Operator("A")
B = Operator("B")
operators.append(A)
operators.append(B)

def call(id): 
    try:
        int(id)
    except:
        print("Please insert valid call number")
        return
    call = Call(id)
    call.callMade()
    calls.append(call)
    receive(call)
    return
            
def answer(id):
    for operator in operators:
        if (operator.id == id):
            operator.callAnswered()
            c = findCall(operator.call)
            c.callAnswered()
            return
            
def reject(id):
    for operator in operators:
        if (operator.id == id):
            c = findCall(operator.call)
            operator.callRejected()
            receive(c)  
            return
            
def hangup(call):
    c = findCall(call)
    if(c.callFinished()):
        for operator in operators:
            if (operator.call == call):
                operator.callFinished() 
                if(len(queue) > 0):
                    receive(queue[0])
                    queue.pop(0)
                return
    else:
        for q in range(len(queue)):
            if (queue[q] == c):
                queue.pop(q)
        for operator in operators:
            if (operator.call == call):
                operator.callHangUp() 
                if(len(queue) > 0):
                    receive(queue[0])
                    queue.pop(0)
                return
        
def receive(call):
    for operator in operators:
        if (operator.state == "available"):
            call.callReceived(operator.id)
            operator.callReceived(call.id)
            return
    call.callWaiting()
    queue.append(call)
    return

def findCall(arg):
    for c in calls:
        if(arg == c.id):
            return c
    
class Commands(cmd.Cmd):
    prompt = '(Basic) '
    
    def do_call(self, arg):
        call(arg)
    def do_answer(self, arg):
        answer(arg)
    def do_reject(self, arg):
        reject(arg)
    def do_hangup(self, arg):
        hangup(arg)
        
a = "call 1"
Commands().onecmd(a)
        