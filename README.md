# Paroļu Pārvaldnieka Programma

## Projekta apraksts
**Paroļu pārvaldnieka programma** ir drošs un lietotājam draudzīgs rīks ar grafisku saskarni paroļu ģenerēšanai, glabāšanai un pārvaldībai. Tā izmanto modernus šifrēšanas algoritmus, lai nodrošinātu datu aizsardzību. Piemērota gan ikdienas lietotājiem, gan profesionālām vajadzībām.

**(Nav 100% drošs neizmantot sensitīviem datiem, tikai izglītībai).**
---

## Funkcionalitāte

- 🖥️ **Grafiskā lietotāja saskarne**: Vienkārša un intuitīva lietošana
- 🔒 **Master paroles aizsardzība**: Droša piekļuve, izmantojot galveno paroli
- 🔑 **Drošu paroļu ģenerēšana**: Veidojiet unikālas, drošas paroles ar izvēlētu garumu
- 📂 **Paroļu glabāšana**: Saglabājiet savas paroles šifrētā datubāzē
- 🔓 **Paroļu atgūšana**: Atgūstiet un nokopējiet paroles starpliktuvē
- 📋 **Glabāto datu pārskats**: Skatiet visus pakalpojumus un lietotājvārdus
- 📱 **Ērta navigācija**: Pārslēdzieties starp dažādām funkcijām, izmantojot cilnes

---

## Sistēmas prasības

- **Python versija**: Python 3.x
- **Operētājsistēma**: Windows, macOS vai Linux
- **Papildu bibliotēkas**: 
  - sqlite3
  - cryptography
  - hashlib
  - pyperclip
  - tkinter
  - secrets

---

## Instalēšanas instrukcija

1. **Lejupielādējiet projekta failus** no repozitorija
2. **Atvērt terminālu pareizajā direktorijā**, right clickot un Open In Terminal
3. **Instalējiet nepieciešamās bibliotēkas**, izpildot terminālā komandu:
```bash
pip install -r requirements.txt
```
4. **Pārliecinieties**, ka jūsu sistēmā ir instalēts Python 3
5. **Palaidiet programmu**, izmantojot komandu:
```bash
python password_manager_gui.py
```

---

## Lietošanas instrukcija

### Pirmā palaišana
1. **Inicializējiet master paroli**
   - Pirmajā palaišanas reizē ievadiet un apstipriniet galveno paroli
   - Šī parole būs nepieciešama katru reizi, atverot programmu

### Galvenā saskarne
Programma piedāvā četras galvenās cilnes:

1. **Pievienot Paroli**
   - Ievadiet pakalpojuma nosaukumu
   - Ievadiet lietotājvārdu
   - Izvēlieties starp manuālu paroles ievadi vai automātisku ģenerēšanu

2. **Iegūt Paroli**
   - Ievadiet pakalpojuma nosaukumu un lietotājvārdu
   - Parole tiks parādīta un automātiski nokopēta starpliktuvē

3. **Ģenerēt Paroli**
   - Norādiet vēlamo paroles garumu
   - Ģenerētā parole tiks parādīta un nokopēta starpliktuvē

4. **Pakalpojumu Saraksts**
   - Pārskatāms saraksts ar visiem saglabātajiem pakalpojumiem
   - Redzami pakalpojumu nosaukumi un lietotājvārdi
   - Iespēja atjaunināt sarakstu

---

## Drošības funkcijas

- 🔐 **Šifrēta datubāze**: Visas paroles tiek glabātas šifrētā veidā
- 🔑 **Droša master parole**: Izmanto PBKDF2 un SHA-256 hash funkcijas
- 🎲 **Drošs paroļu ģenerators**: Izmanto Python secrets moduli
- 📋 **Automātiska kopēšana**: Paroles tiek automātiski kopētas starpliktuvē

---

## Licences informācija

Šis projekts ir izplatīts saskaņā ar **MIT licenci**. Plašāku informāciju skatiet failā LICENSE.

---

## Autors

👤 **Izstrādātājs**: evanora  
📧 **Kontakti**: [sokarihinji@gmail.com](mailto:sokarihinji@gmail.com)
