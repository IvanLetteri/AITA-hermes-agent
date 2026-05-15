cd ~/AITA-hermes-agent

# 1. Scarica le novità dall'ufficiale (senza applicarle ancora)
git fetch upstream

# 2. Vai sul tuo branch principale
git checkout main

# 3. Applica le modifiche upstream sul tuo main
git rebase upstream/main
# oppure merge se preferisci:
# git merge upstream/main

# 4. Aggiorna il tuo GitHub
git push origin main

# 5. Aggiorna le dipendenze se ci sono stati cambiamenti
source venv/bin/activate
uv pip install -e ".[all]"
uv pip install -e "./tinker-atropos"
