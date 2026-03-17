import re
import sys
import requests
import json

# --- Configuration ---
OLLAMA_API = "http://localhost:11434/api/generate"
MODELE_IA = "llama3" # Assure-toi d'avoir pull ce modèle via Ollama
# ---------------------

def anonymiser_log(ligne_log: str) -> str:
    """Masque les adresses IP pour éviter la fuite de données sensibles."""
    # Regex pour IPv4
    ligne_propre = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP_REDACTED]', ligne_log)
    # On pourrait ajouter d'autres Regex ici pour les emails, MAC, etc.
    return ligne_propre

def analyser_erreur(log_anonymise: str) -> str:
    """Envoie le log à l'IA locale pour obtenir un diagnostic."""
    prompt = (
        f"Tu es un expert SysAdmin Linux (SRE). "
        f"Analyse ce message d'erreur d'un log système. "
        f"Donne-moi la cause probable en une phrase, puis la commande Linux pour réparer. "
        f"Erreur : {log_anonymise}"
    )
    
    try:
        reponse = requests.post(
            OLLAMA_API, 
            json={"model": MODELE_IA, "prompt": prompt, "stream": False},
            timeout=30
        )
        reponse.raise_for_status()
        return reponse.json().get('response', 'Aucune réponse générée.')
    except requests.exceptions.RequestException as e:
        return f"Erreur de communication avec Ollama locale : {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 log_whisperer.py \"<ta ligne de log ici>\"")
        sys.exit(1)
        
    log_brut = sys.argv[1]
    print(" Anonymisation des données...")
    log_propre = anonymiser_log(log_brut)
    print(f"Log à envoyer : {log_propre}\n")
    
    print(" Analyse par l'IA locale en cours...")
    diagnostic = analyser_erreur(log_propre)
    
    print("\n--- DIAGNOSTIC SRE ---")
    print(diagnostic)
    print("----------------------")