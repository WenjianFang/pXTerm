import paramiko
import wx
import select
import sys
import tty
import termios
import logging

logger = logging.getLogger('pXTermSSH')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

class pXTermSSH:
    def connect_session(self, connectedSession, ip, user, passwd, port=22):
        # create a socket
        trans = paramiko.Transport((ip, port))
        # start a client
        trans.start_client()
        #
        trans.auth_password(username=user, password=passwd)
        #
        channel = trans.open_session()
        #
        channel.get_pty()
        #
        channel.invoke_shell()

        shell_win = wx.TextCtrl(connectedSession, size=(140, -1))

        # get original term's config
        #oldtty = termios.tcgetattr(sys.stdin)
        try:
            # set the config to remote
            #tty.setraw(sys.stdin)
            channel.settimeout(0)

            while True:
                readlist, writelist, errlist = select.select([channel, sys.stdin,], [], [])
                # if input, the stdin would change
                if sys.stdin in readlist:
                    # read the cmd
                    input_cmd = sys.stdin.read(1)
                    # send cmd to server
                    channel.sendall(input_cmd)

                # select know the result, and read the channel data
                if channel in readlist:
                    # receive result
                    result = channel.recv(1024)
                    # close and exit
                    if len(result) == 0:
                        print("\r\n**** EOF **** \r\n")
                        break
                    # standard output
                    #wx.StaticText(connectedSession, label=result)
                    shell_win.SetValue(result)
                    sys.stdout.write(result)
                    sys.stdout.flush()
        finally:
            # recover original terminal
            logger.info("finally")
            #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

        # close channel
        channel.close()
        # close trans
        trans.close()