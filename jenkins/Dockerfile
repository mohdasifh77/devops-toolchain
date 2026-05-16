# ==============================================================
# Custom Jenkins Image
# Pre-installs all required plugins so Jenkins is ready to use
# ==============================================================

FROM jenkins/jenkins:2.440.1-lts-jdk17

USER root

# Install Docker CLI (for Docker-in-Docker builds)
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Add jenkins user to docker group
RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins

# Skip setup wizard — we configure everything via code
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
ENV JENKINS_OPTS="--httpPort=8090"

# Pre-install plugins
RUN jenkins-plugin-cli --plugins \
    git \
    github \
    pipeline-stage-view \
    workflow-aggregator \
    blueocean \
    docker-workflow \
    docker-plugin \
    sonarqube-scanner \
    nexus-artifact-uploader \
    credentials-binding \
    timestamper \
    junit \
    cobertura \
    build-timeout \
    email-ext \
    slack \
    configuration-as-code \
    job-dsl

# Copy Jenkins configuration as code
COPY jenkins-casc.yaml /var/jenkins_home/casc_configs/jenkins.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs/jenkins.yaml

EXPOSE 8090
