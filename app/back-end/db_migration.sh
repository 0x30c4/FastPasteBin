#!/usr/bin/env bash

# for fish shell only
# cat configs/.env.dev | sed "s/=/ /g" | xargs -n 2 echo set -x | source
alembic upgrade head
