#! /usr/bin/env python

import platform
import os


gpu_unix_command = "lspci | grep VGA"
os_unix_command = "cat /etc/os-release | grep PRETTY_NAME"
cpu_unix_command = "cat /proc/cpuinfo | grep name"


memory_unix_command = {
    "total": "free -m | grep Mem | awk '{print $2}'",
    "used": "free -m | grep Mem | awk '{print $3}'"
}

disk_unix_command = {
    "total": "df -h / | tail -n -1 | awk '{ print $2 \"\t\" }'",
    "used": "df -h / | tail -n -1 | awk '{ print $3 \"\t\" }'"
}

os_name = os.popen(os_unix_command).readlines()[0].split('=')[1].strip()

gpu_info = os.popen(gpu_unix_command).readlines()
cpu_info = os.popen(cpu_unix_command).read().split('\n')

memory = {
    "total": os.popen(memory_unix_command["total"]).read().strip(),
    "used": os.popen(memory_unix_command["used"]).read().strip(),
}

disk = {
    "total": os.popen(disk_unix_command["total"]).read().strip().replace('G', ' GiB'),
    "used": os.popen(disk_unix_command["used"]).read().strip().replace('G', ' GiB'),
}

gpus = ""

for num,i in enumerate(gpu_info):
    if len(gpu_info)>1:
        gpus += f"GPU {num}" + str(i.split("controller")[1])
        gpus += "        "
    else:
        gpus += f"GPU :" + str(i.split("controller:")[1]) + '        '

kernel = platform.release()

fetch = f"""        OS: {os_name}
        Kernel: {kernel}
        DE: {os.environ.get("DESKTOP_SESSION")}
        CPU: {cpu_info[0].split(':')[1]} ({os.cpu_count()})
        {gpus}Disk: {disk['used']} / {disk['total']}
        Memory: {memory['used']} MiB / {memory['total']} MiB"""

print(fetch)
