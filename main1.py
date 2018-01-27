
# -*- coding: utf-8 -*-
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout, gridplot
from bokeh.models.widgets import TextInput, Div, Select, Button, DataTable, TableColumn, StringFormatter
from bokeh.models import Spacer
import jinja2
import math
import logging
import pandas as pd
import itertools
import grafikai
import CDS


# ši dalis, tam, kad būtų galima reguliuoti TextInput width, nes yra nustatytas Bokeh TextInput default min width,
# kurio negalima mažinti per parametrų nurodymą. Pvz. "invard = TextInput(name = "vard", value="", title = "Vardas", width = 130"
# -per TextInput "name" galima nurodyti kažkokį vardą ir tada per html/css bk-root input[name$="vard"] galima nustatyti norimą width.

curdoc().template = jinja2.Template(source='''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta charset="utf-8">
	<title>{{ title if title else "Žintis tyrimas" }} </title>
	{{ bokeh_css }}
	{{ bokeh_js }}
	<style>
		@import url(https://fonts.googleapis.com/css?family=Noto+Sans);
		body {
			width: 90%;
			height: 100%;
			margin: auto;
			text-align: justify;
			text-justify: inter-word;
			font-family: 'Noto Sans', sans-serif;
			-webkit-font-smoothing: antialiased;
			text-rendering: optimizeLegibility;
			}
			.bk-root input[name$="vard"] {
			min-width: 50px !important;
			width: 100px !important;
			}
			.bk-root input[name$="pavard"] {
			min-width: 50px !important;
			width: 130px !important;
			}
			.bk-root input[name$="lyt"] {
			min-width: 50px !important;
			width: 100px !important;
			}
			.bk-root input[name$="amz"] {
			min-width: 34px !important;
			width: 34px !important;
			}
			.bk-root input[name$="rytas"] {
			min-width: 33px !important;
			width: 33px !important;
			}
			.bk-root input[name$="pietus"] {
			min-width: 33px !important;
			width: 33px !important;
			}
			.bk-root input[name$="vakaras"] {
			min-width: 33px !important;
			width: 33px !important;
			}

			#outer-circle {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 24px;
			width: 24px;
			top: 20%;
			left: 20%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle1 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle1 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 22px;
			width: 22px;
			top: 22%;
			left: 22%;
			margin: 50x 50px 50px 50x;}

			#outer-circle2 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle2 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 20px;
			width: 20px;
			top: 24%;
			left: 24%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle3 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle3 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 18px;
			width: 18px;
			top: 26%;
			left: 26%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle4 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle4 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 16px;
			width: 16px;
			top: 28%;
			left: 28%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle5 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle5 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 14px;
			width: 14px;
			top: 30%;
			left: 30%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle6 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle6 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 12px;
			width: 12px;
			top: 32%;
			left: 32%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle7 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle7 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 10px;
			width: 10px;
			top: 34%;
			left: 34%;
			margin: 50x 50px 50px 50x;
			}

			#outer-circle8 {
			background: white;
			border-radius: 50%;
			border: 1px solid;
			height: 40px;
			width: 40px;
			position: relative;
			}

			#inner-circle8 {
			position: absolute;
			background: black;
			border-radius: 50%;
			height: 8px;
			width: 8px;
			top: 38%;
			left: 38%;
			margin: 50x 50px 50px 50x;
			}

			.foo {
			float: left;
			width: 20px;
			height: 20px;
			margin: 5px;
			border: 1px solid rgba(0, 0, 0, .2);
			}

			.blue {
			background: #13b4ff;
			}

			.purple {
			background: #ab3fdd;
			}

			.wine {
			background: #ae163e;
			}


			table {
			border-collapse: collapse;
			margin-bottom:1%;
			}

			th,td {
			border: 1px solid #c6c7cc;
			padding: 5px 5px;
			}

			th {
			font-weight: bold;
			}

			.overlay {
			position: fixed;
			top: 0;
			bottom: 0;
			left: 0;
			right: 0;
			background: rgba(1, 0, 0, 0.8);
			transition: opacity 0ms;
			visibility: hidden;
			opacity: 1;
			overflow-y:scroll;
			z-index: 99;
			}

			.overlay:target {
			visibility: visible;
			opacity: 1;
			}

			.popup {
			margin: 70px auto;
			padding: 20px;
			background: #fff;
			border-radius: 5px;
			width: 30%;
			position: relative;
			}

			.popup h2 {
			color: #333;
			font-family: Verdana, Arial, sans-serif;
			}

			.popup .close {
			position: absolute;
			right: 20px;
			bottom:0px;
			padding: 0 20 20 0:
			transition: all 0ms;
			font-size: 30px;
			font-weight: bold;
			text-decoration: none;
			color: #333;
			}

			.popup .close:hover {
			color: #06D85F;
			}

			.popup .content {
			max-height: 50%;
			overflow: auto;
			text-align: justify;
			text-justify: inter-word;
			}

			@media screen and (max-width: 100%)
			{
			.box{
			width: 70%;
			}

			.popup{
			width: 80%;
			}
			}
		</style>
	</head>
	<body>
		{{ plot_div|indent(8) }}
		{{ plot_script|indent(8) }}
	</body>
	</html>
''')


# viso tyrimo tekstinė dalis TextInput laukeliais, kuriuose reikia suvesti duomenis.
def protok():
	return Div(text="""<br><b>ORGANIZMO BŪKLĖS TYRIMO PROTOKOLAS</b>""", width=330, height=15)


invard = TextInput(name="vard", value="", title="Vardas", width=130, height=20)
inpavard = TextInput(name="pavard", value="", title="Pavardė", width=160, height=20)
lytis = Select(name="lyt", title="Lytis:", options=["Vyras", "Moteris"], width=130, height=20)
inamz = TextInput(name="amz", value="", title="Amžius", width=80, height=20)


def tikslus():
	return Div(text="""Tikslūs organizmo tyrimo metu atliekamų testų rezultatai padeda geriau suprasti organizme vykstančius procesus,
	todėl tinkamas pasirengimas tyrimui yra labai svarbus tikrajai Jūsų organizmo būklei nustatyti:""", width=750)


def pagrapras():
	return Div(text="""<b>3-2 SAVAITĖS IKI TYRIMŲ DIENOS:</b><br>
Jei tai pirmasis tyrimas, pradedama keisti mityba, jei tai pakartotinis tyrimas, toliau
maitinamasi pagal ankstesnio tyrimo metu pateiktas rekomendacijas. Mitybos keitimas
reikalingas norint padėti:
<br>• organizmui „atidengti“ nukrypimus, nes be pasirengimo, dažnai stebima tiek daug
išsibalansavusių parametrų, kad neįmanoma atskirti nukrypimų.
<br>• tiriamajam įsitikinti, ar šis sveikatinimosi kelias jam tinkamas, nes nustačius
nukrypimų, reikalavimai gali likti tokie patys, sugriežtėti arba sušvelnėti.
<br>• atsistatyti storojo žarnyno mikroflorai, nes nustojus vartoti krakmolą ir pradėjus vartoti
daugiau inertinų (ląstelienos) mikroflora persitvarko mažiausiai per 2 sav.
<br>Keičiant mitybą reikia nustoti vartoti šiuos produktus:
<br><b>Krakmolo šaltinius: </b><i>Bulves ir jų produktus (traškučius, lietuviškas mišraines, tirštas
sriubas, kisielių ir pan.), miltų gaminius (duoną, batoną, bandeles, pyragus, blynus,
makaronus ir pan.), grūdus (kviečius, rugius, ryžius, grikius, avižas, miežius, soras ir pan.),
visas kruopas, dribsnius, ankštinius (pupas, pupeles, lęšius, žirnius). GALIMA VARTOTI
žaliuosius žirnelis ir visas daržoves neribotais kiekiais.</i>
<br><b>Saldžius produktus: </b><i>Saldainius, tortus, pyragėlius, sausainius, šokoladą, ledus, medų,
uogienes, sirupus, sultis, limonadus, vaisius, uogas, alų, likerį, saldų bei pusiau sausą vyną,
saldų bei pusiau sausą putojantį vyną.</i>
<br><b>Polinesočiuosius riebalus: </b><i>Saulėgrąžų, rapsų, sezamų, linų sėmenų, moliūgų sėklų,
nakvišų aliejus, žuvų taukus, saulėgrąžas, sėmenis, sezamų sėklas, visus riešutus (išskyrus
kokosų, migdolų ir lazdyno), pistacijas, soją ir jos produktus, margariną, majonezą, picų
padažus, „tepamus riebalų mišinius", „grietinės ir augalinių riebalų mišinius", „sūrio
produktus“. GALIMA VARTOTI alyvuogių, avokadų, kokosų, migdolų, lazdyno riešutų aliejus,
kakavos sviestą, pieno sviestą, lašinius.</i>
<br><b>Stipriai pakitusius baltymus ir riebalus: </b><i>Savo sultis atidavusią kaitintą mėsą, kietai
virtus arba keptus kiaušinius, mėsos ir žuvies konservus, brandintus ir fermentuotus sūrius,
papildomai termiškai apdorotą varškę, pakartotinai pašildytą maistą. GALIMA VARTOTI iki 2
min. kaitintus kiaušinius, iki 3 min. kaitintą žuvį mažais gabaliukais, iki 5 min. kaitintą
paukštieną mažais gabaliukais, iki 7 min. kaitintą kiaulieną, jautieną, žvėrieną mažais
gabaliukais, nekaitintus baltus sūrius, papildomai nekaitintą varškę.</i>
<br><i>Keletas tinkamų patiekalų pavyzdžių:</i>
<br>• Skystai virtas kiaušinis su burokėlių salotomis
<br>• Varškė su grietine ir avokadais
<br>• Troškintos morkos, petražolių šaknys ir pomidorai su mėsos gabaliukais
<br>• Garintas upėtakis su pomidorais, salotomis ir alyvuogių aliejumi
<br>• Grūdėta varškė su žaliaisiais konservuotais žirneliais
<br>• Žali arba troškinti kalafioro griežinėliai grietinės padaže su žolelėmis
<br>• Šaltibarščiai
<br>• Graikiškos salotos<br>
<br><b>MAŽIAUSIAI 2 DIENOS IKI TYRIMŲ DIENOS:</b>
<br>Nuo ryto nustojamos vartoti šios medžiagos: <b>Kava, arbata, kakava, šokoladas, energiniai gėrimai, rūkalai, alkoholis, gazuoti
gėrimai, maisto papildai ir vaistai </b>(IŠSKIRTINIAIS ATVEJAIS, kai vaistų nutraukimas tokiam ilgam periodui gali sukelti pavojų gyvybei,<b> vaistų
nevartoti bent 1 dieną prieš tyrimą)</b>. <i>GALIMA VARTOTI žolelių arbatas, rooibos arbatą</i>. Iki tyrimo neužsiimama intensyvia arba ilgalaike fizine veikla.
<br>
<br><b>TYRIMŲ DIENOS IŠVAKARĖSE:</b>
<br>Jei kitą dieną matavimus atliks sutartu metu atvykęs asmuo, nuo pietų pradedami rinkti 3
šlapimo mėginiai:
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apiepiet – prieš pietus arba bent 2 val. po valgio.</i>
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Vakare – prieš pat miegą, bent 2 val. po valgio.</i>
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ryte – prieš pusryčius, ne vėliau nei 30 min. nuo atsikėlimo.</i>
<br>Šlapimo mėginys imamas į indelius, skirtus šlapimui, jų galima įsigyti vaistinėse. Mėginio
tūris turi būti 60 ml. Mėginius reikia pažymėti, kad jie nebūtų supainioti.
<br><b>Jei kitą dieną matavimai bus atliekami 3 kartus, šlapimo mėginiai imami ir tiriami
tyrimų dieną.</b>
<br>
<br><b>TYRIMŲ DIENĄ:</b>
<br>Tyrimų dieną galima valgyti, bet vis dar laikantis ankstesnių mitybos nurodymų. Iki tyrimo
reikia būti bent 2 val. nevalgius ir bent 30 min. iki tyrimo nieko nekramtyti, tačiau galima
atsigerti negazuoto nešalto vandens.
<br>Jei tyrimą atlieka sutartu laiku atvykęs asmuo, tyrimo metu ištiriami visi 3 šlapimo
mėginiai ir atliekami kitų parametrų matavimai.
<br>Jei tyrimas atliekamas 3 kartus, kiekvienas šlapimo mėginys tiriamas ir kiti parametrai
matuojami po šlapimo mėginio paėmimo, leidus jam atvėsti iki kambario temperatūros.
<br><b>Šlapimo mėginiai tiriami ir kiti parametrai matuojami pagal „Tyrimo aprašą“</b>,
duomenys surašomi į<b>„Organizmo būklės tyrimo formos“</b> skiltį<i>„Tyrimo protokolas“</i>.
<br><b>Atlikus tyrimą ir nustačius organizmo būklę pradedama maitintis pagal būklę
atitinkančias rekomendacijas.</b>
<br>
<br><b>ORGANIZMO BŪKLĖS TYRIMO EIGA:</b>
<br>Organizmo būklės nustatymo tikslumui lemiamos įtakos turi tikslūs organizmo parametrų išmatavimai.
Šiuos parametrus stipriai veikia tiriamojo psichologinė būklė tyrimo metu, taip pat matavimų eilės tvarka.
Svarbu, kad organizmo būklės tyrimas būtų vykdomas griežtai pagal nurodytą seką.
Taip pat rekomenduotina kelias dienas iki tyrimo pasipraktikuoti jį atlikti, kad tyrimo dieną viskas vyktų sklandžiai.
Tyrimo trukmė apie 45 minutės. Pamatuoti duomenys rašomi į <b>„Organizmo būklės tyrimo formos“ </b>skiltį<b><i> „Tyrimo protokolas“</i></b>.
<br><b>PRIEMONĖS</b>:
<br>•pH metras arba daugiaspalėvės rūgštingumo matavimo juostelės (tikslumas bent 0,5, minimalios skalės ribos nuo 4,5 iki 8)
<br>•Areometras (kuo mažesnis, minimalios skalės ribos nuo 1,000 g/ml iki 1,030 g/ml) ir pritaikytas matavimo cilindras jam.
<br>•Chronometras
<br>•Skaitmeninis kraujospūdžio matuoklis (su manžete ant žasto)
<br>•Kūno termometras
<br>•Kūno svarstyklės
<br>•Indeliai šlapimo mėginiams
<br>•Įrankis brėžimui neužapvalintu galu (įtrauktas tušinukas, bambukinė lazdelė ir pan.)
<br>•Popierinis rankšluostis
<br>•Valgomasis šaukštas
<br>•Minkštas metras
<br><br><b>TYRIMO EIGA:</b>
<br><b>1.</b> 2 valandos iki tyrimo <b><i>nevalgyti</b></i>, jei norisi, <b><i>galima gerti negazuoto vandens</b></i>.
<br><b>2.</b> 30 minučių iki tyrimo <b><i>nieko negerti ir nekramtyti</b></i>.
""", width=1300)


