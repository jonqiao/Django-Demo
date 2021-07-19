from xml.etree.ElementTree import ElementTree
from random import choice
from datetime import datetime
import paramiko
import sys


class SSHConnect(object):
  # ssh=SSHConnect('192.168.66.128','jon','D:/WORKSPACE/PSN-WORKSPACE/VSC-Python/ssh/id_rsa')
  def __init__(self, hostname, username, key_file=None, password=None, port=22):
    try:
      self.client = paramiko.SSHClient()
      self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      if password:
        print('Using password for connecting...')
        self.client.connect(hostname=hostname, username=username, password=password, port=port)
      elif key_file:
        print('Using pkey for connecting...')
        privateKey = paramiko.RSAKey.from_private_key_file(key_file)
        self.client.connect(hostname=hostname, username=username, pkey=privateKey, port=port)
      else:
        raise Exception('Must supply either key_file or password')
      self.sftp = self.client.open_sftp()
    except Exception as e:
      print(e)
      if self.client:
        self.client.close()
      # sys.exit(1)
    else:
      print('call init func')

  def __del__(self):
    if self.client:
      self.client.close()
    print('call del func')

  def backup(self, filename):
    # dtnow = datetime.now().strftime('%Y%m%d%H%M%S')
    dtnow = datetime.utcnow().strftime('%Y%m%d')
    bakname = filename + '.' + dtnow + '.bak'
    result = self.copy(filename, bakname)
    return result

  def copy(self, src, dest):
    cmd = 'cp -R ' + src + ' ' + dest
    result = self.exec(cmd)
    return result

  def exec(self, cmd='date; hostname; whoami;'):
    try:
      stdin, stdout, stderr = self.client.exec_command(cmd)
      result = stdout.read().decode('utf-8')
      return result
    except Exception as e:
      print(e)

  def listdir(self, remotedir='.'):
    try:
      self.sftp.chdir(remotedir)
      rdir = self.sftp.listdir(remotedir)
    except Exception as e:
      print(e)
    else:
      return rdir

  def listdirattr(self, remotedir='.'):
    try:
      self.sftp.chdir(remotedir)
      rdirattr = self.sftp.listdir_attr(remotedir)
      # Debug
      # for rda in rdirattr:
      #   fname = str(rda).split(' ')[-1]
      #   print(fname, rda.st_mtime)
    except Exception as e:
      print(e)
    else:
      return rdirattr

  def get(self, remotepath, localpath):
    try:
      self.sftp.get(remotepath, localpath)
    except Exception as e:
      print(e)
    else:
      return "SUCCESS"

  def put(self, localpath, remotepath):
    try:
      # remotepath: Note that the filename should be included.
      self.sftp.put(localpath, remotepath)
    except Exception as e:
      print(e)
    else:
      return "SUCCESS"


# ------------------------- Main -------------------------
if __name__ == "__main__":
  hostname = '192.168.66.128'
  username = 'jon'
  key_file = 'D:/WORKSPACE/PSN-WORKSPACE/VSC-Python/ssh/id_rsa'
  # ssh=SSHConnect(hostname, username, password='root')
  ssh = SSHConnect(hostname, username, key_file)
  if hasattr(ssh, 'sftp'):
    res_cmd = ssh.exec()
    print(res_cmd)
    print('----------------------')
    res_dir = ssh.listdir('/home/jon/paramiko/')
    print(res_dir)
    print('----------------------')
    res_dirattr = ssh.listdirattr('/home/jon/paramiko/')
    print(res_dirattr)
    print('----------------------')
    res_put = ssh.put('D:/WORKSPACE/PSN-WORKSPACE/VSC-Python/PyTest/labtest.py', '/home/jon/paramiko/labtest.py')
    print('ssh.put:', res_put)
    print('----------------------')
    res_get = ssh.get('/home/jon/paramiko/labtest.py', 'D:/labtest.py')
    print('ssh.get:', res_get)
    print('----------------------')

    # backup xml on remote
    ssh.backup('/home/jon/paramiko/FFTS00001.xml')
    # handle xml from remote
    tree = ElementTree()
    with ssh.sftp.open('/home/jon/paramiko/FFTS00001.xml', mode='r') as rfopen:
      rfopen.prefetch()
      tree.parse(rfopen)
      nodes = tree.findall('project_variable')
      for node in nodes:
        name = node.findtext('project_name')
        value = node.findtext('project_value')
        print(name, ':', value)

      print('----------------------')
      for node in nodes:
        name = node.findtext('project_name')
        if name == 'app.support.callout':
          node.find('project_value').text = choice(['BHO', '7X24', 'TICKET'])
          print('app.support.callout updated...')

    print('----------------------')
    with ssh.sftp.open('/home/jon/paramiko/FFTS00001.xml', mode='w') as wfopen:
      tree.write(wfopen, encoding='utf-8', xml_declaration=True)
      wfopen.flush()
