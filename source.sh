#!/bin/bash

input="env.dev.sh"
while IFS= read -r line
do
  echo "export $line"
  eval "export $line"
done < "$input"
