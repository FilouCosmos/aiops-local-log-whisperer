#  AIOps Local Log Whisperer

Un assistant SysAdmin basé sur l'IA (LLM) qui tourne 100% en local. Fini l'envoi de logs sensibles ou d'adresses IP privées vers les serveurs d'OpenAI. Ce script intercepte vos logs, les anonymise (masquage d'IP/PII), et interroge une instance locale d'Ollama pour fournir un diagnostic instantané et une commande de résolution.

##  Fonctionnalités
- **Privacy-First :** Les données ne quittent jamais votre infrastructure.
- **Anonymisation Regex :** Masquage automatique des IP avant analyse.
- **Intégration Ollama :** Compatible avec Llama 3, Mistral, etc.

##  Prérequis
1. Installer [Ollama](https://ollama.com/) sur votre machine/serveur.
2. Télécharger un modèle (ex: `ollama run llama3`).

##  Utilisation
```bash
git clone [https://github.com/FilouCosmos/aiops-local-log-whisperer.git](https://github.com/FilouCosmos/aiops-local-log-whisperer.git)
cd aiops-local-log-whisperer
pip install -r requirements.txt

# Analysez une erreur directement depuis votre terminal :
python3 log_whisperer.py "nginx: [emerg] bind() to 192.168.1.50:80 failed (98: Address already in use)"
