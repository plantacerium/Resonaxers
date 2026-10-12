import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QComboBox, QFrame, QScrollArea, QSplitter
)
from PySide6.QtCore import QTimer, Qt, QRectF, Property, QPropertyAnimation, QEasingCurve, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QFont, QPainterPath

# ══════════════════════════════════════════════════════════════════════════════
# DICCIONARIO BIOLÓGICO Y VIBRACIONAL
# ══════════════════════════════════════════════════════════════════════════════

# Cada aminoácido tiene centros de interacción atómicos reales (Centros alfa, cadenas R,
# grupos amino/carboxilo, puentes aromáticos o tiol, y sitios polares/hidrofóbicos).
RESONANCE_MAP = [
    {
        "seal": "1. Imix (Dragón)", "amino": "Glicina (Gly)", "bija": "LAM", "kototama": "U ➔ A", 
        "formula": "C2H5NO2", "group": "Apolar - Bisagra H",
        "instruction": "Estructura más simple y flexible. Tono bajo fundamental, ancla la bisagra peptídica.",
        "color": "#E74C3C", 
        "codons": [
            {"triplet": "GGU", "kototama": "GA-GA-U", "action": "Anclaje de raíz profunda"},
            {"triplet": "GGC", "kototama": "GA-GA-CHI", "action": "Fijación de bisagra elástica"},
            {"triplet": "GGA", "kototama": "GA-GA-A", "action": "Apertura torsional"},
            {"triplet": "GGG", "kototama": "GA-GA-GI", "action": "Compresión compacta"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.3, "size": 1.2},
            {"name": "Amino (N)", "r": 0.35, "angle": 0.8, "charge": 0.9, "size": 1.0},
            {"name": "Carboxilo (O=C)", "r": 0.45, "angle": 3.8, "charge": -0.8, "size": 1.3},
            {"name": "H-Radical", "r": 0.28, "angle": 2.2, "charge": 0.1, "size": 0.6}
        ]
    },
    {
        "seal": "2. Ik (Viento)", "amino": "Alanina (Ala)", "bija": "YAM", "kototama": "A ➔ E", 
        "formula": "C3H7NO2", "group": "Apolar - Metilo hidrofóbico (-CH3)",
        "instruction": "Glissando aéreo. La cadena alifática corta desvía la onda hacia el cuadrante hidrofóbico.",
        "color": "#3498DB", 
        "codons": [
            {"triplet": "GCU", "kototama": "GA-CHI-U", "action": "Viento ascendente suave"},
            {"triplet": "GCC", "kototama": "GA-CHI-CHI", "action": "Densificación de hélice alfa"},
            {"triplet": "GCA", "kototama": "GA-CHI-A", "action": "Expansión alifática"},
            {"triplet": "GCG", "kototama": "GA-CHI-GI", "action": "Estabilización hidrofóbica"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.1},
            {"name": "Amino (NH3+)", "r": 0.38, "angle": 0.9, "charge": 1.0, "size": 1.0},
            {"name": "Carboxilo (COO-)", "r": 0.42, "angle": 3.7, "charge": -1.0, "size": 1.2},
            {"name": "Metilo-CH3", "r": 0.65, "angle": 2.1, "charge": 0.0, "size": 1.4}
        ]
    },
    {
        "seal": "3. Akbal (Noche)", "amino": "Valina (Val)", "bija": "VAM", "kototama": "O ➔ U", 
        "formula": "C5H11NO2", "group": "Apolar Ramificado en V (Isopropilo)",
        "instruction": "Bifurcación en V asimétrica. Crea una amplia cuña de vacío apolar.",
        "color": "#34495E", 
        "codons": [
            {"triplet": "GUU", "kototama": "GA-U-U", "action": "Hundimiento en el vacío"},
            {"triplet": "GUC", "kototama": "GA-U-CHI", "action": "Cierre de bolsa apolar"},
            {"triplet": "GUA", "kototama": "GA-U-A", "action": "Apertura en V isométrica"},
            {"triplet": "GUG", "kototama": "GA-U-GI", "action": "Anclaje de núcleo interno"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.1},
            {"name": "Amino", "r": 0.35, "angle": 0.6, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.4, "angle": 3.5, "charge": -0.9, "size": 1.1},
            {"name": "C-Beta", "r": 0.48, "angle": 1.9, "charge": 0.0, "size": 1.0},
            {"name": "Metilo Gamma-1", "r": 0.78, "angle": 1.4, "charge": 0.0, "size": 1.3},
            {"name": "Metilo Gamma-2", "r": 0.78, "angle": 2.5, "charge": 0.0, "size": 1.3}
        ]
    },
    {
        "seal": "4. Kan (Semilla)", "amino": "Leucina (Leu)", "bija": "RAM", "kototama": "U ➔ I", 
        "formula": "C6H13NO2", "group": "Apolar Isobutílico (Cadena extendida)",
        "instruction": "Fuerte asimetría longitudinal. El extremo isobutilo genera un vórtice excéntrico.",
        "color": "#F1C40F", 
        "codons": [
            {"triplet": "UUA", "kototama": "U-U-A", "action": "Ignición germinal"},
            {"triplet": "UUG", "kototama": "U-U-GI", "action": "Fijación del brote"},
            {"triplet": "CUU", "kototama": "CHI-U-U", "action": "Impulso de tallo"},
            {"triplet": "CUC", "kototama": "CHI-U-CHI", "action": "Blindaje hidrofóbico"},
            {"triplet": "CUA", "kototama": "CHI-U-A", "action": "Flexión excéntrica"},
            {"triplet": "CUG", "kototama": "CHI-U-GI", "action": "Fuerza estructural mayor"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.32, "angle": 0.7, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.36, "angle": 3.4, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta", "r": 0.45, "angle": 1.8, "charge": 0.0, "size": 0.9},
            {"name": "C-Gamma", "r": 0.65, "angle": 1.9, "charge": 0.0, "size": 1.1},
            {"name": "Delta-1", "r": 0.85, "angle": 1.4, "charge": 0.0, "size": 1.3},
            {"name": "Delta-2", "r": 0.88, "angle": 2.4, "charge": 0.0, "size": 1.3}
        ]
    },
    {
        "seal": "5. Chicchan (Serpiente)", "amino": "Isoleucina (Ile)", "bija": "VAM", "kototama": "A ➔ O ➔ U", 
        "formula": "C6H13NO2", "group": "Apolar Quiral (Sec-butilo asimétrico)",
        "instruction": "Quiralidad dual en C-beta. La onda se tuerce en espiral disimétrica.",
        "color": "#E67E22", 
        "codons": [
            {"triplet": "AUU", "kototama": "A-U-U", "action": "Despertar kundalínico"},
            {"triplet": "AUC", "kototama": "A-U-CHI", "action": "Onda sinusoidal espinal"},
            {"triplet": "AUA", "kototama": "A-U-A", "action": "Expansión en vórtice quiral"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.32, "angle": 0.8, "charge": 0.9, "size": 0.9},
            {"name": "Carboxilo", "r": 0.36, "angle": 3.6, "charge": -0.9, "size": 1.1},
            {"name": "C-Beta Quiral", "r": 0.46, "angle": 2.0, "charge": 0.1, "size": 1.1},
            {"name": "Metilo Gamma", "r": 0.68, "angle": 1.2, "charge": 0.0, "size": 1.2},
            {"name": "Etilo Delta", "r": 0.86, "angle": 2.6, "charge": 0.0, "size": 1.4}
        ]
    },
    {
        "seal": "6. Cimi (Muerte)", "amino": "Prolina (Pro)", "bija": "HUM", "kototama": "Shunyata (Silencio)", 
        "formula": "C5H9NO2", "group": "Iminoácido Cíclico Rígido (Anillo Pirrolidina)",
        "instruction": "Anillo cerrado y rígido. Bloquea la propagación en un sector formando un nudo cerrado.",
        "color": "#ECF0F1", 
        "codons": [
            {"triplet": "CCU", "kototama": "CHI-CHI-U", "action": "Contracción pirrolidínica"},
            {"triplet": "CCC", "kototama": "CHI-CHI-CHI", "action": "Ruptura de hélice (Kink)"},
            {"triplet": "CCA", "kototama": "CHI-CHI-A", "action": "Giro forzado de 90 grados"},
            {"triplet": "CCG", "kototama": "CHI-CHI-GI", "action": "Cierre hermético del ciclo"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.1, "size": 1.0},
            {"name": "Anillo N-Imid", "r": 0.4, "angle": 0.4, "charge": 0.6, "size": 1.2},
            {"name": "Carboxilo", "r": 0.38, "angle": 3.2, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta Anillo", "r": 0.52, "angle": 1.4, "charge": 0.0, "size": 1.1},
            {"name": "C-Gamma Anillo", "r": 0.62, "angle": 0.8, "charge": 0.0, "size": 1.1},
            {"name": "C-Delta Anillo", "r": 0.48, "angle": 0.1, "charge": 0.1, "size": 1.1}
        ]
    },
    {
        "seal": "7. Manik (Mano)", "amino": "Fenilalanina (Phe)", "bija": "YAM", "kototama": "E ➔ I", 
        "formula": "C9H11NO2", "group": "Aromático - Anillo Bencénico Resonante",
        "instruction": "Gran anillo aromático pi-resonante. Nube deslocalizada densa que capta la vibración.",
        "color": "#1ABC9C", 
        "codons": [
            {"triplet": "UUU", "kototama": "U-U-U", "action": "Resonancia orbital pi pura"},
            {"triplet": "UUC", "kototama": "U-U-CHI", "action": "Condensación aromática"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.3, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.35, "angle": 3.8, "charge": -0.9, "size": 1.0},
            {"name": "C-Beta", "r": 0.42, "angle": 2.2, "charge": 0.0, "size": 0.9},
            {"name": "Anillo C1", "r": 0.62, "angle": 2.1, "charge": 0.0, "size": 1.3},
            {"name": "Anillo C2/C3", "r": 0.78, "angle": 1.8, "charge": 0.0, "size": 1.3},
            {"name": "Anillo C4/C5", "r": 0.88, "angle": 2.2, "charge": 0.0, "size": 1.4},
            {"name": "Anillo C6", "r": 0.78, "angle": 2.6, "charge": 0.0, "size": 1.3}
        ]
    },
    {
        "seal": "8. Lamat (Estrella)", "amino": "Tirosina (Tyr)", "bija": "OM", "kototama": "I ➔ A", 
        "formula": "C9H11NO3", "group": "Aromático Polar (Fenol -OH activo)",
        "instruction": "Anillo fenilo con extremo -OH donador de hidrógeno. Dipolo electromagnético extremo.",
        "color": "#F39C12", 
        "codons": [
            {"triplet": "UAU", "kototama": "U-A-U", "action": "Puente fotónico de hidrógeno"},
            {"triplet": "UAC", "kototama": "U-A-CHI", "action": "Activación fosforilante"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.28, "angle": 0.7, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.32, "angle": 3.6, "charge": -0.8, "size": 1.0},
            {"name": "Anillo Fenilo", "r": 0.65, "angle": 2.0, "charge": 0.0, "size": 1.5},
            {"name": "Sitio Activo -OH", "r": 0.92, "angle": 2.0, "charge": 0.9, "size": 1.6}
        ]
    },
    {
        "seal": "9. Muluc (Luna)", "amino": "Serina (Ser)", "bija": "VAM", "kototama": "O ➔ A ➔ O", 
        "formula": "C3H7NO3", "group": "Polar Hidrófilo (Grupo Hidroxilo -OH)",
        "instruction": "Sitio reactivo nucleofílico. La onda entra en resonancia hidrofílica intensa con el agua.",
        "color": "#9B59B6", 
        "codons": [
            {"triplet": "UCU", "kototama": "U-CHI-U", "action": "Fluidez del agua primordial"},
            {"triplet": "UCC", "kototama": "U-CHI-CHI", "action": "Alineación de puente hídrico"},
            {"triplet": "UCA", "kototama": "U-CHI-A", "action": "Deslizamiento catalítico"},
            {"triplet": "UCG", "kototama": "U-CHI-GI", "action": "Centro de corte enzimático"},
            {"triplet": "AGU", "kototama": "A-GA-U", "action": "Marea celular expansiva"},
            {"triplet": "AGC", "kototama": "A-GA-CHI", "action": "Condensación de rocío"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.35, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.38, "angle": 3.6, "charge": -0.9, "size": 1.1},
            {"name": "C-Beta", "r": 0.45, "angle": 2.1, "charge": 0.2, "size": 1.0},
            {"name": "Hidroxilo -OH (Foco)", "r": 0.75, "angle": 2.2, "charge": 0.9, "size": 1.6}
        ]
    },
    {
        "seal": "10. Oc (Perro)", "amino": "Treonina (Thr)", "bija": "YAM", "kototama": "A ➔ E ➔ I", 
        "formula": "C4H9NO3", "group": "Polar Quiral Mixto (-OH / -CH3)",
        "instruction": "Dipolo asimétrico: un polo hidrófilo reactivo y un polo hidrofóbico metílico.",
        "color": "#FF69B4", 
        "codons": [
            {"triplet": "ACU", "kototama": "A-CHI-U", "action": "Afinidad de fidelidad"},
            {"triplet": "ACC", "kototama": "A-CHI-CHI", "action": "Acoplamiento de glucosilación"},
            {"triplet": "ACA", "kototama": "A-CHI-A", "action": "Resonancia cálida del pecho"},
            {"triplet": "ACG", "kototama": "A-CHI-GI", "action": "Firmeza en el enlace"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.32, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.36, "angle": 3.5, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta Quiral", "r": 0.48, "angle": 2.0, "charge": 0.2, "size": 1.0},
            {"name": "Sitio -OH (Polar)", "r": 0.76, "angle": 1.4, "charge": 0.9, "size": 1.5},
            {"name": "Metilo -CH3 (Apolar)", "r": 0.78, "angle": 2.7, "charge": 0.0, "size": 1.2}
        ]
    },
    {
        "seal": "11. Chuen (Mono)", "amino": "Cisteína (Cys)", "bija": "RAM", "kototama": "U ➔ O ➔ E", 
        "formula": "C3H7NO2S", "group": "Tiol Reactivo (-SH, Puentes Disulfuro)",
        "instruction": "Átomo de Azufre masivo. Capaz de crear enlaces covalentes que deforman la estructura global.",
        "color": "#8E44AD", 
        "codons": [
            {"triplet": "UGU", "kototama": "U-GA-U", "action": "Enlace disulfuro S-S puente"},
            {"triplet": "UGC", "kototama": "U-GA-CHI", "action": "Anclaje de plegamiento terciario"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.33, "angle": 0.7, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.35, "angle": 3.7, "charge": -0.9, "size": 1.0},
            {"name": "C-Beta", "r": 0.46, "angle": 2.1, "charge": 0.1, "size": 0.9},
            {"name": "Azufre Tiol (-SH)", "r": 0.82, "angle": 2.2, "charge": 1.1, "size": 1.8}
        ]
    },
    {
        "seal": "12. Eb (Humano)", "amino": "Metionina (Met)", "bija": "LAM", "kototama": "U ➔ A ➔ I", 
        "formula": "C5H11NO2S", "group": "Codón de Inicio Universal (AUG) - Tioéter",
        "instruction": "El origen de toda síntesis proteica. Cadena hidrofóbica con azufre no polar que abre el código.",
        "color": "#D35400", 
        "codons": [
            {"triplet": "AUG", "kototama": "A-U-GI", "action": "INICIO UNIVERSAL: Génesis del ribosoma"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.3, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.33, "angle": 3.5, "charge": -0.8, "size": 1.0},
            {"name": "Cadena C-C", "r": 0.52, "angle": 1.9, "charge": 0.0, "size": 1.0},
            {"name": "Azufre Tioéter (-S-)", "r": 0.74, "angle": 2.0, "charge": 0.4, "size": 1.5},
            {"name": "Metilo Terminal", "r": 0.9, "angle": 2.3, "charge": 0.0, "size": 1.2}
        ]
    },
    {
        "seal": "13. Ben (Caminante)", "amino": "Asparagina (Asn)", "bija": "YAM", "kototama": "A ➔ U ➔ O", 
        "formula": "C4H8N2O3", "group": "Polar Neutro - Grupo Amida (-CONH2)",
        "instruction": "Doble polo aceptor y donador de puentes H. Ondas de interferencia cruzada intensa.",
        "color": "#C0392B", 
        "codons": [
            {"triplet": "AAU", "kototama": "A-A-U", "action": "Transmisión de columna vertical"},
            {"triplet": "AAC", "kototama": "A-A-CHI", "action": "N-glicosilación membranosa"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.32, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.35, "angle": 3.6, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta", "r": 0.48, "angle": 2.0, "charge": 0.1, "size": 0.9},
            {"name": "Amida Carbonilo (O=)", "r": 0.78, "angle": 1.6, "charge": -0.8, "size": 1.4},
            {"name": "Amida Amino (-NH2)", "r": 0.82, "angle": 2.5, "charge": 0.8, "size": 1.4}
        ]
    },
    {
        "seal": "14. Ix (Mago)", "amino": "Glutamina (Gln)", "bija": "AUM", "kototama": "I ➔ O ➔ E", 
        "formula": "C5H10N2O3", "group": "Polar Amida Extendida",
        "instruction": "Cadena amida flexible de largo alcance. Forma puentes de agua de largo radio.",
        "color": "#7D3C98", 
        "codons": [
            {"triplet": "CAA", "kototama": "CHI-A-A", "action": "Intercambio amínico sutil"},
            {"triplet": "CAG", "kototama": "CHI-A-GI", "action": "Expansión en red de nitrógeno"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.3, "angle": 0.7, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.32, "angle": 3.7, "charge": -0.8, "size": 1.0},
            {"name": "Tallo Alifático", "r": 0.58, "angle": 2.0, "charge": 0.0, "size": 1.1},
            {"name": "Amida Terminal O=", "r": 0.86, "angle": 1.7, "charge": -0.9, "size": 1.5},
            {"name": "Amida Terminal NH2", "r": 0.88, "angle": 2.4, "charge": 0.9, "size": 1.5}
        ]
    },
    {
        "seal": "15. Men (Águila)", "amino": "Lisina (Lys)", "bija": "HAM", "kototama": "E ➔ A ➔ I", 
        "formula": "C6H14N2O2", "group": "Básico - Carga Positiva Neta (+1)",
        "instruction": "Brazo catiónico flexible muy largo (+NH3). Emite un campo electrostático atrayente potente.",
        "color": "#2980B9", 
        "codons": [
            {"triplet": "AAA", "kototama": "A-A-A", "action": "Apertura catiónica pura"},
            {"triplet": "AAG", "kototama": "A-A-GI", "action": "Atracción con el esqueleto fosfato de ADN"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.28, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.32, "angle": 3.8, "charge": -0.9, "size": 1.0},
            {"name": "Tallo 4xCH2", "r": 0.6, "angle": 2.1, "charge": 0.0, "size": 1.2},
            {"name": "Epsilon-NH3+ (Catión)", "r": 0.92, "angle": 2.2, "charge": 1.4, "size": 1.8}
        ]
    },
    {
        "seal": "16. Cib (Guerrero)", "amino": "Arginina (Arg)", "bija": "RAM", "kototama": "U ➔ O ➔ U", 
        "formula": "C6H14N4O2", "group": "Básico Fuertemente Catiónico (Guanidinio)",
        "instruction": "Grupo guanidinio con 3 nitrógenos resonantes en estrella plana. Trípode de carga positiva.",
        "color": "#D68910", 
        "codons": [
            {"triplet": "CGU", "kototama": "CHI-GA-U", "action": "Trípode guanidínico firme"},
            {"triplet": "CGC", "kototama": "CHI-GA-CHI", "action": "Enlace salino bidentado con ADN"},
            {"triplet": "CGA", "kototama": "CHI-GA-A", "action": "Dispersión de carga resonante"},
            {"triplet": "CGG", "kototama": "CHI-GA-GI", "action": "Fijación a surco mayor del ADN"},
            {"triplet": "AGA", "kototama": "A-GA-A", "action": "Pulso electrostático amplio"},
            {"triplet": "AGG", "kototama": "A-GA-GI", "action": "Blindaje catiónico denso"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.28, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.3, "angle": 3.6, "charge": -0.9, "size": 1.0},
            {"name": "Tallo Alifático", "r": 0.52, "angle": 2.0, "charge": 0.0, "size": 1.0},
            {"name": "Guanidinio Centro", "r": 0.78, "angle": 2.1, "charge": 1.2, "size": 1.5},
            {"name": "Nitrógeno N1", "r": 0.92, "angle": 1.6, "charge": 0.8, "size": 1.3},
            {"name": "Nitrógeno N2", "r": 0.95, "angle": 2.2, "charge": 0.8, "size": 1.3},
            {"name": "Nitrógeno N3", "r": 0.91, "angle": 2.8, "charge": 0.8, "size": 1.3}
        ]
    },
    {
        "seal": "17. Caban (Tierra)", "amino": "Histidina (His)", "bija": "LAM", "kototama": "A ➔ O ➔ A", 
        "formula": "C6H9N3O2", "group": "Anillo Imidazol Aromático (Interruptor de pH)",
        "instruction": "Anillo imidazol con dos nitrógenos en resonancia. Conmuta entre neutro y catiónico.",
        "color": "#7E5109", 
        "codons": [
            {"triplet": "CAU", "kototama": "CHI-A-U", "action": "Conmutación protónica lenta"},
            {"triplet": "CAC", "kototama": "CHI-A-CHI", "action": "Transferencia de carga catalítica"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.3, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.32, "angle": 3.7, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta", "r": 0.48, "angle": 2.1, "charge": 0.1, "size": 0.9},
            {"name": "Imidazol N-Delta", "r": 0.75, "angle": 1.7, "charge": 0.9, "size": 1.5},
            {"name": "Imidazol C-Epsilon", "r": 0.88, "angle": 2.1, "charge": 0.0, "size": 1.2},
            {"name": "Imidazol N-Epsilon", "r": 0.76, "angle": 2.5, "charge": 0.9, "size": 1.5}
        ]
    },
    {
        "seal": "18. Etznab (Espejo)", "amino": "Aspartato (Asp)", "bija": "HUM", "kototama": "I ➔ E ➔ I", 
        "formula": "C4H7NO4", "group": "Ácido - Carga Negativa Neta (-1)",
        "instruction": "Centro aniónico denso. Polaridad invertida que repele la onda creando un vacío oscuro.",
        "color": "#BDC3C7", 
        "codons": [
            {"triplet": "GAU", "kototama": "GA-A-U", "action": "Vacío aniónico atractor"},
            {"triplet": "GAC", "kototama": "GA-A-CHI", "action": "Bolsa de coordinación para Mg2+"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.32, "angle": 0.9, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo Alfa", "r": 0.35, "angle": 3.7, "charge": -0.9, "size": 1.0},
            {"name": "C-Beta", "r": 0.45, "angle": 2.1, "charge": 0.0, "size": 0.9},
            {"name": "Carboxilato O1 (-)", "r": 0.76, "angle": 1.6, "charge": -1.3, "size": 1.6},
            {"name": "Carboxilato O2 (-)", "r": 0.78, "angle": 2.6, "charge": -1.3, "size": 1.6}
        ]
    },
    {
        "seal": "19. Cauac (Tormenta)", "amino": "Glutamato (Glu)", "bija": "OM", "kototama": "U ➔ A ➔ O ➔ E ➔ I", 
        "formula": "C5H9NO4", "group": "Ácido Aniónico de Cadena Larga (Excitador)",
        "instruction": "Principal neurotransmisor excitatorio del cerebro humano. Alta reactividad y dispersión de carga.",
        "color": "#5D6D7E", 
        "codons": [
            {"triplet": "GAA", "kototama": "GA-A-A", "action": "Descarga sináptica despolarizante"},
            {"triplet": "GAG", "kototama": "GA-A-GI", "action": "Onda excitatoria masiva en red"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.3, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.33, "angle": 3.6, "charge": -0.9, "size": 1.0},
            {"name": "C-Beta/Gamma", "r": 0.55, "angle": 2.0, "charge": 0.0, "size": 1.0},
            {"name": "Carboxilato O1 (-)", "r": 0.86, "angle": 1.5, "charge": -1.4, "size": 1.7},
            {"name": "Carboxilato O2 (-)", "r": 0.88, "angle": 2.5, "charge": -1.4, "size": 1.7}
        ]
    },
    {
        "seal": "20. Ahau (Sol)", "amino": "Triptófano (Trp)", "bija": "AUM", "kototama": "I ➔ A ➔ O ➔ U ➔ E", 
        "formula": "C11H12N2O2", "group": "Aromático Mayor - Sistema Indol Bicíclico",
        "instruction": "El aminoácido más grande y complejo. Doble anillo aromático indol con nitrógeno electroactivo.",
        "color": "#F1C40F", 
        "codons": [
            {"triplet": "UGG", "kototama": "U-GI-GI", "action": "CORONA SOLAR: Síntesis de Serotonina y Melatonina"}
        ],
        "nodes": [
            {"name": "C-Alfa", "r": 0.0, "angle": 0.0, "charge": 0.2, "size": 1.0},
            {"name": "Amino", "r": 0.26, "angle": 0.8, "charge": 0.8, "size": 0.9},
            {"name": "Carboxilo", "r": 0.3, "angle": 3.8, "charge": -0.8, "size": 1.0},
            {"name": "C-Beta", "r": 0.42, "angle": 2.1, "charge": 0.0, "size": 0.9},
            {"name": "Anillo Pirrol N-H", "r": 0.65, "angle": 1.8, "charge": 0.9, "size": 1.5},
            {"name": "Anillo Indol C-C", "r": 0.72, "angle": 2.4, "charge": 0.0, "size": 1.4},
            {"name": "Anillo Benceno C1-C3", "r": 0.92, "angle": 1.8, "charge": 0.0, "size": 1.6},
            {"name": "Anillo Benceno C4-C6", "r": 0.94, "angle": 2.6, "charge": 0.0, "size": 1.6}
        ]
    },
    {
        "seal": "0. MA (Silencio Primordial)", "amino": "Codones STOP (UAA, UAG, UGA)", "bija": "SHUNYATA", "kototama": "M ➔ A ➔ [SILENCIO]", 
        "formula": "Término Peptídico", "group": "Los Tres Grandes Silencios del Código Genético",
        "instruction": "Factores de liberación RF1/RF2 entran al ribosoma. El agua cesa de vibrar y asimila la forma.",
        "color": "#FFFFFF", 
        "codons": [
            {"triplet": "UAA (Ocre)", "kototama": "U-A-A [MA]", "action": "Detención absoluta de la síntesis"},
            {"triplet": "UAG (Ámbar)", "kototama": "U-A-GI [MA]", "action": "Liberación de la cadena peptídica"},
            {"triplet": "UGA (Ópalo)", "kototama": "U-GI-A [MA]", "action": "Integración en el vacío cuántico"}
        ],
        "nodes": [
            {"name": "Ribosoma A-Site", "r": 0.0, "angle": 0.0, "charge": 0.0, "size": 1.5},
            {"name": "Factor RF1", "r": 0.5, "angle": 1.57, "charge": 0.0, "size": 1.2},
            {"name": "Factor RF2", "r": 0.5, "angle": 3.14, "charge": 0.0, "size": 1.2},
            {"name": "Término UGA", "r": 0.5, "angle": 4.71, "charge": 0.0, "size": 1.2}
        ]
    }
]


# ══════════════════════════════════════════════════════════════════════════════
# WIDGET CIMÁTICO (VISUALIZADOR DE ONDAS EN EL AGUA)
# ══════════════════════════════════════════════════════════════════════════════

class CymaticVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(420, 420)
        self.phase = 0.0
        self.breath_scale = 1.0
        self.stage = 1
        self.render_mode = "Cimática Acuática"  # or "Densidad Cuántica / Orbital"
        self.base_color = QColor("#3498DB")
        self.amino_data = None
        
        # Timer for animation (60 fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def set_amino_data(self, data):
        self.amino_data = data
        self.base_color = QColor(data['color'])
        self.stage = 1
        self.update()

    def set_stage(self, stage):
        self.stage = stage
        self.update()

    def set_render_mode(self, mode):
        self.render_mode = mode
        self.update()

    def update_animation(self):
        speed = 0.025 + 0.012 * self.stage
        self.phase += speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        max_radius = min(w, h) / 2.25
        
        # Fondo acuoso oscuro
        bg_grad = QRadialGradient(cx, cy, max_radius * 1.5)
        bg_grad.setColorAt(0, QColor(4, 7, 12))
        bg_grad.setColorAt(1, QColor(0, 0, 0))
        painter.fillRect(0, 0, w, h, bg_grad)

        if not self.amino_data:
            return

        nodes = self.amino_data.get("nodes", [])

        painter.save()
        painter.translate(cx, cy)

        # ══════════════════════════════════════════════════════════════════════
        # ══════════════════════════════════════════════════════════════════════
        # MODO 1: ELECTRODINÁMICA CUÁNTICO-ACUÁTICA (SUPERFLUIDO / ONDA PILOTO DE BROGLIE-BOHM)
        # ══════════════════════════════════════════════════════════════════════
        if self.render_mode == "Densidad Cuántica / Orbital":
            # 1. FLUCTUACIÓN DEL VACÍO CUÁNTICO DE FONDO (Espuma cuántica y superfluido)
            vacuum_radius = max_radius * 1.05 * self.breath_scale
            vacuum_grad = QRadialGradient(0, 0, vacuum_radius)
            c_vac_core = QColor(142, 68, 173, 22)
            c_vac_edge = QColor(5, 7, 15, 0)
            vacuum_grad.setColorAt(0.0, c_vac_core)
            vacuum_grad.setColorAt(0.65, QColor(41, 128, 185, 12))
            vacuum_grad.setColorAt(1.0, c_vac_edge)
            painter.setBrush(QBrush(vacuum_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(0, 0), vacuum_radius, vacuum_radius)

            # 2. FILAMENTOS DE ENTANGLEMENT / TÚNEL CUÁNTICO ENTRE POLOS
            # Hilos de coherencia cuántica que unen los pares de centros activos (oscilación calmada)
            if len(nodes) > 1:
                for i in range(len(nodes)):
                    for j in range(i + 1, len(nodes)):
                        n1 = nodes[i]
                        n2 = nodes[j]
                        p1_x = n1["r"] * max_radius * 0.85 * math.cos(n1["angle"]) * self.breath_scale
                        p1_y = n1["r"] * max_radius * 0.85 * math.sin(n1["angle"]) * self.breath_scale
                        p2_x = n2["r"] * max_radius * 0.85 * math.cos(n2["angle"]) * self.breath_scale
                        p2_y = n2["r"] * max_radius * 0.85 * math.sin(n2["angle"]) * self.breath_scale
                        
                        dist_ij = math.sqrt((p1_x - p2_x)**2 + (p1_y - p2_y)**2)
                        if dist_ij < max_radius * 0.95:
                            flux_path = QPainterPath()
                            flux_path.moveTo(p1_x, p1_y)
                            
                            sub_divs = 20
                            for div in range(1, sub_divs):
                                t = div / sub_divs
                                base_fx = p1_x + (p2_x - p1_x) * t
                                base_fy = p1_y + (p2_y - p1_y) * t
                                
                                normal_x = -(p2_y - p1_y) / (dist_ij + 0.001)
                                normal_y = (p2_x - p1_x) / (dist_ij + 0.001)
                                # Oscilación lenta y armónica
                                wave_osc = math.sin(t * 8.0 - self.phase * 1.5 + i) * (3.8 * self.stage)
                                
                                flux_path.lineTo(base_fx + normal_x * wave_osc, base_fy + normal_y * wave_osc)
                            
                            flux_path.lineTo(p2_x, p2_y)
                            
                            flux_alpha = int(75 * (1.0 - dist_ij / (max_radius * 0.95)))
                            c_flux = QColor(175, 120, 220, flux_alpha)
                            pen_flux = QPen(c_flux, 1.0)
                            pen_flux.setStyle(Qt.DotLine if self.stage == 1 else Qt.SolidLine)
                            painter.setPen(pen_flux)
                            painter.setBrush(Qt.NoBrush)
                            painter.drawPath(flux_path)

            # 3. FUSIÓN ACUÁTICO-CUÁNTICA: LA ONDA PILOTO (DE BROGLIE-BOHM)
            # Cada centro atómico proyecta ondas de interferencia acuática en el superfluido cuántico
            k_quantum_wave = 9.0 + 2.5 * self.stage
            ripple_steps = 90
            num_q_waves = 11

            for idx, node in enumerate(nodes):
                nr = node["r"] * max_radius * 0.85 * self.breath_scale
                na = node["angle"]
                nx = nr * math.cos(na)
                ny = nr * math.sin(na)
                sz = node.get("size", 1.0)
                ch = node.get("charge", 0.0)

                # Tinte cuántico-acuático luminoso
                if ch > 0.4:
                    wave_base = QColor(0, 210, 255)
                elif ch < -0.4:
                    wave_base = QColor(255, 65, 115)
                elif abs(ch) < 0.1 and idx > 0:
                    wave_base = QColor(255, 215, 60)
                else:
                    wave_base = QColor(170, 110, 245)

                for w_idx in range(1, num_q_waves + 1):
                    w_norm = w_idx / num_q_waves
                    r_travel = max_radius * 0.52 * sz * w_norm * self.breath_scale
                    path_pilot = QPainterPath()

                    for step in range(ripple_steps + 1):
                        theta = (step / ripple_steps) * 2 * math.pi
                        dx = math.cos(theta)
                        dy = math.sin(theta)

                        cur_x = nx + r_travel * dx
                        cur_y = ny + r_travel * dy

                        # Interferencia cuántico-acuática de Huygens-Fresnel con los demás centros
                        interference = 0.0
                        for o_idx, o_node in enumerate(nodes):
                            if o_idx == idx:
                                continue
                            onr = o_node["r"] * max_radius * 0.85 * self.breath_scale
                            ona = o_node["angle"]
                            onx = onr * math.cos(ona)
                            ony = onr * math.sin(ona)
                            dist_to_other = math.sqrt((cur_x - onx)**2 + (cur_y - ony)**2)
                            
                            other_wave = math.cos(k_quantum_wave * (dist_to_other / max_radius) - self.phase * 1.8 + o_idx)
                            influence = math.exp(-dist_to_other / (max_radius * 0.36))
                            interference += influence * other_wave * 0.15

                        # Modulación de onda acuática fluida en el espacio cuántico
                        w_deform = math.sin(k_quantum_wave * w_norm - self.phase * 1.8 + idx) * (0.04 * self.stage)
                        r_final = r_travel + max_radius * (w_deform + interference)

                        px = nx + r_final * dx
                        py = ny + r_final * dy

                        if step == 0:
                            path_pilot.moveTo(px, py)
                        else:
                            path_pilot.lineTo(px, py)

                    # Líneas de interferencia con resplandor fluido etéreo
                    alpha_pilot = int(115 * (1.0 - w_norm * 0.65))
                    c_pilot = QColor(wave_base)
                    c_pilot.setAlpha(max(10, min(180, alpha_pilot)))
                    painter.setPen(QPen(c_pilot, 0.9 if w_idx > 3 else 1.2))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawPath(path_pilot)

            # 4. NUBES ORBITALES MULTI-CAPA CON COLORES ESPECTRALES BRILLANTES
            for idx, node in enumerate(nodes):
                nr = node["r"] * max_radius * 0.85 * self.breath_scale
                na = node["angle"]
                nx = nr * math.cos(na)
                ny = nr * math.sin(na)
                ch = node.get("charge", 0.0)
                sz = node.get("size", 1.0)

                # Pulsación calmada y armónica (interferencia cuántica fluida)
                quantum_pulse = 1.0 + 0.18 * math.sin(self.phase * 1.6 + idx * 1.5)
                r_cloud = max_radius * 0.44 * sz * quantum_pulse

                # Paleta espectral de emisión atómica
                if ch > 0.4:
                    neon_core = QColor(0, 210, 255)       # Cian / Catiónico puro (+NH3)
                    neon_outer = QColor(41, 128, 185)
                elif ch < -0.4:
                    neon_core = QColor(255, 46, 99)       # Carmesí Neón / Aniónico (COO-)
                    neon_outer = QColor(192, 57, 43)
                elif abs(ch) < 0.1 and idx > 0:
                    neon_core = QColor(255, 215, 0)       # Oro Cuántico / Apolar hidrofóbico
                    neon_outer = QColor(214, 137, 16)
                else:
                    neon_core = QColor(168, 85, 247)      # Violeta profundo central (C-Alfa)
                    neon_outer = QColor(126, 34, 206)

                # Nube radial hiper-suave con triple parada de degradado
                grad_q = QRadialGradient(nx, ny, r_cloud)
                c_c0 = QColor(neon_core)
                c_c0.setAlpha(150 + 20 * self.stage)
                c_c1 = QColor(neon_outer)
                c_c1.setAlpha(60 + 15 * self.stage)
                grad_q.setColorAt(0.0, c_c0)
                grad_q.setColorAt(0.35, c_c1)
                grad_q.setColorAt(0.8, QColor(neon_outer.red(), neon_outer.green(), neon_outer.blue(), 12))
                grad_q.setColorAt(1.0, QColor(0, 0, 0, 0))

                painter.setBrush(QBrush(grad_q))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(nx, ny), r_cloud, r_cloud)

            # 5. FUNCIÓN DE ONDA Y ARMONÍAS DE SCHRÖDINGER (ISOLÍNEAS VIVAS)
            iso_steps = 100
            for idx, node in enumerate(nodes):
                nr = node["r"] * max_radius * 0.85 * self.breath_scale
                na = node["angle"]
                nx = nr * math.cos(na)
                ny = nr * math.sin(na)
                sz = node.get("size", 1.0)
                ch = node.get("charge", 0.0)

                if ch > 0.4:
                    c_line_base = QColor(0, 240, 255)
                elif ch < -0.4:
                    c_line_base = QColor(255, 80, 120)
                elif abs(ch) < 0.1 and idx > 0:
                    c_line_base = QColor(255, 220, 50)
                else:
                    c_line_base = QColor(200, 140, 255)

                num_shells = 8
                for s_idx in range(1, num_shells + 1):
                    s_norm = s_idx / num_shells
                    r_shell_base = max_radius * 0.32 * sz * s_norm * self.breath_scale
                    path_shell = QPainterPath()

                    for step in range(iso_steps + 1):
                        theta = (step / iso_steps) * 2 * math.pi
                        dx = math.cos(theta)
                        dy = math.sin(theta)

                        field_gradient = 0.0
                        for other_idx, other in enumerate(nodes):
                            if other_idx == idx:
                                continue
                            onr = other["r"] * max_radius * 0.85 * self.breath_scale
                            ona = other["angle"]
                            onx = onr * math.cos(ona)
                            ony = onr * math.sin(ona)
                            d_other = math.sqrt((nx + r_shell_base * dx - onx)**2 + (ny + r_shell_base * dy - ony)**2)
                            field_gradient += math.exp(-d_other / (max_radius * 0.28)) * 0.25

                        m_mode = 2 if abs(ch) > 0.3 else 3
                        angular_harm = math.cos(m_mode * theta + self.phase * 1.5 + idx) * (0.06 * self.stage)
                        r_shell = r_shell_base * (1.0 + field_gradient + angular_harm)

                        px = nx + r_shell * dx
                        py = ny + r_shell * dy

                        if step == 0:
                            path_shell.moveTo(px, py)
                        else:
                            path_shell.lineTo(px, py)

                    alpha_shell = int(160 * (1.0 - s_norm * 0.65))
                    c_line = QColor(c_line_base)
                    c_line.setAlpha(alpha_shell)
                    
                    pen_w = 1.2 if s_idx in (2, 4, 7) else 0.75
                    painter.setPen(QPen(c_line, pen_w))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawPath(path_shell)

            # 6. COLAPSO DE LA FUNCIÓN DE ONDA Y SALTO CUÁNTICO NO-LOCAL (RALENTIZADO Y ETÉREO)
            # Las partículas cuánticas NO parpadean rápido ni siguen órbitas clásicas continuas.
            # Se materializan suavemente en una posición probabilística, sostienen su presencia etérea
            # durante varios segundos, y se desvanecen en el vacío para reaparecer de forma no-local en otra área.
            num_quanta = 28
            for q in range(num_quanta):
                # Ciclo temporal ralentizado: dura entre 2.5 y 4 segundos por colapso
                quantum_time = self.phase * 0.55 + q * 0.28
                quantum_tick = math.floor(quantum_time)
                cycle_progress = quantum_time - quantum_tick  # de 0.0 a 1.0 continuamente

                # Curva suave de respiración y presencia cuántica (campana suave sin parpadeo)
                life_intensity = math.sin(cycle_progress * math.pi)
                alpha_spark = int((life_intensity ** 1.6) * 235)

                if alpha_spark > 12:
                    # Nodo padre elegido determinísticamente según el estado cuántico actual
                    node_idx = (quantum_tick * 3 + q * 7) % len(nodes)
                    p_node = nodes[node_idx]
                    pnx = p_node["r"] * max_radius * 0.85 * math.cos(p_node["angle"]) * self.breath_scale
                    pny = p_node["r"] * max_radius * 0.85 * math.sin(p_node["angle"]) * self.breath_scale

                    # Distribución de probabilidad de Born (|Psi|^2 cuadrática)
                    seed_u1 = ((q * 43 + quantum_tick * 19) % 100) / 100.0
                    seed_u2 = ((q * 89 + quantum_tick * 37) % 100) / 100.0

                    r_prob = max_radius * (0.04 + 0.32 * math.sqrt(seed_u1)) * p_node.get("size", 1.0)
                    theta_prob = seed_u2 * 2.0 * math.pi

                    # Leve flotación cuántica subatómica durante su vida útil (sin saltar a lo loco)
                    drift_x = math.sin(cycle_progress * math.pi) * 2.2
                    drift_y = math.cos(cycle_progress * math.pi) * 1.8

                    qx = pnx + r_prob * math.cos(theta_prob) + drift_x
                    qy = pny + r_prob * math.sin(theta_prob) + drift_y

                    # Color espectral
                    ch = p_node.get("charge", 0.0)
                    if ch > 0.4:
                        spark_c = QColor(0, 240, 255, alpha_spark)
                    elif ch < -0.4:
                        spark_c = QColor(255, 80, 120, alpha_spark)
                    elif abs(ch) < 0.1 and node_idx > 0:
                        spark_c = QColor(255, 220, 50, alpha_spark)
                    else:
                        spark_c = QColor(220, 160, 255, alpha_spark)

                    sz_spark = 2.0 + 1.8 * ((q % 3) == 0)

                    # Micro-ondícula acuática emitida en el cénit del colapso (unión acuático-cuántica)
                    if life_intensity > 0.65:
                        wave_out_r = (life_intensity - 0.65) * 35.0 * sz_spark
                        alpha_wave_out = int((1.0 - (life_intensity - 0.65) / 0.35) * alpha_spark * 0.45)
                        if alpha_wave_out > 5:
                            c_micro = QColor(spark_c)
                            c_micro.setAlpha(alpha_wave_out)
                            painter.setPen(QPen(c_micro, 1.0))
                            painter.setBrush(Qt.NoBrush)
                            painter.drawEllipse(QPointF(qx, qy), wave_out_r, wave_out_r)

                    # Halo difuso del cuanto
                    glow_spark = QRadialGradient(qx, qy, sz_spark * 3.8)
                    glow_spark.setColorAt(0.0, QColor(spark_c.red(), spark_c.green(), spark_c.blue(), int(alpha_spark * 0.65)))
                    glow_spark.setColorAt(1.0, QColor(0, 0, 0, 0))
                    painter.setBrush(QBrush(glow_spark))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(QPointF(qx, qy), sz_spark * 3.8, sz_spark * 3.8)

                    # Núcleo blanco de detección
                    painter.setBrush(QBrush(QColor(255, 255, 255, alpha_spark)))
                    painter.drawEllipse(QPointF(qx, qy), sz_spark, sz_spark)

        # ══════════════════════════════════════════════════════════════════════
        # MODO 2: CIMÁTICA ACUÁTICA (CADA NÚCLEO EMITE SU PROPIA ONDA COHERENTE)
        # ══════════════════════════════════════════════════════════════════════
        else:
            # 1. Cada núcleo atómico emite trenes de ondas acuáticas circulares
            # que se propagan hacia afuera y colisionan con las ondas de los demás
            k_wave = 10.0 + 3.0 * self.stage
            ripple_steps = 100

            for idx, node in enumerate(nodes):
                nr = node["r"] * max_radius * 0.85 * self.breath_scale
                na = node["angle"]
                nx = nr * math.cos(na)
                ny = nr * math.sin(na)
                sz = node.get("size", 1.0)
                ch = node.get("charge", 0.0)

                # Color específico de frecuencia emitido por este centro
                if ch > 0.4:
                    wave_c = QColor("#5DADE2")
                elif ch < -0.4:
                    wave_c = QColor("#E74C3C")
                elif abs(ch) < 0.1 and idx > 0:
                    wave_c = QColor("#F4D03F")
                else:
                    wave_c = QColor(self.base_color)

                num_rings = 14
                for r_idx in range(1, num_rings + 1):
                    # Fase de expansión de la onda que viaja desde este átomo
                    wave_front = (r_idx / num_rings)
                    r_travel = max_radius * 0.55 * sz * wave_front * self.breath_scale

                    path_atom_wave = QPainterPath()

                    for step in range(ripple_steps + 1):
                        theta = (step / ripple_steps) * 2 * math.pi
                        dx = math.cos(theta)
                        dy = math.sin(theta)

                        cur_x = nx + r_travel * dx
                        cur_y = ny + r_travel * dy

                        # Interferencia con las ondas emitidas por los OTROS átomos
                        interference = 0.0
                        for o_idx, o_node in enumerate(nodes):
                            if o_idx == idx:
                                continue
                            onr = o_node["r"] * max_radius * 0.85 * self.breath_scale
                            ona = o_node["angle"]
                            onx = onr * math.cos(ona)
                            ony = onr * math.sin(ona)
                            dist_to_other = math.sqrt((cur_x - onx)**2 + (cur_y - ony)**2)
                            
                            # Onda recibida del otro centro
                            other_wave = math.cos(k_wave * (dist_to_other / max_radius) - self.phase * 3.0 + o_idx)
                            influence = math.exp(-dist_to_other / (max_radius * 0.35))
                            interference += influence * other_wave * 0.18

                        # Modulación del radio local de la onda
                        w_deform = math.sin(k_wave * wave_front - self.phase * 3.2 + idx) * (0.05 * self.stage)
                        r_final = r_travel + max_radius * (w_deform + interference)

                        px = nx + r_final * dx
                        py = ny + r_final * dy

                        if step == 0:
                            path_atom_wave.moveTo(px, py)
                        else:
                            path_atom_wave.lineTo(px, py)

                    # Atenuación con la distancia (1 / r)
                    alpha_w = int(170 * (1.0 - wave_front * 0.7))
                    c_ring = QColor(wave_c)
                    c_ring.setAlpha(max(15, min(240, alpha_w)))

                    painter.setPen(QPen(c_ring, 1.1 if r_idx > 3 else 1.4))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawPath(path_atom_wave)

        # ── ENLACES ATÓMICOS DE PROPAGACIÓN (LIGANDOS) ──
        if self.stage >= 2 and len(nodes) > 1:
            for node in nodes[1:]:
                nr = node["r"] * max_radius * self.breath_scale
                na = node["angle"]
                target_x = nr * math.cos(na)
                target_y = nr * math.sin(na)

                link_path = QPainterPath()
                link_path.moveTo(0, 0)
                
                samples = 12
                for s in range(1, samples + 1):
                    t = s / samples
                    bx = target_x * t
                    by = target_y * t
                    normal_x = -math.sin(na)
                    normal_y = math.cos(na)
                    wobble = math.sin(t * 6.0 - self.phase * 3.5) * (4.0 * self.stage)
                    link_path.lineTo(bx + normal_x * wobble, by + normal_y * wobble)

                c_link = QColor(self.base_color)
                c_link.setAlpha(60 + 35 * self.stage)
                pen_link = QPen(c_link)
                pen_link.setWidthF(1.2)
                pen_link.setStyle(Qt.DashLine if self.stage == 2 else Qt.SolidLine)
                painter.setPen(pen_link)
                painter.drawPath(link_path)

        # ── CENTROS ATÓMICOS REACTIVOS (SITIOS DE INTERACCIÓN Y VACÍOS) ──
        font = QFont("Segoe UI", 8)
        painter.setFont(font)

        for idx, node in enumerate(nodes):
            nr = node["r"] * max_radius * self.breath_scale
            na = node["angle"]
            nx = nr * math.cos(na)
            ny = nr * math.sin(na)
            ch = node.get("charge", 0.0)
            sz = node.get("size", 1.0)

            atom_pulse = 1.0 + 0.25 * math.sin(self.phase * 4.0 + idx)
            base_radius = 5.0 * sz * atom_pulse

            halo_grad = QRadialGradient(nx, ny, base_radius * 3.5)
            if ch > 0.4:
                c_atom = QColor("#5DADE2")
            elif ch < -0.4:
                c_atom = QColor("#E74C3C")
            elif abs(ch) < 0.1 and idx > 0:
                c_atom = QColor("#F4D03F")
            else:
                c_atom = QColor(self.base_color)

            halo_c = QColor(c_atom)
            halo_c.setAlpha(70 if self.stage >= 2 else 35)
            halo_grad.setColorAt(0, halo_c)
            halo_grad.setColorAt(1, QColor(0, 0, 0, 0))

            painter.setBrush(QBrush(halo_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(nx, ny), base_radius * 3.5, base_radius * 3.5)

            core_c = QColor(c_atom)
            core_c.setAlpha(220)
            painter.setBrush(QBrush(core_c))
            painter.setPen(QPen(QColor(255, 255, 255, 180), 1.0))
            painter.drawEllipse(QPointF(nx, ny), base_radius, base_radius)

            if self.stage >= 2:
                label_color = QColor(220, 220, 220, 160)
                painter.setPen(label_color)
                painter.drawText(QPointF(nx + base_radius + 4, ny + 4), node["name"])

        painter.restore()

# ══════════════════════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class DNAResonanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧬 Santuario Cuántico: Activador Cimático de ADN")
        self.resize(1080, 850)
        
        # Estilos Globales
        self.setStyleSheet("""
            QMainWindow { background-color: #050508; }
            QLabel { color: #E0E0E0; font-family: 'Segoe UI'; }
            QComboBox { 
                background: #111; color: #F1C40F; border: 1px solid #333; 
                padding: 8px; font-size: 15px; border-radius: 4px;
            }
            QPushButton {
                background: #1C2833; color: #FFF; border: 1px solid #34495E;
                padding: 10px 14px; font-size: 13px; border-radius: 6px; font-weight: bold;
            }
            QPushButton:hover { background: #2C3E50; border-color: #F1C40F; }
            QScrollArea { border: none; background: transparent; }
        """)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)
        
        # Header Bar con Título y Selector de Modo de Renderizado
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title = QLabel("MOTOR DE MORFOGÉNESIS VOCAL")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #F1C40F; letter-spacing: 2px;")
        subtitle = QLabel("Sincronizando Frecuencias de Agua, Sonido, Tripletes de ARN y Geometría Molecular")
        subtitle.setStyleSheet("color: #888; font-size: 11px;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Selector de Modo Gráfico (Cimática vs Densidad Cuántica)
        mode_label = QLabel("Visualización:")
        mode_label.setStyleSheet("color: #AAA; font-size: 12px;")
        header_layout.addWidget(mode_label)

        self.btn_mode_cymatics = QPushButton("🌊 Cimática Acuática")
        self.btn_mode_cymatics.setStyleSheet("background: #2471A3; color: white; border: 1px solid #5499C7;")
        self.btn_mode_cymatics.clicked.connect(lambda: self.switch_render_mode("Cimática Acuática"))
        header_layout.addWidget(self.btn_mode_cymatics)

        self.btn_mode_orbital = QPushButton("🌌 Densidad Cuántica")
        self.btn_mode_orbital.setStyleSheet("background: #1A1A24; color: #AAA; border: 1px solid #333;")
        self.btn_mode_orbital.clicked.connect(lambda: self.switch_render_mode("Densidad Cuántica / Orbital"))
        header_layout.addWidget(self.btn_mode_orbital)

        main_layout.addLayout(header_layout)

        # Selector de Aminoácido / Sello Maya
        self.selector = QComboBox()
        for r in RESONANCE_MAP:
            self.selector.addItem(f"{r['seal']} ➔ {r['amino']} [ {r['bija']} / {r['kototama']} ]")
        self.selector.currentIndexChanged.connect(self.on_selection_changed)
        main_layout.addWidget(self.selector)

        # ── CUERPO DIVIDIDO: VISUALIZADOR + PANEL DE CODONES ──
        body_splitter = QSplitter(Qt.Horizontal)
        body_splitter.setStyleSheet("QSplitter::handle { background: #222; }")

        # 1. Columna Izquierda: Visualizador
        visual_container = QWidget()
        visual_layout = QVBoxLayout(visual_container)
        visual_layout.setContentsMargins(0, 0, 8, 0)
        self.visualizer = CymaticVisualizer()
        visual_layout.addWidget(self.visualizer)
        body_splitter.addWidget(visual_container)

        # 2. Columna Derecha: Códice de 64 Codones / Tripletes de ARN
        codons_frame = QFrame()
        codons_frame.setStyleSheet("""
            QFrame { background: #0A0D14; border: 1px solid #222B38; border-radius: 8px; }
        """)
        codons_layout = QVBoxLayout(codons_frame)
        codons_layout.setContentsMargins(12, 12, 12, 12)
        codons_layout.setSpacing(8)

        codons_title = QLabel("CÓDICE DE TRIPLETS (ARN)")
        codons_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        codons_title.setStyleSheet("color: #F1C40F; letter-spacing: 1px;")
        codons_layout.addWidget(codons_title)

        self.lbl_codons_subtitle = QLabel("Codones y Micro-Modulaciones de Kototama:")
        self.lbl_codons_subtitle.setStyleSheet("color: #888; font-size: 11px;")
        codons_layout.addWidget(self.lbl_codons_subtitle)

        # Área con scroll para la lista de codones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.codons_list_widget = QWidget()
        self.codons_list_layout = QVBoxLayout(self.codons_list_widget)
        self.codons_list_layout.setContentsMargins(0, 0, 0, 0)
        self.codons_list_layout.setSpacing(6)
        scroll.setWidget(self.codons_list_widget)
        codons_layout.addWidget(scroll, stretch=1)

        # Caja de información molecular
        self.info_box = QLabel("Información molecular...")
        self.info_box.setWordWrap(True)
        self.info_box.setStyleSheet("background: #06080D; border: 1px solid #1C2331; padding: 8px; border-radius: 5px; font-size: 11px; color: #BDC3C7;")
        codons_layout.addWidget(self.info_box)

        body_splitter.addWidget(codons_frame)
        body_splitter.setStretchFactor(0, 3)
        body_splitter.setStretchFactor(1, 2)
        main_layout.addWidget(body_splitter, stretch=1)

        # UI Prompter (Teleprompter)
        prompter_frame = QFrame()
        prompter_frame.setStyleSheet("""
            QFrame { background: #080A10; border: 1px solid #1F2836; border-radius: 8px; padding: 4px; }
        """)
        prompter_layout = QVBoxLayout(prompter_frame)
        prompter_layout.setContentsMargins(10, 8, 10, 8)
        prompter_layout.setSpacing(4)
        
        self.lbl_bija = QLabel("BIJA SEMILLA: ...")
        self.lbl_bija.setFont(QFont("Segoe UI", 11))
        self.lbl_bija.setAlignment(Qt.AlignCenter)
        
        self.lbl_kototama = QLabel("KOTOTAMA: ...")
        self.lbl_kototama.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_kototama.setAlignment(Qt.AlignCenter)
        self.lbl_kototama.setStyleSheet("color: #3498DB; margin: 4px 0;")
        
        self.lbl_instruction = QLabel("Instrucción: ...")
        self.lbl_instruction.setFont(QFont("Segoe UI", 11, italic=True))
        self.lbl_instruction.setAlignment(Qt.AlignCenter)
        self.lbl_instruction.setWordWrap(True)
        self.lbl_instruction.setStyleSheet("color: #AAA;")

        prompter_layout.addWidget(self.lbl_bija)
        prompter_layout.addWidget(self.lbl_kototama)
        prompter_layout.addWidget(self.lbl_instruction)
        main_layout.addWidget(prompter_frame)

        # Metronome / Breath Guide
        self.lbl_breath = QLabel("ESPERANDO...")
        self.lbl_breath.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.lbl_breath.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_breath)

        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("▶ INICIAR SECUENCIA ARMÓNICA")
        self.btn_start.clicked.connect(self.toggle_breath)
        btn_layout.addWidget(self.btn_start)
        main_layout.addLayout(btn_layout)

        # State Variables
        self.is_breathing = False
        self.breath_phase = "INHALE" # INHALE or EXHALE
        self.breath_timer = QTimer(self)
        self.breath_timer.timeout.connect(self.breath_tick)
        self.breath_ticks = 0
        self.current_stage = 1
        self.cycle_count = 1
        self.max_cycles = 3

        # Animación del visualizador (escala de respiración)
        self.anim = QPropertyAnimation(self, b"breath_scale")
        self.anim.setEasingCurve(QEasingCurve.InOutSine)

        # Inicializar UI atómicamente
        self.on_selection_changed(0)

    def switch_render_mode(self, mode):
        self.visualizer.set_render_mode(mode)
        if mode == "Cimática Acuática":
            self.btn_mode_cymatics.setStyleSheet("background: #2471A3; color: white; border: 1px solid #5499C7;")
            self.btn_mode_orbital.setStyleSheet("background: #1A1A24; color: #AAA; border: 1px solid #333;")
        else:
            self.btn_mode_orbital.setStyleSheet("background: #8E44AD; color: white; border: 1px solid #BB8FCE;")
            self.btn_mode_cymatics.setStyleSheet("background: #1A1A24; color: #AAA; border: 1px solid #333;")

    def get_breath_scale(self):
        return self.visualizer.breath_scale
        
    def set_breath_scale(self, val):
        self.visualizer.breath_scale = val
        self.visualizer.update()
        
    breath_scale = Property(float, get_breath_scale, set_breath_scale)

    def on_selection_changed(self, index):
        # ── SOLUCIÓN ATÓMICA AL BUG DE DESFASE: ──
        # Si la secuencia de respiración estaba activa, se detiene y reinicia limpia
        was_running = self.is_breathing
        if was_running:
            self.is_breathing = False
            self.breath_timer.stop()
            self.anim.stop()
            self.set_breath_scale(1.0)
            self.btn_start.setText("▶ INICIAR SECUENCIA ARMÓNICA")

        self.current_stage = 1
        self.cycle_count = 1

        data = RESONANCE_MAP[index]
        self.visualizer.set_amino_data(data)
        self.visualizer.set_stage(1)

        self.lbl_bija.setText(f"BIJA SEMILLA: [ {data['bija']} ]  •  FÓRMULA: {data.get('formula', '')} ({data.get('group', '')})")
        self.lbl_kototama.setText(data['kototama'])
        self.lbl_kototama.setStyleSheet(f"color: {data['color']}; margin: 4px 0;")
        self.lbl_instruction.setText(data['instruction'])
        self.lbl_breath.setText("ESPERANDO...")
        self.lbl_breath.setStyleSheet("color: #E0E0E0;")

        # Actualizar lista de codones de ARN en el panel lateral
        self.update_codons_panel(data)

    def update_codons_panel(self, data):
        # Limpiar widgets previos
        while self.codons_list_layout.count():
            item = self.codons_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        codons = data.get("codons", [])
        for c in codons:
            box = QFrame()
            box.setStyleSheet("""
                QFrame { background: #0E131C; border: 1px solid #1F2836; border-radius: 6px; padding: 6px; }
                QFrame:hover { border-color: #3498DB; background: #131A26; }
            """)
            b_layout = QVBoxLayout(box)
            b_layout.setContentsMargins(6, 4, 6, 4)
            b_layout.setSpacing(2)

            top_row = QHBoxLayout()
            triplet_lbl = QLabel(c["triplet"])
            triplet_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
            triplet_lbl.setStyleSheet(f"color: {data['color']};")
            
            kototama_lbl = QLabel(f"[{c['kototama']}]")
            kototama_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            kototama_lbl.setStyleSheet("color: #5DADE2;")

            top_row.addWidget(triplet_lbl)
            top_row.addStretch()
            top_row.addWidget(kototama_lbl)
            b_layout.addLayout(top_row)

            action_lbl = QLabel(c["action"])
            action_lbl.setStyleSheet("color: #888; font-size: 10px;")
            b_layout.addWidget(action_lbl)

            self.codons_list_layout.addWidget(box)

        self.codons_list_layout.addStretch()

        # Actualizar caja de información
        nodes = data.get("nodes", [])
        self.info_box.setText(
            f"<b>Molécula:</b> {data['amino']}<br>"
            f"<b>Clasificación:</b> {data.get('group', 'Estándar')}<br>"
            f"<b>Centros Atómicos Activos:</b> {len(nodes)} polos<br>"
            f"<b>Tripletes de ARN:</b> {len(codons)} codones de traducción"
        )

    def update_stage_ui(self):
        data = RESONANCE_MAP[self.selector.currentIndex()]
        self.lbl_kototama.setStyleSheet(f"color: {data['color']}; margin: 4px 0;")
        self.visualizer.set_stage(self.current_stage)
        
        if self.current_stage == 1:
            self.lbl_bija.setText(f"FASE 1: ANCLAJE GEOMÉTRICO [{self.cycle_count}/{self.max_cycles}]  •  {data['amino']}")
            self.lbl_kototama.setText(data['bija'])
            self.lbl_instruction.setText(f"Entona la semilla pura [{data['bija']}] para asentar la base atómica en el agua.")
        elif self.current_stage == 2:
            self.lbl_bija.setText(f"FASE 2: MORFOGÉNESIS KOTOTAMA [{self.cycle_count}/{self.max_cycles}]  •  {data['amino']}")
            self.lbl_kototama.setText(data['kototama'])
            self.lbl_instruction.setText(data['instruction'])
        elif self.current_stage == 3:
            self.lbl_bija.setText(f"FASE 3: SÍNTESIS CELULAR [{self.cycle_count}/{self.max_cycles}]  •  {data['amino']}")
            self.lbl_kototama.setText(f"{data['bija']} ➔ {data['kototama']}")
            self.lbl_instruction.setText("Funde la semilla armónica con el barrido de vocales. Resonancia en los codones.")

    def toggle_breath(self):
        if self.is_breathing:
            self.stop_breath()
        else:
            self.start_breath()

    def start_breath(self):
        self.is_breathing = True
        self.btn_start.setText("⏹ DETENER SECUENCIA")
        self.breath_phase = "INHALE"
        self.current_stage = 1
        self.cycle_count = 1
        self.update_stage_ui()
        
        self.breath_ticks = 70  # 7 segundos a 100ms
        self.breath_timer.start(100)
        self.lbl_breath.setStyleSheet("color: #3498DB;")
        
        self.anim.stop()
        self.anim.setDuration(7000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(1.3)
        self.anim.start()

    def stop_breath(self):
        self.is_breathing = False
        self.btn_start.setText("▶ INICIAR SECUENCIA ARMÓNICA")
        self.breath_timer.stop()
        self.anim.stop()
        self.set_breath_scale(1.0)
        self.on_selection_changed(self.selector.currentIndex())
        self.lbl_breath.setText("SECUENCIA DETENIDA")
        self.lbl_breath.setStyleSheet("color: #AAA;")

    def breath_tick(self):
        self.breath_ticks -= 1
        
        if self.breath_ticks <= 0:
            if self.breath_phase == "INHALE":
                self.breath_phase = "EXHALE"
                self.breath_ticks = 140 # 14 segundos exhale
                self.lbl_breath.setStyleSheet("color: #F1C40F;")
                self.anim.stop()
                self.anim.setDuration(14000)
                self.anim.setStartValue(1.3)
                self.anim.setEndValue(1.0)
                self.anim.start()
            else:
                self.cycle_count += 1
                if self.cycle_count > self.max_cycles:
                    self.cycle_count = 1
                    self.current_stage += 1
                    if self.current_stage > 3:
                        self.stop_breath()
                        self.lbl_breath.setText("SECUENCIA COMPLETADA")
                        self.lbl_breath.setStyleSheet("color: #2ECC71;")
                        return
                
                self.update_stage_ui()
                self.breath_phase = "INHALE"
                self.breath_ticks = 70
                self.lbl_breath.setStyleSheet("color: #3498DB;")
                self.anim.stop()
                self.anim.setDuration(7000)
                self.anim.setStartValue(1.0)
                self.anim.setEndValue(1.3)
                self.anim.start()

        sec = self.breath_ticks / 10.0
        if self.breath_phase == "INHALE":
            self.lbl_breath.setText(f"INHALA LUZ... {sec:.1f}s")
        else:
            self.lbl_breath.setText(f"ENTONA Y VIBRA... {sec:.1f}s")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNAResonanceApp()
    window.show()
    sys.exit(app.exec())
