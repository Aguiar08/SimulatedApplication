import json

a = json.dumps({"command" : "hangup" , "id" : "1"})
b = json.loads(a)
print(b["command"])