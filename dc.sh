# Write docker-compose override
if [ ! -f "docker-compose.override.yml" ]; then
  cat <<EOF >> docker-compose.override.yml
version: "3.0"
EOF
fi

set -o allexport
source ./.env

docker-compose -f docker-compose.yml -f docker-compose.override.yml "$@"

set +o allexport
