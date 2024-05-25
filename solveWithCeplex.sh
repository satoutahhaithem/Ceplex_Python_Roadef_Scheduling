#!/bin/bash

# Define the timeout duration (if needed)
timeout_duration="10s"

# Base directories Pc Heythem
base_output_dir="./outputsCeplexPcHeythem"
base_time_dir="./TimeSolvingCeplexPcHeythem"
# Base directories Pc Mis
# base_output_dir="./outputsCeplex"
# base_time_dir="./TimeSolvingCeplex"


# Iterate over the years
for yearRodef in {2024..2021}; do
    output_dir="${base_output_dir}/${yearRodef}"
    time_dir="${base_time_dir}/${yearRodef}"
    
    max_parallel_sessions_range_2024=($(seq 15 -1 9))
    max_parallel_sessions_range_2023=($(seq 18 -1 11))
    max_parallel_sessions_range_2022=($(seq 16 -1 10))
    max_parallel_sessions_range_2021=($(seq 10 -1 4))

    case $yearRodef in
        2024)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2024[@]}")
            ;;
        2023)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2023[@]}")
            ;;
        2022)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2022[@]}")
            ;;
        2021)
            max_parallel_sessions_range=("${max_parallel_sessions_range_2021[@]}")
            ;;
        *)
            echo "Year not supported"
            exit 1
    esac


    # All the instances of one year
    for max_parallel_sessions in "${max_parallel_sessions_range[@]}"; do
        output_file="${output_dir}/${max_parallel_sessions}_session_output.txt"
        time_file="${time_dir}/${max_parallel_sessions}_session_time.txt"

        {
            time timeout --signal=INT "$timeout_duration" python3 ./main.py "$yearRodef" "$max_parallel_sessions" > "$output_file"
        } 2> "$time_file"
    done

    echo "Execution times and outputs for year $yearRodef recorded in respective files."
done
