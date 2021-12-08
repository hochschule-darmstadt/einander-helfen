#!/bin/bash
# Default context
context=DE

while getopts :hc: flag
do
  case "${flag}" in
    h) echo "Switch context with flag -c ['DE' (Default), 'US']";exit;;
    c) context=${OPTARG};;
  esac
done

python3 ../execute_elastic_upload.py -c "$context"