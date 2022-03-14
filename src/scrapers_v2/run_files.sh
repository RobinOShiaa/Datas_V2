  GNU nano 2.9.3                                         run_files.sh
#!/bin/bash

echo "Please enter Mains or Tests to be run,(M/T)"
read input
declare -A options
options[M]="Mains"
options[T]="Tests"

if [ $input == "M" ];
        then
                echo ${options[M]}
                echo "now running ${options[M]}"
                ./run_mains.sh
fi

if [ $input == "T" ];
        then
                echo "now running ${options[T]}"
                ./run_tests.sh
fi




