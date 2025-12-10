from graphviz import Digraph

def create_sandbox_diagram():
    dot = Digraph(comment='Sandbox Analysis', format='png')
    
    # --- Impostazioni Generali ---
    dot.attr(rankdir='LR', splines='ortho') # Layout da Sinistra a Destra, linee ortogonali
    dot.attr('node', fontname='Helvetica', fontsize='12', shape='plaintext')
    dot.attr('edge', color='#555555', penwidth='1.5')

    # ==========================
    # 1. NODO SANDBOX (Sinistra)
    # ==========================
    # Usiamo una tabella HTML per simulare il contenitore "Sandbox"
    # Nota: Le emoji funzionano se il sistema ha i font installati. 
    # Altrimenti vedrai dei rettangolini (in quel caso si usano forme standard).
    sandbox_html = '''<
    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="10">
        <TR><TD><B><FONT POINT-SIZE="14">Ambiente Sandbox</FONT></B></TD></TR>
        <TR>
            <TD BGCOLOR="#E6F2F8" BORDER="1" COLOR="#708090" STYLE="ROUNDED">
                <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
                    <TR>
                        <TD ALIGN="CENTER"><FONT POINT-SIZE="24">🔒</FONT></TD>
                    </TR>
                    <TR>
                        <TD ALIGN="CENTER">
                            <FONT POINT-SIZE="30" COLOR="RED">🦠</FONT> 
                            <FONT POINT-SIZE="20" COLOR="#555555">⚙️</FONT>
                        </TD>
                    </TR>
                    <TR><TD ALIGN="CENTER"><B>Malware</B></TD></TR>
                </TABLE>
            </TD>
        </TR>
        <TR><TD><FONT POINT-SIZE="10">Sandbox<BR/>(Ambiente Isolato)</FONT></TD></TR>
    </TABLE>
    >'''
    dot.node('sandbox', label=sandbox_html)

    # ==========================
    # 2. MONITORING SYSTEM (Centro)
    # ==========================
    monitor_html = '''<
    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
        <TR><TD><FONT POINT-SIZE="24">🖥️</FONT></TD></TR>
        <TR><TD>Monitoring<BR/>System</TD></TR>
    </TABLE>
    >'''
    dot.node('monitor', label=monitor_html)

    # ==========================
    # 3. LISTA CHIAMATE API (Destra)
    # ==========================
    # Replichiamo il testo rosso per le funzioni e nero per i parametri
    api_list_html = '''<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="8" BGCOLOR="#F9F9F9" COLOR="#CCCCCC" STYLE="ROUNDED">
        <TR>
            <TD BORDER="0" ALIGN="LEFT">
                <B><FONT POINT-SIZE="14" COLOR="#333333">Registrazione Chiamate API</FONT></B>
            </TD>
        </TR>
        <TR>
            <TD BORDER="0" ALIGN="LEFT">
                <FONT FACE="Courier New" POINT-SIZE="11">
                10:01:32 - <B><FONT COLOR="#B22222">CreateFile</FONT></B><BR/>
                (C:\\Windows\\System32\\malicious.dll)<BR/>
                <BR/>
                10:01:35 - <B><FONT COLOR="#B22222">RegSetValueEx</FONT></B><BR/>
                (HKCU\\Software\\Microsoft\\...\\Run)<BR/>
                <BR/>
                10:01:40 - <B><FONT COLOR="#B22222">InternetOpenUrl</FONT></B><BR/>
                (http://evil-server.com/data)<BR/>
                <BR/>
                10:01:45 - <B><FONT COLOR="#B22222">SocketConnect</FONT></B><BR/>
                (192.168.1.100:4444)
                </FONT>
            </TD>
        </TR>
    </TABLE>
    >'''
    dot.node('api_list', label=api_list_html)

    # ==========================
    # 4. DATABASE LOG (In basso a destra)
    # ==========================
    # Usiamo la forma standard 'cylinder' per il DB
    dot.node('db', label='Log\nComportamentale', shape='cylinder', 
             style='filled', fillcolor='#D3D3D3', height='0.8')

    # ==========================
    # COLLEGAMENTI
    # ==========================
    
    # Sandbox -> Monitor
    dot.edge('sandbox', 'monitor', constraint='true')
    
    # Monitor -> API List
    dot.edge('monitor', 'api_list', constraint='true')
    
    # API List -> DB
    # Usiamo rank='same' o un edge invisibile per posizionarlo sotto se necessario,
    # ma qui un collegamento diretto verso il basso funziona bene.
    dot.edge('api_list', 'db', xlabel='')

    # Render
    filename = 'sandbox_replication'
    dot.render(filename, view=False)
    print(f"Grafico salvato come {filename}.png")

if __name__ == "__main__":
    create_sandbox_diagram()