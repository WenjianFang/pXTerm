import paramiko

ip = ""
port = 22
user = "root"
password = ""
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, 22, user, password)