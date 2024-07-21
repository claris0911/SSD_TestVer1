pipeline {
    agent any
    stages {
        stage('Checkout SCM!') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git', credentialsId: '8ecd7d43-cbab-4a10-9ee8-1c31ad258a71'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t my-webapp .'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=OWASP -Dsonar.sources=. -Dsonar.host.url=http://127.0.0.1:9000 -Dsonar.token=sqp_1e9ad67fc247066bfab363885cca3e58635c2e69"
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
