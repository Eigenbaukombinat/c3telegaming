# c3telegaming setup

This is an example of a minimal [yate](https://docs.yate.ro/wiki/Main_Page) setup, which registers via an upstream SIP trunk and answers all calls with script. Then sends the DTMF Codes via UDP Packages to the Host System.
On the Host System [phony](https://github.com/Eigenbaukombinat/phony) insert the Key Presses as Keyboard inputs.

## How to

### get the source

``` sh
git clone https://github.com/Eigenbaukombinat/c3telegaming
cd c3telegaming
```

### modify SIP settings

Rename [accfile.conf.sample](config/accfile.conf.sample) accfile.conf to with your SIP Account credentials. If you don't have a SIP Account, you may use an [EPVPN Account](https://eventphone.de/doku/epvpn) for __testing__ purposes.

### run phony on the Host-System

Get the Code from https://github.com/Eigenbaukombinat/phony
Please finde the Manual in the [Readme](https://github.com/Eigenbaukombinat/phony/blob/main/README.md)

### scripts in the Docker Container

- [phony.py](scripts/phony.py) - send phone input as UDP Packages
More examples can be found in the [yate-tcl](https://github.com/bef/yate-tcl) or  [eventphone](https://github.com/eventphone/hotline/tree/master/hotline)repository.

If you want to use custom audio files, place them in the [sounds](sounds) directory

### convert your audio files

You can use the following sox command to convert your mp3 or wav files to slin:

```sh
sox input.mp3 -t raw -r 8000 -c 1 output.slin
```

You may need to install the sox format handler:

```sh
apt install libsox-fmt-mp3
```

### configure c3telegaming

Update [regexroute.conf](config/regexroute.conf) to point to your custom script. You can also route to different scripts depending on the caller or dialed number. Details can be found in the [Yate WIKI](https://docs.yate.ro/wiki/Regular_expressions#The_regexroute_configuration_file).

### build your custom docker container

``` sh
docker build -t c3telegaming .
```

### run

``` sh
docker run -it c3telegaming
```

## Help

If you need any additional help, open github issue.
