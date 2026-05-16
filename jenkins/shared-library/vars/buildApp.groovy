// ==============================================================
// Shared Library: buildApp.groovy
// Reusable function to build Docker image
// Usage in Jenkinsfile: buildApp(name: 'myapp', version: '1.0')
// ==============================================================

def call(Map config = [:]) {
    String appName = config.name    ?: 'app'
    String version = config.version ?: env.BUILD_NUMBER
    String context = config.context ?: '.'

    echo "🐳 Building Docker image: ${appName}:${version}"

    sh """
        docker build \
            --target production \
            --build-arg APP_VERSION=${version} \
            --label git-commit=${env.GIT_COMMIT} \
            --label build-date=\$(date -u +%Y-%m-%dT%H:%M:%SZ) \
            -t ${appName}:${version} \
            -t ${appName}:latest \
            ${context}
    """

    echo "✅ Built ${appName}:${version}"
    return "${appName}:${version}"
}
