#Interfaces with VLC through the LUA CL
#Removes last playlist item when detected that VLC can't play it (otherwise causes endless errors)

import asyncio
import websockets
import time
import random

enable_websockets = True

async def read_stream(stream, cb):  
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break  

async def main():
    command = ["script", "-c cvlc --control cli"]
    #command = ["script", "-c cvlc --control cli --video-wallpaper"]

    vlc_process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    print(vlc_process)

    def send_command(command):
        print("Sending command: "+ command)
        vlc_process.stdin.write(bytes(command, 'utf-8') + b'\n')

    def handle_output(output_raw):
        output = str(output_raw, "utf-8").strip('\n')

        print(output)

        #auto-stop
        if output.__contains__("error"):
            send_command("stop")

        #test auto-stop
        #if output.__contains__("initialized"):
        #    time.sleep(2)
        #    send_command("add a")

        if output.__contains__("initialized"):
            time.sleep(2)
            #send_command("add https://www.youtube.com/watch?v=krLYZmPRtnc")

    async def random_commands():
        commands = [
            "add file:///home/paul/Videos/clown pepe.webm", 
            "add file:///home/paul/Collections/Funny Content/hard knock life.webm", 
            "add file:///home/paul/Videos/webm/AAAA.webm", 
            "add file:///home/paul/Videos/webm/cat gone.webm",
            "add file:///home/paul/Collections/Funny Content/thhhhhh.webm", 
            "add file:///home/paul/Collections/Funny Content/power lifter.webm", 
            "add BABABABABABABABABABABBABABAABABBBABBABABBBABBABBABABABABKFJHAKJHKASDHKASDASDLBAYFAKFIAUFEIUFAIUFH,AHEFB,KEHFGYASDGTYKGFAGJEFHJEFRKLIUHLAEAEGRFLBFABFRLHYAFRHAGERFJHVAWEVAKYUAWEVFKUV",
            "add https://www.youtube.com/watch?v=krLYZmPRtnc" ,
            "add BABABABABABABABABABABBABABAABABBBABBABABBBABBABBABABABABKFJHAKJHKASDHKASDASDLBAYFAKFIAUFEIUFAIUFH,AHEFB,KEHFGYASDGTYKGFAGJEFHJEFRKLIUHLAEAEGRFLBFABFRLHYAFRHAGERFJHVAWEVAKYUAWEVFKUV",
        ]
        while True:
            send_command(random.choice(commands))
            await asyncio.sleep(3)

    async def other():
        while True:
            #print("async as fuck")
            await asyncio.sleep(0.3)

        #read_stream(process.stdout, lambda x: print("STDOUT: %s" % x)),
    
    async def handle_websocket(websocket, path):
        async for message in websocket:
            if message.startswith("#"): 
                message = message[1:]
                send_command(message)
                await websocket.send(message)


    loop.create_task(other())

    #loop.create_task(random_commands())

    handle_stdout = loop.create_task(read_stream(vlc_process.stdout, handle_output))
    handle_stderr = loop.create_task(read_stream(vlc_process.stderr, lambda x: print("STDERR: %s" % x)))

    if enable_websockets: 
        def get_port():
            import socket
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.bind(('', 0))
            addr, port = tcp.getsockname()
            tcp.close()
            return 5894
            return port

        port = get_port()
        loop.create_task(await websockets.serve(handle_websocket, 'localhost', port))
        print("Websocket interface listening on port "+str(port))

    await asyncio.wait([handle_stderr, handle_stdout])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
