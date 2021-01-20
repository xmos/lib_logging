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
            forAllMatch("${REPO}/examples", "app_*/") { path ->
              runXmake(path)
            }
          }
        }
        stage('xs2 docs') {
          steps {
            forAllMatch("${REPO}/examples", "AN*/") { path ->
              runXmake(path)
              runXdoc("${path}/doc")
            }
          }
        }
        stage('xs3 builds') {
          steps {
            forAllMatch("${REPO}/examples", "app_*/") { path ->
              runXmake(path, "", "XCOREAI=1")
            }
            runXmake("${REPO}/tests/debug_printf_test", "", "XCOREAI=1")
          }
        }
        stage('xs3 docs') {
          steps {
            forAllMatch("${REPO}/examples", "AN*/") { path ->
              runXmake(path, "", "XCOREAI=1")
              runXdoc("${path}/doc")
            }
          }
        }
        stage('stash xs3 bins') {
          steps {
            stash name: 'xs3_bins', includes: '**/bin/xcoreai/*.xe'
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
              unstash 'xs3_bins'
              sh 'xrun --io --id 0 bin/xcoreai/debug_printf_test.xe &> debug_printf_test.txt'
              sh 'cat debug_printf_test.txt && diff debug_printf_test.txt tests/test.expect'

              //Just run these and error on exception
              sh 'xrun --io --id 0 bin/xcoreai/AN00239.xe'
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
