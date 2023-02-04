import os
import subprocess

# Command to get docker container id
cmd = ["docker", "container", "ls", "--all", "--quiet", "--filter", "name=rabbitmq-subscriber"]
# Get container id from console
container_id = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
container_id = str(container_id)[2:14]
# Copy graphs to host machine
os.system("docker cp " + container_id + ":/usr/local/source/graph.png /home/student/IoTProject/results")
os.system("docker cp " + container_id + ":/usr/local/source/ml_graph.png /home/student/IoTProject/results")
