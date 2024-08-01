#!/bin/sh

str="./src/.env"

if test -e "$str"; then
    echo -n "DNS=" > .host
    hostname -s | tr -d '\n' >> .host
    
    if grep -q "^DNS=" "$str"; then
        sed -i '/^DNS=/d' "$str"
    fi
    
    cat .host >> "$str"
    rm .host
	echo >> "$str"
fi
