import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import logging

# Setup logger
logging.basicConfig(filename='network_config.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load YAML
with open('exer_network_topology.yaml') as f:
    devices = yaml.safe_load(f)['devices']

# Setup Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('exer_router_config.j2')

# Push configs
for name, config in devices.items():
    try:
        rendered_config = template.render(**config)
        logging.info(f'Generated config for {name}:\n{rendered_config}')

        device_params = {
            'device_type': 'cisco_ios',
            'host': config['interfaces'][list(config['interfaces'].keys())[0]]['ip'],
            'username': 'admin',
            'password': 'admin',
            'secret': 'admin'
        }

        net_connect = ConnectHandler(**device_params)
        net_connect.enable()
        net_connect.send_config_set(rendered_config.splitlines())
        logging.info(f"Configuration pushed to {name}")
        net_connect.disconnect()

    except Exception as e:
        logging.error(f"Error configuring {name}: {e}")
