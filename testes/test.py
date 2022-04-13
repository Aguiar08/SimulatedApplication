
"""
An example of reading a line at a time from standard input
without blocking the reactor.
"""

from twisted.internet import stdio
from twisted.protocols import basic
from twisted.internet import reactor

class Echo(basic.LineReceiver):
    from os import linesep as delimiter
    def connectionMade(self):
        self.transport.write(b'>>> ')

    def lineReceived(self, line):
        self.sendLine('Echo: ' + line)
        self.transport.write(b'>>> ')

def main():
    stdio.StandardIO(Echo())
    reactor.run()

if __name__ == '__main__':
    main()