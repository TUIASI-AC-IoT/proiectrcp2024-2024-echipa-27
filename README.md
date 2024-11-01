# MQTT5 CLIENT - APLICAȚIE DEMONSTRATIVĂ

**Autor:** Ciobanu Constantin-Marcu  
**Grupă:** 1307b  

## Descriere

MQTT este un protocol folosit în lumea IoT, permițând transportul de informație rapid, sigur și eficient. Acest protocol permite clienților să se conecteze la un broker (în acest caz am folosit HiveMQ) folosind o tehnică de comunicare prin pachete de tip *publish-subscribe*. Un broker este un serviciu cloud care permite clienților să se conecteze la acesta și să acceseze anumite topice la care sunt conectați alți end-clients.

## Implementare

Folosim modulul BSD socket pentru a efectua conectarea prin TCP/IP la broker-ul nostru în funcția `main`. După conectarea la broker, vom trimite toate pachetele până la întâlnirea unei erori cu ajutorul funcției blocante `sendall`. Pachetul trimis la broker este returnat din funcția ce construiește pachetul de conectare.

Pachetul de conectare (`connect_packet`) trebuie să fie primul pachet trimis de client spre server, în așteptarea unui `CONNACK` (*connect-CONNACK relationship*).

### Structura pachetului de conectare:

- **Fixed Header**
  - conține tipul de pachet pe 4 biți și lungimea rămasă

- **Variable Header**
  - conține numele protocolului,
  - versiunea,
  - metodele de conectare (`connect_flags`, practic ce are nevoie clientul de la server),
  - `keep_alive` în secunde

- **Payload**
  - conține client ID, username și parola

[Link explicativ despre pachetele MQTT5 CONNECT-CONNACK](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)

După trimiterea pachetului la broker, apelăm funcția blocantă `recv`, care va aștepta un pachet de 4 octeți de la broker printr-un socket TCP. Cu ajutorul unei deplasări la dreapta a mesajului primit, vom extrage cei 4 biți și astfel vom confirma dacă pachetul primit este unul de tip `CONNACK`, ce confirmă conectarea cu succes la server.

## Bibliografie

- [MQTT 5.0 Packet Explained - Connect & CONNACK](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)
- [Documentația oficială MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [MQTT 5.0 Packet Explained - Connect & CONNACK (EMQX)](https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b)
