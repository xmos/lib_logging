@Library('xmos_jenkins_shared_library@feature/check_org_members') _
getApproval()
pipeline {
  agent {
    label 'linux'
  }
  environment {
    VIEW = 'logging'
    REPO = 'lib_logging'
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Do thing') {
      steps {
        isPR()
        script {
          print scm.userRemoteConfigs[0].dump()
        }
      }
    }
  }
  post {
    cleanup {
      cleanWs()
    }
  }
}
