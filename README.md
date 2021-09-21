# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### Goal
You work for a company that is building a app that uses location data from mobile devices. Your company has built a [POC](https://en.wikipedia.org/wiki/Proof_of_concept) application to ingest location data named UdaTracker. This POC was built with the core functionality of ingesting location and identifying individuals who have shared a close geographic proximity.

Management loved the POC so now that there is buy-in, we want to enhance this application. You have been tasked to enhance the POC application into a [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product) to handle the large volume of location data that will be ingested.

To do so, ***you will refactor this application into a microservice architecture using message passing techniques that you have learned in this course***. It’s easy to get lost in the countless optimizations and changes that can be made: your priority should be to approach the task as an architect and refactor the application into microservices. File organization, code linting -- these are important but don’t affect the core functionality and can possibly be tagged as TODO’s for now!

### Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

#### Initialize K3s
In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

#### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
sudo su -
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJlRENDQVIyZ0F3SUJBZ0lCQURBS0JnZ3Foa2pPUFFRREFqQWpNU0V3SHdZRFZRUUREQmhyTTNNdGMyVnkKZG1WeUxXTmhRREUyTXpFMk56UTJOelV3SGhjTk1qRXdPVEUxTURJMU56VTFXaGNOTXpFd09URXpNREkxTnpVMQpXakFqTVNFd0h3WURWUVFEREJock0zTXRjMlZ5ZG1WeUxXTmhRREUyTXpFMk56UTJOelV3V1RBVEJnY3Foa2pPClBRSUJCZ2dxaGtqT1BRTUJCd05DQUFSQ3pQQXpnVFJCejRudDVlQ0xTclJyOXdkRzJaa1A4MGFkU2dFNlNMRlcKZ1VPejJaMWp5aWNycjZsdzROSC9NKy9OMGxxMGwwTlo0TkltNDJPdnd3V2lvMEl3UURBT0JnTlZIUThCQWY4RQpCQU1DQXFRd0R3WURWUjBUQVFIL0JBVXdBd0VCL3pBZEJnTlZIUTRFRmdRVWJLOXNabHF4WlJydGdLNXZtajVsClVkZStNWkF3Q2dZSUtvWkl6ajBFQXdJRFNRQXdSZ0loQUpKajdPTUEvYnhPUVdJeUhuQWx6NGQ5RHNtalZqaTQKNFVKRWRyeE5WV1U0QWlFQThGR2EyODkzMDQ4cXhBbUN4YzEvVDlobXpHUGsyc3lVUGhKSm5iaURSODg9Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJrakNDQVRlZ0F3SUJBZ0lJSlZ3WG5PY3hHb1l3Q2dZSUtvWkl6ajBFQXdJd0l6RWhNQjhHQTFVRUF3d1kKYXpOekxXTnNhV1Z1ZEMxallVQXhOak14TmpjME5qYzFNQjRYRFRJeE1Ea3hOVEF5TlRjMU5Wb1hEVEl5TURreApOVEF5TlRjMU5Wb3dNREVYTUJVR0ExVUVDaE1PYzNsemRHVnRPbTFoYzNSbGNuTXhGVEFUQmdOVkJBTVRESE41CmMzUmxiVHBoWkcxcGJqQlpNQk1HQnlxR1NNNDlBZ0VHQ0NxR1NNNDlBd0VIQTBJQUJQcmdxL2thejJCajJvVDIKUkMrNlM1WjVpK1VLeVZ2RzhmMUV2aXpKRHVnYkdrcXNzN0tLdnBlbTRxU0JqdHR3MFQwcEVFRlJFSU9uTmNzZgpsTVBjS0pxalNEQkdNQTRHQTFVZER3RUIvd1FFQXdJRm9EQVRCZ05WSFNVRUREQUtCZ2dyQmdFRkJRY0RBakFmCkJnTlZIU01FR0RBV2dCUVZXelhNV2JyYjlxWEVaVTd6aUhHN3ljdFJ3ekFLQmdncWhrak9QUVFEQWdOSkFEQkcKQWlFQWpvcGE4ancrT05iV1VxZnBhcUgxMWlMRWxKd0VFRWFxbVJpYmJRQVZGNjhDSVFEaENoekk5ZWZkaGoxcQpjZHRlZWNUNkZoT2srdjgzdmx6aVFjY3BOTmJ1NFE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCi0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLQpNSUlCZGpDQ0FSMmdBd0lCQWdJQkFEQUtCZ2dxaGtqT1BRUURBakFqTVNFd0h3WURWUVFEREJock0zTXRZMnhwClpXNTBMV05oUURFMk16RTJOelEyTnpVd0hoY05NakV3T1RFMU1ESTFOelUxV2hjTk16RXdPVEV6TURJMU56VTEKV2pBak1TRXdId1lEVlFRRERCaHJNM010WTJ4cFpXNTBMV05oUURFMk16RTJOelEyTnpVd1dUQVRCZ2NxaGtqTwpQUUlCQmdncWhrak9QUU1CQndOQ0FBUXJTdk1CZ3hJZjU3M3doVW5DL0NkeEpkMFJjQXVUcTJodGgya2lybXV5CnFsWTdWN3diNmRyZERFcVNCS1RJcHlSdU84b0l1VDdFYVlkQXl5NWR4V1p4bzBJd1FEQU9CZ05WSFE4QkFmOEUKQkFNQ0FxUXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96QWRCZ05WSFE0RUZnUVVGVnMxekZtNjIvYWx4R1ZPODRoeAp1OG5MVWNNd0NnWUlLb1pJemowRUF3SURSd0F3UkFJZ2ZnOVNrWVloaWJSK21QMFBlTEQ0WGpzVVhtVms3OFlwCjloWDcxeG4reWdzQ0lIYUtVRE11eDdMOFJORjNGTStIdVo0ajFBRGpDdWd2RTZLMksvQ2ZpZDdMCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    client-key-data: LS0tLS1CRUdJTiBFQyBQUklWQVRFIEtFWS0tLS0tCk1IY0NBUUVFSUt4OVh2b1FBK0h5elJ3UzdyT1g3NlFKVTFCOTRXbDk1NzRQVUNZNWtvblRvQW9HQ0NxR1NNNDkKQXdFSG9VUURRZ0FFK3VDcitSclBZR1BhaFBaRUw3cExsbm1MNVFySlc4YngvVVMrTE1rTzZCc2FTcXl6c29xKwpsNmJpcElHTzIzRFJQU2tRUVZFUWc2YzF5eCtVdzl3b21nPT0KLS0tLS1FTkQgRUMgUFJJVkFURSBLRVktLS0tLQo=
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Steps for Deploying Services
1. `curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash` - Install Helm
2. `helm repo add bitnami https://charts.bitnami.com/bitnami ` - Add bitnami repo for helm
3. `kubectl apply -f deployment/udaconnect-kafka.yaml` - Install bitnami/kafka deployment with helm
4. `kubectl apply -f deployment/udaconnect-api.yaml` - Set up the service and deployment for the API
5. `kubectl apply -f deployment/udaconnect-app.yaml` - Set up the service and deployment for the web app
6. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
7. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
8. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
9. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)
The following section will continue apply after Docker images deployed
10. `kubectl apply -f deployment/udaconnect-person.yaml` - Set up the service and deployment for the Person API
11. `kubectl apply -f deployment/udaconnect-connections.yaml` - Set up the service and deployment for Connection the API
12. `kubectl apply -f deployment/udaconnect-location-producer.yaml` - Set up the service and deployment for the Location Producer API
13. `kubectl apply -f deployment/udaconnect-location-consumer.yaml` - Set up the deployment for the Location Consumer app (make sure Kafka running)
 
Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the starter project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

