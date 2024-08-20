// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@develop') _

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
            }
            runLibraryChecks("${WORKSPACE}/${REPO}", "v2.0.0")
          }
        }
        stage('Build docs') {
          steps {
            dir("${REPO}") {
              withXdoc("v2.0.20.2.post0") {
                withTools(params.TOOLS_VERSION) {
                  dir("${REPO}/doc") {
                    sh "xdoc xmospdf"
                    archiveArtifacts artifacts: "pdf/*.pdf"
                  }
                  dir("examples/AN00239/doc") {
                    sh "xdoc xmospdf"
                    archiveArtifacts artifacts: "pdf/*.pdf"
                  }
                }
              }
            }
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
