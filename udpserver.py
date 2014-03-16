"""
Recent Changes IRC Bot
Gets recent changes through UDP server defined in LocalSettings
Outputs to IRC server/channel as defined
Based on https://www.mediawiki.org/wiki/User:Thrasher6670/IRC_RC_Bot
"""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.words.protocols import irc
from twisted.internet import protocol
import sys
 
recver = None
 
class RCBot(irc.IRCClient):
    nickname = raw_input("Nickname: ")
    channel = raw_input("Channel: ")
    def signedOn(self):
        global recver
        self.join(self.channel)
        print "Signed on as %s." % (self.nickname,)
        recver = self
        identify = raw_input("Identify to services? Enter password: ")
        self.msg("NickServ","IDENTIFY %s " % (identify,))
        
    def joined(self, channel):
        print "Joined %s." % (channel,)
 
    def gotUDP(self, broadcast):
        self.msg(self.channel, broadcast)
 
class RCFactory(protocol.ClientFactory):
    protocol = RCBot
 
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
 
class Echo(DatagramProtocol):
 
    def datagramReceived(self, data, (host, port)):
        global recver
        recver.gotUDP(data)
 
reactor.listenUDP(51666, Echo())
reactor.connectTCP("irc.freenode.net", 6667, RCFactory())
reactor.run()
