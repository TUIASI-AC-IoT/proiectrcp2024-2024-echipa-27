Ciobanu Constantin-Marcu 1307b
MQTT5 CLIENT. APLICATIE DEMONSTRATIVA
MQTT este un protocol folosit in lumea iot permitand transportul de informatie rapid, sigur si efficient. Acest protocol permite clientilor sa se conecteze la un broker(in acest caz am folosit hivemq) folosing o anumita tehnica de comunicare prin packete de tip publish-subscribe. Un broker este un serviciu cloud care permite clientilor sa se conecteze la acesta si sa acceseze anumite topice la care sunt conectati alti end-clients
Folosim modulul BSD socket pentru a efectua conectarea print tcp/ip la broker-ul nostrum in functia main.
	Dupa conectarea la broker vom trimite toate pachetele pana la intalnirea unei erori cu ajutorul functiei blocante sendall. 
	Pachetul trimis la broker este returnat din functia ce construieste pachetul de conectare.
	Pachetul de conectare connect_pachet trebuie sa fie primul pachet trimis de client spre server in asteparea unui connack (connect-connack relationship). 
	Asadar, pachetul de conectare trebuie sa fie format din :

Fixed Header – 
•	continand pe 4 biti tipul de pachet,lungimea ramasa
Variable header – 
•	continand numele protocolului, 
•	versiunea, 
•	metodele de conectare(connect_flags, practic ce are nevoie clientul de la server) keep_alive in secunde
Payload – client id, username si parola
 
https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b
Dupa trimiterea pachetului la broker, apelam functia blocanta recv ce va astepta un pachet de 4 bytes de la broker printr un socket tcp. Cu ajutorul unei deplasari la dreapta a mesajului primit vom extrage cei 4 biti si astfel vom confirma daca pachetul primit este unul de tip connack ce confirma conectarea cu success la server.



Bibliografie:
https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b
https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
https://emqx.medium.com/mqtt-5-0-packet-explained-01-connect-connack-f941e5c0c61b

Dupa trimiterea pachetului la broker, apelam functia blocanta recv ce va astepta un pachet de 4 bytes de la broker printr un socket tcp. Cu ajutorul unei deplasari la dreapta a mesajului primit vom extrage cei 4 biti si astfel vom confirma daca pachetul primit este unul de tip connack ce confirma conectarea cu success la server.
