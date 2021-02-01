import docker
import time
import requests
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', action='store_true',
                    help='If -c is set then will create containers')
args = parser.parse_args()

if args.c:

    client = docker.from_env()

    image_for_containerB = client.images.build(
        path='./containerB', tag='jkonev/containerb', rm=True)
    image_for_containerA = client.images.build(
        path='./containerA', tag='jkonev/containera', rm=True)

    container = client.containers.run('jkonev/containerb',
                                      detach=True, name='container-b',
                                      ports={'80/tcp': 5001, '22/tcp': 5002})

    ip_add = client.containers.get(
        'container-b').attrs['NetworkSettings']['IPAddress']

    container = client.containers.run('jkonev/containera',
                                      detach=True, name='container-a',
                                      environment=[f"container_b_ip={ip_add}"],
                                      ports={'5000/tcp': 5000})

    for i in range(5):
        print("Waiting for container creation")
        time.sleep(1)

    used_images = ['python:3-onbuild', 'jkonev/apache-ssh-img']

    for i in range(len(used_images)):
        remove_images = client.images.remove(image=used_images[i])

try:
    result = requests.get('http://127.0.0.1:5000/tests')
    jresult = result.json()['data']

    print('\n\nQuerying created container B from container A...')

    http = jresult['http']['http']
    ssh = jresult['ssh']['ssh']
    ping = jresult['ping']['ping']

    http_log = jresult['http']['debug']
    ssh_log = jresult['ssh']['debug']
    ping_log = jresult['ping']['debug']

    print(
        f"\n\nLogs of test results for Container B:\n\n---ping_log--- \n{ping_log}\n---http_log--- \n{http_log}\n---ssh_log--- \n{ssh_log}")
    print(
        f"\n\nTest results for Container B:\nping: {ping}\nhttp: {http}\nssh: {ssh}")

except:
    print("Unexpected error during the connection to Container A. Is it running?")
