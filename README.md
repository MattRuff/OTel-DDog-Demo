<h1>Setup Guide for OpenTelemetry and Datadog Applications</h1>


This guide provides instructions for setting up two applications—one with OpenTelemetry and the other with Datadog—using Docker and Python virtual environments.

<h5> Prerequisites </h5>

Docker: Ensure Docker is installed and running on your system.
Python: Make sure Python is installed.
Virtual Environment: A Python virtual environment is used for dependency management.

<h5> Setup Instructions </h5>
1. Replace API Key

Change the API key from the <Set API key here> in the document below, in otel-shop/config.yaml and otel-shop/otel-collectory.yaml


2. OpenTelemetry Application Setup
The OpenTelemetry setup includes configuring an OpenTelemetry Collector and running a Flask application with OpenTelemetry instrumentation.

Steps:
Navigate to the OpenTelemetry application directory:
cd otel-shop

Activate the virtual environment:
source otel/bin/activate

Install required Python packages:
pip install -U Flask Flask-SQLAlchemy sqlalchemy sqlalchemy.orm opentelemetry-distro opentelemetry-exporter-otlp

Bootstrap OpenTelemetry:
opentelemetry-bootstrap -a install

Start the OpenTelemetry Collector:
docker run -d --rm -v $(pwd)/config.yaml:/etc/otelcol-contrib/config.yaml -p 4317:4317 otel/opentelemetry-collector-contrib:0.104.0

Configure environment variables and run the Flask application:
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --traces_exporter otlp --metrics_exporter otlp --logs_exporter otlp --service_name otel-shop flask run

Deactivate the virtual environment:
deactivate

Return to the original directory:
cd -

3. Datadog Application Setup
The Datadog setup includes starting the Datadog agent and running a Flask application with Datadog tracing.

Steps:
Navigate to the Datadog application directory:
cd ddog-shop

Activate the virtual environment:
source otel/bin/activate

Install required Python packages:
pip install -U Flask Flask-SQLAlchemy sqlalchemy sqlalchemy.orm ddtrace

Start the Datadog agent:
docker run -d --name dd-agent -e DD_API_KEY=<SET API KEY HERE> -e DD_SITE="datadoghq.com" -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -p 8126:8126 -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -v /var/lib/docker/containers:/var/lib/docker/containers:ro gcr.io/datadoghq/agent:7

Configure environment variables and run the Flask application with tracing:
DD_SERVICE="dd_shop" DD_ENV="otel" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" ddtrace-run python app.py

Deactivate the virtual environment:
deactivate

Return to the original directory:
cd -

Notes
Replace <SET API KEY HERE> with your actual Datadog API key.
Ensure that the Docker container names and ports do not conflict with other running containers.
Make sure to handle potential errors and clean up any running background processes if needed.
