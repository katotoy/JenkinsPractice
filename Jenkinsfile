def CONFIG_DIR="/tmp/config_files/" 
def TARGET_NODE=""
def TARGET_HOST="" 
pipeline {
    agent any

    stages {

        stage('Pull Code'){
            steps {
                deleteDir()
                sh "rm -vrf ${CONFIG_DIR}"
                git branch: 'main', changelog: false, credentialsId: '23030b55-4637-4961-ab94-13a5a10e10f4', poll: false, url: 'https://github.com/katotoy/JenkinsPractice'
            }
        }

        stage('Copying Template Folder'){

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
                    TARGET_NODE = SOURCE_DIR
                    TARGET_HOST = sh(script: "echo ${params.SERVER_NODE}", , returnStdout: true).trim()

                    echo "Preparing config files for ${SOURCE_DIR}."
                    sh 'pwd'
                    sh "mkdir ${CONFIG_DIR}"
                    sh 'ls -ll'
                    echo 'Copying templates config to target directory'
                    sh "cp -vR ./${params.LBU}/. ${CONFIG_DIR}"
                    sh "ls -ll ${CONFIG_DIR}"
                }
            }
        }

        stage('Generating Config Files'){
            steps {
                echo 'Replacing values'
                sh 'chmod +x replaceTest.py'
                sh "./replaceTest.py ${TARGET_NODE}"
            }
            
        }

        stage('Copying config files'){
            steps {
                script {

                    echo "TARGET_HOST: ${TARGET_HOST}"
                    def TARGET_HOST_IP = ['100': '192.168.0.15', '101': '192.168.0.16', '68': '192.168.0.17']
                    
                    def remote = [:]
                        remote.name = "targetHost"
                        remote.host = TARGET_HOST_IP[TARGET_HOST] 
                        remote.allowAnyHosts = true

                    echo "remotehost: ${remote.host}"
                    withCredentials([sshUserPrivateKey(credentialsId: 'bcb0f627-1ee2-49f4-a27e-22fa2a883d5e', keyFileVariable: 'identifyFile', passphraseVariable: '', usernameVariable: 'userName')]) {
                        remote.user = userName
                        remote.identityFile = identifyFile
                        stage("SSH Steps Rocks!") {
                            sshPut remote: remote, from: CONFIG_DIR, into: '/tmp/'
                            sshRemove remote: remote, path: CONFIG_DIR
                        }
                    }
                }
            }
        }

    }
}