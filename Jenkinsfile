@Library('xmos_jenkins_shared_library@v0.18.0') _

getApproval()

pipeline {
  agent none
  environment {
    REPO = 'lib_logging'
    VIEW = getViewName(REPO)
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Standard build and XS2 tests') {
      agent {
        label 'x86_64&&brew'
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
              xcoreAllAppNotesBuild('examples')

              //Build these individually (or we can extend xcoreAllAppsBuild to support an argument
              dir('examples/app_debug_printf'){
                runXmake(".", "", "XCOREAI=1")
                stash name: 'app_debug_printf', includes: 'bin/xcoreai/*.xe, '
              }
              dir('examples/AN00239'){
                runXmake(".", "", "XCOREAI=1")
                stash name: 'AN00239', includes: 'bin/xcoreai/*.xe'
              }
              dir('tests/debug_printf_test'){
                runXmake(".", "", "XCOREAI=1")
                stash name: 'debug_printf_test', includes: 'bin/xcoreai/*.xe'
              }
            }
          }
        }
        stage('Build docs') {
          steps {
            runXdoc("${REPO}/${REPO}/doc")
            // Archive all the generated .pdf docs
            archiveArtifacts artifacts: "${REPO}/**/pdf/*.pdf", fingerprint: true, allowEmptyArchive: true
          }
        }
      }// stages
      post {
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }// Stage standard build

    stage('xcore.ai Verification'){
      agent {
        label 'xcore.ai'
      }
      stages{
        stage('Get view') {
          steps {
            xcorePrepareSandbox("${VIEW}", "${REPO}")
          }
        }
        stage('xrun'){
          steps{
            dir("${REPO}") {
              viewEnv {  // load xmos tools
                withVenv {  // activate virtualenv
                  //Install xtagctl and reset xtags
                  sh "pip install -e ${WORKSPACE}/xtagctl"
                  sh 'xtagctl reset_all XCORE-AI-EXPLORER'

                  //Run this and diff against expected output. Note we have the lib files here available
                  unstash 'debug_printf_test'
                  sh 'xrun --io --id 0 bin/xcoreai/debug_printf_test.xe &> debug_printf_test.txt'
                  sh 'cat debug_printf_test.txt && diff debug_printf_test.txt tests/test.expect'

                  //Just run these and error on exception
                  unstash 'AN00239'
                  sh 'xrun --io --id 0 bin/xcoreai/AN00239.xe'
                  unstash 'app_debug_printf'
                  sh 'xrun --io --id 0 bin/xcoreai/app_debug_printf.xe'
                }
              }
            }
          }
        }
      }//stages
      post {
        cleanup {
          cleanWs()
        }
      }
    }// xcore.ai

    stage('Update view files') {
      agent {
        label 'x86_64&&brew'
      }
      when {
        expression { return currentBuild.currentResult == "SUCCESS" }
      }
      steps {
        updateViewfiles()
      }
    }
  }
}
