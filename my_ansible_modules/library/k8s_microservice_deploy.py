#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def deploy_microservice(name, image, replicas, namespace):
    # Создаем деплоймент для микросервиса
    cmd = [
        "kubectl", "create", "deployment", name,
        "--image={}".format(image),
        "--replicas={}".format(replicas),
        "--namespace={}".format(namespace)
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"changed": True, "msg": "Microservice deployed"}
    except subprocess.CalledProcessError as e:
        return {"changed": False, "msg": f"Failed to deploy microservice: {str(e)}"}

def run():
    # Определяем параметры, которые принимает модуль
    module_args = dict(
        name=dict(type="str", required=True),
        image=dict(type="str", required=True),
        replicas=dict(type="int", required=True),  # Убираем default здесь
        namespace=dict(type="str", required=True)
    )

    # Создаем объект AnsibleModule
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # Развертываем микросервис
    result = deploy_microservice(module.params['name'], module.params['image'], module.params['replicas'], module.params['namespace'])

    # Завершаем работу модуля с результатом
    if result["changed"]:
        module.exit_json(changed=True, msg=result["msg"])
    else:
        module.fail_json(msg=result["msg"])

if __name__ == "__main__":
    run()

