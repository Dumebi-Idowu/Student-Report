pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--pull never'
        }
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

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

    environment {
        APP_VERSION  = '2.0.0'
        REPORT_FILE  = 'student_report.txt'
        NOTIFY_EMAIL = 'chukwudumebiuzoigwilo@gmail.com'
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
                sh '''
                    pip install pytest -q --timeout=120 \
                    || pip install pytest -q --timeout=120 \
                    --index-url https://mirrors.aliyun.com/pypi/simple/
                '''
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
                archiveArtifacts artifacts: "${env.REPORT_FILE}",
                                 fingerprint: true,
                                 onlyIfSuccessful: true
            }
        }
    }

    post {
        success {
            echo '✅ Build succeeded!'
            emailext(
                to: "${env.NOTIFY_EMAIL}",
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello Dumebi,

Your Jenkins build was successful! 🎉

Job:      ${env.JOB_NAME}
Build:    #${env.BUILD_NUMBER}
Student:  ${params.STUDENT_NAME}
Score:    ${params.STUDENT_SCORE}
School:   ${params.SCHOOL_NAME}

Download report:
${env.BUILD_URL}artifact/student_report.txt

View full build:
${env.BUILD_URL}

Regards,
Jenkins
                """
            )
        }

        failure {
            echo '❌ Build failed!'
            emailext(
                to: "${env.NOTIFY_EMAIL}",
                subject: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Hello Dumebi,

Your Jenkins build has failed! ❌

Job:     ${env.JOB_NAME}
Build:   #${env.BUILD_NUMBER}
Student: ${params.STUDENT_NAME}
Score:   ${params.STUDENT_SCORE}

Please check the console output for details:
${env.BUILD_URL}console

Regards,
Jenkins
                """
            )
        }

        always {
            cleanWs()
        }
    }
}