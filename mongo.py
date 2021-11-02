#!/usr/bin/env python3
import argparse
import subprocess
import shlex

def initPortForward(namespace, pod):
  cmd= "kubectl -n "+namespace+" port-forward "+ pod + " 27017:27017"
  return subprocess.Popen(shlex.split(cmd))

def getPrimaryPod(username, password):
  getcmd ="mongosh 'mongodb://127.0.0.1:27017' --username "+username+ " --password "+password+" --eval 'rs.isMaster().primary'"
  result = subprocess.run(shlex.split(getcmd), capture_output=True, universal_newlines=True)
  result = result.stdout.encode('utf-8')
  primaryPodUrl = subprocess.run(["grep", "svc.cluster.local"], capture_output=True, input=result).stdout
  return primaryPodUrl.decode('utf-8').split(".")[0]

def portForwardPrimary(namespace, primaryPod):
  cmdPortForwardMaster= "kubectl -n "+ namespace +" port-forward "+ primaryPod + " 27017:27017"
  subprocess.run(shlex.split(cmdPortForwardMaster))
     
def connect(pods, namespace, username, password):
  proc = initPortForward(namespace=namespace, pod=pods)
  subprocess.run(["sleep", "2"])
  primaryPod = getPrimaryPod(username=username, password=password)
  
  subprocess.run(["echo", "primary is "+primaryPod])
  # trinimante the temp process
  proc.terminate()
  # run the port forwaed on the master node
  portForwardPrimary(namespace, primaryPod)
  
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Echo your input')
   
   subparsers = parser.add_subparsers(dest='func')
   connect_parser =  subparsers.add_parser('port-forward',  
                                         help='this is to port-forward to mongodb primary pod')
   connect_parser.add_argument('--pod', '-po',
                               help="mongodb pod name"
                              )
   connect_parser.add_argument('--namespace', '-ns',
                              help="namespace"
                              )
   connect_parser.add_argument('--username', '-u',
                            help="mogodb username",
                            default="admin"
                            )
   connect_parser.add_argument('--password', '-p',
                            help="mogodb password"
                            )

   args = parser.parse_args()
   if args.func == "port-forward":
     connect(args.pod, args.namespace, args.username, args.password)   
