import matplotlib.pyplot as plt
import numpy as np

def genera_torta_italia(ax=None, save=True):
    """Genera il grafico a torta per la distribuzione degli attacchi in Italia."""
    # Se non viene passato un asse (ax), ne crea uno nuovo (modalità stand-alone)
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 7))
    else:
        save = False # Se è parte di un subplot, non salvare il singolo file qui

    # Dati - Fonte: Rapporto Clusit 2025 (Pagina 39, Figura 30)
    labels = ['Malware', 'DDoS', 'Vulnerabilities', 'Phishing', 'Undisclosed', 'Altro']
    sizes = [38, 21, 19, 11, 7, 4]
    colors = ['#ff4d4d', '#d9d9d9', '#d9d9d9', '#d9d9d9', '#d9d9d9', '#d9d9d9']
    explode = (0.1, 0, 0, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                       shadow=True, startangle=140, colors=colors,
                                       textprops=dict(color="black"))

    plt.setp(autotexts, size=10, weight="bold")
    plt.setp(texts, size=11) # Font leggermente ridotto per evitare sovrapposizioni nel combined
    ax.set_title("Distribuzione Tecniche di Attacco in Italia (2024)\n", fontsize=14, fontweight='bold')
    ax.axis('equal')
    
    if save:
        filename = 'grafico_torta_italia.png'
        plt.tight_layout()
        plt.savefig(filename, transparent=True)
        print(f"Grafico salvato come: {filename}")
        plt.close()

def genera_istogramma_confronto(ax=None, save=True):
    """Genera l'istogramma di confronto Italia vs Mondo."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        save = False

    # Dati - Fonte: Rapporto Clusit 2025
    categories = ['Mondo', 'Italia']
    malware_percentages = [32, 38]
    colors = ['#bfbfbf', '#ff4d4d']

    bars = ax.bar(categories, malware_percentages, color=colors, width=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('Incidenza % sul totale incidenti', fontsize=10)
    ax.set_title('Incidenza Attacchi Malware: Italia vs Mondo', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 50)
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    if save:
        filename = 'istogramma_italia_mondo.png'
        plt.tight_layout()
        plt.savefig(filename, transparent=True)
        print(f"Grafico salvato come: {filename}")
        plt.close()

def genera_istogramma_istat(ax=None, save=True):
    """Genera l'istogramma sui dati ISTAT."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        save = False

    # Dati - Fonte: Istat, Report Cittadini e ICT 2024
    categories = ['Famiglie con accesso\na Internet', 'Individui (6+) che\nusano Internet']
    percentages = [86.2, 81.9]
    colors = ['#ff4d4d', '#bfbfbf']

    bars = ax.bar(categories, percentages, color=colors, width=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('Percentuale (%)', fontsize=10)
    ax.set_title('Diffusione di Internet in Italia (2024)', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    if save:
        filename = 'istogramma_istat_internet.png'
        plt.tight_layout()
        plt.savefig(filename, transparent=True)
        print(f"Grafico salvato come: {filename}")
        plt.close()

def genera_dashboard_combinata():
    """Crea un'unica immagine con i grafici relativi al Rapporto Clusit (Torta e Confronto)."""
    # Crea una figura con una griglia 1x2 (solo i due grafici Clusit affiancati)
    # Layout:
    # [  Torta  ][ Istogramma Confronto ]
    
    fig = plt.figure(figsize=(16, 7)) # Altezza ridotta dato che è una sola riga
    
    # Griglia per il layout
    gs = fig.add_gridspec(1, 2)
    
    # Asse per la torta (colonna 1)
    ax1 = fig.add_subplot(gs[0, 0])
    genera_torta_italia(ax=ax1, save=False)
    
    # Asse per confronto Italia vs Mondo (colonna 2)
    ax2 = fig.add_subplot(gs[0, 1])
    genera_istogramma_confronto(ax=ax2, save=False)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Lascia spazio per il titolo
    filename = 'combined_dashboard.png'
    plt.savefig(filename, transparent=True)
    print(f"Grafico combinato salvato come: {filename}")
    plt.close()

if __name__ == "__main__":
    print("Generazione grafici in corso...")
    # Genera i singoli file
    genera_torta_italia()
    genera_istogramma_confronto()
    genera_istogramma_istat()
    # Genera il file combinato (solo Clusit)
    genera_dashboard_combinata()
    print("Finito! Controlla la cartella per i file PNG.")