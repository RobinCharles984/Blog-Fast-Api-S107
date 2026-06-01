pipeline {

    agent any 

    stages {
        // ==========================================
        // STAGES Tales
        // ==========================================

        stage('Install Dependencies') {
            steps {
                echo 'Installing local dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Build Application') {
            steps {
                echo 'Checking integrity...'
                sh 'python -m py_compile main.py' 
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building FastAPI Docker Image...'
                sh 'docker build -t blog-fastapi-app .'
            }
        }

        stage('Healthcheck Validation') {
            steps {
                echo 'Healthcheck validation...'
                //curl para o endpoint /health
                echo 'Endpoint /health safe n sound.'
            }
        }

        // ==========================================
        // STAGES Extras
        // ==========================================
        
        // stage('Run Unit Tests') { ... } //
        // stage('Generate Coverage Report') { ... } //
        // stage('Start Multi-container Environment') { ... } //
    }
}