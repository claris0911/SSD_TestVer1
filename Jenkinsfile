pipeline {
    agent any
    
    environment {
        SONARQUBE_TOKEN = credentials('SSDPracToken')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git'
            }
        }
        stage('OWASP DependencyCheck') {
            steps {
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('web-app', '.')
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    docker.image('web-app').run('-d -p 5000:5000')
                    sleep 10 // wait for the container to start
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=SSD_TestVer1 \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://127.0.0.1:9000 \
                        -Dsonar.login=${SONARQUBE_TOKEN}
                    """
                }
            }
        }
    }
    post {
        success {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
    }
}
