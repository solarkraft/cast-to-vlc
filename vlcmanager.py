#Interfaces with VLC through the LUA CL
#Removes last playlist item when detected that VLC can't play it (otherwise causes endless errors)

import asyncio
import websockets
import time

process = "vlc process one day"

async def read_stream(stream, cb):  
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break  

async def monitor_vlc():
    command = ["script", "-c cvlc --control cli"]

    process = await asyncio.create_subprocess_exec(*command,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)

    def send_command(command):
        print("Sending command: "+ command)
        process.stdin.write(bytes(command, 'utf-8') + b'\n')

    def handle_output(output_raw):
        output = str(output_raw, "utf-8").strip('\n')

        print(output)

        #auto-stop
        if output.__contains__("main input error"):
            send_command("stop")

        #test auto-stop
        if output.__contains__("initialized"):
            time.sleep(2)
            send_command("add a")


    await asyncio.wait([
        #read_stream(process.stdout, lambda x: print("STDOUT: %s" % x)),
        read_stream(process.stdout, handle_output),
        read_stream(process.stderr, lambda x: print("STDERR: %s" % x))
    ])

    return await process.wait()


async def other():
    while True:
        print("henlo")
        await asyncio.sleep(10)

if __name__ == '__main__':

    #command = ["./slowprogram.sh"]
    #command = ["./echo.sh"]

    loop = asyncio.get_event_loop()

    loop.create_task(monitor_vlc())
    loop.create_task(other())

    loop.run_forever()
    loop.close()
