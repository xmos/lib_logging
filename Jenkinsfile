@Library('xmos_jenkins_shared_library@v0.15.1') _

getApproval()

pipeline {
  agent none
  //Tools for AI verif
  parameters {
     string(
       name: 'TOOLS_VERSION',
       defaultValue: '15.0.2',
       description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
     )
   }
  environment {
    // '/XMOS/tools' from get_tools.py and rest from tools installers
    TOOLS_PATH = "/XMOS/tools/${params.TOOLS_VERSION}/XMOS/xTIMEcomposer/${params.TOOLS_VERSION}"
  }
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
              xcoreAllAppNotesBuild('examples')
              dir("${REPO}") {
                runXdoc('doc')
              }
              //Build these individually (or we can extend xcoreAllAppsBuild to support an argument
              dir('examples/app_debug_printf'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'app_debug_printf', includes: 'bin/xcoreai/*.xe, '
              }
              dir('examples/AN00239'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'AN00239', includes: 'bin/xcoreai/*.xe'
              }
              dir('tests/debug_printf_test'){
                runXmake(".", "", "XCOREAI=1")
                sh 'tree'
                stash name: 'debug_printf_test', includes: 'bin/xcoreai/*.xe'
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
        toolsEnv(TOOLS_PATH) {  // load xmos tools
          unstash 'debug_printf_test'
          sh 'tree'
          sh 'xrun --io --id 0 bin/xcoreai/debug_printf_test.xe &> debug_printf_test.txt'
          sh 'cat debug_printf_test.txt && diff debug_printf_test.txt tests/test.expect'
        }
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
