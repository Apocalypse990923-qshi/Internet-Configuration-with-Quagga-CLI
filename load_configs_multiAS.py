import os
import subprocess
import sys

def load_config_to_router(router_name, config_file_paths):
    print("Start configuring router: {0}".format(router_name))
    all_commands = []
    all_commands.append('configure terminal')

    # Parse the .sav files, filtering out unwanted lines and accumulating the commands
    print("Parsing files: {0}, {1}, {2}".format(config_file_paths[0],config_file_paths[1],config_file_paths[2]))
    for path in config_file_paths:
        with open(path, 'r') as f:
            for line in f:
                stripped_line = line.strip()

                # Skip comments, empty lines, and specific unwanted lines
                if stripped_line.startswith('!') or not stripped_line:
                    continue
                if stripped_line.startswith('hostname') or stripped_line.startswith('password'):
                    continue
                if stripped_line.startswith('log file') or stripped_line.startswith('line vty'):
                    continue
                
                all_commands.append(stripped_line)

    all_commands.append('end')
    all_commands.append('write file')
    all_commands.append('write file')

    combined_commands = '\n'.join(all_commands)

    # Get the router's PID and execute the commands in its context
    pid_command = "ps ax | grep 'mininet:{}$' | grep bash | grep -v mxexec | awk '{{print $1}}'".format(router_name)
    pid = subprocess.check_output(pid_command, shell=True).strip()

    # Pass multiple commands to `vtysh`
    cmd = "sudo mxexec -a {0} -b {0} -k {0} vtysh -c '{1}'".format(pid,combined_commands)
    print("Command to execute:")
    print(cmd)
    try:
        subprocess.call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command Output:", e.output)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python load_configs_multiAS.py configs_multiAS")
        sys.exit(1)

    config_base_path = sys.argv[1]
    routers = ["ATLA","CHIC","HOUS","KANS","LOSA","NEWY","SALT","SEAT","WASH","east","west"]
    for router in routers:
        config_files = [os.path.join(config_base_path, router, "zebra.conf.sav"), os.path.join(config_base_path, router, "ospfd.conf.sav"), os.path.join(config_base_path, router, "bgpd.conf.sav")]
        load_config_to_router(router, config_files)
