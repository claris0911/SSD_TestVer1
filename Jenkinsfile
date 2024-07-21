pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/claris0911/SSD_TestVer1.git', credentialsId: '8ecd7d43-cbab-4a10-9ee8-1c31ad258a71' // Replace 'your-credentials-id' with the actual ID from Jenkins
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
    }
}