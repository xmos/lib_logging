// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.34.0') _

getApproval()

pipeline {
  agent none
  environment {
    REPO = 'lib_logging'
  }
  options {
    buildDiscarder(xmosDiscardBuildSettings())
    skipDefaultCheckout()
    timestamps()
  }
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.3.0',
      description: 'The XTC tools version'
    )
    string(
      name: 'XMOSDOC_VERSION',
      defaultValue: 'v6.1.2',
      description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v2.0.1',
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
            dir("${REPO}") {
              checkout scm

              dir("examples") {
                withTools(params.TOOLS_VERSION) {
                  sh 'cmake -G "Unix Makefiles" -B build'
                  sh 'xmake -C build -j 8'
                  stash name: 'examples', includes: '**/*.xe'
                }
              }
              buildDocs()
              dir("examples/AN00239") {
                buildDocs()
              }
            }
            runLibraryChecks("${WORKSPACE}/${REPO}", "${params.INFR_APPS_VERSION}")
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
        dir("${REPO}") {
          checkout scm
          withTools(params.TOOLS_VERSION) {
            dir("tests") {
              sh 'cmake -G "Unix Makefiles" -B build'
              sh 'xmake -C build -j 8'

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
