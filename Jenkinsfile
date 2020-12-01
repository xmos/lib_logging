@Library('xmos_jenkins_shared_library@v0.15.1') _

getApproval()

pipeline {
  agent none
  stages {
    stage('Standard build and XS2 tests') {
      agent {
        label 'x86_64&&brew'
      }
      environment {
        REPO = 'lib_logging'
        VIEW = getViewName(REPO)
      }
      options {
        skipDefaultCheckout()
      }
      stages{
        stage('Get view') {
          steps {
            xcorePrepareSandbox("${VIEW}", "${REPO}")
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
              //Build these individually (or we can extend xcoreAllAppsBuild to support an argument
              dir('examples/app_debug_printf'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'bin/xcoreai', includes: '*.xe'
              }
              dir('examples/AN00239'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'bin/xcoreai', includes: '*.xe'
              }
              dir('tests/debug_printf_test'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'bin/xcoreai', includes: '*.xe'
              }
              xcoreAllAppNotesBuild('examples')
              dir("${REPO}") {
                runXdoc('doc')
              }
            }
          }
        }
      }// stages
      post {
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }//Stage standard build
    stage('XS3 Verification'){
      agent {
        label 'xs3'
      }
      steps{
        println 'Dummy stage on XS3'
      }
      post {
        cleanup {
          cleanWs()
        }
      }
    }
  }
  post {
    success {
      node('linux') { //Need to specify agent. We cannot  use agent syntax unf
        updateViewfiles()
      }
    }
  }
}
