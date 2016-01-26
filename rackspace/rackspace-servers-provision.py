import time
import importlib
import sys
import pyrax
import re
try:
    a=sys.argv[1]
    props=importlib.import_module(a)
    ofile=open(props.OUTPUT_FILE_PATH, "w+")
    ins_type=props.NODES_TYPE
    count=props.NODES_COUNT

    pyrax.set_setting("identity_type", "rackspace")
    pyrax.set_default_region(props.REGION)
    pyrax.set_credentials(props.USERNAME, props.PASSWORD)
    cs = pyrax.cloudservers
    flavor = cs.flavors.get('general1-2')

    def findipaddr(server):
        try:
            ipbunch = server.networks['public']
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', str(ipbunch))
            print(ip[0])
            ofile.write("SERVER"+str(i)+"="+ip[0]+"\n")
        except KeyError as err:
            print("Unable to retrieve ip")

    if(ins_type=="ubuntu"):
        image = pyrax.images.get('59a3fadd-93e7-4674-886a-64883e17115f')
    elif(ins_type=="debian"):
        image = pyrax.images.get('cf16c435-7bed-4dc3-b76e-57b09987866d')
    elif(ins_type=="windows"):
        image = pyrax.images.get('39375b69-899a-43c6-9641-f8c787eea5ee')

    for i in range(1,count+1):
        server = cs.servers.create('sailesh', image.id, flavor.id)
        time.sleep(4)
        findipaddr(server)
except ValueError as erro:
    print(err)
