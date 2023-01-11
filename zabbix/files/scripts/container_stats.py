#!/usr/bin/python
# originaly from
import os
import json
import docker

def stats(server):
    client=docker.from_env()
    client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
    client_stats=client_lowlevel.stats(container=server,decode=True, stream=False)
    return client_stats

def get_env_marathon(data_config, env):
    for i in data_config:
        if i.split("=")[0]==env:
                return i.split("=")[1]

def get_data_container(container_id, parameter):
   with os.popen("docker inspect "+ container_id + " 2>&1") as pipe:
        docker_inspect = pipe.read().strip()
        decoded = json.loads(docker_inspect)
        result = int(decoded[0]["HostConfig"][parameter])
        return result

def cpu_container(total_cpu):
	return float(total_cpu/100000.0)

def status(status):
	if "Error: No such object:" in status:
		return ("0")
	elif status == 'running':
		return ("10")
	elif status == 'created':
		return ("1")
	elif status == 'restarting':
		return ("2")
	elif status == 'removing':
		return ("3")
	elif status == 'paused':
		return ("4")
	elif status == 'exited':
		return ("5")
	elif status == 'dead':
		return ("6")
	else: return ("0")


def get_info_container(id_container):
    container_stats = stats(id_container)
    #
    #cambiar esta linea por una llamada a la API no un comando
    #client_stats=client_lowlevel.stats(container=server,decode=True, stream=False)
    #
    with os.popen("docker inspect -s " + id_container) as pipe:
        container_inspect = json.loads(pipe.read().strip())
    #STATUS
    status_container = status(container_inspect[0]["State"]["Status"])
    containers_envs = container_inspect[0]["Config"]["Env"]
    nCpu_container = cpu_container(container_inspect[0]["HostConfig"]["CpuQuota"])

    #---------
    if status_container == "10":
        #CPU
        cpuDelta = (container_stats["cpu_stats"]["cpu_usage"]["total_usage"] - container_stats["precpu_stats"]["cpu_usage"]["total_usage"])
        systemDelta =  (container_stats["cpu_stats"]["system_cpu_usage"] - container_stats["precpu_stats"]["system_cpu_usage"])
        cpuPercent = (float(cpuDelta) / float(systemDelta)) * float(len(container_stats["cpu_stats"]["cpu_usage"]["percpu_usage"])) * 100.0
        if nCpu_container== 0:
            nCpu_container = container_stats["cpu_stats"]["online_cpus"]
        total_cpu_usage = cpuPercent/nCpu_container
        #---------
        #Memory
        memory_usage = container_stats["memory_stats"]["usage"] - container_stats["memory_stats"]["stats"]["cache"]
        memory_total = container_stats["memory_stats"]["limit"]
        #---------
        #DISK
        disk_usage = container_inspect[0]["SizeRootFs"]
        #---------
        #Name
        name_docker = get_env_marathon(containers_envs, "MARATHON_APP_ID")
        if name_docker==None:
                name_docker = id_container
        #---------
        #networks

	if "networks" in container_stats:
            for t_red in container_stats["networks"]:
                tx_dropped = container_stats["networks"][t_red]["tx_dropped"]
                tx_bytes = container_stats["networks"][t_red]["tx_bytes"]
                tx_errors = container_stats["networks"][t_red]["tx_errors"]
                tx_packets = container_stats["networks"][t_red]["tx_packets"]
                rx_packets = container_stats["networks"][t_red]["rx_packets"]
                rx_bytes = container_stats["networks"][t_red]["rx_bytes"]
                rx_errors = container_stats["networks"][t_red]["rx_errors"]
                rx_dropped = container_stats["networks"][t_red]["rx_dropped"]
        else: tx_dropped=tx_bytes=tx_errors=tx_packets=rx_dropped=rx_bytes=rx_errors=rx_packets=0
    else:
        disk_usage=total_cpu_usage=nCpu_container=memory_usage=memory_total=tx_dropped=tx_bytes=tx_errors=tx_packets=rx_packets=rx_bytes=rx_errors=rx_dropped="0"
        name_docker = id_container

    dict_info_container={}
    dict_info_container["cont_name"]=name_docker
    dict_info_container["cpu_total"]=nCpu_container
    dict_info_container["memory_total"]=memory_total
    dict_info_container["status"]=status_container
    dict_info_container["stats"]={"cpu_usage":total_cpu_usage, "memo_usage":memory_usage,"disk_usage":int(disk_usage)}
    dict_info_container["network"]={"tx_bytes":tx_bytes,"tx_packets":tx_packets,"tx_dropped":tx_dropped,"tx_errors":tx_errors,"rx_bytes":rx_bytes,"rx_packets":rx_packets,"rx_dropped":rx_dropped,"rx_errors":rx_errors}
    return dict_info_container

def get_container_stats():
    dict_container={}
    with os.popen("docker ps -q") as pipe:
        for line in pipe:
            id_container=line.rstrip('\n')
            dict_container[id_container]=get_info_container(id_container)

        with open('/tmp/json_container.json', 'w') as f:
            json.dump(dict_container, f, ensure_ascii=False)

get_container_stats()
