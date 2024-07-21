pipeline {
    agent any
    stages {
        stage('Checkout SCM!!') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git', credentialsId: '8ecd7d43-cbab-4a10-9ee8-1c31ad258a71'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t my-webapp .'
            }
        }
        stage('Wait for SonarQube') {
            steps {
                script {
                    sleep(time: 60, unit: 'SECONDS')
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=ssd_ver1 -Dsonar.sources=. -Dsonar.host.url=http://sonarqube:9000 -Dsonar.token=squ_e70ce54a0a29054227354cdf9ea6d77d737b2305"
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
            recordIssues enabledForFailure: true, tool: sonarQube()
        }
    }
}
