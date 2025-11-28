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
                    sh '''
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                        # run your backend check / tests here:
                        # python app.py
                    '''
                }
             }
        }


       stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                        npm install
                        # make sure react-scripts is executable (ignore error if it already is)
                        chmod +x node_modules/.bin/react-scripts || true
                        # run the build using npx to avoid shell permission issues
                        npx react-scripts build
                    '''
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
