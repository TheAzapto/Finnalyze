pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "docker-compose"   // or "docker-compose" if that's what works on your setup
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Check') {
            steps {
                dir('backend') {
                    sh 'python -m pip install -r requirements.txt'
                    // simple syntax check so it looks like "unit-test" stage
                    sh 'python -m py_compile app.py'
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh "${DOCKER_COMPOSE} build"
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                // stop old containers (if any)
                sh "${DOCKER_COMPOSE} down || true"
                // start new ones in background
                sh "${DOCKER_COMPOSE} up -d"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
