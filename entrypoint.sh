#!/bin/bash
set -e

if [ "$1" = 'sam-nmi' ]; then
    exec /app/sam-nmi
fi

exec "$@"
