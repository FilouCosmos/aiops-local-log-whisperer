import re
import sys
import requests

# --- Config ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
# ---------------------

def mask_pii(log_line):
    # Censure basique d'IPv4 pour eviter les fuites de donnees internes
    return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED_IP]', log_line)

def ask_ai(log_line):
    prompt = f"Act as a Senior Linux SysAdmin. Explain this log error in 1 sentence and give the bash command to fix it. Log: {log_line}"
    
    try:
        res = requests.post(
            OLLAMA_URL, 
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=20
        )
        res.raise_for_status()
        return res.json().get('response', 'No answer from AI.')
    except Exception as e:
        return f"Local Ollama connection failed: {e}"

if __name__ == "__main__":
    # Check si l'utilisateur a bien passe un log en argument
    if len(sys.argv) < 2:
        print("Usage: python3 log_whisperer.py '<your_log_line>'")
        sys.exit(1)
        
    raw_log = sys.argv[1]
    safe_log = mask_pii(raw_log)
    
    print(f"[INFO] Analyzing log: {safe_log}")
    print("[INFO] Interrogating local LLM...")
    
    remediation = ask_ai(safe_log)
    
    print("\n=== AI SRE DIAGNOSTIC ===")
    print(remediation)
    print("=========================")