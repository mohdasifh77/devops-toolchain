// ==============================================================
// seed-job.groovy — Auto-creates all Jenkins jobs using Job DSL
// Run this once inside Jenkins to create all pipelines
// ==============================================================

// Main CI/CD Pipeline
pipelineJob('devops-toolchain-main') {
    displayName('🚀 DevOps Toolchain — Main Pipeline')
    description('Full CI/CD: Test → SonarQube → Build → Nexus → Deploy')

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/YOUR_USERNAME/devops-toolchain.git')
                    }
                    branch('main')
                }
            }
            scriptPath('jenkins/pipelines/Jenkinsfile')
        }
    }

    triggers {
        githubPush()
    }

    properties {
        buildDiscarder {
            strategy {
                logRotator {
                    numToKeepStr('10')
                }
            }
        }
    }
}

// PR Validation Pipeline
pipelineJob('devops-toolchain-pr') {
    displayName('🔍 DevOps Toolchain — PR Validation')
    description('Lightweight pipeline for pull request validation')

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/YOUR_USERNAME/devops-toolchain.git')
                    }
                    branch('${ghprbActualCommit}')
                }
            }
            scriptPath('jenkins/pipelines/Jenkinsfile.pr')
        }
    }
}

// Nightly build
pipelineJob('devops-toolchain-nightly') {
    displayName('🌙 DevOps Toolchain — Nightly Build')
    description('Full test suite run every night at midnight')

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/YOUR_USERNAME/devops-toolchain.git')
                    }
                    branch('main')
                }
            }
            scriptPath('jenkins/pipelines/Jenkinsfile')
        }
    }

    triggers {
        cron('H 0 * * *')  // Every night at midnight
    }
}
