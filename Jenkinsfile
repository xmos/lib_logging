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
        warnError("Expected viewEnv error") {
          viewEnv {
            sh "which xcc"
          }
        }
        warnError("Expected toolsEnv failure") {
          toolsEnv("tools/not/even/a/real/path") {
            sh "which xcc"
        }
        xcorePrepareSandbox("${VIEW}", "${REPO}")
        viewEnv {
          sh "which xcc"
          sh "xcc --version"
        }
        sh "curl https://github0.xmos.com/raw/xmos-int/get_tools/master/get_tools.py | python - '${TOOLS_VERSION}'"
        toolsEnv("tools/${TOOLS_VERSION}/XMOS/xTIMEcomposer/${TOOLS_VERSION}") {
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
