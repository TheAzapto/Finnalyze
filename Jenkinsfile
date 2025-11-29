pipeline {
    agent any

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
                        rm -rf .venv
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                        # run backend checks here if you want, e.g.:
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
                sh '''
                    docker-compose build
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    docker-compose down || true
                    docker-compose up -d
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
