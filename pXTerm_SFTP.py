import paramiko
#from remote->local
ip = ""
port = 22
user = "root"
password = ""
t = paramiko.Transport((ip, port))
t.connect(username= user, password = password)
sftp = paramiko.SFTPClient.from_transport(t)
remotepath = ""
localpath = ""
sftp.get(remotepath, localpath)
t.close()

#from local->remote

t = paramiko.Transport((ip, port))
t.connect(username= user, password = password)
sftp = paramiko.SFTPClient.from_transport(t)
remotepath = ""
localpath = ""
sftp.put(localpath, remotepath)
t.close()