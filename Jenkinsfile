// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.56.0') _

getApproval()
pipeline {

    agent none

    parameters {
        string(
            name: 'TOOLS_VERSION_XS',
            defaultValue: '15.3.1',
            description: 'XTC tools version'
        )
        string(
            name: 'TOOLS_VERSION_VX',
            defaultValue: 'bob@develop',
            description: 'VX tools version'
        )
        string(
            name: 'TOOLS_VERSION_VX_XCC',
            defaultValue: 'slipgate@master:143',
            description: 'VX (XTC) tools version'
        )
        string(
            name: 'XMOSDOC_VERSION',
            defaultValue: 'v8.1.2',
            description: 'xmosdoc version'
        )
        string(
            name: 'INFR_APPS_VERSION',
            defaultValue: 'v3.6.0',
            description: 'The infr_apps version'
        )
    }

    options {
        skipDefaultCheckout()
        timestamps()
        buildDiscarder(xmosDiscardBuildSettings(onlyArtifacts = false))
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

                stage('Examples build') {
                    steps {
                        dir("${REPO_NAME}/examples") {
                            xcoreBuildAllArch()
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

                stage('Tests') {
                    steps {
                        dir("${REPO_NAME}/tests") {
                            createVenv(reqFile: "requirements.txt")
                            withVenv {
                              withTools(params.TOOLS_VERSION_XS) {
                                xcoreBuild(archiveBins: false,  cmakeOpts: '-DLOGGING_BUILD_XC_TESTS=ON')
                                runPytest()
                              }
                              withTools(params.TOOLS_VERSION_VX) {
                                xcoreBuild(archiveBins: false)
                                runPytest()
                              }
                              withTools(params.TOOLS_VERSION_VX_XCC) {
                                xcoreBuild(archiveBins: false, cmakeOpts: '-DAPP_HW_TARGET=XK-EVK-XU416')
                                runPytest()
                              }
                            }
                        }
                    }
                }

                stage("Archive sandbox") {
                    steps {
                        archiveSandbox(REPO_NAME)
                    }
                }
            } // stages
            post {
                cleanup {
                    xcoreCleanSandbox()
                }
            }
        } // stage 'Build and test'

        stage('🚀 Release') {
            when {
                expression { triggerRelease.isReleasable() }
            }
            steps {
                triggerRelease()
            }
        }
    } // stages
} // pipeline
