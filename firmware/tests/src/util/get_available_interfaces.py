import subprocess


def get_available_slcan_interfaces():
    result = subprocess.run(["netstat -i | tail -n +3 |cut -d\" \" -f1"], shell=True, stdout=subprocess.PIPE)
    list_of_interfaces = result.stdout.decode("utf-8").strip().split("\n")
    result_interfaces = []
    for interface_name in list_of_interfaces:
        if "slcan" in interface_name:
            result_interfaces.append("socketcan:" + interface_name)
    print(f"Available interfaces {result_interfaces}")
    return result_interfaces
