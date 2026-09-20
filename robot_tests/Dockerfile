FROM ppodgorsek/robot-framework:latest

USER root

RUN pip3 install --upgrade pip && pip install --no-cache-dir robotframework-jsonlibrary

USER ${ROBOT_UID}:${ROBOT_GID}

ENV PYTHONPATH "${PYTHONPATH}:/opt/robotframework"

COPY ./robot_tests/tests  /opt/robotframework/tests
COPY ./procedure_tools  /opt/robotframework/procedure_tools
