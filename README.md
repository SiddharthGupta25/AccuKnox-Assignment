# Instructions For Problem Statement 1

### Info
<ul>
    <li>OS used: Ubuntu 24.04 LTS </li>
    <li>Please consider creating a virtual environment using the command: <code>python -m venv VENV</code>
    activating it by going to the bin dir inside VENV and executing activate.sh script
    </li>
    <li>After activating the env. consider installing the dependencies</li>
    <b>NOTE:</b> The steps can be ignored while using PyCharm IDE
</ul>

### Deploying Backend
<ul>
    <li>
        We need to first setup a local K8s cluster for which either minikube or kind can be used. In this case, minikube is used. Once, thats done we can verify its status via following command 
        <code>minikube status</code>
    </li>
    <li>
        Once in the output we see that everything is running and is configured properly, we can proceed with deployments 
    </li>
    <li>We'll deploy the backend via K8s first, for doing so one must be in the same directory (for ease) as the desired deployment.yaml file, once in the right directory, execute the following command to deploy the backend: <code>kubectl apply -f backend-deployment.yaml</code> 
    </li>
    <li>
        As it deploys, the deployment can be verified via following command: <code>kubectl get deployments</code> which will list the deployment as 'backend-deployment-####' where ## is a random hash value
    </li>
    <li>
        However, to learn the status of the underlying pod (which is managed by the deployment) we can use the <code>kubectl get pods </code> command, we'll have to wait until that status becomes 'Running' here.  
    </li>
    <li>Once the status is 'Running' we need to ensure that everything is fine inside of the container. For that, we'll check container logs with the following command: <code>kubectl logs (name of the pod) </code> it should show the message: 'Backend service is running on port 3000'
    </li>
    <li>The backend is now running successfully</li>
</ul>

## Deploying Frontend
<ul>
    <li>Move to the directory containing the frontend-deployment file and issue the following command to deploy: <code>kubectl apply -f frontend-deployment.yaml </code> </li>
</ul>
<ul>
    <li>We can verify our deployment with <code>kubectl get deployments</code> and now we should see 2 deployments 1 for backend & 1 for frontend</li>
    <li>
        We should also verify the underlying containers (running inside of pods) by using <code>kubectl get pods</code> & we should see 3 pods running (2 for backend & 1 for frontend)
    </li>
    <li>To ensure that everything is running fine inside of the container, we can check the logs by issuing <code>kubectl logs <pod-name> </code> and we should see the message: Frontend service running on port 8080  </li>
    <li>
        However, upon examining the frontend-deployment.yaml file it was noted that the service is of type LoadBalancer which depends on an external cloud provider to assign an external IP address which later is used to access the front end via a web browser. In this setup, no external provider has been used. So, it won't assign an external IP to the frontend pod. In order to access the frontend from a browser, we can utilize the ip address of minikube itself which can be learnt by the following command: <code>minikube ip</code>
    </li>
    <li>
        After learning the ip address we need to learn the right port number, which can be learnt by issuing the following commnad:
        <code>kubectl get service</code> the output of this command will contain a column for ports, we need to see the port against frontend-deployment-### (it'll be 80:31827 where 31827 is the right port no.)
    </li>
    <li>Now, we have the ip address as well as the right port number, we can pull up the browser and enter the socket address as: <code>http://(minikube-ip):(port-no)</code> </li> and visit the adress to see the message: Hello from the Backend!
</ul>

### Running Test On The Browser 

<ul>
    <li>For testing, selenium with python has been used along with the python bindings for K8s APIs to ensure both the deployments are running fine, before the test runs. If either of the deployment is not running, the test will not run and instead will throw an error about the deployments (if any)  </li>
    <li>Please consider installing selenium: <code>pip install selenium</code> & K8s python binding 
    <code>pip install kubernetes</code> before proceeding </li>
    <li>Now, in order to run the tests, use the command: <code>python test_deployment.py</code> </li>
</ul>

