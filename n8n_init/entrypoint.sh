set -eu
export N8N_USER_FOLDER=/data

if [ ! -f /data/.imported ]; then
  echo "→ importing workflow"
  n8n import:workflow --input=/n8n_init/complaints_flow.json

  echo "→ activating workflow(s)"
  n8n update:workflow --all --active=true

  touch /data/.imported
fi

exec n8n start

