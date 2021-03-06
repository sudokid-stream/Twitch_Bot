import logging
import socket


logger = logging.getLogger(__name__)


class IRC:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, server, port, nick, channel, auth):
        self.server = server
        self.port = port
        self.channel = channel
        self.nick = nick
        self.auth = auth

    def format_msg(self, msg: str):
        formatted_msg = f'PRIVMSG #{self.channel} :{msg}\r\n'
        return formatted_msg.encode()

    def ping(self):
        self.irc.send(b'PONG :tmi.twitch.tv\r\n')

    def send(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')

        formatted_msg = self.format_msg(msg)
        print(formatted_msg)
        self.irc.send(self.format_msg(msg))

    @staticmethod
    def get_user_from_msg(user):
        return user.split('!')

    def connect(self):
        password = f'PASS {self.auth}\r\n'.encode()
        nick = f'NICK {self.nick}\r\n'.encode()
        channel = f'JOIN #{self.channel}\r\n'.encode()

        self.irc.connect((self.server, self.port))
        self.irc.send(password)
        self.irc.send(nick)
        self.irc.send(channel)

    def disconnect(self):
        self.irc.send(f'PART #{self.channel}'.encode())
        logger.info(f'disconnected from channel {self.channel}')

    def get_msg(self):
        response = self.irc.recv(2048).decode().strip('\r\n')
        print(response)
        try:
            user, msg = response.split(':', 2)[1:]
            return self.get_user_from_msg(user), msg
        except ValueError:
            return '', response
