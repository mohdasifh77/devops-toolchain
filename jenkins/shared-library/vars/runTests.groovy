// ==============================================================
// Shared Library: runTests.groovy
// Reusable function to run Python tests
// ==============================================================

def call(Map config = [:]) {
    String workDir  = config.workDir  ?: 'app'
    String testDir  = config.testDir  ?: 'tests'
    String srcDir   = config.srcDir   ?: 'src'
    boolean failFast = config.failFast ?: false

    echo "🧪 Running tests in ${workDir}/${testDir}"

    dir(workDir) {
        sh """
            pip install -r requirements.txt --quiet
            pytest ${testDir}/ \
                -v \
                ${failFast ? '--exitfirst' : ''} \
                --cov=${srcDir} \
                --cov-report=xml:coverage.xml \
                --cov-report=term-missing \
                --junitxml=test-results.xml
        """
    }

    junit "${workDir}/test-results.xml"
    echo "✅ Tests complete"
}
