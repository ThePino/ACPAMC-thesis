import matplotlib.pyplot as plt
from pathlib import Path
import graphviz

data = """
Worm.Win32.Zwr.c,
"009a83236c600fd7ac034973f064284cec62f86631fe96e900cb664f86061431",
"GetSystemDirectoryA","IsDBCSLeadByte","LocalAlloc","CreateSemaphoreW",
"CreateSemaphoreA","GlobalAddAtomW","lstrcpynW","LoadLibraryExW","SearchPathW",
"CreateFileW","CreateFileMappingW","MapViewOfFileEx","GetSystemMetrics",
"RegisterClipboardFormatW","SystemParametersInfoW","GetDC","GetDeviceCaps",
"ReleaseDC","LocalAlloc","GetSysColor","GetSysColorBrush","GetStockObject",
"GetSystemMetrics","LoadCursorW","RegisterClassW","RegisterClassExW",
"LoadLibraryExW","LoadLibraryW","GetCommandLineA","GetStartupInfoA",
"LockResource","GetModuleFileNameA","IsBadWritePtr","RegisterClipboardFormatW",
"SystemParametersInfoW","GetSystemMetrics","LocalAlloc","GetSysColor",
"GetSysColorBrush","GetStockObject","LoadLibraryW","LoadLibraryExW",
"LoadCursorW","RegisterClassW","GetKeyboardType","GetCommandLineA",
"GetStartupInfoA","GetVersion","GetModuleFileNameA","lstrcpynA",
"GetThreadLocale","GetLocaleInfoW","GetLocaleInfoA","lstrlenA",
"LoadLibraryExW","SearchPathW","FindResourceExW","LoadResource","LoadStringA",
"LocalAlloc","VirtualAllocEx","GetThreadLocale","GetLocaleInfoA",
"GetLocaleInfoW","EnumCalendarInfoA","CreateEventA","LoadLibraryExW",
"lstrcpyA","CompareStringA","lstrcmpA","WaitForSingleObjectEx",
"WaitForSingleObject","GetProcessVersion","GlobalAlloc","DuplicateHandle",
"WSAStartup","LoadLibraryExW","CreateSemaphoreA","CreateSemaphoreW",
"ReleaseSemaphore","WaitForSingleObject","WaitForSingleObjectEx",
"GetWindowsDirectoryW","LocalAlloc","FindFirstFileExW","FindFirstFileA",
"GetModuleFileNameA","CreateFileW","WriteFile","CopyFileExW","CopyFileA",
"OpenEventW","WaitForSingleObject","WaitForSingleObjectEx","LoadLibraryW",
"LoadLibraryExW","DuplicateHandle","DeviceIoControl","SwitchToThread",
"WSACleanup","FreeLibrary","VirtualQueryEx","ResetEvent","VirtualFreeEx",
"UnregisterClassW"
"""

def matplot_p(apis: list[str], output: Path):
    plt.figure(figsize=(8, 3))
    plt.text(0.5, 0.5, "\n".join(apis), ha="center", va="center", fontsize=10,
         family="monospace", bbox=dict(boxstyle="round,pad=1", facecolor="whitesmoke"))
    plt.axis("off")
    plt.savefig(output, dpi=300)
    plt.close()

def crea_grafo_sequenza_parole(lista_parole: list, nome_file: str = 'grafo_parole'):
    """
    Crea un grafo orientato (Digraph) da una lista di parole.

    Ogni nodo è unico (anche se le parole si ripetono), etichettato con il suo
    indice e la parola, e rappresentato come un quadrato. Gli archi collegano 
    le parole adiacenti nella sequenza. Il layout è da sinistra a destra (LR).
    Viene garantita la pulizia del file sorgente .gv dopo il rendering.

    Args:
        lista_parole (list): La lista di parole da cui creare il grafo.
        nome_file (str): Nome del file di output (verrà generato 'nome_file.png').
    """
    
    # 1. Crea un grafo orientato (Digraph)
    dot = graphviz.Digraph(
        comment='Grafo Sequenza di Parole', 
        name='SequenceGraph',
        graph_attr={
            'rankdir': 'LR',  # Layout da Sinistra a Destra
            'splines': 'ortho', # Opzionale: per linee ad angolo retto, se preferito
            'bgcolor':'transparent'
        } 
    )

    # 2. Imposta l'attributo di default per i nodi: forma quadrata
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')

    # 3. Aggiungi i nodi e gli archi
    nodi_aggiunti = {}

    for i, parola in enumerate(lista_parole):
        # ID univoco per il nodo: l'indice garantisce che anche le parole ripetute siano nodi diversi.
        node_id = f'n{i + 1}'
        
        # Etichetta del nodo: Indice | Parola. Uso il formato HTML-like per una chiara separazione.
        label = f'<{i + 1} | {parola}>' 
        
        # Aggiungi il nodo con l'etichetta
        dot.node(
            name=node_id, 
            label=label
        )
        nodi_aggiunti[i] = node_id

        # Se non è il primo elemento, aggiungi un arco dal nodo precedente
        if i > 0:
            nodo_precedente_id = nodi_aggiunti[i - 1]
            dot.edge(nodo_precedente_id, node_id) # Arco di adiacenza

    # 4. Salva il sorgente DOT e renderizza il grafo in un file
    # cleanup=True: elimina il file sorgente .gv dopo il rendering
    # view=True: apre l'immagine automaticamente dopo la creazione (può essere rimosso)
    dot.render(nome_file, format='png', view=False, cleanup=True) 
    print(f"Generazione completata. Il file sorgente '{nome_file}.gv' è stato rimosso.")

def main():
    output_file = Path(__file__).resolve().parent / "api_sequence.png"
    tokens = data.replace('\n', '').split(',')
    size = 6
    apis = tokens[2: (size + 2)]
    # matplot(apis, output_file)
    crea_grafo_sequenza_parole(apis, str(output_file).removesuffix('.png'))
    pass

if __name__ == "__main__":
    main()