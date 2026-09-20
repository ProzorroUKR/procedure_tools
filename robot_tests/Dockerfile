# Robot Framework runner for the procedure tests.
#
# Built from the repository root so that procedure_tools itself is installed:
#   docker compose -f robot_tests/docker-compose.yml build
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ROBOT_HOME=/opt/robot

WORKDIR ${ROBOT_HOME}

# procedure_tools provides the actions the keywords wrap; install it first so
# that a change to the tests does not reinstall the dependencies.
COPY pyproject.toml README.md /opt/procedure_tools/
COPY procedure_tools /opt/procedure_tools/procedure_tools
RUN pip install --no-cache-dir /opt/procedure_tools[color] robotframework

COPY robot_tests ${ROBOT_HOME}

# The libraries are imported by name, the data modules by package.
ENV PYTHONPATH=${ROBOT_HOME}/libraries

CMD ["sh", "-c", "robot --outputdir ${ROBOT_HOME}/reports ${ROBOT_OPTIONS} ${ROBOT_HOME}/tests"]
