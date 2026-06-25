import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import sys

print("🛡️ [SISTEMA] A iniciar o Sniper Furtivo (Máquina Descartável)...")

# ==========================================
# 1. LOGÍSTICA E CONEXÃO
# ==========================================
URL_NUVEM = "postgresql://postgres:Y%40smin2306011986@db.wlqpiniaxxrfkfzjdqyf.supabase.co:5432/postgres"
engine_online = create_engine(URL_NUVEM)

ALVOS_TATICOS = ["apostaganha", "apostatudo"]
LIMITE_VELAS = 20000

def obter_headers_camuflados():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.tipminer.com/",
        "Connection": "keep-alive"
    }

def extrair_e_injetar(alvo):
    agora = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{agora}] 🎯 Iniciando ataque ao alvo: {alvo.upper()}...")
    url_api = f"https://www.tipminer.com/br/api/historico/{alvo}/aviator?limit={LIMITE_VELAS}"
    
    try:
        resposta = requests.get(url_api, headers=obter_headers_camuflados(), timeout=20)
        if resposta.status_code == 200:
            dados_brutos = resposta.json()
            
            if isinstance(dados_brutos, dict) and 'data' in dados_brutos:
                df = pd.DataFrame(dados_brutos['data'])
            else:
                df = pd.DataFrame(dados_brutos)
                
            if df.empty:
                print(f"[{agora}] ⚠️ Gráfico vazio retornado para {alvo}.")
                return

            colunas_site = df.columns.tolist()
            col_mult = 'crash' if 'crash' in colunas_site else 'multiplier' if 'multiplier' in colunas_site else colunas_site[0]
            col_data = 'date' if 'date' in colunas_site else 'created_at' if 'created_at' in colunas_site else colunas_site[1]
            
            df = df.rename(columns={col_mult: 'Multiplicador', col_data: 'Datetime'})
            df = df.drop_duplicates(subset=['Datetime', 'Multiplicador']).sort_values('Datetime').reset_index(drop=True)
            
            nome_tabela = f"historico_aviator_{alvo}"
            df.to_sql(nome_tabela, engine_online, if_exists='replace', index=False)
            print(f"[{agora}] ✅ SUCESSO: {len(df)} velas injetadas na tabela '{nome_tabela}'.")
        else:
            print(f"[{agora}] ❌ Erro {resposta.status_code}: Cloudflare bloqueou.")
    except Exception as e:
        print(f"[{agora}] ❌ Falha crítica: {e}")

# ==========================================
# 2. O ATAQUE ÚNICO (O GitHub faz o relógio)
# ==========================================
if __name__ == "__main__":
    for alvo in ALVOS_TATICOS:
        extrair_e_injetar(alvo)
        time.sleep(2) # Pausa leve entre casinos
    print("\n💤 Missão concluída. A destruir a máquina virtual...")
