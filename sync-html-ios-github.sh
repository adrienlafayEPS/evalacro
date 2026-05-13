#!/usr/bin/env bash
# Synchronise le HTML hors ligne vers le bundle iOS, puis pousse ce dossier vers GitHub (evalacro).
# Exécuter depuis le Mac :  bash sync-html-ios-github.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/HTML"
IOS_DST="$ROOT/Xcode/AcrosportiOS/Resources/index.html"
SRC_INDEX="$HTML/index.html"

if [[ ! -f "$SRC_INDEX" ]]; then
  echo "Fichier introuvable : $SRC_INDEX" >&2
  exit 1
fi
if [[ ! -f "$IOS_DST" ]]; then
  echo "Cible iOS introuvable : $IOS_DST" >&2
  exit 1
fi

echo "→ Copie $SRC_INDEX → $IOS_DST"
cp "$SRC_INDEX" "$IOS_DST"
echo "   OK ($(wc -c < "$IOS_DST" | tr -d ' ') octets)"

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
