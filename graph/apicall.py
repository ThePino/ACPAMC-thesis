import matplotlib.pyplot as plt
from pathlib import Path
import graphviz
from collections import Counter

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

def crea_grafo_bow_pipeline(lista_parole: list, nome_file: str = 'grafo_bow_pipeline_final'):
    """
    Crea un grafo orientato che visualizza l'intera pipeline Bag-of-Words,
    utilizzando indici numerici semplici e background trasparente.
    """
    
    # 1. Calcolo del Vocabolario e del Vettore BoW
    frequenze = Counter(lista_parole)
    vocabolario_ordinato = sorted(frequenze.keys())
    vettore_bow = [frequenze[parola] for parola in vocabolario_ordinato]
    num_colonne = len(vocabolario_ordinato)

    # 2. Inizializzazione del Grafo
    dot = graphviz.Digraph(
        comment='Pipeline Bag-of-Words', 
        name='BoWPipelineGraph',
        graph_attr={
            'rankdir': 'TB',
            'bgcolor':'transparent' 
        } 
    )
    
    # FORZATURA CHIAVE PER GARANTIRE LA TRASPARENZA GLOBALE
    dot.attr(bgcolor='transparent')

    # 3. Cluster 1: Sequenza Originale (API Calls)
    with dot.subgraph(name='cluster_sequenza') as seq:
        seq.attr(label='1. Sequenza Originale (API Calls)', style='rounded')
        seq.attr('node', shape='box', style='filled', fillcolor='#DAF7A6') # Verde chiaro
        
        nodi_sequenza = {}

        for i, parola in enumerate(lista_parole):
            node_id = f'seq_{i + 1}'
            label = f'<{i + 1} | {parola}>' # Indice | Parola
            
            seq.node(name=node_id, label=label)
            nodi_sequenza[i] = node_id

            if i > 0:
                nodo_precedente_id = nodi_sequenza[i - 1]
                seq.edge(nodo_precedente_id, node_id)
        
        if nodi_sequenza:
            nodo_inizio_sequenza = nodi_sequenza[0]


    # 4. Cluster 2 & 3 Combinati: Vocabolario e Vettore BoW Allineati
    with dot.subgraph(name='cluster_vettori_allineati') as vettori:
        vettori.attr(label='2. Mappatura e Vettore delle Caratteristiche (BoW)', style='rounded', bgcolor='transparent') # Cluster trasparente
        
        # Costruzione di un'unica tabella HTML
        tabella_allineata = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        
        # Riga A: Intestazione Indici (Vocabolario) 
        tabella_allineata += f'<TR><TD COLSPAN="{num_colonne}" BGCOLOR="#E6E6FA"><B>Vocabolario Ordinato (Feature)</B></TD></TR>'

        # Riga B: Indici delle Feature (0, 1, 2, ...)
        tabella_allineata += '<TR>'
        for i in range(num_colonne):
            tabella_allineata += f'<TD BGCOLOR="#ADD8E6"><B>{i}</B></TD>' 
        tabella_allineata += '</TR>'
        
        # Riga C: Parole (API)
        tabella_allineata += '<TR>'
        for parola in vocabolario_ordinato:
            tabella_allineata += f'<TD>{parola}</TD>'
        tabella_allineata += '</TR>'
        
        # Riga D: Intestazione Vettore Frequenze
        tabella_allineata += f'<TR><TD COLSPAN="{num_colonne}" BGCOLOR="#E6E6FA"><B>Vettore Frequenze (BoW)</B></TD></TR>'
        
        # Riga E: Vettore BoW (Conteggi)
        tabella_allineata += '<TR>'
        for conteggio in vettore_bow:
            tabella_allineata += f'<TD BGCOLOR="#FFC0CB"><B>{conteggio}</B></TD>'
        tabella_allineata += '</TR>'
        
        tabella_allineata += '</TABLE>>'
        
        vettori.node(
            'vettori_node', 
            label=tabella_allineata, 
            shape='none', 
            margin='0.1',
            fontname='Arial'
        )

    # 5. Connessione logica: dalla sequenza ai vettori
    dot.edge(nodo_inizio_sequenza, 'vettori_node', label='Mappatura BoW', arrowhead='normal')

    # 6. Rendering
    dot.render(nome_file, format='png', view=False, cleanup=True) 
    print(f"Generazione completata. Il file di output è '{nome_file}.png'.")

def main():
    output_file = Path(__file__).resolve().parent / "api_sequence"
    tokens = data.replace('\n', '').split(',')
    size = 4
    apis = tokens[2: (size + 2)]
    apis.append(apis[2])
    # matplot(apis, output_file)
    crea_grafo_bow_pipeline(apis, str(output_file).removesuffix('.png'))
    pass

if __name__ == "__main__":
    main()