from twisted.application import internet, service
from server import callFactory

application = service.Application("server")
echoService = internet.TCPServer(5678, callFactory())
echoService.setServiceParent(application)