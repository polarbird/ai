pipeline {
    agent {
        docker {
            image 'nginx:stable'
            args '-v /mnt/acs_mnt/nas/polarbird:/home'
        }
    }
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            steps {
                echo 'Build success'
            }
        }
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                sh 'sh -ex ./jenkins/scripts/deploy.sh'
            }
        }
    }
}
