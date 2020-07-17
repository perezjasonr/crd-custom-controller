# import json
# import yaml
from kubernetes import client, config, watch

group = "stable.example.com"
namespace = "crd-test"
version = "v1"
plural = "dalmations"
resource_version = ""


def evaluate(crd_api, obj):
    metadata = obj.get("metadata")
    collar = obj["spec"]["collar"]
    name = metadata.get("name")
    petname = obj["spec"]["petname"]

    if collar:
        print(f"{petname} already has a collar")
        # make it part of the obj
        # obj["spec"]["comment"] = ""
    else:
        print(f"{petname} doesn't have a collar, giving {petname} a collar")
        # obj["spec"]["comment"] = ""
        obj["spec"]["collar"] = True

    obj["spec"]["evaluated"] = True
    crd_api.replace_namespaced_custom_object(group, version, namespace, plural, name, obj)
    print(f"{petname} has been evaluated")


def main():
    config.load_incluster_config() # load_kube_config()

    crd_api = client.CustomObjectsApi()
    print("Waiting for dalmations:")
    while True:
        w = watch.Watch()
        stream = w.stream(crd_api.list_namespaced_custom_object, group,
                          version, namespace, plural, resource_version=resource_version)

        for event in stream:
            obj = event["object"]
            operation = event["type"]
            spec = obj.get("spec")
            metadata = obj.get("metadata")
            name = metadata["name"]
            cleared = spec.get("evaluated", False)
            print(f"handling {operation} on {name}")
            if cleared:
                continue
            evaluate(crd_api, obj)


if __name__ == "__main__":
    main()