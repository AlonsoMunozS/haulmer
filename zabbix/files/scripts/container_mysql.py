#! /usr/bin/python
import os
import json
import docker
import re

def stats(server):
    client=docker.from_env()
    client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
    client_stats=client_lowlevel.stats(container=server,decode=False, stream=False)
    return client_stats

def get_env_marathon(data_config, env):
    for i in data_config:
        if i.split("=")[0]==env:
                return i.split("=")[1]
def get_mysql_env(data_config):
    data={}
    for i in data_config:
        if "MYSQL" in i.split("=")[0]:
            data[i.split("=")[0]]=i.split("=")[1]
    return data
def get_host_mysql(data_config):
    for i in data_config:
        if "MARATHON_APP_ID" in i.split("=")[0]:
            marathon_app_id=i.split("=")[1]
            return marathon_app_id.replace("/", "")+".marathon.l4lb.thisdcos.directory"


def get_data_container(container_id, parameter):
   with os.popen("docker inspect "+ container_id + " 2>&1") as pipe:
        docker_inspect = pipe.read().strip()
        decoded = json.loads(docker_inspect)
        result = int(decoded[0]["HostConfig"][parameter])
        return result



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
    # container_stats = stats(id_container)
    # client=docker.from_env()
    client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
    # with os.popen("docker inspect -s " + id_container) as pipe:
    #     container_inspect = json.loads(pipe.read().strip())
    container_inspect=client_lowlevel.inspect_container(id_container)
    #print json.dumps(container_inspect)
    #STATUS
    status_container = status(container_inspect["State"]["Status"])
    containers_envs = container_inspect["Config"]["Env"]
 
    if status_container == "10":
        name_docker = get_env_marathon(containers_envs, "MARATHON_APP_ID")
        if name_docker==None:
                name_docker = id_container
        mysql_data=get_mysql_env(containers_envs)
        mysql_data['HOST']=get_host_mysql(containers_envs)
    dict_info_container={}
    dict_info_container["cont_name"]=name_docker
    dict_info_container["status"]=status_container
    dict_info_container['mysql']=mysql_data
    return dict_info_container
def get_current_bd_info_hidden(data, num_bd):
    obj={}
    for i in data:
        rep="MYSQL_"+num_bd+"_"
        if rep in i.split(":")[0]:
            key=i.split(":")[0].split(rep)[1]
            obj[key]=data[i.split(":")[0]]
            obj['HOST']=data['HOST']
    return obj
def get_current_bd_info_cluster(data, num_bd):
    obj={}
    for i in data:
        rep="MYSQL_"+num_bd+"_"
        if rep in i.split(":")[0]:
            key=i.split(":")[0].split(rep)[1]
            obj[key]=data[i.split(":")[0]]
            obj['HOST']=data['HOST'].replace("hidden","cluster")
    return obj 
def get_num_current_bd (name_bd):
    expresion="\d+(?=_DB)"
    num_dbs=re.findall(expresion,name_bd)
    return num_dbs[0]
def get_cluster_info (data):
    obj={}
    obj['PASSWORD']=data['MYSQL_ROOT_PASSWORD']
    obj['DB']=data['MYSQL_CLUSTER_NAME']
    obj['USER']="root"
    obj['HOST']=data['HOST']
    return obj
def print_data_zabbix(info):
    data={}
    array=[]
    for app_id in info:
        obj={}
        obj['{#APP_ID}']=app_id
        array.append(obj)
    data['data']=array
    print json.dumps(data)    
def get_container_stats():
    dict_container={}
    with os.popen("docker ps | grep registry.dev.dcos.haulmer.net/paas/dba/dcos-galera/hidden  | awk -F ' ' '{print $1}'") as pipe:
        for line in pipe:
            id_container=line.rstrip('\n')
            info=get_info_container(id_container) 
            #para cada bd dentro del cluster
            keys_dbs = re.findall(r"MYSQL_[0-9]_DB",json.dumps(info['mysql']))
            for name_bd in keys_dbs:
                app_id_hidden=info['cont_name']+"-"+info['mysql'][name_bd]
                num_bd=get_num_current_bd(name_bd)
                #hidden
                current_bd_info_hidden=get_current_bd_info_hidden(info['mysql'], num_bd)
                dict_container[app_id_hidden]=current_bd_info_hidden
                #cluster
                app_id_cluster=info['cont_name'].replace("hidden","cluster")+"-"+info['mysql'][name_bd]
                current_bd_info_cluster=get_current_bd_info_cluster(info['mysql'], num_bd)
                dict_container[app_id_cluster]=current_bd_info_cluster
            #para el cluster
            # app_id_cluster=info['cont_name']+"-cluster"
            # cluster_info=get_cluster_info(info['mysql'])
            # dict_container[app_id_cluster]=cluster_info
        with open('/tmp/json_mysql.json', 'w') as f:
            json.dump(dict_container, f, ensure_ascii=False)
        print_data_zabbix(dict_container)
get_container_stats()
