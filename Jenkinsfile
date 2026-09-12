// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.53.0') _

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
      name: 'TOOLS_VERSION_XS',
      defaultValue: '15.3.1',
      description: 'The XS XTC tools version'
    )
    string(
      name: 'TOOLS_VERSION_VX',
      defaultValue: '-j --repo arch_vx_slipgate -b master -a XTC 131',
      description: 'The VX XTCtools version'
    )
    string(
      name: 'XMOSDOC_VERSION',
      defaultValue: 'v8.0.1',
      description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v3.6.0',
      description: 'The infr_apps version'
    )
  }

  stages {
    stage('🏗️ Build and test') {
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

        stage('Build XS') {
          steps {
            dir("${REPO_NAME}/examples") {
              xcoreBuild(
                toolsVersion: params.TOOLS_VERSION_XS,
                buildDir: 'build-xs',
              )
            }
          }
        }

        stage('Test XS') {
          steps {
            dir("${REPO_NAME}/tests") {
              xcoreBuild(
                toolsVersion: params.TOOLS_VERSION_XS,
                buildDir: 'build-xs',
                cmakeOpts: '-DLOGGING_BUILD_XC_TESTS=ON',
                archiveBins: false
              )
              withTools(params.TOOLS_VERSION_XS) {
                createVenv(reqFile: 'requirements.txt')
                withVenv {
                  runPytest()
                }
              }
            }
          }
        }

        stage('Build VX') {
          steps {
            dir("${REPO_NAME}/examples") {
              xcoreBuild(
                toolsVersion: params.TOOLS_VERSION_VX,
                buildDir: 'build-vx',
                cmakeOpts: '-DAPP_HW_TARGET=XK-EVK-XU416'
              )
            }
          }
        }

        stage('Test VX') {
          steps {
            dir("${REPO_NAME}/tests") {
              xcoreBuild(
                toolsVersion: params.TOOLS_VERSION_VX,
                buildDir: 'build-vx',
                cmakeOpts: '-DAPP_HW_TARGET=XK-EVK-XU416 -DLOGGING_BUILD_XC_TESTS=OFF',
                archiveBins: false
              )
              withTools(params.TOOLS_VERSION_VX) {
                createVenv(reqFile: 'requirements.txt')
                withVenv {
                  runPytest('--ignore=test_lib_logging_xc.py')
                }
              }
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
    } // stage: Build and test

    stage('🚀 Release') {
      when {
        expression { triggerRelease.isReleasable() }
      }
      steps {
        triggerRelease()
      }
    }

  } // stages
}
