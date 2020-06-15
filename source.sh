#!/bin/bash

input="env.dev.sh" # Your env file, may have an other name
while IFS= read -r line
do
  eval "export $line"
done < "$input"
