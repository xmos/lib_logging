@Library('xmos_jenkins_shared_library@feature/view_env_path') _

getApproval()

pipeline {
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
  stages {
    stage('Get view') {
      steps {
        xcorePrepareSandbox("${VIEW}", "${REPO}")
        viewEnv {
          sh "xcc --version"
        }
        dir("TOOLS") {
          sh "wget -q https://github0.xmos.com/raw/xmos-int/get_tools/master/get_tools.py"
          sh "get_tools.py 15.0.1"
        }
        viewEnv("${WORKSPACE}/TOOLS/tools/${params.TOOLS_VERSION}/XMOS/xTIMEcomposer/${params.TOOLS_VERSION}") {
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
