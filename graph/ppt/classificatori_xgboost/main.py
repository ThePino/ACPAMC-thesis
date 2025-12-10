from graphviz import Digraph

def draw_xgboost_png():
    # CAMBIAMENTO QUI: format='png' invece di 'pdf'
    dot = Digraph(comment='XGBoost Structure', format='png')
    
    # Impostazioni layout
    dot.attr(rankdir='LR', splines='ortho', nodesep='0.6', ranksep='0.5')
    
    # CAMBIAMENTO QUI: Sfondo trasparente
    dot.attr(bgcolor='transparent')
    
    # Stili professionali
    dot.attr('node', shape='box', fontname='Helvetica', style='filled', fillcolor='white', color='#333333')
    dot.attr('edge', color='#555555', arrowsize='0.8')

    # --- 1. NODO INPUT ---
    dot.node('input', 'Input Data\n(x)', shape='cylinder', fillcolor='#E0E0E0', height='0.8')
    
    # --- 2. ALBERO 1 (Base Model) ---
    with dot.subgraph(name='cluster_tree1') as c:
        c.attr(label='Tree 1 (Base)', color='lightgrey', style='dashed', bgcolor='none') # bgcolor='none' per trasparenza cluster
        c.node('t1_root', 'Age < 30?')
        c.node('t1_yes', 'Weight +0.5', shape='ellipse', color='#44aa44', fontcolor='white')
        c.node('t1_no', 'Weight -0.5', shape='ellipse', color='#aa4444', fontcolor='white')
        
        c.edge('t1_root', 't1_yes', label=' Yes', fontsize='10')
        c.edge('t1_root', 't1_no', label=' No', fontsize='10')

    # --- 3. ALBERO 2 (Corregge i residui) ---
    with dot.subgraph(name='cluster_tree2') as c:
        c.attr(label='Tree 2 (Fix Error)', color='lightgrey', style='dashed', bgcolor='none')
        c.node('t2_root', 'Income > 50k?')
        c.node('t2_yes', 'Weight +0.3', shape='ellipse', color='#44aa44', fontcolor='white')
        c.node('t2_no', 'Weight -0.1', shape='ellipse', color='#aa4444', fontcolor='white')
        
        c.edge('t2_root', 't2_yes', label=' Yes', fontsize='10')
        c.edge('t2_root', 't2_no', label=' No', fontsize='10')

    # --- 4. ALBERO 3 (Rifinizione) ---
    with dot.subgraph(name='cluster_tree3') as c:
        c.attr(label='Tree 3 (Refine)', color='lightgrey', style='dashed', bgcolor='none')
        c.node('t3_root', 'Has Debt?')
        c.node('t3_yes', 'Weight -0.2', shape='ellipse', color='#aa4444', fontcolor='white')
        c.node('t3_no', 'Weight +0.1', shape='ellipse', color='#44aa44', fontcolor='white')
        
        c.edge('t3_root', 't3_yes', label=' Yes', fontsize='10')
        c.edge('t3_root', 't3_no', label=' No', fontsize='10')

    # --- 5. SOMMA E OUTPUT ---
    dot.node('sum', 'Σ\n(Sum)', shape='circle', width='0.8', fixedsize='true', 
             fontsize='20', fillcolor='#FFF8E1', color='#FFC107', penwidth='2')
    
    dot.node('output', 'Final Prediction\nŷ = σ(Σ)', shape='doubleoctagon', 
             fillcolor='#D1C4E9', color='#673AB7', fontcolor='black')

    # --- COLLEGAMENTI ---
    dot.edge('input', 't1_root', style='dashed')
    dot.edge('input', 't2_root', style='dashed')
    dot.edge('input', 't3_root', style='dashed')

    dot.edge('t1_yes', 'sum', color='#44aa44')
    dot.edge('t1_no', 'sum', color='#aa4444')
    dot.edge('t2_yes', 'sum', color='#44aa44')
    dot.edge('t2_no', 'sum', color='#aa4444')
    dot.edge('t3_yes', 'sum', color='#aa4444')
    dot.edge('t3_no', 'sum', color='#44aa44')

    dot.edge('sum', 'output', penwidth='2.0')

    # Titolo
    dot.attr(label=r'\nVisualizzazione XGBoost (Ensemble Additivo)\nŷ_i = Σ fk(x_i)', 
             fontsize='14', fontname='Helvetica-Bold')

    # Render
    filename = 'xgboost_diagram'
    # view=False impedisce di provare ad aprire il file se non hai un visualizzatore installato nel container
    output_path = dot.render(filename, view=False)
    
    print(f"Grafico salvato con successo: {output_path} (Formato PNG)")

if __name__ == "__main__":
    draw_xgboost_png()