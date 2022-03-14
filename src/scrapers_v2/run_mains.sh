#!/bin/bash

export PYTHONPATH=/var/lib/jenkins/workspace/wq/src/scrapers_v2/scrapers
export PYTHONPATH=$PYTHONPATH:/var/lib/jenkins/workspace/wq/src/scrapers_v2/scraper_classes
export PYTHONPATH=$PYTHONPATH:/var/lib/jenkins/workspace/wq/src/scrapers_v2

for File in /var/lib/jenkins/workspace/wq/src/scrapers_v2/scrapers/*;do
        export len=${File:69:82}
        echo $len
        export dot=${File:$((${#File}-3)):1}
        echo $dot
        export dot2=${File:$((${#File}-4)):1}
        echo $dot2
        export undrscr=${File:$((${#File}-1)):1}
        echo $undrscr
        if [ "$dot" == "." ] || [ "$dot2" == "." ] || [ "$undrscr" == "_" ] ; then
        echo "Miscelaneos file"
        else
                echo $File
                cd $File
                echo "$File/*"
                for Tests in $File/*;do
                        echo "$Tests"
                        echo "Testing"
                        ls
                        if [[ $Tests != *"test"* && $Tests == *".py"* ]];
                        then
                                python3.7 "$Tests" | cut -d'/' -f 12

                        fi
                done
        fi
done
