#!/usr/bin/python
#

from mockSSH import SSHCommand, commands, runServer

class command_passwd(SSHCommand):
    def start(self):
        self.passwords = []
        if len(self.args) == 1:
            self.username = self.args[0] 
            self.writeln("Changing password for user %s." % self.username)
            self.write("New BIG-IP password: ")
            self.protocol.password_input = True
            self.callbacks = [self.ask_again, self.finish]
        else:
            self.writeln("mockSSH: Supported usage: passwd <username>")
            self.exit()

    def ask_again(self):
        self.write('Retype new BIG-IP password: ')

    def finish(self):
        self.protocol.password_input = False

        if self.passwords[0] != self.passwords[1]:
            self.writeln("Sorry, passwords do not match")
            self.writeln("passwd: Authentication token manipulation error")
            self.writeln("passwd: password unchanged")
            self.exit()
        else:
            self.writeln("Changing password for user %s." % self.username)
            self.writeln("passwd: all authentication tokens updated successfully.")
            self.exit()

    def lineReceived(self, line):
        print 'INPUT (passwd):', line
        self.passwords.append(line.strip())
        self.callbacks.pop(0)()

def main():
    commands['passwd'] = command_passwd
    users = {'testadmin': 'x'}
    runServer(prompt="[root@hostname:Active] testadmin # ",
              **users)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "User interrupted"
        sys.exit(1)
