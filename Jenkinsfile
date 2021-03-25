pipeline {
    agent any

    stages {

        stage('Pull Code'){
            steps {
                git branch: 'main', changelog: false, credentialsId: '23030b55-4637-4961-ab94-13a5a10e10f4', poll: false, url: 'https://github.com/katotoy/JenkinsPractice'
                sh 'pwd'
                sh 'ls'
                sh 'python replaceTest.py'

            }
        }

        stage('Generating Config Files'){
            steps {
                
                script {
                    properties([
                        parameters([
                            choice(choices: ['100', '101', '68', '69'],  name: 'serverNode'),
                            choice(choices: ['pluk', 'pcalt', 'pamb', 'plai'],  name: 'lbu')
                        ])
                    ])                

                    echo 'Preparing config files for ${params.lbu}-${params.ServerNode}.'
                    
                    if(params.ServerNode == '100'){
                        echo 'You selected 100'
                    }else{
                        echo 'You selected other value'
                    }
                }
            }
        }
    }
}