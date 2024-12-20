


async def player(button,ivr: YateIVR):
    dirname = "/usr/local/share/yate/sounds/basic"
    dtmf_symbol = button
    if dtmf_symbol == "*":
        await ivr.silence()
    elif dtmf_symbol == "1":
        await ivr.play_soundfile(os.path.join(dirname, "1.slin"),complete=True, repeat=False)
    elif dtmf_symbol == "2":
        await ivr.play_soundfile(os.path.join(dirname, "2.slin"))
    elif dtmf_symbol == "0":
