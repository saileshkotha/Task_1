import digitalocean
import time
import importlib
import sys
try:
    a=sys.argv[1]
    props=importlib.__import__(a)
    ofile=open(props.OUTPUT_FILE_PATH, "w+")
    ins_type=props.NODES_TYPE
    count=props.NODES_COUNT
    access_tkn=props.ACCESS_TOKEN
    if(ins_type=='ubuntu'):
        image_id='ubuntu-14-04-x64'
    elif(ins_type=='fedora'):
        image_id='fedora-23-x64'
    elif(ins_type=='debian'):
        image_id='debian-8-2-x64'
    else:
        print("Unable to find the given type. Please try ubuntu, fedora or debian")
    print("Creating instances")
    for i in range(1,count+1):
        droplet = digitalocean.Droplet(token=access_tkn,
                                   name='Example',
                                   region='nyc2', 
                                   image=image_id, 
                                   size_slug='512mb',
                                   backups=True)
        droplet.create()
        while(droplet.load()):
            if(droplet.status=="active"):
                print(droplet.ip_address)
                ofile.write("SERVER"+str(i)+"="+droplet.ip_address+"\n")
                break
            time.sleep(2)
    ofile.close()
    print("IP addresses saved to file")
except ValueError as err:
    print(err)
