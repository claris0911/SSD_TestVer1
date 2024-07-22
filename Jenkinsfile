pipeline {
    agent any
    
    environment {
        SONARQUBE_TOKEN = credentials('SSDPracToken')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                sh '''
                docker ps -a
                '''
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('web-app', '.')
                }
            }
        }
        // stage('Run Docker Container') {
        //     steps {
        //         script {
        //             docker.image('web-app').run('-d -p 5001:5000')
        //             sleep 10 // wait for the container to start
        //         }
        //     }
        // }
        // stage('Start SonarQube') {
        //     steps {
        //         script {
        //             sh '/usr/local/bin/docker-compose up -d sonarqube'
        //             sleep 60 // wait for SonarQube to start
        //         }
        //     }
        // }
        stage('SonarQube Analysis') {
            steps {
                script {
                    docker.image('sonarsource/sonar-scanner-cli:latest').inside("--network jenkins") {
                        withSonarQubeEnv('SonarQube') {
                            sh """
                                sonar-scanner \
                                -Dsonar.projectKey=SSD_TestVer1 \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://192.168.1.131:9000 \
                                -Dsonar.login=${SONARQUBE_TOKEN}
                            """
                        }
                    }
                }
            }
        }
        stage('OWASP DependencyCheck') {
            steps {
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
            }
        }
    }
    
    post {
        success {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
        always {
            junit 'tests/*.xml'
        }
    }
}
