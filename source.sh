#!/bin/bash

input="env.dev.sh"
while IFS= read -r line
do
  eval "export $line"
done < "$input"
