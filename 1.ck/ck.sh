#!/bin/bash

check_parameter () {
            : ${1?Repo url required.}
    }
check_parameter $1

REPO=$1
PROJECT_NAME=${REPO##*/}
filename="${PROJECT_NAME}.csv"
mkdir results/"${PROJECT_NAME}"

git clone "$REPO" "$PROJECT_NAME"

while read commit; do
# reading each commit 
echo "$commit"
cd "${PROJECT_NAME}"
git fetch
git checkout $commit
cd .. 
/usr/lib/jvm/jdk-20/bin/java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar "${PROJECT_NAME}" true 0 false ./
mv class.csv results/"${PROJECT_NAME}"/"${PROJECT_NAME}"_"${commit}"_class.csv
mv method.csv results/"${PROJECT_NAME}"/"${PROJECT_NAME}"_"${commit}"_method.csv
done < $filename

rm -Rf "${PROJECT_NAME}"
#for f in *;do mv -i "$f" "${f//[\"\'\r[:space:]]}"; done