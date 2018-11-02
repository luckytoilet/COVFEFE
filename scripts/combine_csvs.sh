#!/bin/bash
# Script to combine all the CSVs in a directory
# Usage: sh combine_csvs.sh [directory] > [result.csv]

CSV_DIRECTORY=$1

ONE_CSV_FILE=$(find $CSV_DIRECTORY -maxdepth 1 -name "*.csv" | head -n 1)
echo $(cat $ONE_CSV_FILE | head -n 1)

for csvf in $(find $CSV_DIRECTORY -maxdepth 1 -name "*.csv"); do
  echo $(cat $csvf | head -2 | tail -1)
done

