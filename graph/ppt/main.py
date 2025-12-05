import matplotlib.pyplot as plt
import numpy as np

def genera_torta_italia():
    """Genera il grafico a torta per la distribuzione degli attacchi in Italia con sfondo trasparente."""
    # Dati
    # Fonte: Rapporto Clusit 2025 (Pagina 39, Figura 30)
    labels = ['Malware', 'DDoS', 'Vulnerabilities', 'Phishing / Social Engineering', 'Undisclosed', 'Altro']
    sizes = [38, 21, 19, 11, 7, 4] # Percentuali. "Altro" include Multiple Techniques e Web Attack
    
    # Colori: Rosso per evidenziare il Malware, grigi/blu spenti per il resto
    colors = ['#ff4d4d', '#d9d9d9', '#bfbfbf', '#a6a6a6', '#8c8c8c', '#737373']
    explode = (0.1, 0, 0, 0, 0, 0)  # "Esplode" la fetta del Malware per evidenziarla

    # Creazione del grafico
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       shadow=True, startangle=140, colors=colors,
                                       textprops=dict(color="black"))

    # Personalizzazione del testo delle percentuali
    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=12)

    # Titolo
    plt.title("Distribuzione Tecniche di Attacco in Italia (2024)\nFonte: Rapporto Clusit 2025", fontsize=14, fontweight='bold')


    # Assicura che il grafico sia disegnato come un cerchio
    ax1.axis('equal')
    
    # Salva il grafico con sfondo trasparente
    filename = 'grafico_torta_italia.png'
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
    print(f"Grafico salvato come: {filename}")
    plt.close() # Chiude la figura per liberare memoria

def genera_istogramma_confronto():
    """Genera l'istogramma di confronto Italia vs Mondo con sfondo trasparente."""
    # Dati
    # Fonte: Rapporto Clusit 2025
    categories = ['Mondo', 'Italia']
    malware_percentages = [32, 38] # 32% Global (Pag 20), 38% Italia (Pag 39)

    # Colori: Grigio per Mondo, Rosso per Italia (per evidenziare il focus)
    colors = ['#bfbfbf', '#ff4d4d']

    # Creazione dell'istogramma
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(categories, malware_percentages, color=colors, width=0.5)

    # Aggiunta delle etichette con i valori sopra le barre
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14, fontweight='bold')

    # Personalizzazione assi e titolo
    ax.set_ylabel('Incidenza % sul totale incidenti', fontsize=12)
    ax.set_title('Incidenza Attacchi Malware: Italia vs Mondo (2024)\nFonte: Rapporto Clusit 2025', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 50) # Imposta il limite y per dare spazio alle etichette
    
    # Aggiunta di una griglia orizzontale leggera per leggibilità
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    # Salva il grafico con sfondo trasparente
    filename = 'istogramma_italia_mondo.png'
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
    print(f"Grafico salvato come: {filename}")
    plt.close()

def genera_istogramma_istat():
    """Genera l'istogramma sui dati ISTAT (Uso di Internet) con sfondo trasparente."""
    # Dati
    # Fonte: Istat, Report Cittadini e ICT 2024 (Pagina 1)
    categories = ['Famiglie con accesso\na Internet', 'Individui (6+) che usano\nInternet (ultimi 3 mesi)']
    percentages = [86.2, 81.9] 
    
    # Colori: Rosso per le Famiglie, Grigio per gli Individui
    colors = ['#ff4d4d', '#bfbfbf']

    # Creazione dell'istogramma
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(categories, percentages, color=colors, width=0.5)

    # Aggiunta delle etichette con i valori sopra le barre
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14, fontweight='bold')

    # Personalizzazione assi e titolo
    ax.set_ylabel('Percentuale (%)', fontsize=12)
    ax.set_title('Diffusione di Internet in Italia (2024)\nFonte: Istat - Cittadini e ICT', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100) # Scala fino a 100%
    
    # Aggiunta di una griglia orizzontale leggera
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Salva il grafico con sfondo trasparente
    filename = 'istogramma_istat_internet.png'
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
    print(f"Grafico salvato come: {filename}")
    plt.close()

if __name__ == "__main__":
    print("Generazione grafici in corso...")
    genera_torta_italia()
    genera_istogramma_confronto()
    genera_istogramma_istat()
    print("Finito! Controlla la cartella per i file PNG.")