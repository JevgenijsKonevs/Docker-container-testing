#### Intro:</br>

Python 3 based project for Docker container testing. By executing coordinate.py, it is possible to create two containers A and B and then, by using container-A Flask server, container-B will be tested.</br>

#### Project required tests:</br>

• Reachability test</br>
• SSH test</br>
• HTTP test</br>

### How to use : </br>

• git clone this repository :
```python
git clone https://github.com/JevgenijsKonevs/Docker-container-testing.git
```
• execute "coordinate.py" in terminal : 
```python
python coordinate.py -c
```
• wait for program to finish and then observe the results in terminal</br>

### How it works : </br>

By starting "coordinate.py" script with a flag "-c", which means create the container, the user is starting the process of downloading the basic images, creation of the new ones, creation of container A and container B as well as testing the container B. </br>
The script will download all necessary software for containers A and B, based on requirements mentioned in Dockerfile for each of them.</br>

The base docker image of container-B contains Debian, apache2 and openssh server installed and it will be downloaded from https://hub.docker.com/repository/docker/jkonev/apache-ssh-img</br> Apache2 and OpenSSH servers will be then turned into "active" status, when the new image, "jkonev/containerb", will be created. </br>
The base docker image of container-A contains "python:3-onbuild" image with all Python necessary software including Flask. </br>
"jkonev/containera" image , which is based on "python:3-onbuild" , includes the start of Python script "rest.py: in order to automatically test container-B.</br>
After downloading and containers installation process, these images, "python:3-onbuild" and "jkonev/apache-ssh-img", will be deleted in order to save the space.</br>
"rest.py" is listening for a request from host machine and when it is received it will run CMD commands, that should be executed in order to test container-b reachability, and then providing the results to host machine.

### Important : </br>

It is import to mention that when the "coordinate.py" script will be executed for a first time, it should contain flag "-c" in order to create the containers, example :
```python
python coordinate.py -c
```

After the creation, the script should be run without "-c" flag, example :

```python
python coordinate.py 
```
</br> 

### Results : </br>

![final](https://user-images.githubusercontent.com/55871427/106460752-78d78c80-649c-11eb-89ef-7c4b839b13c6.JPG)



### Used resources: </br>
• https://docker-py.readthedocs.io/en/stable/</br>
• https://docs.docker.com/</br>
• https://flask-doc.readthedocs.io/en/latest/</br>
