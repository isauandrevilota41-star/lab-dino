#!/usr/bin/env python3
# LAB DINO V12 - Toolkit de Redes e Pentest
# By Isau | Kali Linux
import os
import subprocess
import sys
from datetime import datetime

# Cores
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
CIANO = "\033[96m"
RESET = "\033[0m"
NEGRITO = "\033[1m"

def banner():
    os.system('clear')
    print(f"{VERDE}{NEGRITO}")
    print(r"""
     __       __     ___     ___ _   _  ___  
    |  |     /  \   |   \   |   | \ | |/   \ 
    |  |    / /\ \  | |\ \  |   |  \| |  O  |
    |  |__ / /__\ \ | | \ \ |   |     |   O |
    |____//_/    \_\|_|  \_\|___|_|\__|___/  
    """)
    print(f"{RESET}{CIANO}  Toolkit de Redes & Pentest - V12{RESET}")
    print(f"{AMARELO}  [+] Nmap | Gobuster | Whois | SQLMap | Etc{RESET}\n")

def check_tool(tool):
    return subprocess.call(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def run_cmd(cmd):
    print(f"\n{AZUL}[*] Executando: {cmd}{RESET}\n")
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}[!] Cancelado pelo usuário{RESET}")

def nmap_scan():
    alvo = input(f"{AMARELO}Digite o IP/Domínio: {RESET}").strip()
    if not alvo: return
    print(f"""
{VERDE}[1]{RESET} Scan Rápido (Top 1000 portas)
{VERDE}[2]{RESET} Scan Completo (Todas as portas)
{VERDE}[3]{RESET} Scan + Versão de Serviços (-sV)
{VERDE}[4]{RESET} Scan Agressivo (-A)
{VERDE}[5]{RESET} Detectar SO (-O)
""")
    opc = input(f"{AMARELO}Escolha: {RESET}")
    if opc == "1": run_cmd(f"nmap {alvo}")
    elif opc == "2": run_cmd(f"nmap -p- {alvo}")
    elif opc == "3": run_cmd(f"nmap -sV {alvo}")
    elif opc == "4": run_cmd(f"nmap -A {alvo}")
    elif opc == "5": run_cmd(f"nmap -O {alvo}")
    else: run_cmd(f"nmap {alvo}")

def gobuster_scan():
    if not check_tool("gobuster"):
        print(f"{VERMELHO}[!] Gobuster não instalado. Instale: sudo apt install gobuster{RESET}")
        return
    url = input(f"{AMARELO}Digite a URL (ex: https://site.com): {RESET}").strip()
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.exists(wordlist):
        wordlist = input(f"{AMARELO}Wordlist não encontrada. Digite o caminho: {RESET}").strip()
    run_cmd(f"gobuster dir -u {url} -w {wordlist} -t 50")

def whois_lookup():
    alvo = input(f"{AMARELO}Digite o Domínio/IP: {RESET}").strip()
    run_cmd(f"whois {alvo}")

def dns_lookup():
    alvo = input(f"{AMARELO}Digite o Domínio: {RESET}").strip()
    run_cmd(f"nslookup {alvo} && echo '---' && dig {alvo} ANY +short")

def sqlmap_scan():
    if not check_tool("sqlmap"):
        print(f"{VERMELHO}[!] SQLMap não instalado{RESET}")
        return
    url = input(f"{AMARELO}Digite a URL com parâmetro (ex: site.com?id=1): {RESET}").strip()
    run_cmd(f"sqlmap -u {url} --batch --crawl=1")

def ping_sweep():
    rede = input(f"{AMARELO}Digite a rede (ex: 192.168.1.0/24 ou 192.168.1.1-50): {RESET}").strip()
    # usa nmap pra ping sweep
    run_cmd(f"nmap -sn {rede}")

def meu_ip():
    run_cmd("curl -s ifconfig.me && echo && ip a | grep inet")

def menu():
    while True:
        banner()
        print(f"{NEGRITO}MENU PRINCIPAL:{RESET}")
        print(f"{VERDE}[1]{RESET} Nmap - Scanner de Portas")
        print(f"{VERDE}[2]{RESET} Gobuster - Descoberta de Diretórios")
        print(f"{VERDE}[3]{RESET} Whois - Informações de Domínio")
        print(f"{VERDE}[4]{RESET} DNS Lookup - nslookup/dig")
        print(f"{VERDE}[5]{RESET} SQLMap - Teste SQL Injection")
        print(f"{VERDE}[6]{RESET} Ping Sweep - Varredura de Rede")
        print(f"{VERDE}[7]{RESET} Meu IP - Ver IPs local e público")
        print(f"{VERMELHO}[0]{RESET} Sair\n")
        
        opc = input(f"{CIANO}lab-dino > {RESET}").strip()
        
        if opc == "1": nmap_scan()
        elif opc == "2": gobuster_scan()
        elif opc == "3": whois_lookup()
        elif opc == "4": dns_lookup()
        elif opc == "5": sqlmap_scan()
        elif opc == "6": ping_sweep()
        elif opc == "7": meu_ip()
        elif opc == "0":
            print(f"{VERDE}Saindo... Valeu!{RESET}")
            sys.exit(0)
        else:
            print(f"{VERMELHO}Opção inválida!{RESET}")
        
        input(f"\n{AMARELO}Pressione ENTER para voltar ao menu...{RESET}")

if __name__ == "__main__":
    try:
        if os.geteuid() != 0:
            print(f"{AMARELO}[!] Dica: Rode com sudo para mais funções do Nmap{RESET}\n")
        menu()
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}Saindo...{RESET}")
        sys.exit(0)