Note: The first time you run this project, you will need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### Verifying it Works
Once the project is up and running, you should be able to see 3 deployments and 3 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return `udaconnect-app`, `udaconnect-api`, and `postgres`


These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation
* `http://localhost:30001/api/` - Base path for API
* `http://localhost:30000/` - Frontend ReactJS Application

#### Deployment Note
You may notice the odd port numbers being served to `localhost`. [By default, Kubernetes services are only exposed to one another in an internal network](https://kubernetes.io/docs/concepts/services-networking/service/). This means that `udaconnect-app` and `udaconnect-api` can talk to one another. For us to connect to the cluster as an "outsider", we need to a way to expose these services to `localhost`.

Connections to the Kubernetes services have been set up through a [NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). (While we would use a technology like an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) to expose our Kubernetes services in deployment, a NodePort will suffice for development.)

## Development
### New Services
New services can be created inside of the `modules/` subfolder. You can choose to write something new with Flask, copy and rework the `modules/api` service into something new, or just create a very simple Python application.

As a reminder, each module should have:
1. `Dockerfile`
2. Its own corresponding DockerHub repository
3. `requirements.txt` for `pip` packages
4. `__init__.py`

### Docker Images Deployment
udaconnect-app and udaconnect-api use docker images from isjustintime/udaconnect-app and isjustintime/udaconnect-api. To make changes to the application, build your own Docker image and push it to your own DockerHub repository. Replace the existing container registry path with your own.

