import sys
import importlib
import boto3
from boto3.session import Session
try:    
    a=sys.argv[1]
    props=importlib.__import__(a)
    ofile=open(props.OUTPUT_FILE_PATH, "w+")
    aws_access=props.ACCESS_KEY
    aws_secret=props.SECRET_KEY
    reg_name=props.REGION
    node_count = props.NODES_COUNT
    ins_type=props.NODES_TYPE
    key_name=props.KEY_PAIR_NAME
    #Starting session
    session = Session(aws_access_key_id=aws_access,
                          aws_secret_access_key=aws_secret,
                          region_name=reg_name)
    print("Session Started")

    ec2 = session.resource('ec2')
    ec2client=session.client('ec2')

    if(ins_type=='ubuntu'):
        image_id='ami-9abea4fb'
    elif(ins_type=='redhat'):
        image_id='ami-775e4f16'
    elif(ins_type=='windows'):
        image_id='ami-83a5bce2'
    elif(ins_type=='suse'):
        image_id='ami-d2627db3'
    elif(ins_type=='amazon_linux'):
        image_id='ami-f0091d91'
    else:
        print("Unable to find the given type. Please try ubuntu, redhat, windows, suse or amazon_linux")
    instance = ec2.create_instances(
                    ImageId=image_id,
                    MinCount=node_count,
                    MaxCount=node_count,
                    KeyName=key_name,
                    InstanceType='t2.micro',
                    Monitoring={
                        'Enabled': True
                    },
                )
    print("Instances created")
    ct=0
    for ins in instance:
        ct=ct+1
        inst=ec2.Instance(ins.id)
        inst.wait_until_running()
        descinst=ec2client.describe_instances(
                InstanceIds=[
                        ins.id
                    ]
            )
        ofile.write("SERVER"+str(ct)+"="+descinst['Reservations'][0]['Instances'][0]['PublicIpAddress']+"\n")
        print(descinst['Reservations'][0]['Instances'][0]['PublicIpAddress'])
    ofile.close()
except ValueError as err:
    print(err)
    
