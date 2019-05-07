# Protokollet
## Instruktion
Protokollet ska dokumenteras väl. Dokumentationen ska:

1. Innehålla en utförlig beskrivning av datan som skickas mellan server och klient.

2. Innehålla ett tillståndsdiagram (state diagram) som beskriver vilka tillstånd klienten och servern kan ha samt vad som gör att de övergår från ett tillstånd till ett annat.

3. Vara så detaljerat att en godtycklig student som har klarat kursen kan bygga en ny klient som fungerar med din server utifrån endast protokollet.


# Protokollmetoder

Alla protokollmetoder skickas med en inledande byte som förklarar för mottagaren vilken metod som används (visas genom parentes i listan nedan). Datan som eventuellt överförs med metoden är antingen siffror, strängar eller byte-arrayer.

1. MOVE (1) - Skickas från en klient till servern när användaren vill flytta sig. Består av 3 bytes, där den första byten är en etta för att representera MOVE-metoden och de två andra bytesen representerar förflyttning i x- respektive y-led. Skrivs som signade 8-bit-ints.
Exempel: (Vill flytta mig rakt nedåt ett steg)
0000 0001 0000 0001

2. START (2) - Skickas från server till klient för att meddela att spelet startat. Representeras av en byte med en tvåa som representerar START-metoden.
Exempel: (Spelet startar)
0000 0010

3. MAPTILES (3)  - Skicka kartan som en bytearray från server till klient. Börjar med en byte (3) och sedan storleken på den kvadratiska kartan (0-255) och slutligen kartan i byte-form (varje byte bestående av 1 eller 0)
Exempel: (Servern skickar kartan  "0110" till en spelare)
0100 0010 0000 0000 0000 0001 0000 0001 0000 0000

4. PLAYERPOS (4) - Skickar alla spelares namn och positioner från server till klient. Inleder med en byte (4) och sedan en byte (8 bit int) med antalet spelare och sedan [användarnamn][" "][x][y][#shots] i byteform. Användarnamnet särskiljs alltså från x och y-koordinaten med ett mellanrum.

5. ITEMPOS  (5)  - Skickar alla items och positioner från server till klient. Fungerar ungefär som PLAYERPOS. Inleds med metod-byte (5) , sedan en 8-bit int för antalet items, sedan [itemType][x][y] för alla items.

6. SUCCESS  (6)  - Svar på att en användare faktiskt registrerats

7. SHOT (7)  - Kan skickas av både server och klient. Om det skickas från en klient så ska det tolkas som att en bomb placeras av klienten, om det skickas från en server så ska det tolkas som att en bomb kommer sprängas på en viss position om 4 sekunder.
Exempel:

8. READY (8) - Skickas av klienten när den är redo att börja spela, dvs när den valt sitt namn. Består av en metod-byte (8) följd av klientens önskade användarnamn.

9. GAMEOVER (9) - Skickas från server till en klient när spelet är slut, antingen till följd av en vinst eller en förlust. Inleds med en method-byte (9) följt av en sträng som är det meddelande som kan synas på skärmen för klienten när spelet är slut.

10. ERROR (255) - Skickas för att meddela att något i spelarens förfrågan var felaktigt eller inte gav det resultat som bör vara väntat. Exempelvis om spelaren flyttat till en olaglig position eller om denne försöker flytta sig innan denne är registrerad. Skickas med metod-byte (255) följt av sträng innehållande skälet till att det blev ett error.
