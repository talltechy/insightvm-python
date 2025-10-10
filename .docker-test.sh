#!/bin/bash
# Local Docker testing script
# Run tests in a Docker container matching CI/CD environment

set -e

echo "🐳 Building Docker test image..."
docker build -f Dockerfile.test -t insightvm-test:local .

echo ""
echo "🧪 Running tests in Docker..."
docker run --rm -v "$(pwd)/coverage.xml:/app/coverage.xml" insightvm-test:local

echo ""
echo "✅ Tests complete! Coverage report saved to coverage.xml"
echo "💡 View HTML coverage report: open htmlcov/index.html"
