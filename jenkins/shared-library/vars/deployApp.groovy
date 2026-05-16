// ==============================================================
// Shared Library: deployApp.groovy
// Reusable function to deploy Docker container
// ==============================================================

def call(Map config = [:]) {
    String appName = config.appName  ?: 'app'
    String image   = config.image    ?: "${appName}:latest"
    String env     = config.env      ?: 'staging'
    Integer port   = config.port     ?: 5000
    String network = config.network  ?: 'devops-network'

    echo "🚀 Deploying ${image} to ${env} on port ${port}"

    sh """
        docker rm -f ${appName}-${env} 2>/dev/null || true
        docker run -d \
            --name ${appName}-${env} \
            --network ${network} \
            --restart unless-stopped \
            -e FLASK_ENV=${env} \
            -p ${port}:5000 \
            ${image}
        sleep 8
        HTTP=\$(curl -sf -o /dev/null -w "%{http_code}" http://localhost:${port}/health || echo "000")
        echo "Health check: HTTP \$HTTP"
        [ "\$HTTP" = "200" ] || exit 1
    """

    echo "✅ Deployed to ${env} successfully"
}
