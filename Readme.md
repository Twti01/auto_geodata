Was ist alles in dem Projekt vorhanden: 

1.	Es werden aus einer fetch.py Daten aus dem London Traffic (airquality, bikepoints, station_info, roads) von einer API gezogen und in json Dateien gespeichert. 
2.	Es können über die Kommandozeile Informationen zu bestimmten Stationen abgegriffen werden: Notwendig sind hierfür der Stationsname und entsprechende Flags, die dafür verwendet werden um spezifische Informationen abzugreifen: 
Optionen: -wifi, -location, -baby_change, -bus_interchange, -ramp_route, -lift, -Interchange_info
3.	Mit Flask wird ein Websocket aufgebaut der die bikepoints, airquality, roads Infos in Html darstellt
4.	Man kann über die Kommandozeile eine subscription eingehen: Diese subscription kann nach bedarf Emails verschicken. Mit 
Subsciption login 
Wird die email adresse und das password abgefragt, die in einer config.yaml datei gespeichert werden.
Mit 
Subscription logout 
Kann man sich wieder ausloggen, wodurch die email addresse und das password aus der config datei gelöscht werden
Mit 
Subscription Dailymail
Wird eine tägliche Email versendet die Statusinformationen zum Londoner Traffic absendet 
Dazu gibt es die folgenden flag Möglichkeiten: 
--time erstellt den Eintrag in crontab, zu einer gewissen Uhrzeit, sodass man regelmäßige (daily mails) erhält 
--send sorgt dafür dass die Email gesendet wird, dieser wird für den crontab auftrag dazugeschrieben (man kann ihn aber auch manuell zu jeglicher Uhrzeit schreiben)
Als weiteres kann man Statusemails sich zusenden lassen, wenn man will mit:
Subscription Statusmail
Diese hat folgende flag Möglichkeiten: 
--bikepoints, --pollutants, --roads

Bei diesen Flags kann man auswählen von welchen bikepoints, pollutants und roads man emails bekommen möchte sobald es zu Statusänderungen kommt.
Die email wird zum einen geschickt, wenn man neue bikepoints, pollutants und roads auswählt. Sobald diese aber fest ausgewählt sind werden nur noch Emails verschickt wenn sich der Status ändert. 
Zum Beispiel wenn der Verkehrstatus sich von serious zu good ändert auf der Straße "A1".

Das bash.sh Skript sorgt dafür, dass zum einem das Zeitformat von locale heruntergeladen wird, falls das nicht vorhanden ist. Zum Anderen dafür dass 
ein neues Pyhton environment erstellt wird und in dieses die Packages aus dem requirements.txt heruntergeladen werden. 
Dazu werden in Crontab zwei Aufträge hineingeschrieben. 
Das enthält zum einen das fetching der API Daten aus dem Internet mit der Datei fetch.py, das zur 0. Minute jeder 2 Stunden passiert.
Und es enthält den Auftrag die Statusmail abzusenden, wenn es zu Änderungen. Dies wird auf die 2. Minute jeder 2 Stunden gesetzt, sodass dieses Modul erst durchlaufen wird,
wenn die aktuellen Werte aus dem Internet gezogen wurden (also nach dem fetching). Also sollte es immer zu Veränderungen kommen wird alle 2 Stunden eine Statusemail verschickt.
