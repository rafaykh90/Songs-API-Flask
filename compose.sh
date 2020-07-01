
#!/usr/bin/env bash

CURRENT_DIR=$(dirname ${0})

echo ${CURRENT_DIR}

COMMAND="docker-compose"

if [ "${1}" == "run" ]; then
  shift
  COMMAND="${COMMAND} run --rm"
fi

echo ${COMMAND} ${@}

${COMMAND} ${@}

