"""
    Author: Siddharth Gupta
    email: gsiddharth47@gmail.com
    OS: Ubuntu 24.04
"""

# Please install kubernetes & selenium python bindings before proceeding via 
# pip install kubernetes
# pip install selenium  

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from kubernetes import client, config

def get_k8s_api() -> client.CoreV1Api:
    config.load_kube_config(context='minikube')
    return client.CoreV1Api()

def get_pod_names(namespace="default"):
    try:
        api = get_k8s_api()
        pods_list = api.list_namespaced_pod(namespace=namespace)
        pod_names = [pod.metadata.name for pod in pods_list.items]
        return pod_names
    except Exception:
        print("[-] Please ensure pods are running")
    

def get_pod_logs(namespace, pod_name):
    try:
        api = get_k8s_api()
        logs = api.read_namespaced_pod_log(namespace=namespace,
                                            name=pod_name)
        return logs
    except Exception:
        print("[-] Please ensure pods are running")


def is_backend_up():
    try:
        logs = get_pod_logs(namespace="default",
                    pod_name=get_pod_names()[0])
        if "running on port" in logs:
            return True
        else:
            return False
    except Exception:
        print("[-] Please ensure pods are running")
        return False

def is_frontend_up():
    try:
        logs = get_pod_logs(namespace="default",
                            pod_name=get_pod_names()[1])
        if "running on port" in logs:
            return True
        else:
            return False
    except Exception:
        print("[-] Please ensure pods are running")
        return False
    

def webdriver_setup():
    chrome_service = Service(executable_path="/home/siddharth/webdriver/chromedriver")
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=chrome_service,
                              options=chrome_options)
    return driver

def test_web_app():
    driver = webdriver_setup()
    driver.get("http://192.168.49.2:31827/")
    actual_heading = driver.find_element(By.XPATH, "//h1").text
    expected_heading = "Hello from the Backend!"
    if(actual_heading == expected_heading):
        print(f"\t [*] Heading: {actual_heading} \n Test Passed" )
        assert True
    else:
        assert False

def main():
    if(is_backend_up() and is_frontend_up):
        print("Frontend & Backend deployments are running... \n starting browser based test")
        test_web_app()
    else:
        print("[-] Please ensure that frontend & backend deployments are running...")

if __name__ == '__main__':
    main()