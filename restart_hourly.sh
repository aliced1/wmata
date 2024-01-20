#!/bin/bash

PATH=/home/alice/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:/home/alice

while true
do
	python /home/alice/wmata/driver.py &
	TIME=$( date +%s )

	while [ $(date +%s) -lt $(($TIME+15)) ]
	TEST=$(( $(date +%s) - $(($TIME+15)) ))
	do
		printf "test = %s" "$TEST"
		sleep 5
	done
	killall python
	sleep 10
done
