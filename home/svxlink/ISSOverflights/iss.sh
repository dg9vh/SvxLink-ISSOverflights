#!/bin/bash
cd /home/svxlink/ISSOverflights
/usr/bin/python3 create_announcement.py

FILE=/home/svxlink/ISSOverflights/ISS.txt
if [ -f "$FILE" ]; then
	echo "Running TTS"
	messageT=$(cat $FILE)
        echo $messageT
	pico2wave --lang de-DE --wave /var/spool/svxlink/issinfo/message.wav "$messageT"
	echo "Normalize audio-file"
	normalize-audio -g 1dB /var/spool/svxlink/issinfo/message.wav
fi
