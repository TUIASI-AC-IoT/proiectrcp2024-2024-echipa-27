![image](https://github.com/user-attachments/assets/a0c2d0b5-9f2f-4aeb-aaef-e0357ae03c0d)# MQTT5 CLIENT - APLICAȚIE DEMONSTRATIVĂ

**Autor:** Ciobanu Constantin-Marcu  
**Grupă:** 1307b  

---

## Introducere

**MQTT** este un protocol esențial în lumea IoT, folosit pentru transportul rapid, sigur și eficient al informațiilor între dispozitive. Acesta permite clienților să se conecteze la un broker (în acest caz am folosit HiveMQ), folosind o tehnică de comunicare prin pachete de tip **publish-subscribe**.

Un broker MQTT este un serviciu cloud care facilitează comunicarea între clienți, permițându-le să acceseze și să publice mesaje pe diferite topice. Astfel, clienții se pot abona la aceste topice, pentru a primi mesaje de la alți end-clients conectați la același broker.

---

## Descrierea Aplicatiei

Această aplicație demonstrativă ilustrează un **client MQTT5** care se conectează la brokerul HiveMQ și interacționează cu acesta folosind pachete de date structurate.

---

## Tehnologie Utilizată

- **Broker**: HiveMQ
- **Protocol de Transport**: TCP/IP
- **Librărie de Comunicație**: BSD Sockets

---

## Implementare

### 1. Conectarea la Broker

Pentru a realiza conectarea, folosim **modulul BSD socket**, care ne permite să stabilim o conexiune prin **TCP/IP** la broker-ul nostru, în funcția principală (`main`). Această conexiune este esențială pentru a permite clientului nostru să comunice eficient cu brokerul HiveMQ.

### 2. Trimiterea Pachetelor

După conectarea la broker, vom trimite pachetele construite către server, până la întâlnirea unei erori, folosind funcția blocantă `sendall`. Această funcție asigură că toate pachetele sunt transmise complet, fără pierderi de date, înainte de a trece la următoarea operație.

### 3. Pachetul de Conectare (`connect_packet`)

Pachetul de conectare, numit **connect_packet**, trebuie să fie primul pachet trimis de client spre server. Acesta este esențial pentru stabilirea relației **connect-CONNACK**, în care clientul trimite un pachet de tip `CONNECT` și așteaptă confirmarea de conectare (`CONNACK`) din partea brokerului.

---

## Structura Pachetului de Conectare
![Pachet de Conectare](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-27/blob/main/img/connect_packet.png)

Primul pachet pe care clientul il trimite trebuie sa fie unul de tip CONNECT ce include mai multe aspecte:

## Antet Fix (Fixed Header)

În antetul fix al pachetului `CONNECT`, câmpul **Packet Type** (Tipul Pachetului), situat în cei 4 biți superiori ai primului octet, trebuie să fie setat la 1 (`0b0001`), iar cei 4 biți inferiori ai primului octet trebuie să fie toți 0.

Astfel, valoarea primului octet al pachetului `CONNECT` trebuie să fie `0x10`. Putem utiliza această valoare pentru a determina dacă un pachet este de tip `CONNECT`.

## Antet Variabil (Variable Header)

Antetul variabil al pachetului `CONNECT` conține următoarele câmpuri, în ordine:

### Numele Protocolului (Protocol Name)

- Un șir de caractere, utilizat pentru a indica numele protocolului.
- În MQTT, primii doi octeți ai șirului codificat în UTF-8 sunt folosiți pentru a indica lungimea datelor efective de caractere care urmează.
- Numele protocolului este fixat ca `MQTT` în versiunile MQTT 3.1.1 și MQTT 5.0, astfel încât conținutul complet corespunzător în octeți hexazecimali este `00 04 4D 51 54 54`, unde `4D 51 54 54` reprezintă valorile ASCII ale șirului `MQTT`.
- 
### Versiunea Protocolului (Protocol Version)

- Un întreg unsigned de un octet, utilizat pentru a indica versiunea protocolului.
- Valorile posibile sunt:
  - `3` pentru MQTT 3.1
  - `4` pentru MQTT 3.1.1
  - `5` pentru MQTT 5.0

### Flaguri de Conectare (Connect Flags)

- Un octet care conține mai mulți biți de flaguri, utilizate pentru a indica comportamentul conexiunii sau dacă anumite câmpuri există în Payload.
- Structura flagurilor:
  - **User Name Flag**: Indică dacă Payload-ul conține Username.
  - **Password Flag**: Indică dacă Payload-ul conține Password.
  - **Will Retain**: Indică dacă mesajul "Will" este un mesaj reținut.
  - **Will QoS**: Indică nivelul QoS al mesajului "Will".
  - **Will Flag**: Indică dacă Payload-ul conține câmpuri relevante pentru mesajul "Will".
  - **Clean Start**: Indică dacă conexiunea curentă este o sesiune nouă sau continuarea uneia existente, determinând dacă serverul va crea direct o sesiune nouă sau va încerca să reutilizeze una existentă.
  - **Reserved**: Acesta este un bit rezervat, valoarea sa trebuie să fie 0.

### Keep Alive

- Un întreg nesemnat de doi octeți, utilizat pentru a indica intervalul maxim de timp între două pachete de control consecutive trimise de client.

### Proprietăți (Properties)

Tabelul de mai jos listează toate proprietățile disponibile ale pachetului `CONNECT`:

| Identificator | Nume Proprietate              | Tip                    |
|---------------|-------------------------------|------------------------|
| `0x11`        | Session Expiry Interval       | Întreg pe 4 octeți     |
| `0x21`        | Receive Maximum               | Întreg pe 2 octeți     |
| `0x27`        | Maximum Packet Size           | Întreg pe 4 octeți     |
| `0x22`        | Topic Alias Maximum           | Întreg pe 2 octeți     |
| `0x19`        | Request Response Information  | Octet                  |
| `0x17`        | Request Problem Information   | Octet                  |
| `0x26`        | User Property                 | Pereche de șiruri UTF-8|
| `0x15`        | Authentication Method         | Șir codificat UTF-8    |
| `0x16`        | Authentication Data           | Date binare            |

## Payload

În Payload-ul pachetului `CONNECT`, în afară de **Client ID**, toate celelalte câmpuri sunt opționale. Existența lor depinde de valoarea flagurilor corespunzătoare din Connect Flags ale antetului variabil. Cu toate acestea, dacă aceste câmpuri există, ele trebuie să apară în următoarea ordine:

1. **Client ID**
2. **Will Properties**
3. **Will Topic**
4. **Will Payload**
5. **User Name**
6. **Password**

---

## Comunicarea cu Brokerul

După trimiterea pachetului de conectare către broker, clientul folosește funcția blocantă `recv` pentru a aștepta un răspuns de la broker, în mod specific un pachet de 4 octeți. Acest răspuns este necesar pentru a confirma dacă brokerul a acceptat conexiunea. Acest raspuns este denumit si un packet de tip CONNACK ce contine mai multe aspecte de confirmarea a conexiunii cu broker-ul, acesta are urmatoarea structura: 

## Antet Fix (Fixed Header)

În antetul fix al pachetului `CONNACK`, valoarea celor 4 biți superiori ai primului octet este `2` (`0b0010`), ceea ce indică faptul că acesta este un pachet de tip `CONNACK`.

## Antet Variabil (Variable Header)

Antetul variabil al pachetului `CONNACK` conține următoarele câmpuri, în această ordine:

### Connect Acknowledge Flags (Flaguri de Confirmare a Conexiunii)

Aceste flaguri indică starea conexiunii:

- **Reserved** (Bit 7 - 1): Biți rezervați, trebuie setați la 0.
- **Session Present** (Bit 0): Arată dacă serverul folosește o sesiune existentă pentru a relua comunicarea cu clientul. `Session Present` poate fi `1` doar dacă clientul a setat `Clean Start` la `0` în cererea de conectare (pachetul `CONNECT`).

### Reason Code 

Codul-motiv explică rezultatul conexiunii:

| Valoare | Nume Cod Motiv           | Descriere                                                                                          |
|---------|---------------------------|----------------------------------------------------------------------------------------------------|
| `0x00`  | Success                   | Conexiunea a fost acceptată.                                                                       |
| `0x81`  | Malformed Packet          | Serverul nu poate analiza corect pachetul `CONNECT` (ex.: bitul rezervat nu este setat corect).    |
| `0x82`  | Protocol Error            | Pachetul `CONNECT` nu respectă specificațiile protocolului.                                        |
| `0x84`  | Unsupported Protocol Version | Serverul nu suportă versiunea de protocol solicitată de client.                                |
| `0x85`  | Client Identifier not valid | ID-ul clientului este valid, dar nu este acceptat de server (ex.: depășește limita de lungime). |
| `0x86`  | Bad User Name or Password | Conexiunea a fost refuzată din cauza numelui de utilizator sau parolei incorecte.                  |
| `0x95`  | Packet too large          | Pachetul `CONNECT` depășește dimensiunea maximă permisă de server.                                |
| `0x8A`  | Banned                    | Clientul este interzis (ex.: adăugat pe lista neagră de către un administrator sau din alte motive). |

### Proprietăți (Properties)

Lista de proprietăți din `CONNACK` poate include o serie de setări și informații despre sesiune:

| Identificator | Nume Proprietate                | Tip                    |
|---------------|---------------------------------|------------------------|
| `0x11`        | Session Expiry Interval         | Întreg pe 4 octeți     |
| `0x21`        | Receive Maximum                 | Întreg pe 2 octeți     |
| `0x24`        | Maximum QoS                     | Octet                  |
| `0x25`        | Retain Available                | Octet                  |
| `0x27`        | Maximum Packet Size             | Întreg pe 4 octeți     |
| `0x12`        | Assigned Client Identifier      | Șir codificat UTF-8    |
| `0x22`        | Topic Alias Maximum             | Întreg pe 2 octeți     |
| `0x1F`        | Reason String                   | Șir codificat UTF-8    |
| `0x26`        | User Property                   | Pereche de șiruri UTF-8|
| `0x28`        | Wildcard Subscription Available | Octet                  |
| `0x29`        | Subscription Identifier Available | Octet                |
| `0x2A`        | Shared Subscription Available   | Octet                  |
| `0x13`        | Server Keep Alive               | Întreg pe 2 octeți     |
| `0x1A`        | Response Information            | Șir codificat UTF-8    |
| `0x1C`        | Server Reference                | Șir codificat UTF-8    |
| `0x15`        | Authentication Method           | Șir codificat UTF-8    |
| `0x16`        | Authentication Data             | Date binare            |

## Payload

Pachetul `CONNACK` **nu are un Payload**. Toate informațiile necesare despre conexiune sunt transmise prin antetul fix și antetul variabil.

### Validarea Răspunsului `CONNACK`

După ce pachetul este primit de la broker, aplicăm o deplasare la dreapta asupra mesajului pentru a extrage primii 4 biți. Acești biți ne permit să confirmăm dacă pachetul primit este de tip `CONNACK`. Un pachet `CONNACK` validează faptul că brokerul a acceptat conexiunea și că clientul este acum conectat cu succes la server.
![Packet Connack](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-27/blob/main/img/connack.png)

---
# Modelul de Comunicare Publish-Subscribe în MQTT5

Într-o rețea MQTT5, clienții comunică printr-n model  **publish-subscribe**. Acest model implică două roluri principale pentru clienți: 

- **Publisher (Publicator)**: Clientul care trimite (publică) informația.
- **Subscriber (Abonat)**: Clientul care primește informația publicată.

În acest model, mesajele sunt transmise prin intermediul unui canal de comunicare numit **topic**. 

## Exemplu Practic

Să luăm exemplul unui senzor de temperatură și al unui smartphone care primeste datele de temperatura:

1. **Publicarea (Publish)**: Senzorul de temperatură, care trimite datele, publică informația pe un **topic** specific, de exemplu, `senzor/temperatura/living`. Acest topic funcționează ca un canal prin care sunt transmise datele.

2. **Abonarea (Subscribe)**: Smartphone-ul utilizatorului este abonat (subscribed) la acest topic `senzor/temperatura/living`. Fiind abonat la acest topic, smartphone-ul primește automat toate mesajele publicate de senzorul de temperatură pe acest canal.

3. **Recepționarea Mesajelor**: De fiecare dată când senzorul publică un nou mesaj despre temperatura din cameră, smartphone-ul, fiind abonat la topic, va primi aceste date, fără să fie nevoie de o conexiune directă între cele două dispozitive.

## Rolul Brokerului în Publish-Subscribe

În modelul publish-subscribe din MQTT5, broker-ul este intermediarul ce preia aceste mesaje. Acesta gestionează comunicarea dintre clienți, astfel:

- Brokerul primește mesajele publicate de la publisher (senzorul).
- Brokerul le distribuie către toți clienții abonați la acel topic (în acest caz, smartphone-ul).

## Topicuri în MQTT5

Un **topic** este un canal logic de comunicare care permite organizarea mesajelor. În MQTT, topicurile pot fi ierarhice și sunt structurate cu ajutorul slash-urilor `/`. În exemplul de mai sus, `senzor/temperatura/living` este un topic specific pentru temperatura din living.

MQTT permite, de asemenea, utilizarea **wildcard-urilor** pentru a facilita abonarea la mai multe topicuri simultan:
- `+` (plus) – Se potrivește cu un singur nivel de topic. De exemplu, `senzor/+/living` se va potrivi cu toate sub-topicurile, cum ar fi `senzor/temperatura/living` sau `senzor/umiditate/living`.
- `#` (diez) – Se potrivește cu toate nivelurile de la acel punct în jos. De exemplu, `senzor/#` va include toate sub-topicurile din `senzor`, precum `senzor/temperatura/living`, `senzor/umiditate`, etc.

## Avantajele Modelului Publish-Subscribe

- **Decuplare între Dispozitive**: Publisherul și subscriberul nu trebuie să știe unul de altul; fiecare interacționează doar cu brokerul.
- **Scalabilitate**: Un singur publisher poate trimite mesaje către un număr mare de subscriberi, ceea ce face ca modelul să fie foarte eficient în rețele mari.
- **Flexibilitate**: Abonamentele și publicările se pot schimba dinamic, fără a afecta restul sistemului.

## Cum MQTT5 functioneaza folosind pachete, in mod analog cu relatia de tip connect connact functioneaza si metodele de publish si subscribe, asadar:
### Pachetul `SUBSCRIBE`
![publish packet](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-27/blob/main/img/subsisuback.png)
Pachetul `SUBSCRIBE` este utilizat de un client pentru a se **abona** la unul sau mai multe topicuri pe broker. Prin acest pachet, clientul cere brokerului să îi trimită toate mesajele publicate pe topicurile respective.

#### Structura Pachetului `SUBSCRIBE`:
- **Fixed Header**: Conține tipul de pachet și setările pentru QoS (Quality of Service).
- **Variable Header**:
  - **Packet Identifier**: Un identificator unic al pachetului, utilizat pentru a corela `SUBSCRIBE` cu răspunsul `SUBACK`.
- **Payload**:
  - Lista topicurilor la care se abonează clientul, împreună cu nivelul QoS dorit pentru fiecare topic.

### Pachetul `SUBACK`

Pachetul `SUBACK` este răspunsul brokerului la cererea de abonare (`SUBSCRIBE`). Acesta confirmă dacă abonarea a fost realizată cu succes și specifică nivelul de QoS acceptat de broker pentru fiecare topic.

#### Structura Pachetului `SUBACK`:
- **Fixed Header**: Include tipul de pachet.
- **Variable Header**:
  - **Packet Identifier**: Același identificator de pachet trimis în `SUBSCRIBE`, pentru a corela răspunsul.
- **Payload**:
  - Lista nivelurilor de QoS acceptate pentru fiecare topic la care clientul s-a abonat. Dacă abonarea a eșuat pentru un anumit topic, este specificat un cod de eroare.

### Pachetul `PUBLISH`
![publish packet](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-27/blob/main/img/publish.png)
Pachetul `PUBLISH` este utilizat de un client pentru a **trimite un mesaj** către broker pe un anumit topic. Brokerul redirecționează mesajul către toți clienții abonați la acel topic.

#### Structura Pachetului `PUBLISH`:
- **Fixed Header**:
  - **Packet Type**: Identifică pachetul ca fiind de tip `PUBLISH`.
  - **QoS Level**: Definește calitatea serviciului pentru mesaj (0, 1 sau 2).
  - **DUP Flag**: Indică dacă este o retransmisie a unui mesaj anterior.
  - **Retain Flag**: Indică dacă mesajul ar trebui reținut de broker pentru a fi trimis noilor subscriberi.
- **Variable Header**:
  - **Topic Name**: Specifică topicul pe care este publicat mesajul.
  - **Packet Identifier**: Folosit pentru mesajele QoS 1 și QoS 2 pentru a corela cu răspunsul.
- **Payload**:
  - Conținutul efectiv al mesajului.

### Pachetul `PUBACK`
![publish packet](https://github.com/TUIASI-AC-IoT/proiectrcp2024-2024-echipa-27/blob/main/img/puback.png)
Pachetul `PUBACK` este folosit ca răspuns pentru un mesaj `PUBLISH` de tip QoS 1. Acest pachet confirmă brokerului că mesajul a fost primit de către client. QoS 1 asigură că mesajul este primit cel puțin o dată, iar `PUBACK` finalizează acest proces.

#### Structura Pachetului `PUBACK`:
- **Fixed Header**: Include tipul de pachet.
- **Variable Header**:
  - **Packet Identifier**: Același identificator de pachet ca în pachetul `PUBLISH`, pentru a corela răspunsul cu mesajul original.
- **Payload**:
  - În MQTT 5, poate conține un cod de motiv pentru a specifica succesul sau eșecul confirmării.


---

Acest model de comunicare face din MQTT o alegere populară pentru aplicațiile IoT, unde multe dispozitive au nevoie să schimbe date în mod eficient și organizat.

## Bibliografie

1. [MQTT 5.0 Packet Explained - Connect & CONNACK](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)
2. [Documentația oficială MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
3. [MQTT 5.0 Packet Explained - Connect & CONNACK (EMQX)](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)

---

## Concluzie

Prin această aplicație demonstrativă, am ilustrat procesul de conectare al unui client MQTT5 la un broker HiveMQ, utilizând BSD sockets. Structura pachetelor și mecanismul de confirmare al conexiunii sunt esențiale pentru o comunicare eficientă în rețelele IoT. Această implementare oferă o bază solidă pentru dezvoltarea aplicațiilor IoT care necesită transfer rapid și sigur de date.
