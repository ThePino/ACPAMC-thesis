#!/bin/bash

# --- CONFIGURAZIONE ---
WIDTH_CM="14cm"
DPI=300
BG_COLOR="202020" # Grigio scuro per stile Native

FILES=("clean.cpp" "clean.s" "obs.cpp" "obs.s")

echo "--- Inizio generazione (Fix Sovrapposizione: Bera Mono) ---"

for FILE in "${FILES[@]}"; do
    if [ ! -f "$FILE" ]; then continue; fi

    FILENAME=$(basename -- "$FILE")
    NAME="${FILENAME%.*}"
    EXT="${FILENAME##*.}"
    OUT_NAME="${NAME}_${EXT}"

    rm -rf _minted-temp_wrap

    if [ "$EXT" == "s" ]; then LAN="gas"; else LAN="cpp"; fi

    echo -n "Processando $FILE... "

    cat <<EOF > temp_wrap.tex
\documentclass[varwidth=$WIDTH_CM, border=10pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% --- IL FIX È QUI ---
% 'beramono' è un font monospazio molto robusto che non si sovrappone mai.
% Se non hai beramono, usa {courier} al suo posto.
\usepackage{courier}

\usepackage{minted}
\usepackage{xcolor}

\definecolor{codebg}{HTML}{$BG_COLOR}

\setminted{
    style=native,
    bgcolor=codebg,
    fontsize=\small,
    breaklines=true,
    breakanywhere=false,
    tabsize=4,
    fontfamily=tt   % Questo userà Bera Mono
}

\begin{document}
\inputminted{$LAN}{$FILE}
\end{document}
EOF

    pdflatex -shell-escape -interaction=nonstopmode temp_wrap.tex > compilation.log 2>&1

    if [ -f "temp_wrap.pdf" ]; then
        inkscape --export-type="png" \
                 --export-dpi="$DPI" \
                 --export-filename="${OUT_NAME}.png" \
                 temp_wrap.pdf > /dev/null 2>&1
        echo "OK -> ${OUT_NAME}.png"
        rm temp_wrap.tex temp_wrap.pdf temp_wrap.log temp_wrap.aux compilation.log 2>/dev/null
    else
        echo "ERRORE"
        echo "Controlla se hai il pacchetto 'beramono' installato."
        tail -n 5 compilation.log
    fi
done

rm -rf _minted-temp_wrap