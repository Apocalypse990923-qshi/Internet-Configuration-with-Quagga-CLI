import os
import subprocess
import sys

def load_config_to_host(host_id, hosts, interfaces):
    print("Start configuring the {0}th host: {1}".format(host_id+1, hosts[host_id]))

    # Get the host's PID and execute the commands in its context
    pid_command = "ps ax | grep 'mininet:{}$' | grep bash | grep -v mxexec | awk '{{print $1}}'".format(hosts[host_id])
    pid = subprocess.check_output(pid_command, shell=True).strip()

    sample_cmd = "sudo mxexec -a {0} -b {0} -k {0} ifconfig".format(pid)
    # Pass multiple commands to `vtysh`
    cmd1 = "sudo mxexec -a {0} -b {0} -k {0} sudo ifconfig {1} 4.10{2}.0.1/24 up".format(pid,interfaces[host_id],host_id+1)
    cmd2 = "sudo mxexec -a {0} -b {0} -k {0} sudo route add default gw 4.10{1}.0.2 {2}".format(pid,host_id+1,interfaces[host_id])
    print("Command to execute ip address configuration:")
    print(cmd1)
    try:
        subprocess.call(cmd1, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command Output:", e.output)
    print("Command to execute default gateway configuration:")
    print(cmd2)
    try:
        subprocess.call(cmd2, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Command Output:", e.output)


if __name__ == '__main__':
    hosts = ["NEWY-host","CHIC-host","WASH-host","ATLA-host","KANS-host","HOUS-host","SALT-host","LOSA-host","SEAT-host"]
    interfaces = ["newy","chic","wash","atla","kans","hous","salt","losa","seat"]
    for i in range(9):
        load_config_to_host(i, hosts, interfaces)
