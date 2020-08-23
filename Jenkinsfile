pipeline {
    agent{
        label 'python'
    }
    stages {
        stage('Prepare: Python') {
            steps {
                sh 'python3.7 -m venv .venv'
                sh './.venv/bin/python -m pip install -r requirements.txt'
                sh './.venv/bin/python -m pip install pylint'
            }
        }
        stage('Tests: Static') {
            steps {
                sh './.venv/bin/pylint eoq_calculator.py'
            }
        }
        stage('Tests: Functions') {
            steps {
                sh './.venv/bin/python eoq_calculator_tests.py -v'
            }
        }
    }
}