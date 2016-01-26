import sys
import importlib
import os
import time
try:
    a=sys.argv[1]
    props=importlib.__import__(a)
    ofile=open(props.OUTPUT_FILE_PATH, "w+")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = props.JSON_FILE
    zone = props.ZONE
    project_id=props.PROJECT_ID
    disk_type=props.NODES_TYPE
    count=props.NODES_COUNT

    if(disk_type=="debian"):
        sdi="projects/debian-cloud/global/images/debian-8-jessie-v20160119"
    elif(disk_type=="ubuntu"):
        sdi="projects/ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20160114e"
    elif(disk_type=="suse"):
        sdi="projects/opensuse-cloud/global/images/opensuse-13-2-v20150511"
    elif(disk_type=="redhat"):
        sdi="projects/rhel-cloud/global/images/rhel-7-v20160119"
    elif(disk_type=="windows"):
        sdi="projects/windows-cloud/global/images/windows-server-2012-r2-dc-v20160112"
        
    from oauth2client.client import GoogleCredentials
    credentials = GoogleCredentials.get_application_default()

    from googleapiclient import discovery
    compute = discovery.build('compute', 'v1', credentials=credentials)

    def list_instances(compute, project, zone):
        result = compute.instances().list(project=project, zone=zone).execute()
        return result['items']

    def create_instance(compute, project, zone, name, sdi):
        source_disk_image = \
            sdi
        machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
        
        config = {
            'name': name,
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],

        }

        return compute.instances().insert(
            project=project,
            zone=zone,
            body=config).execute()

    for i in range(1, count+1):
        print(create_instance(compute, project_id, zone,"nametemp"+str(i), sdi))
        time.sleep(5)

    all_inst=list_instances(compute, project_id, zone)
    ct=0
    for list_inst in all_inst:
        ct=ct+1
        ofile.write("SERVER"+str(ct)+"="+list_inst["networkInterfaces"][0]["accessConfigs"][0]["natIP"]+"\n")
    ofile.close()
except ValueError as err:
    print(err)
