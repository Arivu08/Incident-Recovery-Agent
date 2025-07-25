import docker

def restart_container(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.restart()
    return f"Container '{container_name}' restarted."

def list_containers():
    client = docker.from_env()
    return [c.name for c in client.containers.list(all=True)]
