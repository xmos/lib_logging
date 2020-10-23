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
        setGitHubStatus("QUICK", "Test Status", "SUCCESS", "https://github.com/xmos/lib_logging","95b416a8b131e69653068a7aaff76a1631810279")
        xcorePrepareSandbox("${VIEW}", "${REPO}")
        setGitHubStatus("DEFAULT", "Test Status Defaults", "SUCCESS")
      }
    }
    stage('Library checks') {
      steps {
        xcoreLibraryChecks("${REPO}")
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
          withGitHubStatus("App build") {
            xcoreAllAppsBuild('examples')
          }
          withGitHubStatus("App notes") {
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
