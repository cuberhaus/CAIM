#!/bin/bash


while read -r line 
do
    gnome-terminal --tab -e "bash -c 'eval $line && sleep 5'"     
done < $1
