pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_Lab.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=SSDPrac -Dsonar.sources=. -Dsonar.host.url=http://127.0.0.1:9000 -Dsonar.login=admin -Dsonar.password=09J48v02"
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker-compose down'
        }
    }
}
