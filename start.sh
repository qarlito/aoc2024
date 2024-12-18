set -e -u

num=$1

INPUT=P${num}_input.py
SOLUTION=P${num}_solution.py

if [ -e ${INPUT} ]; then
    echo Error file already exists
    exit 1
fi

if [ -e ${SOLUTION} ]; then
    echo Error file already exists
    exit 1
fi

cp P00_input_template.py ${INPUT}

echo "#!./venv/bin/python3" > ${SOLUTION}
echo "from P${num}_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT" >> ${SOLUTION}
cat P00_solution_template.py >> ${SOLUTION}
chmod u+x ${SOLUTION}

