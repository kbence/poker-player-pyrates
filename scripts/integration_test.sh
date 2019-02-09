#!/usr/bin/env bash

ROOT=$(cd $(dirname ${BASH_SOURCE[0]:-$0}); pwd)
export PORT=1234

pushd "$ROOT"

python player_service.py &
PID=$?
trap "kill $PID" EXIT
sleep 2

OUTPUT=$(curl -XPOST -d'action=version&game_state={}' localhost:$PORT)

popd

[[ -z $OUTPUT ]] && echo "Failed! (Output for version: '$OUTPUT')" || echo "Succeeded"
