@Library('xmos_jenkins_shared_library@feature/support_xcoreai_2') _

getApproval()

pipeline {
  agent none
  //Tools for AI verif stage. Tools for standard stage in view file
  parameters {
     string(
       name: 'TOOLS_VERSION',
       defaultValue: '15.0.2',
       description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
     )
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
        stage('xs2 builds') {
          steps {
            xcoreAllAppsBuild("${REPO}/examples")
            xcoreAllAppNotesBuild("${REPO}/examples")
          }
        }
        stage('xs3 builds') {
          steps {
            xcoreAllAppsBuild("${REPO}/examples", "", "XCOREAI=1")
            xcoreAllAppNotesBuild("${REPO}/examples", "", "XCOREAI=1")
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
        label 'xcore.ai-explorer'
      }
      environment {
        // '/XMOS/tools' from get_tools.py and rest from tools installers
        TOOLS_PATH = "/XMOS/tools/${params.TOOLS_VERSION}/XMOS/xTIMEcomposer/${params.TOOLS_VERSION}"
      }
      stages{
        stage('Install Dependencies') {
          steps {
            sh '/XMOS/get_tools.py ' + params.TOOLS_VERSION
            installDependencies()
          }
        }
        stage('xrun'){
          steps{
            toolsEnv(TOOLS_PATH) {  // load xmos tools
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
        expression { return currentBuild.result == "SUCCESS" }
      }
      steps {
        updateViewfiles()
      }
    }
  }
}
