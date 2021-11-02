# mongodb k8s Port-forward

Goal:
- Sometimes you want to expose your mongodb using port-forward in k8s
- Most of the time you will need to connect to the primary repica
- But there is no way that tell you which pod is the primary
- So you need to do port-forward first and see which one is primary
- Then you do port forward on that one
- The main goad of this script is to eliminate that and it does do port-forward directly to the primary repica
## Prerquist
- Python3 
- Kubectl 
- [Mongo shell client](https://docs.mongodb.com/mongodb-shell/install/#std-label-mdb-shell-install)

## How to use it. 
- Download the script
- Then run the Following command. 
```shell
./mongo.py port-forward -po ${podname} -ns ${namespace} -u ${mongo-username} -p ${mongo-password} 
``` 
- Where ${podname} and pod from the mongo cluster
- ${namespace} k8s namespace that has the mongo cluster
- ${mongo-username} username to connect to mongodb default to ``admin``
- ${mongo-password} password for mongodb
