import paramiko
import os
import select
import sys
import tty
import termios

# create a socket
trans = paramiko.Transport(('192.168.1.105', 22))
# start a client
trans.start_client()

# if use rsa to login
'''
default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
trans.auth_publickey(username='super', key=prikey)
'''
#
trans.auth_password(username='wenjian', password='1314')
#
channel = trans.open_session()
#
channel.get_pty()
#
channel.invoke_shell()

# get original term's config
oldtty = termios.tcgetattr(sys.stdin)
try:
    # set the config to remote
    tty.setraw(sys.stdin)
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
            sys.stdout.write(result)
            sys.stdout.flush()
finally:
    # recover original terminal
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

# close channel
channel.close()
# close trans
trans.close()