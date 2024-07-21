pipeline {
    agent any
    stages {
        stage('Checkout SCM!!!') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git'
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
                    sleep(time: 20, unit: 'SECONDS')
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh "/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQube/bin/sonar-scanner -Dsonar.projectKey=SSDPrac -Dsonar.sources=. -Dsonar.host.url=http://192.168.1.131:9000 -Dsonar.token= sqp_7fbaba389640a60a847c45b8cd7d357a5246fd23"
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
