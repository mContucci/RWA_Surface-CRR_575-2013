RWA Surface Calculator (CRR 575/2013 Art. 153)

Questo progetto genera un output *interattivo in HTML* della funzione di calcolo del *Risk Weight (RW)*, secondo la formula regolamentare definita nel *CRR 575/2013*, Articolo 153 (pag. 97).

Moltiplicando il RW per l’*EAD (Exposure At Default)* si ottiene il valore dell’*RWA (Risk-Weighted Assets)*:


RWA = RW × EAD


🎯 Obiettivo

Mostrare come si comporta il *RW* al variare dei seguenti parametri:

- *PD* (Probability of Default)
- *LGD* (Loss Given Default)
- *M* (Maturity, in anni)

Il risultato è visualizzato in:

- un *grafico 3D interattivo* (Plotly)
- con uno *slider* per variare *Maturity* dinamicamente
