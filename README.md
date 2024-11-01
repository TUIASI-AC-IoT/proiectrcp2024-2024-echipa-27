# MQTT5 CLIENT - APLICAȚIE DEMONSTRATIVĂ

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

Pentru a crea un pachet de conectare valid, acesta trebuie să includă următoarele secțiuni:

### Fixed Header

- **Descriere**: Contine informații de bază despre pachet.
- **Conținut**:
  - Tipul de pachet (pe 4 biți)
  - Lungimea rămasă

### Variable Header

- **Descriere**: Informații suplimentare despre conexiune.
- **Conținut**:
  - Numele protocolului (de exemplu, `MQTT`)
  - Versiunea protocolului
  - Metodele de conectare (`connect_flags`), care specifică cerințele clientului de la server
  - Timpul de menținere a conexiunii (keep_alive) în secunde

### Payload

- **Descriere**: Date de autentificare și identificare.
- **Conținut**:
  - Client ID (identificatorul unic al clientului)
  - Username (opțional)
  - Parolă (opțional)

> [Detalii suplimentare despre structura pachetelor CONNECT-CONNACK în MQTT5](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)

---

## Comunicarea cu Brokerul

După trimiterea pachetului de conectare către broker, clientul folosește funcția blocantă `recv` pentru a aștepta un răspuns de la broker, în mod specific un pachet de 4 octeți. Acest răspuns este necesar pentru a confirma dacă brokerul a acceptat conexiunea.

### Validarea Răspunsului `CONNACK`

După ce pachetul este primit de la broker, aplicăm o deplasare la dreapta asupra mesajului pentru a extrage primii 4 biți. Acești biți ne permit să confirmăm dacă pachetul primit este de tip `CONNACK`. Un pachet `CONNACK` validează faptul că brokerul a acceptat conexiunea și că clientul este acum conectat cu succes la server.

---

## Bibliografie

1. [MQTT 5.0 Packet Explained - Connect & CONNACK](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)
2. [Documentația oficială MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
3. [MQTT 5.0 Packet Explained - Connect & CONNACK (EMQX)](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)

---

## Concluzie

Prin această aplicație demonstrativă, am ilustrat procesul de conectare al unui client MQTT5 la un broker HiveMQ, utilizând BSD sockets. Structura pachetelor și mecanismul de confirmare al conexiunii sunt esențiale pentru o comunicare eficientă în rețelele IoT. Această implementare oferă o bază solidă pentru dezvoltarea aplicațiilor IoT care necesită transfer rapid și sigur de date.
