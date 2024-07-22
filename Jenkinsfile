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
        stage('Install SonarQube Scanner') {
            steps {
                sh '''
                    wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.6.2.2472-linux.zip
                    unzip sonar-scanner-cli-4.6.2.2472-linux.zip
                    export PATH=$PATH:$(pwd)/sonar-scanner-4.6.2.2472-linux/bin
                '''
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
                    // Stop and remove any existing container using port 5000
                    def existingContainerId = sh(script: "docker ps -q -f ancestor=web-app", returnStdout: true).trim()
                    if (existingContainerId) {
                        sh "docker stop ${existingContainerId}"
                        sh "docker rm ${existingContainerId}"
                    }

                    // Start a new container on a different port to avoid conflicts
                    sh "docker run -d -p 5001:5000 web-app"
                    sleep 10 // wait for the container to start
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        ./sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner \
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
