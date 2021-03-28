pipeline {
    agent any

    stages {

        environment {
                CONFIG_DIR="/tmp/config_files" 
        }

        stage('Pull Code'){
            steps {
                deleteDir()
                git branch: 'main', changelog: false, credentialsId: '23030b55-4637-4961-ab94-13a5a10e10f4', poll: false, url: 'https://github.com/katotoy/JenkinsPractice'
            }
        }

        stage('Generating Config Files'){

            environment {
                SOURCE_DIR = sh(script: "echo ${params.LBU}-${params.SERVER_NODE}", , returnStdout: true).trim()
            }

            steps {
                
                script {
                    properties([
                        parameters([
                            choice(choices: ['PLUK', 'PCALT', 'PAMB', 'PLAI'],  name: 'LBU'),
                            choice(choices: ['100', '101', '68', '69'],  name: 'SERVER_NODE')
                        ])
                    ])                

                    echo "Preparing config files for ${SOURCE_DIR}."
                    sh 'pwd'
                    sh "mkdir ${CONFIG_DIR}"
                    sh 'ls -ll'
                    echo 'Copying templates config to target directory'
                    sh "cp -R ./${params.LBU}/. /${CONFIG_DIR}/"
                    sh "ls -ll ${CONFIG_DIR}"
                }
            }
        }


    }
}