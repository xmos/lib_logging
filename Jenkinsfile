@Library('xmos_jenkins_shared_library@feature/view_env_path') _

getApproval()

pipeline {
  agent {
    label 'x86_64&&brew&&linux'
  }
  environment {
    REPO = 'lib_logging'
    VIEW = getViewName(REPO)
    TOOlS_VERSION = '15.0.1'
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Get view') {
      steps {
        xcorePrepareSandbox("${VIEW}", "${REPO}")
        viewEnv {
          sh "which xcc"
          sh "xcc --version"
        }
        viewEnv("${WORKSPACE}/Installs/Linux/External/Product") {
          sh "which xcc"
          sh "xcc --version"
        }
        dir("TOOLS") {
          sh "wget -q https://github0.xmos.com/raw/xmos-int/get_tools/master/get_tools.py"
          sh "python get_tools.py ${TOOLS_VERSION}"
        }
        viewEnv("${WORKSPACE}/TOOLS/tools/${.TOOLS_VERSION}/XMOS/xTIMEcomposer/${TOOLS_VERSION}") {
          sh "which xcc"
          sh "xcc --version"
        }
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
        }
      }
    }
  }
  post {
    success {
      updateViewfiles()
    }
    cleanup {
      xcoreCleanSandbox()
    }
  }
}
