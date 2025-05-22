from jinja2 import Environment, FileSystemLoader
import yaml

# Declare template environment
ENV = Environment(loader=FileSystemLoader('.'))

def get_interface_speed(interface_name):
    """Returns Mbps based on interface name."""
    if 'gigabit' in interface_name.lower() or 'g1' in interface_name.lower():
        return 1000
    if 'fast' in interface_name.lower():
        return 100
    if 'v' in interface_name.lower():  # for virtual interfaces
        return 10000  # assume virtual links are high-speed
    return 10  # default for unknown types

# Add custom filter
ENV.filters['get_interface_speed'] = get_interface_speed

# Load template
template = ENV.get_template("assignment.j2")

# Load YAML data
with open("assignment.yml") as f:
    interfaces = yaml.load(f, Loader=yaml.SafeLoader)

# Render and print
print(template.render(interface_list=interfaces))
