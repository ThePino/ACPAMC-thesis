import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_thesis_transparent_curved():
    # --- CONFIGURAZIONE STILE TESI ---
    # Figura larga per contenere tutto il testo
    # Impostiamo facecolor='none' per preparare la figura alla trasparenza
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='none')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Palette colori (Scala di grigi professionale)
    color_border = 'black'
    color_header = '#e8e8e8'  # Grigio chiaro opaco per le sezioni fisse
    color_body = 'white'      # Bianco opaco per il corpo
    
    # Font (Famiglie generiche per compatibilità cross-platform)
    font_txt = {'family': 'serif', 'size': 11, 'color': 'black'}
    font_title = {'family': 'serif', 'size': 16, 'weight': 'bold', 'color': 'black'}
    font_code = {'family': 'monospace', 'size': 11, 'color': '#222222'}

    # ==========================
    # GEOMETRIA
    # ==========================
    y_top = 7.0
    
    # EXE (Sinistra)
    x_exe = 0.5
    w_exe = 7.5 
    h_row = 0.7 
    h_opt = 3.6 
    
    # DLL (Destra)
    x_dll = 9.5
    w_dll = 4.0
    h_total = (3 * h_row) + h_opt 

    # ==========================
    # 1. DISEGNO EXE
    # ==========================
    
    ax.text(x_exe + w_exe/2, y_top + 0.3, "EXE", ha='center', **font_title)

    # Funzione helper per disegnare rettangoli
    def draw_rect(x, y, w, h, text, fill, align='center', x_txt_offset=0):
        rect = patches.Rectangle((x, y - h), w, h, linewidth=1.2, edgecolor=color_border, facecolor=fill)
        ax.add_patch(rect)
        
        if align == 'center':
            ax.text(x + w/2, y - h/2, text, ha='center', va='center', **font_txt)
        else:
            ax.text(x + x_txt_offset, y - h/2, text, ha='left', va='center', **font_txt)
        return y - h

    # A. Intestazioni Fisse
    y_curr = draw_rect(x_exe, y_top, w_exe, h_row, "STUB MS-DOS", color_header)
    y_curr = draw_rect(x_exe, y_curr, w_exe, h_row, "Firma PE", color_header, align='left', x_txt_offset=0.2)
    y_curr = draw_rect(x_exe, y_curr, w_exe, h_row, "Intestazione COFF", color_header, align='left', x_txt_offset=0.2)

    # B. Intestazione Facoltativa
    rect_opt = patches.Rectangle((x_exe, y_curr - h_opt), w_exe, h_opt, linewidth=1.2, edgecolor=color_border, facecolor=color_body)
    ax.add_patch(rect_opt)
    
    split = 2.2
    ax.plot([x_exe + split, x_exe + split], [y_curr, y_curr - h_opt], color='black', lw=1.2)
    ax.text(x_exe + split/2, y_curr - h_opt/2, "intestazione\nfacoltativa", ha='center', va='center', **font_txt)

    h_sub = h_opt / 3
    
    # Righe a destra
    ax.plot([x_exe + split, x_exe + w_exe], [y_curr - h_sub, y_curr - h_sub], color='black', lw=1.2)
    ax.text(x_exe + split + 0.2, y_curr - h_sub/2, "Campi standard intestazione facoltativi", ha='left', va='center', **font_txt)
    
    ax.plot([x_exe + split, x_exe + w_exe], [y_curr - 2*h_sub, y_curr - 2*h_sub], color='black', lw=1.2)
    ax.text(x_exe + split + 0.2, y_curr - 1.5*h_sub, "Campi specifici dell'intestazione\nfacoltativa di windows", ha='left', va='center', **font_txt)
    
    ax.text(x_exe + split + 0.2, y_curr - 2.5*h_sub, "Directory dati intestazione facoltative", ha='left', va='center', **font_txt)

    # Punto per la freccia
    arrow_start = (x_exe + w_exe, y_curr - 2.5*h_sub)

    # ==========================
    # 2. DISEGNO DLL
    # ==========================
    
    ax.text(x_dll + w_dll/2, y_top + 0.3, "DLL (User32.dll)", ha='center', **font_title)

    rect_dll = patches.Rectangle((x_dll, y_top - h_total), w_dll, h_total, linewidth=1.2, edgecolor=color_border, facecolor=color_body)
    ax.add_patch(rect_dll)

    funcs = ["ClipCursor", "CopyCursor", "CreateCursor", "..."]
    start_text_y = y_top - 1.5 
    for i, func in enumerate(funcs):
        ax.text(x_dll + 0.4, start_text_y - (i * 0.8), func, ha='left', va='center', **font_code)

    # ==========================
    # 3. FRECCIA ARMONIOSA
    # ==========================
    
    arrow_end = (x_dll, start_text_y)
    
    # MODIFICA QUI: connectionstyle con 'rad' crea la curva.
    # rad=-0.15 crea una curva dolce verso il basso.
    # Aumentato leggermente head_width e lw per solidità.
    arrow = patches.FancyArrowPatch(
        posA=arrow_start, posB=arrow_end,
        arrowstyle='-|>,head_width=6,head_length=12',
        connectionstyle="arc3,rad=-0.15", 
        color='black', lw=1.5
    )
    ax.add_patch(arrow)

    plt.tight_layout()
    
    # SALVATAGGIO CON TRASPARENZA (transparent=True)
    output_png = 'diagramma_tesi_trasparente.png'
    output_pdf = 'diagramma_tesi_trasparente.pdf'
    
    plt.savefig(output_png, dpi=300, bbox_inches='tight', transparent=True)
    plt.savefig(output_pdf, bbox_inches='tight', transparent=True)
    
    print(f"Grafici salvati con sfondo trasparente: {output_png} e {output_pdf}")

if __name__ == "__main__":
    draw_thesis_transparent_curved()