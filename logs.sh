#!/bin/bash

containers=$(docker ps --format "{{.Names}}")

#colors=
#(
#	"\033[0;31m"  # Red
#    "\033[0;32m"  # Green
#    "\033[0;33m"  # Yellow
#    "\033[0;34m"  # Blue
#    "\033[0;35m"  # Magenta
#    "\033[0;36m"  # Cyan
#    "\033[0;37m"  # White
#)
#
#reset="\033[0m"
#
#color_index=0
#
#for container in $containers; do
#	color=${colors[$color_index]}
#	echo -e "${color}$container${reset}"
#	docker logs "$container" | sed "s/^/${color}/" | sed "s/$/S{reset}/"
#	echo "\n---------------------------------------\n"
#	color_index=$(( (color_index + 1) % ${#colors[@]} ))
#done


for container in $containers; do
	echo -e "\033[0;33m\n---------------------------------------\n"
	echo -e "$container"
	echo -e "\n---------------------------------------\n\033[0m"
	docker logs "$container"
done
