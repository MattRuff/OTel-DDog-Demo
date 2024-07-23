#!/bin/bash

# Function to set up OpenTelemetry application
setup_opentelemetry() {
    echo "Setting up OpenTelemetry application..."

    # Navigate to the directory containing otel-shop/app.py
    cd otel-shop || { echo "Directory 'otel-shop' not found."; exit 1; }
    
    # Activate virtual environment
    source otel/bin/activate

    pip install -U Flask Flask-SQLAlchemy sqlalchemy sqlalchemy.orm opentelemetry-distro \
        opentelemetry-exporter-otlp

    opentelemetry-bootstrap -a install
    # Start OpenTelemetry collector
    docker run -d --rm -v $(pwd)/config.yaml:/etc/otelcol-contrib/config.yaml -p 4317:4317 \
        otel/opentelemetry-collector-contrib:0.104.0 &
  
    # Configure environment variables and start Flask application with instrumentation
    export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
    opentelemetry-instrument \
        --traces_exporter otlp \
        --metrics_exporter otlp \
        --logs_exporter otlp \
        --service_name otel-shop \
        flask run &

    # Deactivate virtual environment
    deactivate

    # Navigate back to the original directory
    cd - > /dev/null
}
# Function to set up Datadog application
setup_datadog() {
    echo "Setting up Datadog application..."

    # Navigate to the directory containing ddog-shop/app.py
    cd ddog-shop || { echo "Directory 'ddog-shop' not found."; exit 1; }

    # Activate virtual environment
    source otel/bin/activate
    
    pip install -U Flask Flask-SQLAlchemy sqlalchemy sqlalchemy.orm ddtrace


    # Start Datadog agent
    docker run -d --name dd-agent \
    -e DD_API_KEY=<SET API KEY HERE> \
    -e DD_SITE="datadoghq.com" \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /proc/:/host/proc/:ro \
    -p 8126:8126 \
    -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
    -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
    gcr.io/datadoghq/agent:7 &

    # Configure Datadog environment variables and start application with tracing
    DD_SERVICE="dd_shop" DD_ENV="otel" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" \
        ddtrace-run python app.py &

    # Deactivate virtual environment
    deactivate

    # Navigate back to the original directory
    cd - > /dev/null
}

# Main script starts here

# Run setup functions
setup_opentelemetry
setup_datadog