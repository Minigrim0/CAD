#!/bin/bash

input=$1
while IFS= read -r line
do
  eval "export $line"
done < "$input"
