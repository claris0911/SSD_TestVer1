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
                    withSonarQubeEnv('SonarQube') {
                        sh '/var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQube/bin/sonar-scanner ' +
                           '-Dsonar.projectKey=SSDPrac ' +
                           '-Dsonar.sources=. ' +
                           '-Dsonar.host.url=http://192.168.1.131:9000 ' +
                           '-Dsonar.login=sqp_dc1991fa3554c4b9feac069b36e60953ab10118a'
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
