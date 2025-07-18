// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.39.0') _

getApproval()

pipeline {
  agent none
  environment {
    REPO_NAME = 'lib_logging'
  }
  options {
    buildDiscarder(xmosDiscardBuildSettings())
    skipDefaultCheckout()
    timestamps()
  }
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.3.1',
      description: 'The XTC tools version'
    )
    string(
      name: 'XMOSDOC_VERSION',
      defaultValue: 'v7.3.0',
      description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v2.2.0',
      description: 'The infr_apps version'
    )
  }
  stages {
    stage('Build') {
      agent {
        label 'x86_64 && linux'
      }
      stages {
        stage('xcore app build') {
          steps {
            dir("${REPO_NAME}") {
              checkoutScmShallow()

              dir("examples") {
                withTools(params.TOOLS_VERSION) {
                  xcoreBuild()
                  stash name: 'examples', includes: '**/*.xe'
                }
              }
              buildDocs()
              dir("examples/AN00239") {
                buildDocs()
              }
            }
            runLibraryChecks("${WORKSPACE}/${REPO_NAME}", "${params.INFR_APPS_VERSION}")
          }
        }
      }
      post {
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }

    stage('xcore.ai Verification') {
      agent {
        label 'xcore.ai'
      }
      steps {
        dir("${REPO_NAME}") {
          checkoutScmShallow()
          withTools(params.TOOLS_VERSION) {
            dir("tests") {
              xcoreBuild()

              //Run this and diff against expected output. Note we have the lib files here available
              sh 'xrun --io --id 0 debug_printf_test/bin/debug_printf_test.xe &> debug_printf_test.txt'
              sh 'cat debug_printf_test.txt && diff debug_printf_test.txt test.expect'
            }

            dir("examples") {
              unstash 'examples'
              //Just run these and error on exception
              sh 'xrun --io --id 0 AN00239/bin/AN00239.xe'
              sh 'xrun --io --id 0 app_debug_printf/bin/app_debug_printf.xe'
            }
          }
        }
      }
      post {
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }// xcore.ai
  }
}
