#!/usr/bin/env bash
# Synchronise le HTML + icônes vers le bundle iOS, puis pousse ce dossier vers GitHub (evalacro).
# Exécuter depuis le Mac :  bash sync-html-ios-github.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/HTML"
IOS_RES="$ROOT/Xcode/AcrosportiOS/Resources"

ASSETS=(
  index.html
  icon-source.png
  icon-192.png
  icon-512.png
  apple-touch-icon.png
  favicon-32x32.png
)

mkdir -p "$IOS_RES"
for f in "${ASSETS[@]}"; do
  if [[ ! -f "$HTML/$f" ]]; then
    echo "Fichier introuvable : $HTML/$f" >&2
    exit 1
  fi
  echo "→ Copie $f → bundle iOS"
  cp "$HTML/$f" "$IOS_RES/$f"
done
echo "   OK ($(wc -c < "$IOS_RES/index.html" | tr -d ' ') octets pour index.html)"

cd "$HTML"
if [[ ! -d .git ]]; then
  echo "Pas de dépôt git dans $HTML" >&2
  exit 1
fi

git add -A
if git diff --staged --quiet; then
  echo "→ Git : rien à commiter (déjà à jour)."
  exit 0
fi

MSG="chore: sync Acrosport $(date '+%Y-%m-%d %H:%M')"
git commit -m "$MSG"
echo "→ Git : commit créé."
echo "→ GitHub : envoi sur origin/main …"
if git push origin main; then
  echo "   Push OK."
else
  echo "" >&2
  echo "Échec du push (identifiants GitHub ou réseau)." >&2
  echo "Configure une fois les identifiants HTTPS, ou SSH, puis relance ce script." >&2
  exit 1
fi
