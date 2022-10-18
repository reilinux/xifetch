#! /usr/bin/env python

import platform
import os
import psutil


# gpu info
gpu_unix_command = "lspci | grep VGA"
cpu_unix_command = "cat /proc/cpuinfo | grep name"

disk_info = psutil.disk_usage('/')

result = os.popen(gpu_unix_command).readlines()
cpu_info = os.popen(cpu_unix_command).read().split('\n')

gpus = ""

for num,i in enumerate(result):
        if len(result)>1:
                gpus += f"GPU {num}" + str(i.split("controller")[1])
                gpus += "        "
        else:
                gpus += f"GPU " + str(i.split("controller:")[1]) + '        '

os_name = platform.node()
kernel = platform.release()


memory = {
        'total':round(psutil.virtual_memory().total/(1024*1024)),
        'free':round(psutil.virtual_memory().free/(1024*1024)),
        'used':round(psutil.virtual_memory().used/(1024*1024)),
}

fetch = f"""        OS: {os_name}
        Kernel: {kernel}
        DE: {os.environ.get("DESKTOP_SESSION")}
        CPU: {cpu_info[0].split(':')[1]} ({os.cpu_count()})
        {gpus}Disk: {round(disk_info.used/(1028**3))} GiB / {round(disk_info.total/(1028*1028*1028))} GiB
        Memory: {memory['used']} MiB / {memory['total']} MiB"""

print(fetch)
