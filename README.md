## RWA Surface Calculator (CRR 575/2013 Art. 153)
This project generates an **interactive HTML output** of the **Risk Weight (RW)** calculation function, based on the regulatory formula defined in **CRR 575/2013**, Article 153 (page 97).
By multiplying RW by the *EAD (Exposure At Default)*, you obtain the *RWA (Risk-Weighted Assets)*:
**RWA = RW × EAD**

## Objective
To illustrate how **RW** behaves as the following parameters vary:
- **PD** (Probability of Default)
- **LGD** (Loss Given Default)
- **M** (Maturity, in years)

The result is displayed in:
- an *interactive 3D plot* (Plotly)
- with a *slider* to dynamically adjust *Maturity*

## References
- Regulation (EU) No 575/2013 (CRR) – [eur-lex.europa.eu](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R0575)
