@Library('xmos_jenkins_shared_library@master') _
pipeline {
  agent {
    label 'x86&&macOS&&Apps'
  }
  environment {
    VIEW = 'logging'
    REPO = 'lib_logging'
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Get view') {
      steps {
        prepareAppsSandbox("${VIEW}", "${REPO}")
      }
    }
    stage('Library checks') {
      steps {
        xcoreLibraryChecks("${REPO}")
      }
    }
    stage('Tests') {
      steps {
        runXmostest("${REPO}", 'tests')
      }
    }
    stage('xCORE builds') {
      steps {
        dir("${REPO}") {
          xcoreAllAppsBuild('examples')
          xcoreAllAppNotesBuild('examples')
          dir("${REPO}") {
            runXdoc('doc')
          }
        }
      }
    }
  }
  post {
    success {
      updateViewfiles()
    }
    cleanup {
      cleanWs()
    }
  }
}
