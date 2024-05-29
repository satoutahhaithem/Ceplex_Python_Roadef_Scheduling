
#!/bin/bash

# Define the timeout duration (if needed)
timeout_duration="3600s"



####################################################### With Z Variable  #######################################################

# Base directories Pc Heythem
# base_output_dir="./RevisedCode/OneThreadPcHeythem/outputsCeplexPcHeythem"
# base_time_dir="./RevisedCode/OneThreadPcHeythem/TimeSolvingCeplexPcHeythem"
# Base directories Pc Mis
base_output_dir="./RevisedCode/OneThreadPcMis/outputsCeplex"
base_time_dir="./RevisedCode/OneThreadPcMis/TimeSolvingCeplex"




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
        time timeout --signal=INT "$timeout_duration" python3 ./revisedCode.py "$yearRodef" "$max_parallel_sessions" > "$output_file"
    } 2> "$time_file"
done

echo "Execution times and outputs for all specified years recorded in respective files With Z Variable."


###################################################################################################################################






####################################################### Without Z Variable  #######################################################



# base_output_dir_without_z="./RevisedCode/OneThreadPcHeythem/WithoutZoutputsCeplexPcHeythem"
# base_time_dir_without_z="./RevisedCode/OneThreadPcHeythem/WithoutZTimeSolvingCeplexPcHeythem"
# Base directories Pc Mis
base_output_dir_without_z="./RevisedCode/OneThreadPcMis/WithoutZoutputsCeplex"
base_time_dir_without_z="./RevisedCode/OneThreadPcMis/WithoutZTimeSolvingCeplex"




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
        time timeout --signal=INT "$timeout_duration" python3 ./revisedCode.py "$yearRodef" "$max_parallel_sessions" 0 > "$output_file"
    } 2> "$time_file"
done

echo "Execution times and outputs for all specified years recorded in respective files Without Z Variable."


###########################################################################################################################