from twisted.application import internet, service
from echo import EchoFactory

application = service.Application("server")
echoService = internet.TCPServer(8000, callClientFactory())
echoService.setServiceParent(application)