@Library('xmos_jenkins_shared_library@feature/gh_commit_status') _

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
      }
    }
    stage('Library checks') {
      steps {
        withGitHubStatus("lib checks") {
          xcoreLibraryChecks("${REPO}")
        }
      }
    }
    stage('Tests') {
      steps {
        withGitHubStatus("xmostest") {
          runXmostest("${REPO}", 'tests')
        }
      }
    }
    stage('xCORE builds') {
      steps {
        dir("${REPO}") {
          withGitHubStatus("app build") {
            xcoreAllAppsBuild('examples')
          }
          withGitHubStatus("app notes") {
            xcoreAllAppNotesBuild('examples')
            dir("${REPO}") {
              runXdoc('doc')
            }
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
