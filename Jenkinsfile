pipeline {
    agent none

    environment {
        PGSQL_PASSWD = sh(script:"sed -n 5p api/dbconfig | cut -d '=' -f 2-", returnStdout: true).trim()
        PGSQL_USERNAME = sh(script:"sed -n 4p api/dbconfig | cut -d '=' -f 2-", returnStdout: true).trim()
    }

    stages {
        stage('build') {
            agent {
                docker { image 'python:3.11.4-alpine3.18'}
            }
            steps {
                sh 'apt-get install python3-pip'
                sh 'pip3 install flask'

                script {
                    docker.image('postgres:12.6')
                          .withRun('--name postgresql-container -e POSTGRES_PASSWORD=${PGSQL_PASSWD}') { c ->
                        def port = sh(returnStdout: true, script: "docker inspect --format='{{(index (index .NetworkSettings.Ports \"5432/tcp\") 0).HostPort}}' ${c.id}").trim()
                        sh "while ! curl http://localhost:${port}/ 2>&1 | grep '52'; do echo 'waiting for postgres'; sleep 1; done;"
                    }
                }

                sh 'apt install postgresql postgresql-contrib'
                sh '-i -u postgres'
                sh 'psql'
                sh 'create role ${PGSQL_USERNAME} with login superuser password ['${PGSQL_PASSWD}'];'
            }
        }

        stage('deploy') {
            steps {
                sh 'python3 api/init_db.py'
                sh 'python3 api/app.py'
            }
        }

        post {
            failure {
                echo 'Algo deu errado, se vira pra descobrir'
            }
        }
    }
}
