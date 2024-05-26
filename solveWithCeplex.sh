#!/bin/bash

# Define the timeout duration (if needed)
timeout_duration="3600s"





####################################################### With Z Variable  #######################################################

# Base directories Pc Heythem
# base_output_dir="./PcHeythem/outputsCeplexPcHeythem"
# base_time_dir="./PcHeythem/TimeSolvingCeplexPcHeythem"
# Base directories Pc Mis
base_output_dir="./PcMis/outputsCeplex"
base_time_dir="./PcMis/TimeSolvingCeplex"


# # Iterate over the years
# for yearRodef in {2024..2021}; do
#     output_dir="${base_output_dir}/${yearRodef}"
#     time_dir="${base_time_dir}/${yearRodef}"
    
#     max_parallel_sessions_range_2024=($(seq 15 -1 10))
#     max_parallel_sessions_range_2023=($(seq 18 -1 12))
#     max_parallel_sessions_range_2022=($(seq 16 -1 11))
#     max_parallel_sessions_range_2021=($(seq 10 -1 5))

#     case $yearRodef in
#         2024)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2024[@]}")
#             ;;
#         2023)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2023[@]}")
#             ;;
#         2022)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2022[@]}")
#             ;;
#         2021)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2021[@]}")
#             ;;
#         *)
#             echo "Year not supported"
#             exit 1
#     esac


#     # All the instances of one year
#     for max_parallel_sessions in "${max_parallel_sessions_range[@]}"; do
#         output_file="${output_dir}/${max_parallel_sessions}_session_output.txt"
#         time_file="${time_dir}/${max_parallel_sessions}_session_time.txt"

#         {
#             time timeout --signal=INT "$timeout_duration" python3 ./main.py "$yearRodef" "$max_parallel_sessions" > "$output_file"
#         } 2> "$time_file"
#     done

#     echo "Execution times and outputs for year $yearRodef recorded in respective files."
# done

# Define the years and corresponding max parallel sessions
years=("2024" "2023" "2022" "2021")
sessions=("9" "11" "10" "4")

# Loop through each year and session
for i in ${!years[@]}; do
    yearRodef=${years[$i]}
    max_parallel_sessions=${sessions[$i]}
    
    output_dir="${base_output_dir}/${yearRodef}"
    time_dir="${base_time_dir}/${yearRodef}"
    


    output_file="${output_dir}/${max_parallel_sessions}_session_output.txt"
    time_file="${time_dir}/${max_parallel_sessions}_session_time.txt"

    {
        time timeout --signal=INT "$timeout_duration" python3 ./main.py "$yearRodef" "$max_parallel_sessions" > "$output_file"
    } 2> "$time_file"
done

echo "Execution times and outputs for all specified years recorded in respective files With Z Variable."


###################################################################################################################################






####################################################### Without Z Variable  #######################################################



# base_output_dir_without_z="./PcHeythem/WithoutZoutputsCeplexPcHeythem"
# base_time_dir_without_z="./PcHeythem/WithoutZTimeSolvingCeplexPcHeythem"
# Base directories Pc Mis
base_output_dir_without_z="./PcMis/WithoutZoutputsCeplex"
base_time_dir_without_z="./PcMis/WithoutZTimeSolvingCeplex"


# for yearRodef in {2024..2021}; do
#     output_dir="${base_output_dir_without_z}/${yearRodef}"
#     time_dir="${base_time_dir_without_z}/${yearRodef}"

#     # Ensure directories exist
#     mkdir -p "$output_dir"
#     mkdir -p "$time_dir"
    
#     # Define max parallel sessions range for each year
#     max_parallel_sessions_range_2024=($(seq 15 -1 10))
#     max_parallel_sessions_range_2023=($(seq 18 -1 12))
#     max_parallel_sessions_range_2022=($(seq 16 -1 11))
#     max_parallel_sessions_range_2021=($(seq 10 -1 5))

#     # Select the appropriate range for the current year
#     case $yearRodef in
#         2024)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2024[@]}")
#             ;;
#         2023)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2023[@]}")
#             ;;
#         2022)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2022[@]}")
#             ;;
#         2021)
#             max_parallel_sessions_range=("${max_parallel_sessions_range_2021[@]}")
#             ;;
#         *)
#             echo "Year not supported"
#             exit 1
#     esac

#     # Loop through max parallel sessions
#     for max_parallel_sessions in "${max_parallel_sessions_range[@]}"; do
#         output_file="${output_dir}/${max_parallel_sessions}_session_output.txt"
#         time_file="${time_dir}/${max_parallel_sessions}_session_time.txt"

#         {
#             time timeout --signal=INT "$timeout_duration" python3 ./main.py "$yearRodef" "$max_parallel_sessions" 0 > "$output_file"
#         } 2> "$time_file"
#     done

#     echo "Execution times and outputs for year $yearRodef recorded in respective files."
# done

# Define the years and corresponding max parallel sessions
years=("2024" "2023" "2022" "2021")
sessions=("9" "11" "10" "4")

# Loop through each year and session
for i in ${!years[@]}; do
    yearRodef=${years[$i]}
    max_parallel_sessions=${sessions[$i]}
    
    output_dir="${base_output_dir_without_z}/${yearRodef}"
    time_dir="${base_time_dir_without_z}/${yearRodef}"

    # Ensure directories exist
    mkdir -p "$output_dir"
    mkdir -p "$time_dir"

    output_file="${output_dir}/${max_parallel_sessions}_session_output.txt"
    time_file="${time_dir}/${max_parallel_sessions}_session_time.txt"

    {
        time timeout --signal=INT "$timeout_duration" python3 ./main.py "$yearRodef" "$max_parallel_sessions" 0 > "$output_file"
    } 2> "$time_file"
done

echo "Execution times and outputs for all specified years recorded in respective files Without Z Variable."


###################################################################################################################################