def slapimo():
	return Div(text="""<b>3. Šlapimo parametrų matavimas:</b>""", width=300)


def aprslarugs():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup5"><br>Rūgštingumas<br>(rodmuo ekrane arba pagal spalvos skalę)</a>
</div>

<div id="popup5" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Rūgštingumas</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Jei turimas rūgštingumo matuoklis, matuojama pagal jo instrukcijas.
Sukalibruoto matuoklio daviklis merkiamas į šlapimą, lengvai pamaišoma ir laukiama, kol
nusistovės rodmuo. Vertė įrašoma eilutėje 2.1 „Rūgštingumas (matuokliu), U-pH 1 “. Atlikus
matavimą, matuoklio daviklis nuplaunamas pamaišant stiklinėje su čiaupo vandeniu, po
to su distiliuotu vandeniu ir nusausinamas, priglaudus (bet netrinant) švelnia servetėlė.
<i>Jei naudojamos tik rūgštingumo matavimo juostelės, šis punktas praleidžiamas</i>.
<br>Rūgštingumo matavimo juostelės naudojamos pagal jų instrukcijas, nurodytas ant
dėžutės. Juostelės spalvinės zonos merkiamos į šlapimą, pamaišoma, ištraukiama,
padedama ant popierinio rankšluosčio spalvinėmis zonomis į viršų ir paleidžiamas
chronometras. Po instrukcijoje nurodyto laiko stebimi spalvinių zonų atspalviai, jie
lyginami su skale ant dėžutės. Vertė įrašoma eilutėje 2.2 „Rūgštingumas (juostele),
U-pH 2 “.<i>Jei naudojamas tik matuoklis, šis punktas praleidžiamas</i>.
		</div>
	</div>
</div>
	""", width=250)


slarugrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
slarugpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
slarugvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprslasvies():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup6"><br>Šviesumas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup6" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Šviesumas</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Šlapimo mėginys įpilamas į matavimo cilindrą iki atitinkamos ribos, kad įmerktas areometras galėtų pilnai panirti ir šlapimas neišsilietų.
Matavimo cilindras pastatomas gerai apžviestoje vietoje be tiesioginių spindulių baltame fone (rašomojo popieriaus lapo),
stebimas ir vertinamas vizualiai. Eilutėje 2.4 „Šviesumas, U-šv“ nurodomas šlapimo šviesumas pagal žemiau pateiktoje skalėje šlapimo spalvą
atitinkančio stulpelio numerį:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Spalva</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td><div class="foo blue"></div></td>
		<td>Ruda, artima pieniškam šokoladui arba obuolių kompotui</td>
	</tr>
	<tr>
		<td>+3</td>
		<td><div class="foo purle"></div></td>
		<td>Ruda kaip stipri žalioji arbata</td>
	</tr>
	<tr>
		<td>+2</td>
		<td><div class="foo wine"></div></td>
		<td>Rusva kaip silpna žalioji arbata arba šviesus alus</td>
	</tr>
	<tr>
		<td>+1</td>
		<td><div class="foo blue"></div></td>
		<td>Geltona, bet nešvyti</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><div class="foo purle"></div></td>
		<td>Ryški ir švytinti geltona</td>
	</tr>
	<tr>
		<td>-1</td>
		<td><div class="foo wine"></div></td>
		<td>Geltona, šiek tiek švyti, kaip baltas vynas</td>
	</tr>
	<tr>
		<td>-2</td>
		<td><div class="foo blue"></div></td>
		<td>Gelsva, nešvyti</td>
	</tr>
	<tr>
		<td>-3</td>
		<td><div class="foo purle"></div></td>
		<td>Spalva labai silpna, bet regima</td>
	</tr>
	<tr>
		<td>-4</td>
		<td><div class="foo wine"></div></td>
		<td>Visiškai bespalvė, beveik kaip vanduo</td>
	</tr>
</table>
		</div>
	</div>
</div>
	""", width=250)


slasvrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
slasvpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
slasvvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprslatank():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup7"><br>Tankis<br>(rodmuo, g/ml)</a>
</div>

<div id="popup7" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Tankis</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Matavimo cilindras su šlapimu pastatomas ant tvirto pagrindo ir į jį
įmerkiamas areometras. Kai aerometras nustoja svyruoti, jis labai lengvai stumtelimas iš
viršau, kad dar susvyruotų. Nusistovėjus skalės rodmuo atskaitomas ties menisko
(įgaubto vandens paviršiaus) apačia ir įrašoma eilutėje 2.3 „Tankis, d“. Jei areometras
pritraukiamas prie matavimo cilindro sienelės, reikia jį ištraukti, nuplauti, nusausinti ir
matavimą pakartoti.
		</div>
	</div>
</div>
	""", width=250)


slatankrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
slatankpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
slatankvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprslaputo():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup8"><br>Putojimas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup8" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Putojimas</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Šlapimo mėginys supilamas atgal į indelį, tvirtai užsukamas ir plakamas
10 sekundžių. Po to pastatomas ant popierinio rankšluosčio, iškart atsukamas ir
paleidžiamas chronometras. Stebima, kada centre prasiskirs putos. Vertinama pagal
skalę ir įrašoma eilutėje 2.5 „Putojimas, U-put“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+3</td>
		<td>putos prasiskiria per daugiau nei 15 min.</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>putos prasiskiria per 15 min.</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>putos prasiskiria per 5 min.</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>putos prasiskiria per 1 min.</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>atsukus putos jau prasiskyrusios</td>
	</tr>
</table>
		</div>
	</div>
</div>
	""", width=250)


slaputrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
slaputpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
slaputvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def prikseil():
	return Div(text="""<b > 4.</b><i>Tiriamojo paprašoma prikaupti seilių ir įspjauti į valgomąjį šaukštą. Seilių turi būti
maždaug mažojo piršto galinio narelio dydžio lašas.</i>""", width=750)


def seiliu():
	return Div(text="""<b>5. Seilių parametrų matavimas:</b>""", width=300)


def aprseilrugst():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup9"><br>Rūgštingumas<br>(rodmuo ekrane arba skaičius pagal skalę)</a>
</div>

<div id="popup9" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Rūgštingumas</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Jei turimas rūgštingumo matuoklis, matuojama pagal jo instrukcijas.
Sukalibruoto matuoklio daviklis merkiamas į seiles ir laukiama, kol nusistovės rodmuo (jei
daviklis ne stiklinis, tuomet seilių lašas užlašinamas ant jautrios zonos). Vertė įrašoma
eilutėje 3.1 „Rūgštingumas (matuokliu), S-pH 1 “. Atlikus matavimą, matuoklio daviklis
nuplaunamas pamaišant stiklinėje su čiaupo vandeniu, po to su distiliuotu vandeniu ir
nusausinamas, priglaudus (bet netrinant) švelnia servetėlė. Jei naudojamos tik
rūgštingumo matavimo juostelės, šis punktas praleidžiamas.
<br>Rūgštingumo matavimo juostelės naudojamos pagal jų instrukcijas, nurodytas ant
dėžutės. Juostelės spalvinėmis zonos žemyn merkiamos į seiles, pamaišoma,
ištraukiama, padedama ant popierinio rankšluosčio spalvinėmis zonomis į viršų ir
paleidžiamas chronometras. Po instrukcijoje nurodyto laiko seilių perteklius
nusausinamas į servetėlę nebraukiant, stebimi spalvinių zonų atspalviai, jie lyginami su
skale ant dėžutės. Vertė įrašoma eilutėje 2.2 „Rūgštingumas (juostele), S-pH 2 “.<i>Jei
naudojamas tik matuoklis, šis punktas praleidžiamas</i>.
		</div>
	</div>
</div>
	""", width=250)


serrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
serpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
servakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprseilklamp():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup10"><br>Klampumas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup10" class="overlay">
	<div class="popup">
		<h2>Klampumas</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Kol laukiama rūgštingumo duomenų, valgomasis šaukštas su likusiu
seilių mėginiu pavartomas, kad pagal jų tekėjimą vizualiai būtų galima įvertinti jų
klampumą. Klampumas vertinamas pagal skalę ir vertė įrašoma į eilutę 3.3 “Klampumas,
S-kl”:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+2</td>
		<td>tirštos, daug putų, neteka</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>Labai klampios, kaip sirupas, teka lėtai</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>vidutiniškai klampios, kaip žalias kiaušinio baltymas</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>skystos, bet klampesnės už vandenį, kaip liesas kefyras</td>
	</tr>
	<tr>
		<td>-2</td>
		<td>visiškai skystos, kaip vanduo</td>
	</tr>
</table>
		</div>
	</div>
</div>
	""", width=250)


sekrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
sekpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
sekvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def tiriam():
	return Div(text="""<b>6.</b><i>Tiriamojo paprašoma atsisėsti ant sofos arba lovos per vidurį.</i>""", width=780)


def kraujot():
	return Div(text="""<b>7. Kraujotakos parametrų matavimas:</b>""", width=300)


def aprpulsed():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup11"><br>Pulsas sėdint<br>(dūžių skaičius per 15 s,×4)</a>
</div>

<div id="popup11" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Pulsas sėdint</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Užčiuopiamas pulsas ant tiriamojo riešo, tai geriausia padaryti trimis
pirštais, sudėtais greta – šoninius pirštus spaudžiant prie kaulo šiek tiek stipriau nei
vidurinį tam tikru metu pradedamas justi tvinkčiojimas. Jei tvinkčiojimas matavimo metu
silpnėja, reikia keisti atskirų pirštų spaudimą, kol vėl pajuntamas tvinkčiojimas.
<br>Užčiuopus pulsą, 5-10 dūžių stebima, ar pulsas tolygus, ar nėra aritmijos, ar
tiriamasis nusiraminęs. Tada su dūžiu paleidžiamas chronometras ir 15 sekundžių
skaičiuojami širdies dūžiai. Jei laikas baigėsi anksčiau, nei įvyko paskutinis širdies dūžis,
prie pilnų dūžių skaičiaus dar pridedama 0,5. Gautą skaičių padauginus iš 4 gauname
pulsą sėdint, šis skaičius įrašomas eilutėje 5.1 „Pulsas sėdint, P sėd “.
<br><font size="1"><i>Pvz: Jei chronometras rodo 0:14, o Jūs mintyse esate suskaičiavęs 18 dūžių, 19-tą dūžį
pajuntate tuo pat metu, kaip chronometras parodo 0:15. Tuomet į juodraštį užsirašote
skaičių „19”, o pulsas bus P sėd = 4×19 = 76.
Jei chronometras rodo 0:14, o Jūs mintyse esate suskaičiavęs 18 dūžių, tačiau 19-tą dūžį
pajuntate po to, kaip chronometras parodo 0:15. Tuomet į juodraštį užsirašote skaičių
„18,5”, o pulsas bus P sėd = 4×18,5 = 74.</i></font>
		</div>
	</div>
</div>
	""", width=250)


psrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pspietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
psvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def refleksu():
	return Div(text="""<b>8. Refleksų tyrimas:</b>""", width=300)


def aprkunotemp():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup12"><br>Kūno temperatūra</a>
</div>

<div id="popup12" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Kūno temperatūra</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Kūno termometras naudojamas pagal jo naudojimo instrukciją.
<br>Jei matuojama infraraudonųjų spindulių (IR) termometru, matuojama ausies angos
vidaus temperatūra.
<br>Jei matuojama skaitmeniniu kontaktiniu termometru, matuojama burnos gleivinės
temperatūra po liežuviu.
<br>Jei matuojama skystiniu termometru (gyvsidabriniu, spiritiniu), prieš tai jis
nupurtomas iki 35,5 °C rodmens ir tada tiriamojo paprašoma jį įsidėti į kairės rankos
pažastį, matuojama 5-7 minutes. Temperatūros rodmuo Celsijaus laipsniais su vienu
skaičiumi po kablelio įrašomas eilutėje 4.1 „Kūno temperatūra, Temp“.
		</div>
	</div>
</div>
	""", width=250)


ktrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
ktpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
ktvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprdermoref():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup13"><br>Dermografinis refleksas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup13" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Dermografinis refleksas</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo paprašoma atsiraitoti dešinės rankos rankovę,
atidengiant bicepsą. Žinomo pločio, neaštriu, bet neužapvalintu daiktu (pavyzdžiui,
įtrauktu tušinuku, bambukine valgymo lazdele ir pan.) ne per stipriai brėžiamos
besikryžiuojančios linijos ant paciento dešinės rankos vidinės pusės per 3 pirštus nuo
linkio vietos. Pirma ant dilbio, po to ant žasto. Paleidžiamas chronometras. Stebima
paciento reakcija po 1 min. ir po 6 min. Vertinama pagal skalę ir įrašoma eilutėje 4.2
„Dermografizmas, Dermo“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td>po 1 minutės paraudimas su iškilumais arba daugiau nei 2 cm pločio paraudimas</td>
	</tr>
	<tr>
		<td>+3</td>
		<td>po 6 minučių paraudimas su iškilumais arba daugiau nei 2 cm pločio paraudimas</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>po 6 minučių raudonos linijos ant žasto ir ant dilbio platesnės nei brėžiklis</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>po 6 minučių raudonos linijos ant žasto ir ant dilbio</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>po 6 minučių raudonos linijos ant žasto, bet jokio paraudimo ant dilbio</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>po 6 minučių jokio paraudimo</td>
	</tr>
	<tr>
		<td>-2</td>
		<td>po 1 minutės jokio paraudimo</td>
	</tr>
</table>
		</div>
	</div>
