import time
import sys
import importlib
from linode import Api

try:
    a=sys.argv[1]
    props=importlib.__import__(a)
    node_count = props.NODES_COUNT
    ofile=open(props.OUTPUT_FILE_PATH, "w+")
    apikey=props.API_KEY
    api=Api(apikey)
    for i in range(1,node_count+1):
        linode_hand=api.linode.create(DatacenterID=2,PlanID=1,PaymentTerm=1)
        time.sleep(1)
        ofile.write("SERVER"+str(i)+"="+api.linode.ip.list(LinodeID=linode_hand['LinodeID'])[0]['IPADDRESS']+"\n")
    ofile.close()
except ValueError as err:
    print(err)
