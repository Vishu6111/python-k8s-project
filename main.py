from kubernetes import client, config
import yaml

def create_nginx_deployment_service_from_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    
    deployment_name = yaml_data['deploymentName']
    replica_count = yaml_data['replicaCount']
    image = yaml_data['Image']

    config.load_kube_config()  # Load kube config from default location or use load_incluster_config() for in-cluster config

    api_instance = client.AppsV1Api()
    deployment_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": deployment_name},
        "spec": {
            "replicas": replica_count,
            "selector": {"matchLabels": {"app": deployment_name}},
            "template": {
                "metadata": {"labels": {"app": deployment_name}},
                "spec": {"containers": [{"name": "nginx", "image": image}]}
            }
        }
    }
    api_instance.create_namespaced_deployment(body=deployment_manifest, namespace="default")

    service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": deployment_name},
        "spec": {
            "selector": {"app": deployment_name},
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": 80}]
        }
    }
    api_instance = client.CoreV1Api()
    api_instance.create_namespaced_service(body=service_manifest, namespace="default")

# Usage
create_nginx_deployment_service_from_yaml("nginx_config.yaml")

