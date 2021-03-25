pipeline {
    agent any

    stages {

        stage('Pull Code'){
            steps {
                deleteDir()
                git branch: 'main', changelog: false, credentialsId: '23030b55-4637-4961-ab94-13a5a10e10f4', poll: false, url: 'https://github.com/katotoy/JenkinsPractice'
            }
        }

        stage('Generating Config Files'){
            steps {
                
                script {
                    properties([
                        parameters([
                            choice(choices: ['pluk', 'pcalt', 'pamb', 'plai'],  name: 'lbu'),
                            choice(choices: ['100', '101', '68', '69'],  name: 'serverNode')
                        ])
                    ])                

                    sh "echo sh isBar is ${params.lbu}"

                     environment {
                        SOURCE_DIR = "${params.lbu}-${params.serverNode}"
                     }
                    echo 'Preparing config files for ${SOURCE_DIR}.'
                    sh 'mkdir new_config'
                    sh 'cd ${SOURCE_DIR}'
                }
            }
        }
    }
}