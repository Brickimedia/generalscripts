#!/usr/bin/perl

# NOTE: This script is an alternative to udpserver.py
#       Do not use it unless udpserver.py fails

use warnings;
use strict;

use POE;
use IO::Socket::INET;
use POE::Component::IRC;

use constant DATAGRAM_MAXLEN => 1024;

select((select(STDOUT), $|=1)[0]);


# Create the component that will represent an IRC network.
my ($irc) = POE::Component::IRC->spawn;

# Create the bot session.  The new() call specifies the events the bot
# knows about and the functions that will handle those events.
POE::Session->create(
                     inline_states => {
        _start     => \&bot_start,
        irc_001    => \&on_connect,
        irc_public => \&on_public,
    },
                     );

POE::Session->create(
    inline_states => {
        _start       => \&server_start,
        get_datagram => \&server_read,
      }
);

$poe_kernel->run;

exit;


# UDP Server
sub server_start {
    my $kernel = $_[KERNEL];

    my $socket = IO::Socket::INET->new(
        Proto     => 'udp',
        LocalPort => 51666,
    );

    die "Couldn't create server socket: $!" unless $socket;
    $kernel->select_read( $socket, "get_datagram" );
}

sub server_read {
    my ( $kernel, $socket ) = @_[ KERNEL, ARG0 ];
    my $ircmessage = "";
    recv( $socket, my $message = "",  DATAGRAM_MAXLEN, 0 );
    $message =~ /\[\[(.+)\]\]/s;
    $ircmessage = $1;
    $irc->yield( privmsg => "#brickimedia-cvn", $ircmessage );

}



# IRC Server

# The bot session has started.  Register this bot with the "magnet"
# IRC component.  Select a nickname.  Connect to a server.
sub bot_start {
    my $kernel  = $_[KERNEL];
    my $heap    = $_[HEAP];
    my $session = $_[SESSION];

    $irc->yield( register => "all" );

    my $nick = 'MeikoBot';
    $irc->yield( connect =>
                 { Nick => $nick,
            Username => 'MeikoBot',
            Ircname  => 'MeikoBot',
            Server   => 'irc.freenode.net',
            Port     => '6667',
               }
                 );
}

# The bot has successfully connected to a server.  Join a channel.
sub on_connect {
    $irc->yield( join => "#brickimedia-cvn" );
}

# The bot has received a public message.  Parse it for commands, and
# respond to interesting things.
sub on_public {
    my ( $kernel, $who, $where, $msg ) = @_[ KERNEL, ARG0, ARG1, ARG2 ];
    my $nick = ( split /!/, $who )[0];
    my $channel = $where->[0];

    my $ts = localtime;
    print " [$ts] <$nick:$channel> $msg\n";
}
