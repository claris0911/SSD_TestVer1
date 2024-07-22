pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git'
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
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=SSDPrac \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://192.168.1.131:9000 \
                      -Dsonar.login=sqp_7f6b61eee86d461af49270cf67c765ad1db31ca5
                    '''
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
