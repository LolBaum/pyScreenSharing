import socket
import sys


system_args = sys.argv[1:]
if len(system_args) == 0:
    SERVER = "127.0.0.1"
elif len(system_args) >= 1:
    SERVER = system_args[0]


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = "10.10.5.59"
ADDR = (SERVER, PORT)

print(f"connecting to {SERVER} on port {PORT}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class Command:
    def __init__(self, _name: str, _keywords: list, _short_description: str,
                 _func, _has_args=False, _infotext: str = "") -> None:
        self.name = _name
        self.keywords = _keywords
        self.short_description = _short_description
        if _infotext != "":
            self.infotext = _infotext
        else:
            self.infotext = self.short_description

        self.has_args = _has_args
        self.function = _func

    def __eq__(self, cmd: str):
        return cmd in self.keywords

    def info_short(self):
        print(f"{self.name}: {' '.join(self.keywords)} - {self.short_description}")

    def info(self):
        print(f"[info] Command: {self.name}")
        print("keywords: ", self.keywords)
        print(self.infotext)


class CommandList:
    def __init__(self):
        self.commands = []
        self.load_commands()

    def load_commands(self):
        self.commands.append(Command("Disconnect",
                                     ["/d", "/disconnect"],
                                     "closes the connection to the server",
                                     disconnect))
        self.commands.append(Command("Exit",
                                     ["/q", "/quit", "/exit"],
                                     "terminates the program",
                                     end_program))

    def find_cmd(self, cmd: str):
        command = None
        for c in self.commands:
            if cmd == c:
                command = c
                break
        return command

    def print_help(self):
        print("[Info] what can you do?")
        print("1.\ttype a message and press Enter to send the msg\n"
              "\tas plain text to the server")
        print("2.\tstart your msg with an / to use a command")
        for cmd in self.commands:
            cmd.info_short()

def run_cmd(cmd: Command, args=None):
    if cmd.has_args:
        cmd.function(args)
    else:
        cmd.function()




def end_program():
    print("exiting.")
    send(DISCONNECT_MESSAGE)
    exit()

def disconnect():
    print("closing connection")
    send(DISCONNECT_MESSAGE)

def help():
    CommandList.print_help()





def send(msg):
    print("sending: ", msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))





def main_console_input():
    commands = CommandList()
    commands.print_help()
    running = True
    while running:
        user_input = input(">>> ")
        if user_input[0] == "/":
            user_input_separated = user_input.split()
            cmd_string = user_input_separated[0]
            args = user_input_separated[1:]
            cmd = commands.find_cmd(cmd_string)
            if cmd != None:
                run_cmd(cmd, args)
            else:
                print(cmd_string, " not found")
        else:
            send(user_input)


main_console_input()

#send(DISCONNECT_MESSAGE)