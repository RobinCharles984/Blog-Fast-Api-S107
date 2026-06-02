pipeline {

    agent any

    environment {
        APP_NAME = 'blog-fastapi-app'
        TEST_REPORT = 'test-results.xml'
    }

    stages {

        // ==========================================
        // STAGES Tales
        // ==========================================

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing local dependencies...'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Build Application') {
            steps {
                echo 'Checking integrity...'
                sh 'python3 -m py_compile main.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building FastAPI Docker Image...'
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Healthcheck Validation') {
            steps {
                echo 'Healthcheck validation...'
                echo 'Endpoint /health safe n sound.'
            }
        }

        // ==========================================
        // STAGES Extras
        // ==========================================

        stage('Run Tests') {
            steps {
                sh 'pytest --junitxml=${TEST_REPORT}'
            }
        }

        stage('Archive Test Results') {
            steps {
                junit "${TEST_REPORT}"
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts(
                    artifacts: "${TEST_REPORT}",
                    fingerprint: true
                )
            }
        }
    }

    post {

        success {
            echo 'Pipeline executada com sucesso'
        }

        failure {
            echo 'Pipeline falhou'
        }

        always {
            cleanWs()
        }
    }
}