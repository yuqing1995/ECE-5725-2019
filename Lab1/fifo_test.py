#Qing Yu (qy95), Weiran Wang (ww463), Lab1, 9/11/2018

import subprocess

while(1):
    prompt_text = "Enter a command: "
    user_in = raw_input(prompt_text)
    user_command = user_in

    cmd = 'echo ' +user_command+" > /home/pi/video_fifo"
    print subprocess.check_output(cmd, shell=True)
    if (user_command == "quit"):
        break