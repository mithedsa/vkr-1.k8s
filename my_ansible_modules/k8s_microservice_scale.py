from ansible.module_utils.basic import AnsibleModule
import subprocess

def scale_microservice(name, replicas, namespace):
    """Масштабирует количество реплик в Deployment"""
    cmd = [
        "kubectl", "scale", "deployment", name,
        "--replicas={}".format(replicas),
        "--namespace={}".format(namespace)
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"changed": True, "msg": f"Scaled {name} to {replicas} replicas"}
    except subprocess.CalledProcessError as e:
        return {"changed": False, "msg": f"Failed to scale microservice: {str(e)}"}

def delete_microservice(name, namespace):
    """Удаляет Deployment"""
    cmd = [
        "kubectl", "delete", "deployment", name,
        "--namespace={}".format(namespace)
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"changed": True, "msg": f"Deleted microservice {name}"}
    except subprocess.CalledProcessError as e:
        return {"changed": False, "msg": f"Failed to delete microservice: {str(e)}"}

def run():
    module_args = dict(
        name=dict(type="str", required=True),
        namespace=dict(type="str", required=True),
        replicas=dict(type="int", required=False),
        state=dict(type="str", choices=["present", "absent"], required=True)
    )
    
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    name = module.params['name']
    namespace = module.params['namespace']
    state = module.params['state']
    replicas = module.params.get('replicas')

    if state == "present":
        if replicas is None:
            module.fail_json(msg="Replicas parameter is required when state=present")
        result = scale_microservice(name, replicas, namespace)
    elif state == "absent":
        result = delete_microservice(name, namespace)

    if result["changed"]:
        module.exit_json(changed=True, msg=result["msg"])
    else:
        module.fail_json(msg=result["msg"])

if __name__ == "__main__":
    run()

