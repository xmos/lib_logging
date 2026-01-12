// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.41.1') _

getApproval()

pipeline {
  agent none
  
  options {
    buildDiscarder(xmosDiscardBuildSettings(onlyArtifacts = false))
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
      defaultValue: 'v7.4.0',
      description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v3.1.1',
      description: 'The infr_apps version'
    )
  }

  stages {
    stage('🏗️ Build and checks') {
      agent {
        label 'x86_64 && linux && documentation'
      }

      stages {
        stage('Checkout') {
          steps {
            println "Stage running on ${env.NODE_NAME}"

            script {
              def (server, user, repo) = extractFromScmUrl()
              env.REPO_NAME = repo
            }

            dir(REPO_NAME){
              checkoutScmShallow()
            }
          }
        }

        stage('Examples build') {
          steps {
            dir("${REPO_NAME}/examples") {
              xcoreBuild()
              stash name: 'examples', includes: '**/*.xe'
            }
          }
        }

        stage('Repo checks') {
          steps {
            warnError("Repo checks failed")
            {
              runRepoChecks("${WORKSPACE}/${REPO_NAME}")
            }
          }
        }

        stage('Doc build') {
          steps {
            dir(REPO_NAME) {
              buildDocs()
            }
          }
        }
        stage("Archive sandbox") {
          steps
          {
            archiveSandbox(REPO_NAME)
          }
        }
      }
    } // stage: Build and checks

    stage('xcore.ai Verification') {
      agent {
        label 'xcore.ai'
      }
      steps {
        dir("${REPO_NAME}") {
          checkoutScmShallow()
          withTools(params.TOOLS_VERSION) {
            dir("tests") {
              createVenv(reqFile: "requirements.txt")
              withVenv {
                xcoreBuild(archiveBins: false)
                sh "pytest -n auto --junitxml=pytest_result.xml"
              }
            }
            dir("examples") {
              unstash 'examples'
              //Just run these and error on exception
              sh 'xrun --io --id 0 app_debug_unit/bin/app_debug_unit.xe'
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
    } // xcore.ai

    stage('🚀 Release') {
      steps {
        triggerRelease()
      }
    }

  } // stages
}