1. `docker build -t udaconnect-person . `
2. `docker build -t udaconnect-connections . `
3. `docker build -t udaconnect-location-producer . `
4. `docker build -t udaconnect-location-consumer . `
5. `docker run -it -d -p 30002:5002 udaconnect-person` 
6. `docker run -it -d -p 30006:5006 udaconnect-connections` 
7. `docker run -it -d -p 30005:5005 udaconnect-location-producer`
8. `docker run -it -d -p 30004:5004 udaconnect-location-consumer`
9. `docker build --no-cache -t ailinelim/udaconnect-frontend .`
10. `docker tag udaconnect-person ailinelim/udaconnect-person:latest`
11. `docker tag udaconnect-connections ailinelim/udaconnect-connections:latest`
12. `docker tag udaconnect-location-producer ailinelim/udaconnect-location-producer:latest`
13. `docker tag udaconnect-location-consumer ailinelim/udaconnect-location-consumer:latest`
14. `docker push ailinelim/udaconnect-person:latest`  
15. `docker push ailinelim/udaconnect-connections:latest`  
16. `docker push ailinelim/udaconnect-location-producer:latest`
17. `docker push ailinelim/udaconnect-location-consumer:latest`
18. `docker push ailinelim/udaconnect-frontend:latest`
19. `docker ps docker logs <pod name>`

## gRPC
Create gRPC files: 
```bash
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ locations.proto`udaconnect-app` and `udaconnect-api` 
```

## Configs and Secrets
In `deployment/db-secret.yaml`, the secret variable is `d293aW1zb3NlY3VyZQ==`. The value is simply encoded and not encrypted -- this is ***not*** secure! Anyone can decode it to see what it is.
```bash
# Decodes the value into plaintext
echo "d293aW1zb3NlY3VyZQ==" | base64 -d

# Encodes the value to base64 encoding. K8s expects your secrets passed in with base64
echo "hotdogsfordinner" | base64
```
This is okay for development against an exclusively local environment and we want to keep the setup simple so that you can focus on the project tasks. However, in practice we should not commit our code with secret values into our repository. A CI/CD pipeline can help prevent that.

## PostgreSQL Database
The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_You may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from you. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.

### Database Connection
While the Kubernetes service for `postgres` is running (you can use `kubectl get services` to check), you can expose the service to connect locally:
```bash
kubectl port-forward svc/postgres 5432:5432
```
This will enable you to connect to the database at `localhost`. You should then be able to connect to `postgresql://localhost:5432/geoconnections`. This is assuming you use the built-in values in the deployment config map.

### Software
To manually connect to the database, you will need software compatible with PostgreSQL.
* CLI users will find [psql](http://postgresguide.com/utilities/psql.html) to be the industry standard.
* GUI users will find [pgAdmin](https://www.pgadmin.org/) to be a popular open-source solution.

## Architecture Diagrams
Your architecture diagram should focus on the services and how they talk to one another. For our project, we want the diagram in a `.png` format. Some popular free software and tools to create architecture diagrams:
1. [Lucidchart](https://www.lucidchart.com/pages/)
2. [Google Docs](docs.google.com) Drawings (In a Google Doc, _Insert_ - _Drawing_ - _+ New_)
3. [Diagrams.net](https://app.diagrams.net/)

## Tips
* We can access a running Docker container using `kubectl exec -it <pod_id> sh`. From there, we can `curl` an endpoint to debug network issues.
* The starter project uses Python Flask. Flask doesn't work well with `asyncio` out-of-the-box. Consider using `multiprocessing` to create threads for asynchronous behavior in a standard Flask application.



