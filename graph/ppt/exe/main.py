import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_thesis_no_arrow():
    # --- CONFIGURAZIONE STILE TESI ---
    # Figsize ampia per mantenere alta risoluzione e proporzioni
    fig, ax = plt.subplots(figsize=(30, 22), facecolor='none')
    
    # Limiti assi
    ax.set_xlim(0, 16)
    ax.set_ylim(-1.5, 9) 
    ax.axis('off')

    # Palette colori
    color_border = 'black'
    color_header = '#e8e8e8' 
    color_body = 'white'
    
    # --- FONT E SPESSORI ---
    font_txt = {'family': 'serif', 'size': 50, 'color': 'black'}
    font_title = {'family': 'serif', 'size': 30, 'weight': 'bold', 'color': 'black'}
    font_code = {'family': 'monospace', 'size': 50, 'color': '#222222'}
    
    line_w = 2.5

    # ==========================
    # GEOMETRIA
    # ==========================
    y_top = 8.5 
    
    # EXE (Sinistra)
    x_exe = 0.5
    w_exe = 7.5 
    h_row = 1.0  
    h_opt = 5.2 
    
    # DLL (Destra)
    x_dll = 10.0  # Posizione bilanciata
    w_dll = 5.5  
    h_total = (3 * h_row) + h_opt 

    # ==========================
    # 1. DISEGNO EXE
    # ==========================
    
    def draw_rect(x, y, w, h, text, fill, align='center', x_txt_offset=0):
        rect = patches.Rectangle((x, y - h), w, h, linewidth=line_w, edgecolor=color_border, facecolor=fill)
        ax.add_patch(rect)
        if align == 'center':
            ax.text(x + w/2, y - h/2, text, ha='center', va='center', **font_txt)
        else:
            ax.text(x + x_txt_offset, y - h/2, text, ha='left', va='center', **font_txt)
        return y - h

    # Intestazioni Fisse
    y_curr = draw_rect(x_exe, y_top, w_exe, h_row, "STUB MS-DOS", color_header)
    y_curr = draw_rect(x_exe, y_curr, w_exe, h_row, "Firma PE", color_header, align='left', x_txt_offset=0.3)
    y_curr = draw_rect(x_exe, y_curr, w_exe, h_row, "Intestazione COFF", color_header, align='left', x_txt_offset=0.3)

    # Intestazione Facoltativa
    rect_opt = patches.Rectangle((x_exe, y_curr - h_opt), w_exe, h_opt, linewidth=line_w, edgecolor=color_border, facecolor=color_body)
    ax.add_patch(rect_opt)
    
    split = 2.6
    ax.plot([x_exe + split, x_exe + split], [y_curr, y_curr - h_opt], color='black', lw=line_w)
    
    ax.text(x_exe + split/2, y_curr - h_opt/2, "intestazione\nfacoltativa", ha='center', va='center', **font_txt)

    h_sub = h_opt / 3
    
    # Righe a destra (Campi intestazione)
    ax.plot([x_exe + split, x_exe + w_exe], [y_curr - h_sub, y_curr - h_sub], color='black', lw=line_w)
    ax.text(x_exe + split + 0.2, y_curr - h_sub/2, "Campi standard\nintestazione facoltativi", ha='left', va='center', **font_txt)
    
    ax.plot([x_exe + split, x_exe + w_exe], [y_curr - 2*h_sub, y_curr - 2*h_sub], color='black', lw=line_w)
    ax.text(x_exe + split + 0.2, y_curr - 1.5*h_sub, "Campi specifici\ndell'intestazione\nfacoltativa di windows", ha='left', va='center', **font_txt)
    
    ax.text(x_exe + split + 0.2, y_curr - 2.5*h_sub, "Directory dati\nintestazione facoltative", ha='left', va='center', **font_txt)

    # TITOLO EXE (SOTTO)
    ax.text(x_exe + w_exe/2, (y_curr - h_opt) - 0.8, "EXE", ha='center', va='top', **font_title)

    # ==========================
    # 2. DISEGNO DLL
    # ==========================
    
    rect_dll = patches.Rectangle((x_dll, y_top - h_total), w_dll, h_total, linewidth=line_w, edgecolor=color_border, facecolor=color_body)
    ax.add_patch(rect_dll)

    funcs = ["ClipCursor", "CopyCursor", "CreateCursor", "..."]
    start_text_y = y_top - 1.8 
    
    for i, func in enumerate(funcs):
        ax.text(x_dll + 0.5, start_text_y - (i * 1.3), func, ha='left', va='center', **font_code)

    # TITOLO DLL (SOTTO)
    ax.text(x_dll + w_dll/2, (y_top - h_total) - 0.8, "DLL (User32.dll)", ha='center', va='top', **font_title)

    # ==========================
    # SALVATAGGIO
    # ==========================

    plt.tight_layout()
    
    output_png = 'diagramma_tesi_clean.png'
    output_pdf = 'diagramma_tesi_clean.pdf'
    
    plt.savefig(output_png, dpi=300, bbox_inches='tight', transparent=True)
    plt.savefig(output_pdf, bbox_inches='tight', transparent=True)
    
    print(f"Grafico salvato senza freccia: {output_png}")

if __name__ == "__main__":
    draw_thesis_no_arrow()