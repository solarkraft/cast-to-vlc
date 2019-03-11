#Interfaces with VLC through the LUA CL
#Removes last playlist item when detected that VLC can't play it (otherwise causes endless errors)

import subprocess
import time

#command = ["./slowprogram.sh"]
#command = ["./echo.sh"]
command = ["script", "-c cvlc --control cli"]

with subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, shell=False) as p:
    def send(command):
        p.stdin.write(bytes(command, 'utf-8') + b'\n')
        p.stdin.flush()

    for line in iter(p.stdout.readline, b''):
        print(str(line, 'utf-8').strip('\n'))
        #time.sleep(0.1)

        if line.__contains__(b"Command Line Interface initialized"):
            #time.sleep(1)
            send("add abcd")

        if line.__contains__(b"main input error"):
            send("stop")


        
p.wait()