</div>
	""", width=250)


drrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
drpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
drvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprvasomref():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup14"><br>Vasomotorinis refleksas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup14" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Vasomotorinis refleksas</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Vienos rankos delnu lieskite tiriamojo tricepsą (žasto
nugarinę dalį), o kitos rankos delnu – tiriamojo plaštakos išorinę pusę. Kelis kartus
rankas sukeiskite ir lyginkite tricepso ir plaštakos temperatūrų skirtumą. Vertinama pagal
skalę ir įrašoma eilutėje 4.3 „Vasomotorinis, Vaso“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td>plaštaka labai stipriai karštesnė už žastą</td>
	</tr>
	<tr>
		<td>+3</td>
		<td>plaštaka ryškiai šiltesnė už žastą ir/arba prakaituotas delnas</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>plaštaka vos šiltesnė už žastą</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>plaštakos ir žasto temperatūros vienodos</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>plaštaka vos vėsesnė už žastą</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>plaštaka ryškiai vėsesnė už žastą</td>
	</tr>
	<tr>
		<td>-2</td>
		<td>plaštaka akivaizdžiai vėsesnė už žastą</td>
	</tr>
	<tr>
		<td>-3</td>
		<td>plaštaka stipriai vėsesnė už žastą ir/arba prakaituotas delnas</td>
	</tr>
	<tr>
		<td>-4</td>
		<td>plaštaka labai stipriai šaltesnė už žastą</td>
	</tr>

</table>
		</div>
	</div>
</div>
	""", width=250)


vrrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
vrpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
vrvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprvyzdyd():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup15"><br>Vyzdžio dydis<br>(skaičius pagal skalę)</a>
</div>

<div id="popup15" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Vyzdžio dydis</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo regos lauke neturi būti ryškios šviesos (lempos ar lango),
geriausia, kad jis sėdėtų priešais šviesios spalvos sieną. Pakeliamas pirštas prieš
tiriamojo akis maždaug per dilbio ilgio atstumą nuo veido. Paprašoma žvilgsnį
sufokusuoti į pirštą, kai vyzdžio dydis nusistovi paprašoma žvilgsnį sufokusuoti į sieną
priešais tiriamąjį, ir vėl laukiama, kol vyzdžio dydis nusistovi. Taip kartojama kelis kartus,
stebima, apie kokį plotį svyruoja vyzdys. Vertinama pagal skalę ir įrašoma eilutėje 4.4
„Vyzdžio dydis, Vyzd“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Vaizdas</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td><div id="outer-circle">
			<div id="inner-circle">
				</div>
					</div></td>
		<td>Vyzdys 2 kartus didesnis už rainelės plotį tarp vyzdžio ir krašto</td>
	</tr>
	<tr>
		<td>+3</td>
		<td><div id="outer-circle1">
			<div id="inner-circle1">
				</div>
					</div></td>
		<td></td>
	</tr>
	<tr>
		<td>+2</td>
		<td><div id="outer-circle2">
			<div id="inner-circle2">
				</div>
					</div></td>
		<td>Vyzdys 1,5 karto didesnis už rainelės plotį tarp vyzdžio ir krašto</td>
	</tr>
	<tr>
		<td>+1</td>
		<td><div id="outer-circle3">
			<div id="inner-circle3">
				</div>
					</div></td>
		<td></td>
	</tr>
	<tr>
		<td > 0</td>
		<td><div id="outer-circle4">
			<div id="inner-circle4">
				</div>
					</div></td>
		<td><b>Vyzdžio dydis toks pat, kaip rainelės plotis tarp vyzdžio ir krašto</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td><div id="outer-circle5">
			<div id="inner-circle5">
				</div>
					</div></td>
		<td></td>
	</tr>
	<tr>
		<td>-2</td>
		<td><div id="outer-circle6">
			<div id="inner-circle6">
				</div>
					</div></td>
		<td>Vyzdys 1,5 karto mažesnis už rainelės plotį tarp vyzdžio ir krašto</td>
	</tr>
	<tr>
		<td>-3</td>
		<td><div id="outer-circle7">
			<div id="inner-circle7">
				</div>
					</div></td>
		<td></td>
	</tr>
	<tr>
		<td>-4</td>
		<td><div id="outer-circle8">
			<div id="inner-circle8">
				</div>
					</div></td>
		<td>Vyzdys 2 kartus mažesnis už rainelės plotį tarp vyzdžio ir krašto</td>
	</tr>

</table>
		</div>
	</div>
</div>
	""", width=250)


vdrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
vdpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
vdvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprtremoref():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup16"><br>Tremoro (drebulio) refleksas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup16" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Tremoro (drebulio) refleksas</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo paprašoma išsižioti ir iškišti liežuvį tiesiai į
priekį. Stebimas liežuvio judesys ir raumenų drebulys. Jei reikia, patikrinamas ir galūnių
drebulys, padedant popieriaus lapą ant į šoną ištiestos iš delnu į viršų pasuktos
plaštakos, kai tiriamasis žiūri tiesiai. Vertinama pagal skalę ir įrašoma eilutėje 4.5
„Tremoras (drebulys), Trem“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td>ypatingai didelis liežuvio ir galūnių drebulys</td>
	</tr>
	<tr>
		<td>+3</td>
		<td>didelis liežuvio drebulys ir pastebimas galūnių drebulys</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>vidutinis liežuvio drebulys ir stiprus judesys (negali išlaikyti vietoje)</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>lengvas liežuvio drebulys ir judesys</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>jokio liežuvio drebulio ir lengvas liežuvio judesys</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>jokio liežuvio drebulio ir labai mažas liežuvio judesys</td>
	</tr>
	<tr>
		<td>-2</td>
		<td>absoliučiai jokio liežuvio drebulio ir judesio</td>
	</tr>
</table>
		</div>
	</div>
</div>
	""", width=250)


trrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
trpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
trvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprsneruzgu():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup17"><br>Šnervių užgulimas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup17" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Šnervių užgulimas</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo paprašoma pirštu užspausti dešiniąją šnervę ir kelis
kartus įkvėpti bei iškvėpti per kairiąją, po to paprašoma tą patį padaryti su kita šnerve.
Tiriamojo paprašoma apibūdinti kvėpavimo lengvumą. Vertinama pagal skalę ir įrašoma į
eilutę 4.6 „Šnervių užgulimas, Nos“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td>Dešinė šnervė visiškai užgulta, pro kairę kvėpuojama lengviau.</td>
	</tr>
	<tr>
		<td>+3</td>
		<td>Dešinė šnervė užgulta labiau nei kairė, bet orą su jėga galima prapūsti.</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>Pro dešinę šnervę kvėpuojama, bet reikia pridėti papildomos jėgos (ilgaikvėpuojant pavargstama), pro kairę kvėpuojama lengviau.</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>Pro dešinę šnervę kvėpuojama laisvai, bet jaučiamas švilpimas, kairėje švilpimas nejaučiamas.</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>Pro abi šnerves kvėpuojama laisvai be jokio pasipriešinimo ar švilpimo.</b></td>
	</tr>
	<tr>
		<td>-1</td>
		<td>Pro kairę šnervę kvėpuojama laisvai, bet jaučiamas švilpimas, dešinėje švilpimas nejaučiamas.</td>
	</tr>
	<tr>
		<td>-2</td>
		<td>Pro kairę šnervę kvėpuojama, bet reikia pridėti papildomos jėgos (ilgai kvėpuojant pavargstama), pro dešinę kvėpuojama lengviau.</td>
	</tr>
	<tr>
		<td>-3</td>
		<td>Kairė šnervė užgulta labiau nei dešinė, bet orą su jėga galima prapūsti.</td>
	</tr>
	<tr>
		<td>-4</td>
		<td>Kairė šnervė visiškai užgulta, pro dešinę kvėpuojama lengviau.</td>
	</tr>

</table>
		</div>
	</div>
</div>
	""", width=250)


surytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
supietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
suvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def tiriam1():
	return Div(text="""<i>Tiriamojo paprašoma atsigulti ant sofos ar lovos ant kurios sėdi. Gulamasi
ištiestomis kojomis, galvą dedant taip, kad prie sofos ar lovos krašto būtų tiriamojo kairė
pusė. Paliekamas toks tarpas nuo sofos ar lovos krašto, kad tiriamojo kairė ranka laisvai
gulėtų šalia delnu į viršų. Paprašoma atsipalaiduoti, nekalbėti ir nusiraminti. Taip
tiriamasis turi pagulėti daugiau nei 1 minutę.</i>""", width=750)


def aprsarglinref():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup18"><br>Sargento linijos refleksas<br>(skaičius pagal skalę)</a>
</div>

<div id="popup18" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Sargento linijos refleksas</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo paprašoma atidengti pilvą nuo bambos iki
krūtinkaulio. Žinomo pločio, neaštriu daiktu (pavyzdžiui, įtrauktu tušinuku, bambukine
valgymo lazdele ir pan.) labai lengvai, spaudžiant tik daikto svoriui, braukiama per pilvo
odą nuo bambos link krūtinkaulio. Paleidžiamas chronometras ir stebimas linijos
išryškėjimas. Vertinama pagal skalę ir įrašoma į eilutę 4.7 „Sargento linija, Sarg“:
<table>
	<tr>
		<th scope="col"><b>Vertė</b></th>
		<th scope="col"><b>Aprašymas</b></th>
	</tr>
	<tr>
		<td>+4</td>
		<td>balta linija pasirodo per 15 s ir išlieka daugiau nei 1 min.</td>
	</tr>
	<tr>
		<td>+3</td>
		<td>balta linija pasirodo per 15 s ir išlieka mažiau nei 1 min.</td>
	</tr>
	<tr>
		<td>+2</td>
		<td>balta linija pasirodo vėliau nei po 15 s.</td>
	</tr>
	<tr>
		<td>+1</td>
		<td>balta linija pasirodo vėliau nei po 30 s.</td>
	</tr>
	<tr>
		<td > 0</td>
		<td><b>balta linija per 1 min. nepasirodo.</b></td>
	</tr>
</table>
		<i>Šio tyrimo metu patogu kartu atlikti ir kvėpavimo dažnio matavimą.</i></div>
	</div>
</div>
	""", width=250)


slrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
slpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
slvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def tiriam2():
	return Div(text="""<b>9.</b><i>Tiriamajam pranešama, kad jis jau gali užsidengti pilvą ir paprašoma atsipalaiduoti,
nekalbėti ir nusiraminti. Taip tiriamasis turi pagulėti daugiau nei 1 minutę.</i></b>""", width=750)


def kvepparmat10():
	return Div(text="""<b>10. Kvėpavimo parametrų matavimas:</b>""", width=300)


def aprkvepdaz():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup19"><br>Kvėpavimo dažnis<br>(Įkvėpimo-iškvėpimo ciklų<br>skaičius per 30 s,×2)</a>
</div>

<div id="popup19" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Kvėpavimo dažnis</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamojo kairėje rankoje užčiuopiamas pulsas (kad tiriamasis
nežinotų, jog stebimas jo kvėpavimas) ir akies kampu stebimas pilvo ir krūtinės
kilnojimasis. Įsitikinama, kad kvėpavimas tolygus ir nėra nevalingų kvėpavimo sulaikymų
ilgesniam laikui. Kai tiriamasis yra iškvėpęs, paleidžiamas chronometras. 30 sekundžių
skaičiuojami pilni įkvėpimo-iškvėpimo ciklai. Jei laikas baigėsi anksčiau, nei tiriamasis
iškvepia paskutinį kartą, tai prie pilnų ciklų skaičiaus pridedama trupmeninė dalis pagal
kriterijus:
<br>• jei laikas baigėsi tiriamajam įkvėpinėjant, tai +0,25
<br>• jei laikas baigėsi tiriamajam įkvėpus, tai +0,5
<br>• jei laikas baigėsi tiriamajam iškvėpinėjant, tai +0,75
<br>Gautą skaičių padauginus iš 2 gaunamas kvėpavimo dažnis, jis įrašomas eilutėje 6.1
„Kvėpavimo dažnis, KD“.
<br><font size="1"><i>Pavyzdžiui: Chronometras rodo 0:29, o Jūs mintyse esate suskaičiavęs 7 pilnų ciklų.
Chronometras parodo 0:30, kai tiriamais įkvėpinėja, tuomet į juodraštį užsirašote skaičių
„7,25”, ir kvėpavimo dažnis bus KD = 2×7,25 = 14,5.
Chronometras parodo 0:30, kai tiriamais yra pilnai įkvėpęs, tuomet į juodraštį užsirašote
skaičių „7,5”, ir kvėpavimo dažnis bus KD = 2×7,5 = 15.
Chronometras parodo 0:30, kai tiriamais iškvėpinėja, tuomet į juodraštį užsirašote skaičių
„7,75”, ir kvėpavimo dažnis bus KD = 2×7,75 = 15,5.
Chronometras parodo 0:30, kai tiriamais pilnai iškvėpė, tuomet į juodraštį užsirašote
skaičių „8”, ir kvėpavimo dažnis bus KD = 2×8 = 16.</i>/div>
	</div>
</div>
	""", width=250)


kdrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
kdpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
kdvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def tiriam3():
	return Div(text="""<b>11.</b><i>Tiriamajam ant kairės rankos žasto uždedama kraujospūdžio matavimo manžetė.</i>""", width=750)


def kraujparmat():
	return Div(text="""<b>12. Kraujotakos parametrų matavimas:</b>""", width=300)


def aprpulgul():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup20"><br>Pulsas gulint<br>(dūžių skaičius per 15 s,×4)</a>
</div>

<div id="popup20" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Pulsas gulint</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Užčiuopiamas pulsas ant tiriamojo riešo, tai geriausia padaryti trimis
pirštais, sudėtais greta – šoninius pirštus spaudžiant prie kaulo šiek tiek stipriau nei
vidurinį tam tikru metu pradedamas justi tvinkčiojimas. Jei tvinkčiojimas matavimo metu
silpnėja, reikia keisti atskirų pirštų spaudimą, kol vėl pajuntamas tvinkčiojimas.
<br>Užčiuopus pulsą, 5-10 dūžių stebima, ar pulsas tolygus, ar nėra aritmijos, ar
tiriamasis nusiraminęs. Tada su dūžiu paleidžiamas chronometras ir 15 sekundžių
skaičiuojami širdies dūžiai. Jei laikas baigėsi anksčiau, nei įvyko paskutinis širdies dūžis,
prie pilnų dūžių skaičiaus dar pridedama 0,5. Gautą skaičių padauginus iš 4 gauname
pulsą gulint, šis skaičius įrašomas eilutėje 5.1 „Pulsas gulint, P sėd “.
<br><font size="1"><i>Pvz: Jei chronometras rodo 0:14, o Jūs mintyse esate suskaičiavęs 18 dūžių, 19-tą dūžį
pajuntate tuo pat metu, kaip chronometras parodo 0:15. Tuomet į juodraštį užsirašote
skaičių „19”, o pulsas bus P gul = 4×19 = 76.
Jei chronometras rodo 0:14, o Jūs mintyse esate suskaičiavęs 18 dūžių, tačiau 19-tą dūžį
pajuntate po to, kaip chronometras parodo 0:15. Tuomet į juodraštį užsirašote skaičių
„18,5”, o pulsas bus P gul = 4×18,5 = 74.</i></font>
		</div>
	</div>
</div>
	""", width=250)


pgrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pgpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pgvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprsiskraujgul():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup21"><br>Sistolinis kraujospūdis gulint<br>(rodmuo ekrane ties „SYS“)</a>
</div>

<div id="popup21" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Sistolinis kraujospūdis gulint</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Manžetė pripumpuojama oro iki slėgio 180-200 mmHg ir
pamatuojamas kraujospūdis. Sistolinis kraujospūdis (didesnis rodmuo ties užrašu „SYS“)
įrašomas eilutėje 5.3 „Sistolinis kraujospūdis gulint, Sis 1“,
		</div>
	</div>
</div>
	""", width=250)


skgrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
skgpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
skgvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprdiakraujgul():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup22"><br>Diastolinis kraujospūdis gulint<br>(rodmuo ekrane ties „DIA“)</a>
</div>

<div id="popup22" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Diastolinis kraujospūdis gulint</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Manžetė pripumpuojama oro iki slėgio 180-200 mmHg ir
pamatuojamas kraujospūdis. Diastolinis kraujospūdis (mažesnis rodmuo ties užrašu „DIA“ ) įrašomas eilutėje 5.4 „Diastolinis kraujospūdis
gulint, Dia 1 “.
		</div>
	</div>
</div>
	""", width=250)


dkgrytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
dkgpietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
dkgvakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def ortatest():
	return Div(text="""<b>Ortostatinis testas.</b> Tiriamajam atsistojus, kraujospūdžio matuoklio žarnelė neturi
būti tempiama, todėl matuoklį reikia <i>padėti ant paaukštinimo, pritvirtinti prie manžetės
arba duoti laikyti tiriamajam laisvoje rankoje</i>.
<br>• Tiriamajam pranešama, kad paprašius reikės RAMIAI atsistoti šalia ir atsisėsti
TIK LEIDUS.
<br>• Įjungiamas kraujospūdžio matuoklis ir jo pompa paimama dešinės rankos
mažyliu, bevardžiu ir didžiuoju pirštais, taip pat į dešinę ranką paimamas
chronometras ir laikomas taip, kad smiliumi arba nykščiu būtų galima lengvai
nuspausti paleidimo mygtuką.
<br>• Kaire ranka užčiuopiamas tiriamojo pulsas kairėje rankoje taip, kaip nurodyta 8
punkte. Riešą reikia apminti patogiai, kad pirštai testo metu nenuslystų, ir tam,
kad būtų galima testo metu lengvai koreguoti jų padėtį.
<br>•<i>Tiriamojo paprašoma atsistoti</i>. Jo kairė ranka laikoma sulenkta stačiu kampu.
Tiriamajam besistojant, Jūs turite likti sėdėti.""", width=750)


def aprpulsatsi15():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup23">• Pulsas tik ką atsistojus ir po 15 s:</a>
</div>

<div id="popup23" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Pulsas tik ką atsistojus ir po 15 s</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Tiriamajam pilnai atsistojus paleidžiamas
chronometras ir pradedami skaičiuoti širdies dūžiai kaip ir 8 punkte.
Skaičiuojama 15 sekundžių, skaičius įsimenamas arba garsiai pasakomas
asistentui, nestabdant chronometro, iškart pradedamas skaičiuoti antras pulsas,
skaičiuojama dar 30 sekundžių, t.y. kol chronometras rodys 0:45, skaičius taip
pat įsimenamas arba garsiai pasakomas asistentui:
		</div>
	</div>
</div>
	""", width=250)


def atsist():
	return Div(text="""<br>Atsistojus<br>(dūžių skaičius per pirmas 15 s,×4)""", width=300)


def po15():
	return Div(text="""<br>Po 15 s.<br>(dūžių skaičius tarp 15-tos ir 45-tos sekundės,×2)""", width=300)


parytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
papietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

pa15rytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pa15pietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pa15vakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def aprkraujpulsatsi45():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup24">• Kraujospūdis ir pulsas atsistojus po 45 s:</a>
</div>

<div id="popup24" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Kraujospūdis ir pulsas atsistojus po 45 s</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
<i>Triamojo paprašoma atpalaiduoti
ranką bei stovėti ramiai</i>. Tuomet kairė tiriamojo ranka nuleidžiama, pripučiama
kraujospūdžio matuoklio manžetė ir pamatuojamas kraujospūdis (automatiškai
pamatuojamas ir pulsas).
<br>Tiriamojo paprašoma atsisėsti. Išleidžiamas oras iš manžetės. Juodraštyje
užsirašomi abu įsiminti skaičiai iš eilės. Pirmąjį skaičių padauginę iš 4 gauname
pulsą iškart atsistojus, jis įrašomas eilutėje 5.5 „Puslas tik ką atsistojus, P 2 ”.
Antrąjį skaičių padauginę iš 2, gauname antrąjį pulsą atsistojus, jis įrašomas
eilutėje „Pulsas atsistojus po 15 s, P 3 ”. Užsirašomi kraujospūdžio matuoklio
ekrane rodomi skaičiai: sistolinis kraujospūdis (didesnis rodmuo ties užrašu
„SYS“) įrašomas eilutėje 5.7 „Sistolinis kraujospūdis atsistojus, Sis 2 “, diastolinis
kraujospūdis (mažesnis rodmuo ties užrašu „DIA“) įrašomas eilutėje 5.8
„Diastolinis kraujospūdis atsistojus, Dia 2 “, o ekrane rodomas pulsas – eilutėje 5.9
„Pulsas atsistojus po 45 s, P 4 ”.
		</div>
	</div>
</div>
	""", width=250)


def siskraujatsi():
	return Div(text="""<br>Sistolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „SYS“ po 45 s)""", width=300)


def diaskraujatsi():
	return Div(text="""<br>Diastolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „DIA“)""", width=300)


def pulsatsi45():
	return Div(text="""<br>Pulsas atsistojus po 45 s<br>(rodmuo ekrane ties „PULS“)""", width=300)


skarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
skapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
skavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

dkarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
dkapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
dkavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

pa45rytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pa45pietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pa45vakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def tiriam4():
	return Div(text="""<b>13.</b><i> Nuimama manžetė nuo tiriamojo žasto.</i>""", width=300)


def kvepparmat14():
	return Div(text="""<b>14. Kvėpavimo parametrų matavimas:</b>""", width=300)


def aprkvepsu():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup25"><br>Kvėpavimo sulaikymas įkvėpus</a>
</div>

<div id="popup25" class="overlay">
	<div class="popup" id="showpopup">
		<h2>Kvėpavimo sulaikymas įkvėpus</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Įsitikinama, kad tiriamasis sėdi tiesia nugara.
Tiriamojo paprašoma pajausti savo kvėpavimą kelis kartus įkvėpiant ir iškvėpiant, tuomet
įkvėpti, bet IŠLAIKYTI TIESIĄ NUGARĄ, nekelti pečių ar kitaip nepersitempti, sulaikius
kvėpavimą duoti ženklą linktelint galvą. Kvėpavimą sulaikyti kiek įmanoma ilgiau, iškvėpti
tik kai jau visiškai neįmanoma sulaikyti kvėpavimo nė sekundės ilgiau, tačiau nesimuistyti
ar kitaip nebandyti užtęsti laiko. Tiriamajam įkvėpus ir linktelėjus galvą, paleidžiamas
chronometras, jam pilnai iškvėpus, chronometras stabdomas. Chronometro ekrane
rodomas laikas sekundėmis įrašomas eilutėje 6.2 „Kvėpavimo sulaikymas įkvėpus, t“.
		</div>
	</div>
