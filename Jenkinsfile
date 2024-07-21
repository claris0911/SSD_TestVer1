pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git', credentialsId: '8ecd7d43-cbab-4a10-9ee8-1c31ad258a71'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t my-webapp .'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker run --rm my-webapp pytest tests/'
            }
        }
        stage('Code Quality Check via SonarQube') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=ssd_ver1 \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://192.168.1.131:9000 \
                            -Dsonar.token=sqp_0c3811652bd2c25f9158dc9d69d8b9d32afc6148"
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
    post {
        always {
            recordIssues(enabledForFailure: true, tool: sonarQube())
        }
    }
}
