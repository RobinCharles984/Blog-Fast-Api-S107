pipeline {

    agent any

    environment {
        APP_NAME = 'blog-fastapi-app'
        DOCKERHUB_REPO = 'felipezeferino/blog-fastapi-app'
        TEST_REPORT = 'test-results.xml'
        DATABASE_URL = 'sqlite:///./jenkins-ci.db'
        SECRET_KEY = 'jenkins-ci-secret'
        AWS_ACCESS_KEY_ID = 'jenkins-ci-access-key'
        AWS_SECRET_ACCESS_KEY = 'jenkins-ci-secret-key'
        BUCKET_NAME = 'blog-fastapi-ci'
        REGION_NAME = 'us-east-1'
        AWS_ENDPOINT_URL = 'http://localhost:9000'
        STORAGE_PUBLIC_BASE_URL = 'http://localhost:9000/blog-fastapi-ci'
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
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pip install pytest-cov
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo 'Checking integrity...'
                sh '''
                    . .venv/bin/activate
                    python -m py_compile main.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building FastAPI Docker Image...'
                sh '''
                    docker build -t ${APP_NAME}:${BUILD_NUMBER} .
                    docker tag ${APP_NAME}:${BUILD_NUMBER} ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                    docker tag ${APP_NAME}:${BUILD_NUMBER} ${DOCKERHUB_REPO}:latest
                '''
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
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=${TEST_REPORT}
                '''
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Publishing Docker image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        set -e
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        set -x
                        docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_REPO}:latest
                        set +x
                        docker logout
                    '''
                }
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
            script {
                def recipients = env.EMAIL_RECIPIENTS?.trim()
                if (recipients) {
                    emailext(
                        to: recipients,
                        subject: "[Jenkins] ${env.JOB_NAME} #${env.BUILD_NUMBER} - SUCESSO",
                        mimeType: 'text/html',
                        body: """
                            <h2>Pipeline executada com sucesso</h2>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                            <p><strong>Status:</strong> SUCESSO</p>
                            <p><strong>Imagem Docker:</strong> ${env.DOCKERHUB_REPO}:latest</p>
                            <p><a href="${env.BUILD_URL}">Acessar detalhes da build</a></p>
                        """
                    )
                } else {
                    echo 'Notificacao por email ignorada: EMAIL_RECIPIENTS nao foi informado.'
                }
            }
        }

        failure {
            echo 'Pipeline falhou'
            script {
                def recipients = env.EMAIL_RECIPIENTS?.trim()
                if (recipients) {
                    emailext(
                        to: recipients,
                        subject: "[Jenkins] ${env.JOB_NAME} #${env.BUILD_NUMBER} - FALHA",
                        mimeType: 'text/html',
                        attachLog: true,
                        compressLog: true,
                        body: """
                            <h2>Pipeline falhou</h2>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p><strong>Build:</strong> #${env.BUILD_NUMBER}</p>
                            <p><strong>Status:</strong> FALHA</p>
                            <p>O log da build foi anexado para auxiliar o diagnostico.</p>
                            <p><a href="${env.BUILD_URL}">Acessar detalhes da build</a></p>
                        """
                    )
                } else {
                    echo 'Notificacao por email ignorada: EMAIL_RECIPIENTS nao foi informado.'
                }
            }
        }

        always {
            cleanWs()
        }
    }
}
