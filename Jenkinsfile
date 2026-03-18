pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--pull never'
        }
    }

    // ✅ CONCEPT 4: Triggers
    triggers {
        pollSCM('H/5 * * * *')
    }

    // ✅ CONCEPT 3: Parameters
    parameters {
        string(
            name: 'STUDENT_NAME',
            defaultValue: 'Dumebi Idowu',
            description: 'Enter student name'
        )
        string(
            name: 'STUDENT_SCORE',
            defaultValue: '72',
            description: 'Enter student score (0-100)'
        )
        choice(
            name: 'SCHOOL_NAME',
            choices: ['Greenfield Academy', 'Bluefield College', 'Redfield University'],
            description: 'Select the school'
        )
    }

    // ✅ CONCEPT 2: Environment Variables
    environment {
        APP_VERSION = '1.0.0'
        REPORT_FILE = 'student_report.txt'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "🚀 Student Report System version ${env.APP_VERSION}"
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install pytest -q'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python -m pytest test_student_report.py -v'
            }
        }

        stage('Generate Report') {
            steps {
                echo "Generating report for ${params.STUDENT_NAME}..."
                // ✅ CONCEPT 5: Credentials
                withCredentials([string(credentialsId: 'report-signing-key', variable: 'SIGNING_KEY')]) {
                    sh """
                        export STUDENT_NAME="${params.STUDENT_NAME}"
                        export STUDENT_SCORE="${params.STUDENT_SCORE}"
                        export SCHOOL_NAME="${params.SCHOOL_NAME}"
                        export SIGNING_KEY="${SIGNING_KEY}"
                        python student_report.py
                    """
                }
            }
        }

        stage('Archive Report') {
            steps {
                echo 'Saving report as artifact...'
                // ✅ CONCEPT 6: Artifacts
                archiveArtifacts artifacts: "${env.REPORT_FILE}",
                                 fingerprint: true,
                                 onlyIfSuccessful: true
            }
        }
    }

    post {
        success {
            echo "✅ Report for ${params.STUDENT_NAME} generated and saved!"
        }
        failure {
            echo '❌ Pipeline failed. Check the logs.'
        }
        always {
            cleanWs()
        }
    }
}