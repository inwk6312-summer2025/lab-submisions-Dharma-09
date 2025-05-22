import yaml
from netmiko import ConnectHandler
import textfsm
import logging

# Setup logger
logging.basicConfig(filename='routing_table.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_routing_table(output):
    with open('cisco_ios_show_ip_route.textfsm') as f:
        fsm = textfsm.TextFSM(f)
        result = fsm.ParseText(output)
    return result

# Load device YAML
with open('exer_network_topology.yaml') as f:
    devices = yaml.safe_load(f)['devices']

# Collect routes
for name, config in devices.items():
    try:
        device_params = {
            'device_type': 'cisco_ios',
            'host': config['interfaces'][list(config['interfaces'].keys())[0]]['ip'],
            'username': 'admin',
            'password': 'admin',
            'secret': 'admin'
        }

        net_connect = ConnectHandler(**device_params)
        net_connect.enable()

        output = net_connect.send_command("show ip route")
        routes = parse_routing_table(output)

        logging.info(f"Routing table for {name}:\n{routes}")
        print(f"{name} Routes:\n{routes}\n")

        net_connect.disconnect()

    except Exception as e:
        logging.error(f"Error collecting routing table from {name}: {e}")
