# Paroļu Pārvaldnieka Programma

## Projekta apraksts
**Paroļu pārvaldnieka programma** ir drošs un lietotājam draudzīgs rīks paroļu ģenerēšanai, glabāšanai un pārvaldībai. Tā izmanto modernus šifrēšanas algoritmus, lai nodrošinātu datu aizsardzību. Piemērota gan ikdienas lietotājiem, gan profesionālām vajadzībām (Nav 100% drošs neizmantot sensitīviem datiem, tikai izglītībai).

---

## Funkcionalitāte

- 🔒 **Master paroles aizsardzība**: Droša piekļuve, izmantojot galveno paroli.
- 🔑 **Drošu paroļu ģenerēšana**: Veidojiet unikālas, drošas paroles ar izvēlētu garumu.
- 📂 **Paroļu glabāšana**: Saglabājiet savas paroles šifrētā datubāzē.
- 🔓 **Paroļu atgūšana**: Atgūstiet un nokopējiet paroles starpliktuvē.
- 📋 **Glabāto datu pārskats**: Skatiet visus pakalpojumus un lietotājvārdus.

---

## Sistēmas prasības

- **Python versija**: Python 3.x  
- **Operētājsistēma**: Windows, macOS vai Linux  
- **Papildu bibliotēkas**: `sqlite3`,`cryptography`, `hashlib`, `pyperclip`, `getpass`, `secrets`.

---

## Instalēšanas instrukcija

1. **Lejupielādējiet projekta failus** no repozitorija.
2. **Instalējiet nepieciešamās bibliotēkas**, izpildot terminālā komandu:
   ```bash
   pip install -r requirements.txt
   ```
3. **Pārliecinieties**, ka jūsu sistēmā ir instalēts Python 3.
4. **Palaidiet programmu**, izmantojot komandu:
   ```bash
   python password_manager.py
   ```

---

## Lietošanas instrukcija

1. **Inicializējiet master paroli**: Pirmajā palaišanas reizē ievadiet un apstipriniet galveno paroli.
2. **Izvēlieties darbību** no izvēlnes:
   - 🆕 **Pievienot jaunu paroli**
   - 🔍 **Atgūt esošu paroli**
   - 🎲 **Ģenerēt drošu paroli**
   - 📋 **Apskatīt saglabātos pakalpojumus un lietotājvārdus**
   - ❌ **Iziet no programmas**
3. **Sekojiet ekrānā redzamajiem norādījumiem.**

---

## Piemērs

### Drošas paroles ģenerēšana
- **Ievade**: Paroles garums - 12  
- **Rezultāts**: `A$2lK8q#dP3y`  
  *(Parole tiek nokopēta uz starpliktuvi.)*

### Paroles pievienošana
- **Pakalpojums**: Gmail  
- **Lietotājvārds**: lietotajs@gmail.com  
- **Parole**: `A$2lK8q#dP3y`  
  *(Tiek pievienota drošā datubāzē.)*

### Paroles atgūšana
- **Pakalpojums**: Gmail  
- **Lietotājvārds**: lietotajs@gmail.com  
- **Rezultāts**: `A$2lK8q#dP3y`  
  *(Parole tiek nokopēta uz starpliktuvi.)*

---

## Licences informācija

Šis projekts ir izplatīts saskaņā ar **MIT licenci**. Plašāku informāciju skatiet failā `LICENSE`.

---

## Autors

👤 **Izstrādātājs**: Jūsu Vārds  
📧 **Kontakti**: [lietotajs@epasts.lv](mailto:lietotajs@epasts.lv)