</div>
	""", width=250)


ksirytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
ksipietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
ksivakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


def kataanab():
	return Div(text="""<b>KATABOLIZMAS|ANABOLIZMAS</b>""", width=300)


def rekokatego():
	return Div(text="""Kategorijos išdėstytos svarbos mažėjimo tvarka,
		tad jei prioritetai dėl tam tikrų maisto produktų vienas kitam prieštarauja, vadovautis tuo, kuris yra aukščiau.""", width=570)


def rekotipai():
	return Div(text="""<i>Prioritetų žymėjimas:
		„T“ rekomenduojama vartoti daugiau,
		„N“ vartoti nerekomenduojama,
		„S“ vartoti saikingai (taip retai, kad būtų sunku prisiminti ankstesnio vartojimo datą),
		„-“ papildomų rekomendacijų nėra.</i>""", width=570)


def maistproduk():
	return Div(text="""<b>Maisto produktų prioritetai</b>""", width=270)


rekomendmyg = Button(label="Rekomendacijos", button_type="success", height=20)
spacer_0 = Spacer(width=150, height=20)
spacer_1 = Spacer(width=150, height=89)
spacer_2 = Spacer(width=150, height=89)
spacer_3 = Spacer(width=150, height=89)
spacer_4 = Spacer(width=150, height=89)
spacer_5 = Spacer(width=150, height=89)
spacer_6 = Spacer(width=150, height=89)
spacer_7 = Spacer(width=150, height=89)

p1 = grafikai.make_graf(grafikai.plist[0], grafikai.pavadin[0], grafikai.countsp, grafikai.factorssp)
p2 = grafikai.make_graf(grafikai.plist[1], grafikai.pavadin[1], grafikai.countkg, grafikai.factorskg)
p3 = grafikai.make_graf(grafikai.plist[2], grafikai.pavadin[2], grafikai.countda, grafikai.factorsda)
p4 = grafikai.make_graf(grafikai.plist[3], grafikai.pavadin[3], grafikai.countmalac, grafikai.factorsmalac)
p5 = grafikai.make_graf(grafikai.plist[4], grafikai.pavadin[4], grafikai.countetp, grafikai.factorsetp)
p6 = grafikai.make_graf(grafikai.plist[5], grafikai.pavadin[5], grafikai.countktp, grafikai.factorsktp)
p7 = grafikai.make_graf(grafikai.plist[6], grafikai.pavadin[6], grafikai.countralac, grafikai.factorsralac)


def make_lin(pav, *src):
	if len(src) == 1:
		linij = pav.line(x='x', y='y', source=src[0], line_width=8)
		return [linij]
	else:
		linij = pav.line(x='x', y='y', source=src[0], line_width=8)
		linij1 = pav.line(x='x', y='y', source=src[1], line_width=8)
		return [linij, linij1]


def verte(*reiksme):
	L = []
	for r in reiksme:
		if L is not None:
			L = []
			L.append(r)
	if len(L[0]) == 1:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		return verte1
	elif len(L[0]) == 2:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		verte2 = float("".join(str(i) for i in (L[0][-1].value)).replace(",", "."))
		return verte1, verte2
	elif len(L[0]) == 3:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		verte2 = float("".join(str(i) for i in (L[0][1].value)).replace(",", "."))
		verte3 = float("".join(str(i) for i in (L[0][-1].value)).replace(",", "."))
		return verte1, verte2, verte3
	elif len(L[0]) == 4:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		verte2 = float("".join(str(i) for i in (L[0][1].value)).replace(",", "."))
		verte3 = float("".join(str(i) for i in (L[0][2].value)).replace(",", "."))
		verte4 = float("".join(str(i) for i in (L[0][-1].value)).replace(",", "."))
		return verte1, verte2, verte3, verte4
	else:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		verte2 = float("".join(str(i) for i in (L[0][1].value)).replace(",", "."))
		verte3 = float("".join(str(i) for i in (L[0][2].value)).replace(",", "."))
		verte4 = float("".join(str(i) for i in (L[0][3].value)).replace(",", "."))
		verte5 = float("".join(str(i) for i in (L[0][4].value)).replace(",", "."))
		verte6 = float("".join(str(i) for i in (L[0][-1].value)).replace(",", "."))
		return verte1, verte2, verte3, verte4, verte5, verte6


def formule_kt_ar_ap(skirtum, lin, ind, lentel, k, *arg):
	NormaKT = lentel.loc[lentel.index[ind], "Norma KT"]
	NormaAP = lentel.loc[lentel.index[ind], "Norma AP"]

	if NormaAP == 1000:
		NormaAP = arg[0]
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaAP, NormaKT]) / len([NormaAP, NormaKT])
	elif NormaKT == NormaAP == 1001:
		if arg[0] < 6.4:
			NormaKT = 67
			NormaAP = 52
		elif arg[0] > 7.1:
			NormaKT = 46
			NormaAP = 31
		else:
			NormaKT = (-30 * arg[0]) + 259
			NormaAP = (-30 * arg[0]) + 244
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaAP, NormaKT]) / len([NormaAP, NormaKT])
	elif NormaKT == NormaAP == 1002:
		if arg[0] < 6.4:
			NormaKT = 64
			NormaAP = 68
		elif arg[0] > 7.1:
			NormaKT = 92
			NormaAP = 96
		else:
			NormaKT = (40 * arg[0]) - 192
			NormaAP = (40 * arg[0]) - 188
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaAP, NormaKT]) / len([NormaAP, NormaKT])
	elif NormaKT == -0.28 and NormaAP == -0.18:
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = -0.1
	elif NormaKT == 10 and NormaAP == 10:
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = 0
	else:
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaAP, NormaKT]) / len([NormaAP, NormaKT])

	if (NormaKT - balansas) < 0:
		kryptis = 1
	else:
		kryptis = -1

	if (skirtum - balansas) * kryptis >= 0:
		zenklas = 1
	else:
		zenklas = -1

# nustatoma alfa  ir beta reikšmės
	if zenklas > 0:
		alfa = (1 - pagrindas) / (balansas - NormaAP)
		beta = (pagrindas * balansas - NormaAP) / (balansas - NormaAP)
	else:
		alfa = (1 - pagrindas) / (balansas - NormaKT)
		beta = (pagrindas * balansas - NormaKT) / (balansas - NormaKT)

# nustatoma katabolizmo|trūkumo arba anabolizmo|pertekliaus reikšmė
	if zenklas < 0:
		if NormaKT == 16 and NormaAP == 22:
			pagrindas = 16
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
		else:
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))

	else:
		if NormaKT == 16 and NormaAP == 8:
			pagrindas = 16
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
		else:
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))

# nurodomos skirtingos spalvos
	if len(lin) == 1:
		if ktarap > 0:
			lin[0].glyph.line_color = "blue"
		else:
			lin[0].glyph.line_color = "red"
	else:
		if ktarap > 0:
			lin[0].glyph.line_color = "red"
			lin[1].glyph.line_color = "blue"
		else:
			lin[0].glyph.line_color = "red"
			lin[1].glyph.line_color = "blue"

# apribojama reikšmė iki 4 arba -4
	if ktarap > 4:
		ktarapriba = 4
	elif ktarap < -4:
		ktarapriba = -4
	else:
		ktarapriba = ktarap
	return ktarapriba


def buklnustat(val1, val2, val3, param):
	for api, skaic in param.items():
		if skaic is not None:
			buklkr = len([val1[i] for i in val1 if val1[i] < -1])
			buklar = len([val1[i] for i in val1 if val1[i] > 1])
			buklkp = len([val2[i] for i in val2 if val2[i] < -1])
			buklap = len([val2[i] for i in val2 if val2[i] > 1])
			buklkv = len([val3[i] for i in val3 if val3[i] < -1])
			buklav = len([val3[i] for i in val3 if val3[i] > 1])

			if buklkr >= skaic:
				bksrreiksme = "T"
			else:
				bksrreiksme = "N"
			if buklar >= skaic:
				bkprreiksme = "T"
			else:
				bkprreiksme = "N"

			if buklkp >= skaic:
				bkspreiksme = "T"
			else:
				bkspreiksme = "N"
			if buklap >= skaic:
				bkppreiksme = "T"
			else:
				bkppreiksme = "N"

			if buklkv >= skaic:
				bksvreiksme = "T"
			else:
				bksvreiksme = "N"
			if buklav >= skaic:
				bkpvreiksme = "T"
			else:
				bkpvreiksme = "N"

		else:
			if api != "kaliotalpac":
				kdtksikphir = [val1["kdrytas"], val1["tksirytas"], val1["kphirytas"]]
				kdtksikphip = [val2["kdpietūs"], val2["tksipietūs"], val2["kphipietūs"]]
				kdtksikphiv = [val3["kdvakaras"], val3["tksivakaras"], val3["kphivakaras"]]

				uphksphkr = [val1["uphkrytas"], val1["sphkrytas"]]
				uphksphkp = [val2["uphkpietūs"], val2["sphkpietūs"]]
				uphksphkv = [val3["uphkvakaras"], val3["sphkvakaras"]]

				p1p4p1r = [val1["p(1)rytas"], val1["p4p1rytas"]]
				p1p4p1p = [val2["p(1)pietūs"], val2["p4p1pietūs"]]
				p1p4p1v = [val3["p(1)vakaras"], val3["p4p1vakaras"]]
			else:
				kdtksikphir = [val1["kdrytas"], val1["tksirytas"], val1["kphirytas"]]
				kdtksikphip = [val2["kdpietūs"], val2["tksipietūs"], val2["kphipietūs"]]
				kdtksikphiv = [val3["kdvakaras"], val3["tksivakaras"], val3["kphivakaras"]]

				uphksphkr = [val1["uphkrytas"], val1["sphkrytas"]]
				uphksphkp = [val2["uphkpietūs"], val2["sphkpietūs"]]
				uphksphkv = [val3["uphkvakaras"], val3["sphkvakaras"]]

				p1p4p1r = [val1["dermrytas"], val1["vyzdrytas"], val1["p4p1rytas"]]
				p1p4p1p = [val2["dermpietūs"], val2["vyzdpietūs"], val2["p4p1pietūs"]]
				p1p4p1v = [val3["dermvakaras"], val3["vyzdvakaras"], val3["p4p1vakaras"]]

			buklkdtksikphirkr = len([i for i in kdtksikphir if i < -1])
			uphksphkrkr = len([i for i in uphksphkr if i < -1])
			p1p4p1rkr = len([i for i in p1p4p1r if i < -1])
			buklkdtksikphirar = len([i for i in kdtksikphir if i > 1])
			uphksphkrar = len([i for i in uphksphkr if i > 1])
			p1p4p1rar = len([i for i in p1p4p1r if i > 1])

			buklkdtksikphipkp = len([i for i in kdtksikphip if i < -1])
			uphksphkpkp = len([i for i in uphksphkp if i < -1])
			p1p4p1pkp = len([i for i in p1p4p1r if i < -1])
			buklkdtksikphipap = len([i for i in kdtksikphip if i > 1])
			uphksphkpap = len([i for i in uphksphkp if i > 1])
			p1p4p1pap = len([i for i in p1p4p1p if i > 1])

			buklkdtksikphivkv = len([i for i in kdtksikphiv if i < -1])
			uphksphkvkv = len([i for i in uphksphkv if i < -1])
			p1p4p1vkv = len([i for i in p1p4p1v if i < -1])
			buklkdtksikphivav = len([i for i in kdtksikphiv if i > 1])
			uphksphkvav = len([i for i in uphksphkv if i > 1])
			p1p4p1vav = len([i for i in p1p4p1v if i > 1])

			if buklkdtksikphirkr >= 2 and uphksphkrkr == 2 and p1p4p1rkr >= 1:
				bksrreiksme = "T"
			else:
				bksrreiksme = "N"
			if buklkdtksikphirar >= 2 and uphksphkrar == 2 and p1p4p1rar >= 1:
				bkprreiksme = "T"
			else:
				bkprreiksme = "N"

			if buklkdtksikphipkp >= 2 and uphksphkpkp == 2 and p1p4p1pkp >= 1:
				bkspreiksme = "T"
			else:
				bkspreiksme = "N"
			if buklkdtksikphipap >= 2 and uphksphkpap == 2 and p1p4p1pap >= 1:
				bkppreiksme = "T"
			else:
				bkppreiksme = "N"

			if buklkdtksikphivkv >= 2 and uphksphkvkv == 2 and p1p4p1vkv >= 1:
				bksvreiksme = "T"
			else:
				bksvreiksme = "N"
			if buklkdtksikphivav >= 2 and uphksphkvav == 2 and p1p4p1vav >= 1:
				bkpvreiksme = "T"
			else:
				bkpvreiksme = "N"

	bendraskn = len([i for i in [bksrreiksme, bkspreiksme, bksvreiksme] if i == "N"])
	bendraskt = len([i for i in [bksrreiksme, bkspreiksme, bksvreiksme] if i == "T"])
	bendrasan = len([i for i in [bkprreiksme, bkppreiksme, bkpvreiksme] if i == "N"])
	bendrasat = len([i for i in [bkprreiksme, bkppreiksme, bkpvreiksme] if i == "T"])

	if bendraskn > bendraskt:
		galutineknt = "N"
	else:
		galutineknt = "T"

	if bendrasan > bendrasat:
		galutineant = "N"
	else:
		galutineant = "T"

	print("Katabolizmo", api, galutineknt, val1, val2, val3)
	print("Anabolizmo", api, galutineant, val1, val2, val3)


# Simpatinis|parasimpatinis

simparasim = {
	"Norma KT": [-2, 11, 25, 6, 36.7, 1, -1, 1, 1, -1, 1, 1],
	"Norma AP": [0, 6, 22, 4, 36.5, 2, 1, -1, -1, 1, -1, -1],
	"Pagrindas": [2, 2, 2, 1.001, 2, 1.2, 1.001, 1.001, 1.001, 1.001, 1.001, 1.001]}

parametrupavsp = ["Ps-1", "S+D", "Pm1+Pm4", "KRi", "Temp", "Derm", "Vaso", "Vyzd", "Trem", "Nos", "Sarg", "S-kl"]
lentelesp = pd.DataFrame(simparasim, index=parametrupavsp)
lentelesp = lentelesp[["Norma KT", "Norma AP", "Pagrindas"]]

parametsp = {
	"ps1rytas": [[psrytas, pgrytas], "ps1r", CDS.srcps1r.data, make_lin(p1, CDS.srcps1r), parametrupavsp.index("Ps-1")],
	"ps1pietūs": [[pspietus, pgpietus], "ps1p", CDS.srcps1p.data, make_lin(p1, CDS.srcps1p), parametrupavsp.index("Ps-1")],
	"ps1vakaras": [[psvakaras, pgvakaras], "ps1v", CDS.srcps1v.data, make_lin(p1, CDS.srcps1v), parametrupavsp.index("Ps-1")],

	"s+drytas": [[skarytas, skgrytas, dkarytas, dkgrytas], "s+dr", CDS.srcspdr.data, make_lin(p1, CDS.srcspdr), parametrupavsp.index("S+D")],
	"s+dpietūs": [[skapietus, skgpietus, dkapietus, dkgpietus], "s+dp", CDS.srcspdp.data, make_lin(p1, CDS.srcspdp), parametrupavsp.index("S+D")],
	"s+dvakaras": [[skavakaras, skgvakaras, dkavakaras, dkgvakaras], "s+dv", CDS.srcspdv.data, make_lin(p1, CDS.srcspdv), parametrupavsp.index("S+D")],

	"pm1+pm4rytas": [[pgrytas, parytas, pa15rytas, pa45rytas], "pm1+pm4r", CDS.srcpm1ppm4r.data, make_lin(p1, CDS.srcpm1ppm4r), parametrupavsp.index("Pm1+Pm4")],
	"pm1+pm4pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus], "pm1+pm4p", CDS.srcpm1ppm4p.data, make_lin(p1, CDS.srcpm1ppm4p), parametrupavsp.index("Pm1+Pm4")],
	"pm1+pm4vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras], "pm1+pm4v", CDS.srcpm1ppm4v.data, make_lin(p1, CDS.srcpm1ppm4v), parametrupavsp.index("Pm1+Pm4")],

	"krirytas": [[psrytas, kdrytas], "krir", CDS.srckrir.data, make_lin(p1, CDS.srckrir), parametrupavsp.index("KRi")],
	"kripietūs": [[pspietus, kdpietus], "krip", CDS.srckrip.data, make_lin(p1, CDS.srckrip), parametrupavsp.index("KRi")],
	"krivakaras": [[psvakaras, kdvakaras], "kriv", CDS.srckriv.data, make_lin(p1, CDS.srckriv), parametrupavsp.index("KRi")],

	"temprytas": [[ktrytas], "tempr", CDS.srctempr.data, make_lin(p1, CDS.srctempr), parametrupavsp.index("Temp")],
	"temppietūs": [[ktpietus], "tempp", CDS.srctempp.data, make_lin(p1, CDS.srctempp), parametrupavsp.index("Temp")],
	"tempvakaras": [[ktvakaras], "tempv", CDS.srctempv.data, make_lin(p1, CDS.srctempv), parametrupavsp.index("Temp")],

	"dermrytas": [[drrytas], "dermr", CDS.srcdermspr.data, make_lin(p1, CDS.srcdermspr), parametrupavsp.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", CDS.srcdermspp.data, make_lin(p1, CDS.srcdermspp), parametrupavsp.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", CDS.srcdermspv.data, make_lin(p1, CDS.srcdermspv), parametrupavsp.index("Derm")],

	"vasorytas": [[vrrytas], "vasor", CDS.srcvasor.data, make_lin(p1, CDS.srcvasor), parametrupavsp.index("Vaso")],
	"vasopietūs": [[vrpietus], "vasop", CDS.srcvasop.data, make_lin(p1, CDS.srcvasop), parametrupavsp.index("Vaso")],
	"vasovakaras": [[vrvakaras], "vasov", CDS.srcvasov.data, make_lin(p1, CDS.srcvasov), parametrupavsp.index("Vaso")],

	"vyzdrytas": [[vdrytas], "vyzdr", CDS.srcvyzdspr.data, make_lin(p1, CDS.srcvyzdspr), parametrupavsp.index("Vyzd")],
	"vyzdpietūs": [[vdpietus], "vyzdp", CDS.srcvyzdspp.data, make_lin(p1, CDS.srcvyzdspp), parametrupavsp.index("Vyzd")],
	"vyzdvakaras": [[vdvakaras], "vyzdv", CDS.srcvyzdspv.data, make_lin(p1, CDS.srcvyzdspv), parametrupavsp.index("Vyzd")],

	"tremrytas": [[trrytas], "tremr", CDS.srctremr.data, make_lin(p1, CDS.srctremr), parametrupavsp.index("Trem")],
	"trempietūs": [[trpietus], "tremp", CDS.srctremp.data, make_lin(p1, CDS.srctremp), parametrupavsp.index("Trem")],
	"tremvakaras": [[trvakaras], "tremv", CDS.srctremv.data, make_lin(p1, CDS.srctremv), parametrupavsp.index("Trem")],

	"nosrytas": [[surytas], "nosr", CDS.srcnosr.data, make_lin(p1, CDS.srcnosr), parametrupavsp.index("Nos")],
	"nospietūs": [[supietus], "nosp", CDS.srcnosp.data, make_lin(p1, CDS.srcnosp), parametrupavsp.index("Nos")],
	"nosvakaras": [[suvakaras], "nosv", CDS.srcnosv.data, make_lin(p1, CDS.srcnosv), parametrupavsp.index("Nos")],

	"sargrytas": [[slrytas], "sargr", CDS.srcsargr.data, make_lin(p1, CDS.srcsargr), parametrupavsp.index("Sarg")],
	"sargpietūs": [[slpietus], "sargp", CDS.srcsargp.data, make_lin(p1, CDS.srcsargp), parametrupavsp.index("Sarg")],
	"sargvakaras": [[slvakaras], "sargv", CDS.srcsargv.data, make_lin(p1, CDS.srcsargv), parametrupavsp.index("Sarg")],

	"sklrytas": [[sekrytas], "sklr", CDS.srcsklr.data, make_lin(p1, CDS.srcsklr), parametrupavsp.index("S-kl")],
	"sklpietūs": [[sekpietus], "sklp", CDS.srcsklp.data, make_lin(p1, CDS.srcsklp), parametrupavsp.index("S-kl")],
	"sklvakaras": [[sekvakaras], "sklv", CDS.srcsklv.data, make_lin(p1, CDS.srcsklv), parametrupavsp.index("S-kl")]}


def simparasim_update(attr, old, new):
	simparasimr = {}
	simparasimp = {}
	simparasimv = {}
	dictpav = {"simparasim": 5}
	for key in parametsp.keys():
		if "ps1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2 = verte(n)
			formule = (v1 - v2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)

	# taip bokeh atnaujinama x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "s+d" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2, v3, v4 = verte(n)
			formule = (v1 - v2) + (v3 - v4)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "pm1+pm4" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2, v3, v4 = verte(n)
			r1 = max(v1, v2, v3, v4) - v1
			r2 = max(v1, v2, v3, v4) - v4
			formule = (r1 + r2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "kri" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2 = verte(n)
			if v2 != 0:
				formule = (v1 / v2)
				karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
				new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
				sourcedata.update(new_data)
			else:
				pass

		elif "temp" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "derm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "vaso" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "vyzd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "trem" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "nos" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "sarg" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "skl" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		# if "rytas" in str(key):
		# 	simparasimr[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	simparasimp[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	simparasimv[key] = karareiksme

		# if len(simparasimr) == len(simparasimp) == len(simparasimv) == 12:
		# 	buklnustat(simparasimr, simparasimp, simparasimv, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametsp.values()]])):
	w.on_change("value", simparasim_update)


# Ketogeninis|gliukogeninis

ketogliuko = {
	"Norma KT": [15, 1001, 1002, 6, 5, 1, -0.28],
	"Norma AP": [1000, 1001, 1002, 8, 0, -1, -0.18],
	"Pagrindas": [2, 1.2, 2.5, 2, 2, 1.1, 1.2]}

parametrupavkg = ["KD", "t(ksi)", "P4", "KpHi", "D2-P4", "U-šv", "U-put"]
lentelekg = pd.DataFrame(ketogliuko, index=parametrupavkg)
lentelekg = lentelekg[["Norma KT", "Norma AP", "Pagrindas"]]

parametkg = {
	"kdrytas": [[kdrytas, slatankrytas, serrytas], "kdr", CDS.srckdkgr.data, make_lin(p2, CDS.srckdkgr), parametrupavkg.index("KD")],
	"kdpietūs": [[kdpietus, slatankpietus, serpietus], "kdp", CDS.srckdkgp.data, make_lin(p2, CDS.srckdkgp), parametrupavkg.index("KD")],
	"kdvakaras": [[kdvakaras, slatankvakaras, servakaras], "kdv", CDS.srckdkgv.data, make_lin(p2, CDS.srckdkgv), parametrupavkg.index("KD")],

	"tksirytas": [[ksirytas, slatankrytas, serrytas], "tksir", CDS.srctksikgr.data, make_lin(p2, CDS.srctksikgr), parametrupavkg.index("t(ksi)")],
	"tksipietūs": [[ksipietus, slatankpietus, serpietus], "tksip", CDS.srctksikgp.data, make_lin(p2, CDS.srctksikgp), parametrupavkg.index("t(ksi)")],
	"tksivakaras": [[ksivakaras, slatankvakaras, servakaras], "tksiv", CDS.srctksikgv.data, make_lin(p2, CDS.srctksikgv), parametrupavkg.index("t(ksi)")],

	"p4rytas": [[pa45rytas, slatankrytas, serrytas], "p4r", CDS.srcp4r.data, make_lin(p2, CDS.srcp4r), parametrupavkg.index("P4")],
	"p4pietūs": [[pa45pietus, slatankpietus, serpietus], "p4p", CDS.srcp4p.data, make_lin(p2, CDS.srcp4p), parametrupavkg.index("P4")],
	"p4vakaras": [[pa45vakaras, slatankvakaras, servakaras], "p4v", CDS.srcp4v.data, make_lin(p2, CDS.srcp4v), parametrupavkg.index("P4")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", CDS.srckphikgr.data, make_lin(p2, CDS.srckphikgr), parametrupavkg.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", CDS.srckphikgp.data, make_lin(p2, CDS.srckphikgp), parametrupavkg.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", CDS.srckphikgv.data, make_lin(p2, CDS.srckphikgv), parametrupavkg.index("KpHi")],

	"d2p(4)rytas": [[dkarytas, pa45rytas], "d2p(4)r", CDS.srcd2p4r.data, make_lin(p2, CDS.srcd2p4r,), parametrupavkg.index("D2-P4")],
	"d2p(4)pietūs": [[dkapietus, pa45pietus], "d2p(4)p", CDS.srcd2p4p.data, make_lin(p2, CDS.srcd2p4p), parametrupavkg.index("D2-P4")],
	"d2p(4)vakaras": [[dkavakaras, pa45vakaras], "d2p(4)v", CDS.srcd2p4v.data, make_lin(p2, CDS.srcd2p4v), parametrupavkg.index("D2-P4")],

	"usvrytas": [[slasvrytas], "usvr", CDS.srcusvkgr.data, make_lin(p2, CDS.srcusvkgr), parametrupavkg.index("U-šv")],
	"usvpietūs": [[slasvpietus], "usvp", CDS.srcusvkgp.data, make_lin(p2, CDS.srcusvkgp), parametrupavkg.index("U-šv")],
	"usvvakaras": [[slasvvakaras], "usvv", CDS.srcusvkgv.data, make_lin(p2, CDS.srcusvkgv), parametrupavkg.index("U-šv")],

	"uputrytas": [[slaputrytas], "uputr", [CDS.srcuputkgr.data, CDS.srcuputkg1r.data], make_lin(p2, CDS.srcuputkgr, CDS.srcuputkg1r), parametrupavkg.index("U-put")],
	"uputpietūs": [[slaputpietus], "uputp", [CDS.srcuputkgp.data, CDS.srcuputkg1p.data], make_lin(p2, CDS.srcuputkgp, CDS.srcuputkg1p), parametrupavkg.index("U-put")],
	"uputvakaras": [[slaputvakaras], "uputv", [CDS.srcuputkgv.data, CDS.srcuputkg1v.data], make_lin(p2, CDS.srcuputkgv, CDS.srcuputkg1v), parametrupavkg.index("U-put")]}


def ketogliuko_update(attr, old, new):
	ketogliukor = {}
	ketogliukop = {}
	ketogliukov = {}
	dictpav = {"ketogliuko": 4}
	for key in parametkg.keys():
		if "kd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, stv, serv = verte(n)
			tankindx = (stv * 1000) - 1000
			sphk = serv + (0.033333 * tankindx) - 0.533333
			if 7 > sphk >= 6.8:
				sphkv = 16
			else:
				sphkv = 17
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key, sphkv)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, stv, serv = verte(n)
			tankindx = (stv * 1000) - 1000
			sphk = serv + (0.033333 * tankindx) - 0.533333
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key, sphk)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p4" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, stv, serv = verte(n)
			tankindx = (stv * 1000) - 1000
			sphk = serv + (0.033333 * tankindx) - 0.533333
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key, sphk)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "d2p(4)" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "usv" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uput" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1 = verte(n)
			sourcedata1, sourcedata2 = sourcedata
			formule = v1
			if formule < 0:
				karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, key)
			else:
				karareiksme = 0
			new_data1 = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata1.update(new_data1)
			new_data2 = {'x': [0, -karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata2.update(new_data2)

		# if "rytas" in str(key):
		# 	if key == "uputrytas":
		# 		key1 = "uputrytas1"
		# 		ketogliukor[key] = karareiksme
		# 		ketogliukor[key1] = -karareiksme
		# 	else:
		# 		ketogliukor[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	if key == "uputpietūs":
		# 		key1 = "uputpietūs1"
		# 		ketogliukop[key] = karareiksme
		# 		ketogliukop[key1] = -karareiksme
		# 	else:
		# 		ketogliukop[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	if key == "uputvakaras":
		# 		key1 = "uputvakaras1"
		# 		ketogliukov[key] = karareiksme
		# 		ketogliukov[key1] = -karareiksme
		# 	else:
		# 		ketogliukov[key] = karareiksme

		# if len(ketogliukor) == len(ketogliukop) == len(ketogliukov) == 8:
		# 	buklnustat(ketogliukor, ketogliukop, ketogliukov, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametkg.values()]])):
	w.on_change("value", ketogliuko_update)

# Disaerobinis|anaerobinis

disaeanae = {
	"Norma KT": [18, 6.1, 6.8, 1, 1, 0.75],
	"Norma AP": [14, 6.3, 6.6, 2, -1, -0.5],
	"Pagrindas": [1.5, 2, 2, 1.5, 1.3, 1.1]}

parametrupavda = ["d(tank)", "U-pHK", "S-pHK", "Derm", "U-šv", "U-put"]
lenteleda = pd.DataFrame(disaeanae, index=parametrupavda)
lenteleda = lenteleda[["Norma KT", "Norma AP", "Pagrindas"]]

parametda = {
	"dtankrytas": [[slatankrytas], "dtankr", CDS.srcdtankr.data, make_lin(p3, CDS.srcdtankr), parametrupavda.index("d(tank)")],
	"dtankpietūs": [[slatankpietus], "dtankp", CDS.srcdtankp.data, make_lin(p3, CDS.srcdtankp), parametrupavda.index("d(tank)")],
	"dtankvakaras": [[slatankvakaras], "dtankv", CDS.srcdtankv.data, make_lin(p3, CDS.srcdtankv), parametrupavda.index("d(tank)")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", CDS.srcuphkdar.data, make_lin(p3, CDS.srcuphkdar), parametrupavda.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", CDS.srcuphkdap.data, make_lin(p3, CDS.srcuphkdap), parametrupavda.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", CDS.srcuphkdav.data, make_lin(p3, CDS.srcuphkdav), parametrupavda.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", CDS.srcsphkdar.data, make_lin(p3, CDS.srcsphkdar), parametrupavda.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", CDS.srcsphkdap.data, make_lin(p3, CDS.srcsphkdap), parametrupavda.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", CDS.srcsphkdav.data, make_lin(p3, CDS.srcsphkdav), parametrupavda.index("S-pHK")],

	"dermrytas": [[drrytas], "dermr", CDS.srcdermdar.data, make_lin(p3, CDS.srcdermdar), parametrupavda.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", CDS.srcdermdap.data, make_lin(p3, CDS.srcdermdap), parametrupavda.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", CDS.srcdermdav.data, make_lin(p3, CDS.srcdermdav), parametrupavda.index("Derm")],

	"usvrytas": [[slasvrytas], "usvr", CDS.srcusvdar.data, make_lin(p3, CDS.srcusvdar), parametrupavda.index("U-šv")],
	"usvpietūs": [[slasvpietus], "usvp", CDS.srcusvdap.data, make_lin(p3, CDS.srcusvdap), parametrupavda.index("U-šv")],
	"usvvakaras": [[slasvvakaras], "usvv", CDS.srcusvdav.data, make_lin(p3, CDS.srcusvdav), parametrupavda.index("U-šv")],

	"uputrytas": [[slaputrytas], "uputr", CDS.srcuputdar.data, make_lin(p3, CDS.srcuputdar), parametrupavda.index("U-put")],
	"uputpietūs": [[slaputpietus], "uputp", CDS.srcuputdap.data, make_lin(p3, CDS.srcuputdap), parametrupavda.index("U-put")],
	"uputvakaras": [[slaputvakaras], "uputv", CDS.srcuputdav.data, make_lin(p3, CDS.srcuputdav), parametrupavda.index("U-put")]}


def disaeanae_update(attr, old, new):
	disaeanaer = {}
	disaeanaep = {}
	disaeanaev = {}
	dictpav = {"disaeanae": 3}
	for key in parametda.keys():
		if "dtank" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = (v1 * 1000) - 1000
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "derm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "usv" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uput" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		# if "rytas" in str(key):
		# 	disaeanaer[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	disaeanaep[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	disaeanaev[key] = karareiksme

		# if len(disaeanaer) == len(disaeanaep) == len(disaeanaev) == 6:
		# 	buklnustat(disaeanaer, disaeanaep, disaeanaev, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametda.values()]])):
	w.on_change("value", disaeanae_update)

# Metabolinė alkalozė|acidozė

alkaacid = {
	"Norma KT": [13, 65, 5, 6.3, 6.6, 67, 0],
	"Norma AP": [19, 40, 10, 5.9, 6.8, 75, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.5, 2]}

parametrupavalac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "P1", "P4–P1"]
lentelealac = pd.DataFrame(alkaacid, index=parametrupavalac)
lentelealac = lentelealac[["Norma KT", "Norma AP", "Pagrindas"]]

parametalac = {
	"kdrytas": [[kdrytas], "kdr", CDS.srckdalacr.data, make_lin(p4, CDS.srckdalacr), parametrupavalac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", CDS.srckdalacp.data, make_lin(p4, CDS.srckdalacp), parametrupavalac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", CDS.srckdalacv.data, make_lin(p4, CDS.srckdalacv), parametrupavalac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", CDS.srctksialacr.data, make_lin(p4, CDS.srctksialacr), parametrupavalac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", CDS.srctksialacp.data, make_lin(p4, CDS.srctksialacp), parametrupavalac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", CDS.srctksialacv.data, make_lin(p4, CDS.srctksialacv), parametrupavalac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", CDS.srckphialacr.data, make_lin(p4, CDS.srckphialacr), parametrupavalac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", CDS.srckphialacp.data, make_lin(p4, CDS.srckphialacp), parametrupavalac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", CDS.srckphialacv.data, make_lin(p4, CDS.srckphialacv), parametrupavalac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", CDS.srcuphkalacr.data, make_lin(p4, CDS.srcuphkalacr), parametrupavalac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", CDS.srcuphkalacp.data, make_lin(p4, CDS.srcuphkalacp), parametrupavalac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", CDS.srcuphkalacv.data, make_lin(p4, CDS.srcuphkalacv), parametrupavalac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", CDS.srcsphkalacr.data, make_lin(p4, CDS.srcsphkalacr), parametrupavalac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", CDS.srcsphkalacp.data, make_lin(p4, CDS.srcsphkalacp), parametrupavalac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", CDS.srcsphkalacv.data, make_lin(p4, CDS.srcsphkalacv), parametrupavalac.index("S-pHK")],

	"p(1)rytas": [[pgrytas], "p1r", CDS.srcp1alacr.data, make_lin(p4, CDS.srcp1alacr), parametrupavalac.index("P1")],
	"p(1)pietūs": [[pgpietus], "p1p", CDS.srcp1alacp.data, make_lin(p4, CDS.srcp1alacp), parametrupavalac.index("P1")],
	"p(1)vakaras": [[pgvakaras], "p1v", CDS.srcp1alacv.data, make_lin(p4, CDS.srcp1alacv), parametrupavalac.index("P1")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", CDS.srcp4p1alacr.data, make_lin(p4, CDS.srcp4p1alacr), parametrupavalac.index("P4–P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", CDS.srcp4p1alacp.data, make_lin(p4, CDS.srcp4p1alacp), parametrupavalac.index("P4–P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", CDS.srcp4p1alacv.data, make_lin(p4, CDS.srcp4p1alacv), parametrupavalac.index("P4–P1")]}


def alkaacid_update(attr, old, new):
	alkaacidr = {}
	alkaacidp = {}
	alkaacidv = {}
	dictpav = {"alkaacid": None}
	for key in parametalac.keys():
		if "kd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p(1)" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p4p1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac, key)
			if karareiksme < 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		# if "rytas" in str(key):
		# 	alkaacidr[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	alkaacidp[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	alkaacidv[key] = karareiksme

		# if len(alkaacidr) == len(alkaacidp) == len(alkaacidv) == 7:
		# 	buklnustat(alkaacidr, alkaacidp, alkaacidv, dictpav) GERAi


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametalac.values()]])):
	w.on_change("value", alkaacid_update)

# Elektrolitų trūkumas|perteklius

elektroltp = {
	"Norma KT": [16, 16, 10, 180, -8],
	"Norma AP": [8, 22, 10, 220, 2],
	"Pagrindas": [2, 2, 1.2, 1.001, 1.4]}

parametrupavetp = ["Pm1-S21", "Pm1+S21", "Pm1-Pm4", "Sm+Dm", "S-D"]
lenteleetp = pd.DataFrame(elektroltp, index=parametrupavetp)
lenteleetp = lenteleetp[["Norma KT", "Norma AP", "Pagrindas"]]

parametetp = {
	"pm1-s21rytas": [[pgrytas, parytas, pa15rytas, pa45rytas, skarytas, skgrytas], "pm1-s21r", CDS.srcpm1ms21r.data, make_lin(p5, CDS.srcpm1ms21r), parametrupavetp.index("Pm1-S21")],
	"pm1-s21pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus, skapietus, skgpietus], "pm1-s21p", CDS.srcpm1ms21p.data, make_lin(p5, CDS.srcpm1ms21p), parametrupavetp.index("Pm1-S21")],
	"pm1-s21vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras, skavakaras, skgvakaras], "pm1-s21v", CDS.srcpm1ms21v.data, make_lin(p5, CDS.srcpm1ms21v), parametrupavetp.index("Pm1-S21")],

	"pm1+s21rytas": [[pgrytas, parytas, pa15rytas, pa45rytas, skarytas, skgrytas], "pm1+s21r", CDS.srcpm1ps21r.data, make_lin(p5, CDS.srcpm1ps21r), parametrupavetp.index("Pm1+S21")],
	"pm1+s21pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus, skapietus, skgpietus], "pm1+s21p", CDS.srcpm1ps21p.data, make_lin(p5, CDS.srcpm1ps21p), parametrupavetp.index("Pm1+S21")],
	"pm1+s21vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras, skavakaras, skgvakaras], "pm1+s21v", CDS.srcpm1ps21v.data, make_lin(p5, CDS.srcpm1ps21v), parametrupavetp.index("Pm1+S21")],

	"pm1-pm4rytas": [[pgrytas, parytas, pa15rytas, pa45rytas], "pm1-pm4r", [CDS.srcpm1mpm4r.data, CDS.src1pm1mpm4r.data], make_lin(p5, CDS.srcpm1mpm4r, CDS.src1pm1mpm4r), parametrupavetp.index("Pm1-Pm4")],
	"pm1-pm4pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus], "pm1-pm4p", [CDS.srcpm1mpm4p.data, CDS.src1pm1mpm4p.data], make_lin(p5, CDS.srcpm1mpm4p, CDS.src1pm1mpm4p), parametrupavetp.index("Pm1-Pm4")],
	"pm1-pm4vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras], "pm1-pm4v", [CDS.srcpm1mpm4v.data, CDS.src1pm1mpm4v.data], make_lin(p5, CDS.srcpm1mpm4v, CDS.src1pm1mpm4v), parametrupavetp.index("Pm1-Pm4")],

	"smdmrytas": [[skgrytas, skarytas, dkgrytas, dkarytas], "smdmr", CDS.srcsmdmr.data, make_lin(p5, CDS.srcsmdmr), parametrupavetp.index("Sm+Dm")],
	"smdmpietūs": [[skgpietus, skapietus, dkgpietus, dkapietus], "smdmp", CDS.srcsmdmp.data, make_lin(p5, CDS.srcsmdmp), parametrupavetp.index("Sm+Dm")],
	"smdmvakaras": [[skgvakaras, skavakaras, dkgvakaras, dkavakaras], "smdmv", CDS.srcsmdmv.data, make_lin(p5, CDS.srcsmdmv), parametrupavetp.index("Sm+Dm")],

	"s-drytas": [[skgrytas, skarytas, dkgrytas, dkarytas], "s-dr", [CDS.srcsmdr.data, CDS.srcsmd1r.data], make_lin(p5, CDS.srcsmdr, CDS.srcsmd1r), parametrupavetp.index("S-D")],
	"s-dpietūs": [[skgpietus, skapietus, dkgpietus, dkapietus], "s-dp", [CDS.srcsmdp.data, CDS.srcsmd1p.data], make_lin(p5, CDS.srcsmdp, CDS.srcsmd1p), parametrupavetp.index("S-D")],
	"s-dvakaras": [[skgvakaras, skavakaras, dkgvakaras, dkavakaras], "s-dv", [CDS.srcsmdv.data, CDS.srcsmd1v.data], make_lin(p5, CDS.srcsmdv, CDS.srcsmd1v), parametrupavetp.index("S-D")]}


def elektroltp_update(attr, old, new):
	elektroltpr = {}
	elektroltpp = {}
	elektroltpv = {}
	dictpav = {"elektroltp": 3}
	for key in parametetp.keys():
		if "pm1-s21" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametetp[key]
			v1, v2, v3, v4, v5, v6 = verte(n)
			r1 = max(v1, v2, v3, v4) - v1
			formule = r1 - v5 + v6
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleetp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "pm1+s21" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametetp[key]
			v1, v2, v3, v4, v5, v6 = verte(n)
			r1 = max(v1, v2, v3, v4) - v1
			formule = r1 + v5 - v6
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleetp, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "pm1-pm4" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametetp[key]
			v1, v2, v3, v4 = verte(n)
			r1 = max(v1, v2, v3, v4) - v1
			r2 = max(v1, v2, v3, v4) - v4
			sourcedata1, sourcedata2 = sourcedata
			formule = (r1 - r2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleetp, key)
			if karareiksme < 0:
				karareiksme
			else:
				karareiksme = 0
			new_data1 = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata1.update(new_data1)
			new_data2 = {'x': [0, -karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata2.update(new_data2)

		elif "smdm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametetp[key]
			v1, v2, v3, v4 = verte(n)
			formule = max(v1, v2) + max(v3, v4)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleetp, key)
			# kažką sugalvoti, kad negali būti 0
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "s-d" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametetp[key]
			v1, v2, v3, v4 = verte(n)
			sourcedata1, sourcedata2 = sourcedata
			formule = v2 - v1 - v4 + v3
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleetp, key)
			# kažką sugalvoti, kad negali būti 0
			if karareiksme < 0:
				new_data1 = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
				sourcedata1.update(new_data1)
				new_data2 = {'x': [0, -karareiksme], 'y': [yreiksme, yreiksme]}
				sourcedata2.update(new_data2)
			else:
				new_data1 = {'x': [0, 0], 'y': [yreiksme, yreiksme]}
				sourcedata1.update(new_data1)
				new_data2 = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
				sourcedata2.update(new_data2)

		# if "rytas" in str(key):
		# 	if key == "pm1-pm4rytas":
		# 		key1 = "pm1-pm4rytas1"
		# 		elektroltpr[key] = karareiksme
		# 		elektroltpr[key1] = -karareiksme
		# 	elif key == "s-drytas":
		# 		if karareiksme < 0:
		# 			key1 = "s-drytas1"
		# 			elektroltpr[key] = karareiksme
		# 			elektroltpr[key1] = -karareiksme
		# 		else:
		# 			key1 = "s-drytas1"
		# 			elektroltpr[key] = 0
		# 			elektroltpr[key1] = karareiksme
		# 	else:
		# 		elektroltpr[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	if key == "pm1-pm4pietūs":
		# 		key1 = "pm1-pm4pietūs1"
		# 		elektroltpp[key] = karareiksme
		# 		elektroltpp[key1] = -karareiksme
		# 	elif key == "s-dpietūs":
		# 		if karareiksme < 0:
		# 			key1 = "s-dpietūs1"
		# 			elektroltpp[key] = karareiksme
		# 			elektroltpp[key1] = -karareiksme
		# 		else:
		# 			key1 = "s-dpietūs1"
		# 			elektroltpp[key] = 0
		# 			elektroltpp[key1] = karareiksme
		# 	else:
		# 		elektroltpp[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	if key == "pm1-pm4vakaras":
		# 		key1 = "pm1-pm4vakaras1"
		# 		elektroltpv[key] = karareiksme
		# 		elektroltpv[key1] = -karareiksme
		# 	elif key == "s-dvakaras":
		# 		if karareiksme < 0:
		# 			key1 = "s-dvakaras1"
		# 			elektroltpv[key] = karareiksme
		# 			elektroltpv[key1] = -karareiksme
		# 		else:
		# 			key1 = "s-dvakaras1"
		# 			elektroltpv[key] = 0
		# 			elektroltpv[key1] = karareiksme
		# 	else:
		# 		elektroltpv[key] = karareiksme

		# if len(elektroltpr) == len(elektroltpp) == len(elektroltpv) == 7:
		# 	buklnustat(elektroltpr, elektroltpp, elektroltpv, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametetp.values()]])):
	w.on_change("value", elektroltp_update)

# Kalio trūkumo alkalozė|pertekliaus acidozė

kaliotalpac = {
	"Norma KT": [13, 65, 5, 5.9, 6.6, 1, 1, 0],
	"Norma AP": [19, 40, 10, 6.3, 6.8, -1, 2, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.001, 1.2, 2]}

parametrupavktalpac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "Vyzd", "Derm", "P4-P1"]
lentelektalpac = pd.DataFrame(kaliotalpac, index=parametrupavktalpac)
lentelektalpac = lentelektalpac[["Norma KT", "Norma AP", "Pagrindas"]]

parametktalpac = {
	"kdrytas": [[kdrytas], "kdr", CDS.srckdktalpacr.data, make_lin(p6, CDS.srckdktalpacr), parametrupavktalpac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", CDS.srckdktalpacp.data, make_lin(p6, CDS.srckdktalpacp), parametrupavktalpac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", CDS.srckdktalpacv.data, make_lin(p6, CDS.srckdktalpacv), parametrupavktalpac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", CDS.srctksiktalpacr.data, make_lin(p6, CDS.srctksiktalpacr), parametrupavktalpac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", CDS.srctksiktalpacp.data, make_lin(p6, CDS.srctksiktalpacp), parametrupavktalpac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", CDS.srctksiktalpacv.data, make_lin(p6, CDS.srctksiktalpacv), parametrupavktalpac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", CDS.srckphiktalpacr.data, make_lin(p6, CDS.srckphiktalpacr), parametrupavktalpac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", CDS.srckphiktalpacp.data, make_lin(p6, CDS.srckphiktalpacp), parametrupavktalpac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", CDS.srckphiktalpacv.data, make_lin(p6, CDS.srckphiktalpacv), parametrupavktalpac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", CDS.srcuphkktalpacr.data, make_lin(p6, CDS.srcuphkktalpacr), parametrupavktalpac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", CDS.srcuphkktalpacp.data, make_lin(p6, CDS.srcuphkktalpacp), parametrupavktalpac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", CDS.srcuphkktalpacv.data, make_lin(p6, CDS.srcuphkktalpacv), parametrupavktalpac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", CDS.srcsphkktalpacr.data, make_lin(p6, CDS.srcsphkktalpacr), parametrupavktalpac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", CDS.srcsphkktalpacp.data, make_lin(p6, CDS.srcsphkktalpacp), parametrupavktalpac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", CDS.srcsphkktalpacv.data, make_lin(p6, CDS.srcsphkktalpacv), parametrupavktalpac.index("S-pHK")],

	"vyzdrytas": [[vdrytas], "vyzdr", CDS.srcvyzdktalpacr.data, make_lin(p6, CDS.srcvyzdktalpacr), parametrupavktalpac.index("Vyzd")],
	"vyzdpietūs": [[vdpietus], "vyzdp", CDS.srcvyzdktalpacp.data, make_lin(p6, CDS.srcvyzdktalpacp), parametrupavktalpac.index("Vyzd")],
	"vyzdvakaras": [[vdvakaras], "vyzdv", CDS.srcvyzdktalpacv.data, make_lin(p6, CDS.srcvyzdktalpacv), parametrupavktalpac.index("Vyzd")],

	"dermrytas": [[drrytas], "dermr", CDS.srcdermktalpacr.data, make_lin(p6, CDS.srcdermktalpacr), parametrupavktalpac.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", CDS.srcdermktalpacp.data, make_lin(p6, CDS.srcdermktalpacp), parametrupavktalpac.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", CDS.srcdermktalpacv.data, make_lin(p6, CDS.srcdermktalpacv), parametrupavktalpac.index("Derm")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", CDS.srcp4p1ktalpacr.data, make_lin(p6, CDS.srcp4p1ktalpacr), parametrupavktalpac.index("P4-P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", CDS.srcp4p1ktalpacp.data, make_lin(p6, CDS.srcp4p1ktalpacp), parametrupavktalpac.index("P4-P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", CDS.srcp4p1ktalpacv.data, make_lin(p6, CDS.srcp4p1ktalpacv), parametrupavktalpac.index("P4-P1")]}


def kaliotalpac_update(attr, old, new):
	kaliotalpacr = {}
	kaliotalpacp = {}
	kaliotalpacv = {}
	dictpav = {"kaliotalpac": None}
	for key in parametktalpac.keys():
		if "kd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			if karareiksme < 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "vyzd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			if karareiksme > 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "derm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			if karareiksme > 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p4p1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametktalpac[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelektalpac, key)
			if karareiksme < 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		# if "rytas" in str(key):
		# 	kaliotalpacr[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	kaliotalpacp[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	kaliotalpacv[key] = karareiksme

		# if len(kaliotalpacr) == len(kaliotalpacp) == len(kaliotalpacv) == 8:
		# 	buklnustat(kaliotalpacr, kaliotalpacp, kaliotalpacv, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametktalpac.values()]])):
	w.on_change("value", kaliotalpac_update)

# Respiracinė alkalozė|acidozė

respialac = {
	"Norma KT": [13, 65, 5, 6.3, 6.8, 67, 0],
	"Norma AP": [19, 40, 10, 5.9, 6.6, 75, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.5, 2]}

parametrupavralac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "P1", "P4-P1"]
lenteleralac = pd.DataFrame(respialac, index=parametrupavralac)
lenteleralac = lenteleralac[["Norma KT", "Norma AP", "Pagrindas"]]

parametralac = {
	"kdrytas": [[kdrytas], "kdr", CDS.srckdralacr.data, make_lin(p7, CDS.srckdralacr), parametrupavralac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", CDS.srckdralacp.data, make_lin(p7, CDS.srckdralacp), parametrupavralac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", CDS.srckdralacv.data, make_lin(p7, CDS.srckdralacv), parametrupavralac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", CDS.srctksiralacr.data, make_lin(p7, CDS.srctksiralacr), parametrupavralac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", CDS.srctksiralacp.data, make_lin(p7, CDS.srctksiralacp), parametrupavralac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", CDS.srctksiralacv.data, make_lin(p7, CDS.srctksiralacv), parametrupavralac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", CDS.srckphiralacr.data, make_lin(p7, CDS.srckphiralacr), parametrupavralac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", CDS.srckphiralacp.data, make_lin(p7, CDS.srckphiralacp), parametrupavralac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", CDS.srckphiralacv.data, make_lin(p7, CDS.srckphiralacv), parametrupavralac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", CDS.srcuphkralacr.data, make_lin(p7, CDS.srcuphkralacr), parametrupavralac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", CDS.srcuphkralacp.data, make_lin(p7, CDS.srcuphkralacp), parametrupavralac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", CDS.srcuphkralacv.data, make_lin(p7, CDS.srcuphkralacv), parametrupavralac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", CDS.srcsphkralacr.data, make_lin(p7, CDS.srcsphkralacr), parametrupavralac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", CDS.srcsphkralacp.data, make_lin(p7, CDS.srcsphkralacp), parametrupavralac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", CDS.srcsphkralacv.data, make_lin(p7, CDS.srcsphkralacv), parametrupavralac.index("S-pHK")],

	"p(1)rytas": [[pgrytas], "p1r", CDS.srcp1ralacr.data, make_lin(p7, CDS.srcp1ralacr), parametrupavralac.index("P1")],
	"p(1)pietūs": [[pgpietus], "p1p", CDS.srcp1ralacp.data, make_lin(p7, CDS.srcp1ralacp), parametrupavralac.index("P1")],
	"p(1)vakaras": [[pgvakaras], "p1v", CDS.srcp1ralacv.data, make_lin(p7, CDS.srcp1ralacv), parametrupavralac.index("P1")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", CDS.srcp4p1ralacr.data, make_lin(p7, CDS.srcp4p1ralacr), parametrupavralac.index("P4-P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", CDS.srcp4p1ralacp.data, make_lin(p7, CDS.srcp4p1ralacp), parametrupavralac.index("P4-P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", CDS.srcp4p1ralacv.data, make_lin(p7, CDS.srcp4p1ralacv), parametrupavralac.index("P4-P1")]}


def respialac_update(attr, old, new):
	respialacr = {}
	respialacp = {}
	respialacv = {}
	dictpav = {"respialac": None}
	for key in parametralac.keys():
		if "kd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p(1)" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			if karareiksme < 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		elif "p4p1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametralac[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleralac, key)
			if karareiksme < 0:
				karareiksme = 0
			else:
				karareiksme
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)

		# if "rytas" in str(key):
		# 	respialacr[key] = karareiksme
		# elif "pietūs" in str(key):
		# 	respialacp[key] = karareiksme
		# elif "vakaras" in str(key):
		# 	respialacv[key] = karareiksme

		# if len(respialacr) == len(respialacp) == len(respialacv) == 7:
		# 	buklnustat(respialacr, respialacp, respialacv, dictpav) GERAI


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametralac.values()]])):
	w.on_change("value", respialac_update)

# Geriamasis vanduo

gervandfm = StringFormatter(font_style="bold")
gervandcol = [TableColumn(field="grupe", title="Geriamasis vanduo:", formatter=gervandfm)]
gerbandtable = DataTable(source=CDS.gervandsource, columns=gervandcol, width=600, height=75, row_headers=None)

# Organinės rūgštys

orgrugfm = StringFormatter(font_style="bold")
orgrugcol = [TableColumn(field="grupe", title="Organinės rūgštys:", formatter=orgrugfm)]
orgrugtable = DataTable(source=CDS.orgrugsource, columns=orgrugcol, width=600, height=125, row_headers=None)

# Hidrokarbonatai

hidrokarbofm = StringFormatter(font_style="bold")
hidrokarbocol = [TableColumn(field="grupe", title="Hidrokarbonatai:", formatter=hidrokarbofm)]
hidrokarbotable = DataTable(source=CDS.hidrokarbosource, columns=hidrokarbocol, width=600, height=50, row_headers=None)

# Natris, chloras, fluoras

natchlofluofm = StringFormatter(font_style="bold")
natchlofluocol = [TableColumn(field="grupe", title="Natris, chloras, fluoras:", formatter=natchlofluofm)]
natchlofluotable = DataTable(source=CDS.natchlofluosource, columns=natchlofluocol, width=600, height=75, row_headers=None)

# Sulfatai

sulfatfm = StringFormatter(font_style="bold")
sulfatcol = [TableColumn(field="grupe", title="Sulfatai:", formatter=sulfatfm)]
sulfattable = DataTable(source=CDS.sulfatsource, columns=sulfatcol, width=600, height=50, row_headers=None)

# Krakmolo šaltiniai

krakmolfm = StringFormatter(font_style="bold")
krakmolcol = [TableColumn(field="grupe", title="Krakmolo šaltiniai:", formatter=krakmolfm)]
krakmoltable = DataTable(source=CDS.krakmolsource, columns=krakmolcol, width=600, height=50, row_headers=None)

# Augaliniai inertinai (ląsteliena)

augalinertfm = StringFormatter(font_style="bold")
augalinertcol = [TableColumn(field="grupe", title="Augaliniai inertinai (ląsteliena):", formatter=augalinertfm)]
augalinerttable = DataTable(source=CDS.augalinertsource, columns=augalinertcol, width=600, height=50, row_headers=None)

# Neaugaliniai inertinai

neaugalinertfm = StringFormatter(font_style="bold")
neaugalinertcol = [TableColumn(field="grupe", title="Neaugaliniai inertinai:", formatter=neaugalinertfm)]
neaugalinerttable = DataTable(source=CDS.neaugalinertsource, columns=neaugalinertcol, width=600, height=75, row_headers=None)

# Polinesotieji riebalai

poliriebfm = StringFormatter(font_style="bold")
poliriebcol = [TableColumn(field="grupe", title="Polinesotieji riebalai:", formatter=poliriebfm)]
poliriebtable = DataTable(source=CDS.poliriebsource, columns=poliriebcol, width=600, height=175, row_headers=None)


# Mononesotieji riebalai

monoriebfm = StringFormatter(font_style="bold")
monoriebcol = [TableColumn(field="grupe", title="Mononesotieji riebalai:", formatter=monoriebfm)]
monoriebtable = DataTable(source=CDS.monoriebsource, columns=monoriebcol, width=600, height=100, row_headers=None)

# Sotieji riebalai

sotriebfm = StringFormatter(font_style="bold")
sotriebcol = [TableColumn(field="grupe", title="Sotieji riebalai:", formatter=sotriebfm)]
sotriebtable = DataTable(source=CDS.sotriebsource, columns=sotriebcol, width=600, height=75, row_headers=None)

# Stipriai pakitę baltymai ir riebalai

spbaltirriebfm = StringFormatter(font_style="bold")
spbaltirriebcol = [TableColumn(field="grupe", title="Stipriai pakitę baltymai ir riebalai:", formatter=spbaltirriebfm)]
spbaltirriebtable = DataTable(source=CDS.spbaltirriebsource, columns=spbaltirriebcol, width=600, height=200, row_headers=None)


# Kiaušiniai

kiausiniaifm = StringFormatter(font_style="bold")
kiausiniaicol = [TableColumn(field="grupe", title="Kiaušiniai:", formatter=kiausiniaifm)]
kiausiniaitable = DataTable(source=CDS.kiaussource, columns=kiausiniaicol, width=600, height=50, row_headers=None)

# Organai

organaifm = StringFormatter(font_style="bold")
organaicol = [TableColumn(field="grupe", title="Organai:", formatter=organaifm)]
organaitable = DataTable(source=CDS.organsource, columns=organaicol, width=600, height=50, row_headers=None)


# Pieno baltymai datatable

pienbaltfm = StringFormatter(font_style="bold")
pienbaltcol = [TableColumn(field="grupe", title="Pieno baltymai:", formatter=pienbaltfm)]
pienbalttable = DataTable(source=CDS.pienbaltsource, columns=pienbaltcol, width=600, height=75, row_headers=None)

# Moliuskai ir vėžiagyviai

moliuvezfm = StringFormatter(font_style="bold")
moliuvezcol = [TableColumn(field="grupe", title="Moliuskai ir vėžiagyviai:", formatter=moliuvezfm)]
moliuveztable = DataTable(source=CDS.moliuvezsource, columns=moliuvezcol, width=600, height=50, row_headers=None)

# Balta mėsa

baltamesafm = StringFormatter(font_style="bold")
baltamesacol = [TableColumn(field="grupe", title="Balta mėsa:", formatter=baltamesafm)]
baltamesatable = DataTable(source=CDS.baltamesasource, columns=baltamesacol, width=600, height=75, row_headers=None)

# Raudona mėsa

raudomesafm = StringFormatter(font_style="bold")
raudomesacol = [TableColumn(field="grupe", title="Raudona mėsa:", formatter=raudomesafm)]
raudomesatable = DataTable(source=CDS.raudomesasource, columns=raudomesacol, width=600, height=75, row_headers=None)

# Grybai

grybaifm = StringFormatter(font_style="bold")
grybaicol = [TableColumn(field="grupe", title="Grybai:", formatter=grybaifm)]
grybaitable = DataTable(source=CDS.grybaisource, columns=grybaicol, width=600, height=50, row_headers=None)

# Augaliniai baltymai

augalbaltfm = StringFormatter(font_style="bold")
augalbaltcol = [TableColumn(field="grupe", title="Augaliniai baltymai:", formatter=augalbaltfm)]
augalbalttable = DataTable(source=CDS.augalbaltsource, columns=augalbaltcol, width=600, height=50, row_headers=None)


# visi elementai sujungiami į norimą layout
lay1 = row(protok(), invard, inpavard, lytis, inamz)
lay2 = column(tikslus(), pagrapras())
lay3 = layout(
	[slapimo()],
	[aprslarugs(), slarugrytas, slarugpietus, slarugvakaras],
	[aprslasvies(), slasvrytas, slasvpietus, slasvvakaras],
	[aprslatank(), slatankrytas, slatankpietus, slatankvakaras],
	[aprslaputo(), slaputrytas, slaputpietus, slaputvakaras],
	[prikseil()],
	[seiliu()],
	[aprseilrugst(), serrytas, serpietus, servakaras],
	[aprseilklamp(), sekrytas, sekpietus, sekvakaras],
	[tiriam()],
	[kraujot()],
	[aprpulsed(), psrytas, pspietus, psvakaras],
	[refleksu()],
	[aprkunotemp(), ktrytas, ktpietus, ktvakaras],
	[aprdermoref(), drrytas, drpietus, drvakaras],
	[aprvasomref(), vrrytas, vrpietus, vrvakaras],
	[aprvyzdyd(), vdrytas, vdpietus, vdvakaras],
	[aprtremoref(), trrytas, trpietus, trvakaras],
	[aprsneruzgu(), surytas, supietus, suvakaras],
	[tiriam1()],
	[aprsarglinref(), slrytas, slpietus, slvakaras],
	[tiriam2()],
	[kvepparmat10()],
	[aprkvepdaz(), kdrytas, kdpietus, kdvakaras],
	[tiriam3()],
	[kraujparmat()],
	[aprpulgul(), pgrytas, pgpietus, pgvakaras],
	[aprsiskraujgul(), skgrytas, skgpietus, skgvakaras],
	[aprdiakraujgul(), dkgrytas, dkgpietus, dkgvakaras],
	[ortatest()],
	[aprpulsatsi15()],
	[atsist(), parytas, papietus, pavakaras],
	[po15(), pa15rytas, pa15pietus, pa15vakaras],
	[aprkraujpulsatsi45()],
	[siskraujatsi(), skarytas, skapietus, skavakaras],
	[diaskraujatsi(), dkarytas, dkapietus, dkavakaras],
	[pulsatsi45(), pa45rytas, pa45pietus, pa45vakaras],
	[tiriam4()],
	[kvepparmat14()],
	[aprkvepsu(), ksirytas, ksipietus, ksivakaras])

grid = gridplot([spacer_1, p1, spacer_2, p2, spacer_3, p3, spacer_4, p4, spacer_5, p5, spacer_6, p6, spacer_7, p7], ncols=1)
lay4 = row(spacer_0, rekomendmyg)
lay5 = column(grid, lay4, rekokatego(), rekotipai())
lay6 = row(lay3, lay5)

dt1 = column(
	gerbandtable,
	orgrugtable,
	hidrokarbotable,
	natchlofluotable,
	sulfattable,
	krakmoltable,
	neaugalinerttable,
	poliriebtable,
	monoriebtable,
	sotriebtable,
	spbaltirriebtable,
	kiausiniaitable,
	organaitable,
	pienbalttable,
	moliuveztable,
	baltamesatable,
	raudomesatable,
	grybaitable,
	augalbalttable
)
lay7 = column(maistproduk(), dt1)
lay8 = column(lay1, lay2, lay6, lay7)

# add the layout to curdoc
curdoc().add_root(lay8)
