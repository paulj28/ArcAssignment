Web Server:
    - A simple web server was created which ran on port 8000. The server on getting a GET request would respond with a JSON file with one field. Initially a base64 encoded image was also attached (will look into putting it back once the project is complete). On getting a post request it would return an error with status code 400 as the code must only accept GET requests. The response is stored in a JSON file as well and on call is verified with the right answer to ensure that the data has not been tampered with. It can be run with the command: 
        python3 -m server.py 
 

Minikube Setup:
    - Since users do not have root access on their remote desktops, it is possible that you may face issues while installing and configuring Minikube on your system. I was unable to configure Minikube and got 'Permission Denied' errors. The steps I took to fix this, though it might not be the right way, were to make a copy of the kubectl.conf file that needed to be modified into a directory which I had access to edit files. I then changed the Kubeconfig environment variable to point to the new location. Minikube was then configured without any other issues.

Enable Ingress Addon:
    - It is of utmost importance that the ingress addon is enabled to ensure that Ingress can be used in the deployment.
    minikube addons enable ingress

Note: It is assumed that Minikube has been configured and the Ingress addon has been enabled as mentioned in the problem statement.

Docker Image:
    - The server.py and tester.py codes had been dockerized and pushed into docker hub so that they can be accessed while creating the pods. The image can be accessed with docker.io/pauljohn28/ws.

Yaml File:
    - To deploy the web server on Kubernetes a .yaml file was created which was split into three parts, the Ingress, the Deployment and the Service. The Ingress part behaves as a load balancer to the service. The deployment was made to have 2 replicas for testing purposes. The service is open on port 8000. The port 8000 for the deployment is exposed so that the local host can communicate with the deployment. Many online sources which provide insights into the syntax and form of the yaml file have deprecated and must check with more modern sources to ensure correct behaviour. The deployment takes in the image created earlier from docker hub for the pods. 

Kubernetes Deployment:
    - Once the yaml file is generated the deployment can be launched using the command: 
        kubeclt apply -f <name of yaml file>.yaml
    Once all three have been created you can check their status using the commands:
        kubectl get deployments             -        For all the deployment details.
        kubectl get services                -        For all the service details.
        kubectl get ingress                 -        For all the Ingress details.
        kubectl describe <Feature> <Name>   -        For information on a specific feature.

    Then we must expose the port 8000 for the deployment so that it can communicate with the local host, using the command: 
        kubectl expose deployment <Name> --port=8000.

Build and Deploy Script:
    - The build and deploy script initially runs a test on the server to ensure it works fine. It then dockerizes the web server and pushes it to a repository. As soon as the push is complete, the deployment script is run. The services and ingress are created as well. The system then waits 30 seconds before completing to ensure that the ingress is set up. The script can be run using the command:
        bash bd.sh

Note: Once the makefile has run it is required to wait for a minnute before sending the request, so that the Service and the Ingress can be set up properly.

Results:
    - Once you view the Ingress details, on using the curl command on the ip of the Ingress, we should get the required JSON file. Using the host local.arcesium.org in Ingress could not be done as that would require root access. Instead we use the nip.io service. To send a curl GET request to the server, all we have to do is run the command:
		curl  app.192.168.49.2.nip.io/athlete
This gives us the desired JSON as output. In my case:
		{myFavouriteAthlete : Lionel Messi}
