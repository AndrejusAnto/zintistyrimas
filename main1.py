
# -*- coding: utf-8 -*-

from bokeh.io import curdoc, export_png, export_svgs
from bokeh.layouts import column, row, layout, gridplot
from bokeh.models.widgets import TextInput, Div, Select, Button, DataTable, TableColumn, StringFormatter, TextAreaInput
from bokeh.models import Spacer
import jinja2
from statistics import mean
import math
import logging
import pandas as pd
import itertools
import grafikai
import CDS
import base64
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
from collections import OrderedDict

from bokeh.core.properties import String, Instance
from bokeh.models import LayoutDOM, Slider, InputWidget


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
			min-width: 50px !important;
			width: 50px !important;
			}
			.bk-root input[name$="rytas"] {
			min-width: 60px !important;
			width: 60px !important;
			}
			.bk-root input[name$="pietus"] {
			min-width: 60px !important;
			width: 60px !important;
			}
			.bk-root input[name$="vakaras"] {
			min-width: 60px !important;
			width: 60px !important;
			}

			textarea {
			font-family:"Noto Sans", sans-serif;
			font-size: 13px;
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
			top: 50%;
			left: 50%;
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
# def protok():
# 	return Div(text="""<br><b>ORGANIZMO BŪKLĖS TYRIMO PROTOKOLAS</b>""", width=330, height=15)
protok = Div(text="""<br><b>ORGANIZMO BŪKLĖS TYRIMO PROTOKOLAS</b>""", width=330, height=50)
invard = TextInput(name="vard", value="", title="Vardas", width=130, height=20)
inpavard = TextInput(name="pavard", value="", title="Pavardė", width=160, height=20)
lytis = Select(name="lyt", title="Lytis:", options=["Vyras", "Moteris"], value="Vyras", width=130, height=20)
inamz = TextInput(name="amz", value="", title="Amžius", width=80, height=20)

pagrapras = Div(text="""Tikslūs organizmo tyrimo metu atliekamų testų rezultatai padeda geriau suprasti organizme vykstančius procesus,
	todėl tinkamas pasirengimas tyrimui yra labai svarbus tikrajai Jūsų organizmo būklei nustatyti:<br>
<b>3-2 SAVAITĖS IKI TYRIMŲ DIENOS:</b><br>
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

slapimo = Div(text="""<b>3. Šlapimo parametrų matavimas:</b>""", width=300)

aprslarugs = Div(text="""
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


aprslasvies = Div(text="""
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

aprslatank = Div(text="""
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

aprslaputo = Div(text="""
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

prikseil = Div(text="""<b > 4.</b><i>Tiriamojo paprašoma prikaupti seilių ir įspjauti į valgomąjį šaukštą. Seilių turi būti
maždaug mažojo piršto galinio narelio dydžio lašas.</i>""", width=750)

seiliu = Div(text="""<b>5. Seilių parametrų matavimas:</b>""", width=300)

aprseilrugst = Div(text="""
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

aprseilklamp = Div(text="""
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

tiriam = Div(text="""<b>6.</b><i>Tiriamojo paprašoma atsisėsti ant sofos arba lovos per vidurį.</i>""", width=780)
kraujot = Div(text="""<b>7. Kraujotakos parametrų matavimas:</b>""", width=300)

aprpulsed = Div(text="""
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

refleksu = Div(text="""<b>8. Refleksų tyrimas:</b>""", width=300)

aprkunotemp = Div(text="""
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

aprdermoref = Div(text="""
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


aprvasomref = Div(text="""
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

aprvyzdyd = Div(text="""
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

aprtremoref = Div(text="""
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

aprsneruzgu = Div(text="""
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


tiriam1 = Div(text="""<i>Tiriamojo paprašoma atsigulti ant sofos ar lovos ant kurios sėdi. Gulamasi
ištiestomis kojomis, galvą dedant taip, kad prie sofos ar lovos krašto būtų tiriamojo kairė
pusė. Paliekamas toks tarpas nuo sofos ar lovos krašto, kad tiriamojo kairė ranka laisvai
gulėtų šalia delnu į viršų. Paprašoma atsipalaiduoti, nekalbėti ir nusiraminti. Taip
tiriamasis turi pagulėti daugiau nei 1 minutę.</i>""", width=750)

aprsarglinref = Div(text="""
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

tiriam2 = Div(text="""<b>9.</b><i>Tiriamajam pranešama, kad jis jau gali užsidengti pilvą ir paprašoma atsipalaiduoti,
nekalbėti ir nusiraminti. Taip tiriamasis turi pagulėti daugiau nei 1 minutę.</i></b>""", width=750)

kvepparmat10 = Div(text="""<b>10. Kvėpavimo parametrų matavimas:</b>""", width=300)

aprkvepdaz = Div(text="""
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

tiriam3 = Div(text="""<b>11.</b><i>Tiriamajam ant kairės rankos žasto uždedama kraujospūdžio matavimo manžetė.</i>""", width=750)

kraujparmat = Div(text="""<b>12. Kraujotakos parametrų matavimas:</b>""", width=300)

aprpulgul = Div(text="""
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

aprsiskraujgul = Div(text="""
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

aprdiakraujgul = Div(text="""
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

ortatest = Div(text="""<b>Ortostatinis testas.</b> Tiriamajam atsistojus, kraujospūdžio matuoklio žarnelė neturi
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

aprpulsatsi15 = Div(text="""
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
atsist = Div(text="""<br>Atsistojus<br>(dūžių skaičius per pirmas 15 s,×4)""", width=300)
po15 = Div(text="""<br>Po 15 s.<br>(dūžių skaičius tarp 15-tos ir 45-tos sekundės,×2)""", width=300)

parytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
papietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

pa15rytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pa15pietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pa15vakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

aprkraujpulsatsi45 = Div(text="""
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

siskraujatsi = Div(text="""<br>Sistolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „SYS“ po 45 s)""", width=300)
diaskraujatsi = Div(text="""<br>Diastolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „DIA“)""", width=300)
pulsatsi45 = Div(text="""<br>Pulsas atsistojus po 45 s<br>(rodmuo ekrane ties „PULS“)""", width=300)

skarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
skapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
skavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

dkarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
dkapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
dkavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

pa45rytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pa45pietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pa45vakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

tiriam4 = Div(text="""<b>13.</b><i> Nuimama manžetė nuo tiriamojo žasto.</i>""", width=300)

kvepparmat14 = Div(text="""<b>14. Kvėpavimo parametrų matavimas:</b>""", width=300)

aprkvepsu = Div(text="""
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

maistproduk = Div(text="""<b>Maisto produktų prioritetai</b>""", width=270)
kitumedz = Div(text="""<b>Kitų medžiagų vartojimo prioritetai</b>""", width=270)
kitielgsen = Div(text="""<b>Kiti elgsenos prioritetai</b>""", width=270)
kitosreko = Div(text="""<b>Kitos rekomendacijos</b>""", width=270)

kitosrekolentel = TextAreaInput(rows=10)

rekomendmyg = Button(label="Rekomendacijos", button_type="success", height=30)
rekokatego = Div(text="""Kategorijos išdėstytos svarbos mažėjimo tvarka,
		tad jei prioritetai dėl tam tikrų maisto produktų vienas kitam prieštarauja, vadovautis tuo, kuris yra aukščiau.""", width=570)
rekotipai = Div(text="""<i>Prioritetų žymėjimas:
		Žalia spalva - rekomenduojama vartoti daugiau,
		Raudona spalva - vartoti nerekomenduojama,
		Tamsiai geltona spalva - vartoti saikingai (taip retai, kad būtų sunku prisiminti ankstesnio vartojimo datą),
		Jokios spalvos - papildomų rekomendacijų nėra.</i>""", width=570)

spacer_0 = Spacer(width=150, height=20)
spacer_1 = Spacer(width=150, height=60)
spacer_2 = Spacer(width=150, height=60)
spacer_3 = Spacer(width=150, height=60)
spacer_4 = Spacer(width=150, height=60)
spacer_5 = Spacer(width=150, height=60)
spacer_6 = Spacer(width=150, height=60)
spacer_7 = Spacer(width=150, height=60)
spacer_8 = Spacer(width=180)

# Maisto produktų prioritetai
# Geriamasis vanduo datatable
vandulist = CDS.vanduo()
vanduocds = CDS.gervandsource()
gervandfm = StringFormatter(font_style="bold")
gervandcol = [TableColumn(field="grupe", title="Geriamasis vanduo:", formatter=gervandfm)]
gervandtable = DataTable(source=vanduocds, columns=gervandcol, width=600, height=75, index_header=None, index_position=None)


# Organinės rūgštys
orgruglist = CDS.orgrug()
orgrugcds = CDS.orgrugsource()
orgrugfm = StringFormatter(font_style="bold")
orgrugcol = [TableColumn(field="grupe", title="Organinės rūgštys:", formatter=orgrugfm)]
orgrugtable = DataTable(source=orgrugcds, columns=orgrugcol, width=600, height=125, index_header=None, index_position=None)

# Hidrokarbonatai
hidrokarbolist = CDS.hidrokarbo()
hidrokarbocds = CDS.hidrokarbosource()
hidrokarbofm = StringFormatter(font_style="bold")
hidrokarbocol = [TableColumn(field="grupe", title="Hidrokarbonatai:", formatter=hidrokarbofm)]
hidrokarbotable = DataTable(source=hidrokarbocds, columns=hidrokarbocol, width=600, height=50, index_header=None, index_position=None)

# Natris, chloras, fluoras
natchlofluolist = CDS.natchlofluo()
natchlofluocds = CDS.natchlofluosource()
natchlofluofm = StringFormatter(font_style="bold")
natchlofluocol = [TableColumn(field="grupe", title="Natris, chloras, fluoras:", formatter=natchlofluofm)]
natchlofluotable = DataTable(source=natchlofluocds, columns=natchlofluocol, width=600, height=75, index_header=None, index_position=None)

# Sulfatai
sulfatlist = CDS.sulfat()
sulfatcds = CDS.sulfatsource()
sulfatfm = StringFormatter(font_style="bold")
sulfatcol = [TableColumn(field="grupe", title="Sulfatai:", formatter=sulfatfm)]
sulfattable = DataTable(source=sulfatcds, columns=sulfatcol, width=600, height=50, index_header=None, index_position=None)

# Krakmolo šaltiniai
krakmollist = CDS.krakmol()
krakmolcds = CDS.krakmolsource()
krakmolfm = StringFormatter(font_style="bold")
krakmolcol = [TableColumn(field="grupe", title="Krakmolo šaltiniai:", formatter=krakmolfm)]
krakmoltable = DataTable(source=krakmolcds, columns=krakmolcol, width=600, height=50, index_header=None, index_position=None)

# Augaliniai inertinai (ląsteliena)
augalinertlist = CDS.augalinert()
augalinertcds = CDS.augalinertsource()
augalinertfm = StringFormatter(font_style="bold", text_color="green")
augalinertcol = [TableColumn(field="grupe", title="Augaliniai inertinai (ląsteliena):", formatter=augalinertfm)]
augalinerttable = DataTable(source=augalinertcds, columns=augalinertcol, width=600, height=50, index_header=None, index_position=None)

# Neaugaliniai inertinai
neaugalinert = CDS.neaugalinert()
neaugalinertcds = CDS.neaugalinertsource()
neaugalinertfm = StringFormatter(font_style="bold", text_color="green")
neaugalinertcol = [TableColumn(field="grupe", title="Neaugaliniai inertinai:", formatter=neaugalinertfm)]
neaugalinerttable = DataTable(source=neaugalinertcds, columns=neaugalinertcol, width=600, height=75, index_header=None, index_position=None)

# Polinesotieji riebalai
polirieblist = CDS.polirieb()
poliriebcds = CDS.poliriebsource()
poliriebfm = StringFormatter(font_style="bold")
poliriebcol = [TableColumn(field="grupe", title="Polinesotieji riebalai:", formatter=poliriebfm)]
poliriebtable = DataTable(source=poliriebcds, columns=poliriebcol, width=600, height=175, index_header=None, index_position=None)

# Mononesotieji riebalai
monorieblist = CDS.monorieb()
monoriebcds = CDS.monoriebsource()
monoriebfm = StringFormatter(font_style="bold")
monoriebcol = [TableColumn(field="grupe", title="Mononesotieji riebalai:", formatter=monoriebfm)]
monoriebtable = DataTable(source=monoriebcds, columns=monoriebcol, width=600, height=100, index_header=None, index_position=None)

# Sotieji riebalai
sotrieblist = CDS.sotrieb()
sotriebcds = CDS.sotriebsource()
sotriebfm = StringFormatter(font_style="bold")
sotriebcol = [TableColumn(field="grupe", title="Sotieji riebalai:", formatter=sotriebfm)]
sotriebtable = DataTable(source=sotriebcds, columns=sotriebcol, width=600, height=75, index_header=None, index_position=None)

# Stipriai pakitę baltymai ir riebalai
spbaltirrieblist = CDS.spbaltirrieb()
spbaltirriebcds = CDS.spbaltirriebsource()
spbaltirriebfm = StringFormatter(font_style="bold")
spbaltirriebcol = [TableColumn(field="grupe", title="Stipriai pakitę baltymai ir riebalai:", formatter=spbaltirriebfm)]
spbaltirriebtable = DataTable(source=spbaltirriebcds, columns=spbaltirriebcol, width=600, height=200, index_header=None, index_position=None)

# Kiaušiniai
kiausiniailist = CDS.kiausiniai()
kiausiniaicds = CDS.kiaussource()
kiausiniaifm = StringFormatter(font_style="bold")
kiausiniaicol = [TableColumn(field="grupe", title="Kiaušiniai:", formatter=kiausiniaifm)]
kiausiniaitable = DataTable(source=kiausiniaicds, columns=kiausiniaicol, width=600, height=50, index_header=None, index_position=None)

# Organai
organailist = CDS.organai()
organaicds = CDS.organsource()
organaifm = StringFormatter(font_style="bold")
organaicol = [TableColumn(field="grupe", title="Organai:", formatter=organaifm)]
organaitable = DataTable(source=organaicds, columns=organaicol, width=600, height=50, index_header=None, index_position=None)

# Pieno baltymai
pienbaltlist = CDS.pienbalt()
pienbaltcds = CDS.pienbaltsource()
pienbaltfm = StringFormatter(font_style="bold")
pienbaltcol = [TableColumn(field="grupe", title="Pieno baltymai:", formatter=pienbaltfm)]
pienbalttable = DataTable(source=pienbaltcds, columns=pienbaltcol, width=600, height=75, index_header=None, index_position=None)

# Moliuskai ir vėžiagyviai
moliuvezlist = CDS.moliuvez()
moliuvezcds = CDS.moliuvezsource()
moliuvezfm = StringFormatter(font_style="bold")
moliuvezcol = [TableColumn(field="grupe", title="Moliuskai ir vėžiagyviai:", formatter=moliuvezfm)]
moliuveztable = DataTable(source=moliuvezcds, columns=moliuvezcol, width=600, height=50, index_header=None, index_position=None)

# Balta mėsa
baltamesalist = CDS.baltamesa()
baltamesacds = CDS.baltamesasource()
baltamesafm = StringFormatter(font_style="bold")
baltamesacol = [TableColumn(field="grupe", title="Balta mėsa:", formatter=baltamesafm)]
baltamesatable = DataTable(source=baltamesacds, columns=baltamesacol, width=600, height=75, index_header=None, index_position=None)

# Raudona mėsa
raudomesalist = CDS.raudomesa()
raudomesacds = CDS.raudomesasource()
raudomesafm = StringFormatter(font_style="bold")
raudomesacol = [TableColumn(field="grupe", title="Raudona mėsa:", formatter=raudomesafm)]
raudomesatable = DataTable(source=raudomesacds, columns=raudomesacol, width=600, height=75, index_header=None, index_position=None)

# Grybai
grybailist = CDS.grybai()
grybaicds = CDS.grybaisource()
grybaifm = StringFormatter(font_style="bold")
grybaicol = [TableColumn(field="grupe", title="Grybai:", formatter=grybaifm)]
grybaitable = DataTable(source=grybaicds, columns=grybaicol, width=600, height=50, index_header=None, index_position=None)

# Augaliniai baltymai
augalbaltlist = CDS.augalbalt()
augalbaltcds = CDS.augalbaltsource()
augalbaltfm = StringFormatter(font_style="bold")
augalbaltcol = [TableColumn(field="grupe", title="Augaliniai baltymai:", formatter=augalbaltfm)]
augalbalttable = DataTable(source=augalbaltcds, columns=augalbaltcol, width=600, height=50, index_header=None, index_position=None)

# Kitų medžiagų vartojimo prioritetai

# Pakeistų savybių vanduo
paksavyvanduolist = CDS.paksavyvanduo()
paksavyvanduocds = CDS.paksavyvanduosource()
paksavyvanduofm = StringFormatter(font_style="bold")
paksavyvanduocol = [TableColumn(field="grupe", title="Pakeistų savybių vanduo:", formatter=paksavyvanduofm)]
paksavyvanduotable = DataTable(source=paksavyvanduocds, columns=paksavyvanduocol, width=600, height=75, index_header=None, index_position=None)

# Slopikliai
slopikailist = CDS.slopikai()
slopikaicds = CDS.slopikaisource()
slopikaifm = StringFormatter(font_style="bold")
slopikaicol = [TableColumn(field="grupe", title="Slopikliai:", formatter=slopikaifm)]
slopikaitable = DataTable(source=slopikaicds, columns=slopikaicol, width=600, height=50, index_header=None, index_position=None)

# Stimuliatoriai
stimuliatlist = CDS.stimuliat()
stimuliatcds = CDS.stimuliatsource()
stimuliatfm = StringFormatter(font_style="bold")
stimuliatcol = [TableColumn(field="grupe", title="Stimuliatoriai:", formatter=stimuliatfm)]
stimuliattable = DataTable(source=stimuliatcds, columns=stimuliatcol, width=600, height=75, index_header=None, index_position=None)

# Rūkalai
rukalailist = CDS.rukalai()
rukalaicds = CDS.rukalaisource()
rukalaifm = StringFormatter(font_style="bold")
rukalaicol = [TableColumn(field="grupe", title="Rūkalai:", formatter=rukalaifm)]
rukalaitable = DataTable(source=rukalaicds, columns=rukalaicol, width=600, height=50, index_header=None, index_position=None)

# Kiti elgsenos prioritetai

# Didelio intensyvumo trumpos trukmės fizinė veikla
didintesyvlist = CDS.didintesyv()
didintesyvcds = CDS.didintesyvsource()
didintesyvfm = StringFormatter(font_style="bold")
didintesyvcol = [TableColumn(field="grupe", title="Didelio intensyvumo trumpos trukmės fizinė veikla:", formatter=didintesyvfm)]
didintesyvtable = DataTable(source=didintesyvcds, columns=didintesyvcol, width=600, height=75, index_header=None, index_position=None)

# Mažo intensyvumo ilgos trukmės fizinė veikla
mazointesyvlist = CDS.mazointesyv()
mazointesyvcds = CDS.mazointesyvsource()
mazointesyvfm = StringFormatter(font_style="bold")
mazointesyvcol = [TableColumn(field="grupe", title="Mažo intensyvumo ilgos trukmės fizinė veikla:", formatter=mazointesyvfm)]
mazointesyvtable = DataTable(source=mazointesyvcds, columns=mazointesyvcol, width=600, height=50, index_header=None, index_position=None)

# Kvėpavimo balansavimas
kvepasulaiklist = CDS.kvepasulaik()
kvepasulaikcds = CDS.kvepasulaiksource()
kvepasulaikfm = StringFormatter(font_style="bold", text_color="#CCCC00")
kvepasulaikcol = [TableColumn(field="grupe", title="Kvėpavimo balansavmas:", formatter=kvepasulaikfm)]
kvepasulaiktable = DataTable(source=kvepasulaikcds, columns=kvepasulaikcol, width=600, height=50, index_header=None, index_position=None)

# Hipoventiliacija
hipoventillist = CDS.hipoventil()
hipoventilcds = CDS.hipoventilsource()
hipoventilfm = StringFormatter(font_style="bold")
hipoventilcol = [TableColumn(field="grupe", title="Hipoventiliacija:", formatter=hipoventilfm)]
hipoventiltable = DataTable(source=hipoventilcds, columns=hipoventilcol, width=600, height=50, index_header=None, index_position=None)

# Grūdinimasis
grudinimaslist = CDS.grudinimas()
grudinimascds = CDS.grudinimassource()
grudinimasfm = StringFormatter(font_style="bold")
grudinimascol = [TableColumn(field="grupe", title="Grūdinimasis:", formatter=grudinimasfm)]
grudinimastable = DataTable(source=grudinimascds, columns=grudinimascol, width=600, height=50, index_header=None, index_position=None)

# Kaitinimasis
kaitinimaslist = CDS.kaitinimas()
kaitinimascds = CDS.kaitinimassource()
kaitinimasfm = StringFormatter(font_style="bold")
kaitinimascol = [TableColumn(field="grupe", title="Kaitinimasis:", formatter=kaitinimasfm)]
kaitinimastable = DataTable(source=kaitinimascds, columns=kaitinimascol, width=600, height=50, index_header=None, index_position=None)

# Galūnių laikymas šiltai
galuniulsillist = CDS.galuniulsil()
galuniulsilcds = CDS.galuniulsilsource()
galuniulsilfm = StringFormatter(font_style="bold")
galuniulsilcol = [TableColumn(field="grupe", title="Galūnių laikymas šiltai:", formatter=galuniulsilfm)]
galuniulsiltable = DataTable(source=galuniulsilcds, columns=galuniulsilcol, width=600, height=50, index_header=None, index_position=None)

# Galūnių laikymas šaltai
galuniulsallist = CDS.galuniulsal()
galuniulsalcds = CDS.galuniulsalsource()
galuniulsalfm = StringFormatter(font_style="bold")
galuniulsalcol = [TableColumn(field="grupe", title="Galūnių laikymas šaltai:", formatter=galuniulsalfm)]
galuniulsaltable = DataTable(source=galuniulsalcds, columns=galuniulsalcol, width=600, height=50, index_header=None, index_position=None)

# Buvimas šiltesnėje aplinkoje
buvsilapllist = CDS.buvsilapl()
buvsilaplcds = CDS.buvsilaplsource()
buvsilaplfm = StringFormatter(font_style="bold")
buvsilaplcol = [TableColumn(field="grupe", title="Buvimas šiltesnėje aplinkoje:", formatter=buvsilaplfm)]
buvsilapltable = DataTable(source=buvsilaplcds, columns=buvsilaplcol, width=600, height=50, index_header=None, index_position=None)

# Buvimas šaltesnėje aplinkoje
buvsalapllist = CDS.buvsalapl()
buvsalaplcds = CDS.buvsalaplsource()
buvsalaplfm = StringFormatter(font_style="bold")
buvsalaplcol = [TableColumn(field="grupe", title="Buvimas šaltesnėje aplinkoje:", formatter=buvsalaplfm)]
buvsalapltable = DataTable(source=buvsalaplcds, columns=buvsalaplcol, width=600, height=50, index_header=None, index_position=None)

# Atidėta ejakuliacija (vyrams)
atidejakullist = CDS.atidejakul()
atidejakulcds = CDS.atidejakulsource()
atidejakulfm = StringFormatter(font_style="bold")
atidejakulcol = [TableColumn(field="grupe", title="Atidėta ejakuliacija (vyrams):", formatter=atidejakulfm)]
atidejakultable = DataTable(source=atidejakulcds, columns=atidejakulcol, width=600, height=50, index_header=None, index_position=None)

# Pakartotinis orgazmas (moterims)
pakartotorglist = CDS.pakartotorg()
pakartotorgcds = CDS.pakartotorgsource()
pakartotorgfm = StringFormatter(font_style="bold")
pakartotorgcol = [TableColumn(field="grupe", title="Pakartotinis orgazmas (moterims):", formatter=pakartotorgfm)]
pakartotorgtable = DataTable(source=pakartotorgcds, columns=pakartotorgcol, width=600, height=50, index_header=None, index_position=None)

# Limfotakos aktyvavimas
limfoaktyvlist = CDS.limfoaktyv()
limfoaktyvcds = CDS.limfoaktyvsource()
limfoaktyvfm = StringFormatter(font_style="bold")
limfoaktyvcol = [TableColumn(field="grupe", title="Limfotakos aktyvavimas:", formatter=limfoaktyvfm)]
limfoaktyvtable = DataTable(source=limfoaktyvcds, columns=limfoaktyvcol, width=600, height=50, index_header=None, index_position=None)

# Subalansuotas miegas
subalanmieglist = CDS.subalanmieg()
subalanmiegcds = CDS.subalanmiegsource()
subalanmiegfm = StringFormatter(font_style="bold", text_color="green")
subalanmiegcol = [TableColumn(field="grupe", title="Subalansuotas miegas:", formatter=subalanmiegfm)]
subalanmiegtable = DataTable(source=subalanmiegcds, columns=subalanmiegcol, width=600, height=75, index_header=None, index_position=None)

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
				ktarap = 0
		else:
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
			else:
				ktarap = 0
	else:
		if NormaKT == 16 and NormaAP == 8:
			pagrindas = 16
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
			else:
				ktarap = 0
		else:
			if (alfa * skirtum + beta) > 0:
				ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
			else:
				ktarap = 0


# nustatmomos grafiko linijų (katabolizmo ir anabolizmo reikšmių) skirtingos spalvos
	if ktarap > 0:
		if len(lin) == 1:
			lin[0].glyph.line_color = "blue"
		else:
			lin[0].glyph.line_color = "blue"
			lin[1].glyph.line_color = "red"

	else:
		if len(lin) == 1:
			lin[0].glyph.line_color = "red"
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
	katanaboltn = {}

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

		katanaboltn[api] = {"Katabolizmas": galutineknt, "Anabolizmas": galutineant}
	print(katanaboltn)
	return katanaboltn


# Simpatinis|parasimpatinis

simparasim = {
	"Norma KT": [-2, 11, 25, 6, 36.7, 1, -1, 1, 1, -1, 1, 1],
	"Norma AP": [0, 6, 22, 4, 36.5, 2, 1, -1, -1, 1, -1, -1],
	"Pagrindas": [2, 2, 2, 1.001, 2, 1.2, 1.001, 1.001, 1.001, 1.001, 1.001, 1.001]}

parametrupavsp = ["Ps-1", "S+D", "Pm1+Pm4", "KRi", "Temp", "Derm", "Vaso", "Vyzd", "Trem", "Nos", "Sarg", "S-kl"]
lentelesp = pd.DataFrame(simparasim, index=parametrupavsp)
lentelesp = lentelesp[["Norma KT", "Norma AP", "Pagrindas"]]

srcps1rcds = CDS.srcps1rcds()
srcps1pcds = CDS.srcps1pcds()
srcps1vcds = CDS.srcps1vcds()

srcspdrcds = CDS.srcspdrcds()
srcspdpcds = CDS.srcspdpcds()
srcspdvcds = CDS.srcspdvcds()

srcpm1ppm4rcds = CDS.srcpm1ppm4rcds()
srcpm1ppm4pcds = CDS.srcpm1ppm4pcds()
srcpm1ppm4vcds = CDS.srcpm1ppm4vcds()

srckrircds = CDS.srckrircds()
srckripcds = CDS.srckripcds()
srckrivcds = CDS.srckrivcds()

srctemprcds = CDS.srctemprcds()
srctemppcds = CDS.srctemppcds()
srctempvcds = CDS.srctempvcds()

srcdermsprcds = CDS.srcdermsprcds()
srcdermsppcds = CDS.srcdermsppcds()
srcdermspvcds = CDS.srcdermspvcds()

srcvasorcds = CDS.srcvasorcds()
srcvasopcds = CDS.srcvasopcds()
srcvasovcds = CDS.srcvasovcds()

srcvyzdsprcds = CDS.srcvyzdsprcds()
srcvyzdsppcds = CDS.srcvyzdsppcds()
srcvyzdspvcds = CDS.srcvyzdspvcds()

srctremrcds = CDS.srctremrcds()
srctrempcds = CDS.srctrempcds()
srctremvcds = CDS.srctremvcds()

srcnosrcds = CDS.srcnosrcds()
srcnospcds = CDS.srcnospcds()
srcnosvcds = CDS.srcnosvcds()

srcsargrcds = CDS.srcsargrcds()
srcsargpcds = CDS.srcsargpcds()
srcsargvcds = CDS.srcsargvcds()

srcsklrcds = CDS.srcsklrcds()
srcsklpcds = CDS.srcsklpcds()
srcsklvcds = CDS.srcsklvcds()

parametsp = {
	"ps1rytas": [[psrytas, pgrytas], "ps1r", srcps1rcds.data, make_lin(p1, srcps1rcds), parametrupavsp.index("Ps-1")],
	"ps1pietūs": [[pspietus, pgpietus], "ps1p", srcps1pcds.data, make_lin(p1, srcps1pcds), parametrupavsp.index("Ps-1")],
	"ps1vakaras": [[psvakaras, pgvakaras], "ps1v", srcps1vcds.data, make_lin(p1, srcps1vcds), parametrupavsp.index("Ps-1")],

	"s+drytas": [[skarytas, skgrytas, dkarytas, dkgrytas], "s+dr", srcspdrcds.data, make_lin(p1, srcspdrcds), parametrupavsp.index("S+D")],
	"s+dpietūs": [[skapietus, skgpietus, dkapietus, dkgpietus], "s+dp", srcspdpcds.data, make_lin(p1, srcspdpcds), parametrupavsp.index("S+D")],
	"s+dvakaras": [[skavakaras, skgvakaras, dkavakaras, dkgvakaras], "s+dv", srcspdvcds.data, make_lin(p1, srcspdvcds), parametrupavsp.index("S+D")],

	"pm1+pm4rytas": [[pgrytas, parytas, pa15rytas, pa45rytas], "pm1+pm4r", srcpm1ppm4rcds.data, make_lin(p1, srcpm1ppm4rcds), parametrupavsp.index("Pm1+Pm4")],
	"pm1+pm4pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus], "pm1+pm4p", srcpm1ppm4pcds.data, make_lin(p1, srcpm1ppm4pcds), parametrupavsp.index("Pm1+Pm4")],
	"pm1+pm4vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras], "pm1+pm4v", srcpm1ppm4vcds.data, make_lin(p1, srcpm1ppm4vcds), parametrupavsp.index("Pm1+Pm4")],

	"krirytas": [[psrytas, kdrytas], "krir", srckrircds.data, make_lin(p1, srckrircds), parametrupavsp.index("KRi")],
	"kripietūs": [[pspietus, kdpietus], "krip", srckripcds.data, make_lin(p1, srckripcds), parametrupavsp.index("KRi")],
	"krivakaras": [[psvakaras, kdvakaras], "kriv", srckrivcds.data, make_lin(p1, srckrivcds), parametrupavsp.index("KRi")],

	"temprytas": [[ktrytas], "tempr", srctemprcds.data, make_lin(p1, srctemprcds), parametrupavsp.index("Temp")],
	"temppietūs": [[ktpietus], "tempp", srctemppcds.data, make_lin(p1, srctemppcds), parametrupavsp.index("Temp")],
	"tempvakaras": [[ktvakaras], "tempv", srctempvcds.data, make_lin(p1, srctempvcds), parametrupavsp.index("Temp")],

	"dermrytas": [[drrytas], "dermr", srcdermsprcds.data, make_lin(p1, srcdermsprcds), parametrupavsp.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", srcdermsppcds.data, make_lin(p1, srcdermsppcds), parametrupavsp.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", srcdermspvcds.data, make_lin(p1, srcdermspvcds), parametrupavsp.index("Derm")],

	"vasorytas": [[vrrytas], "vasor", srcvasorcds.data, make_lin(p1, srcvasorcds), parametrupavsp.index("Vaso")],
	"vasopietūs": [[vrpietus], "vasop", srcvasopcds.data, make_lin(p1, srcvasopcds), parametrupavsp.index("Vaso")],
	"vasovakaras": [[vrvakaras], "vasov", srcvasovcds.data, make_lin(p1, srcvasovcds), parametrupavsp.index("Vaso")],

	"vyzdrytas": [[vdrytas], "vyzdr", srcvyzdsprcds.data, make_lin(p1, srcvyzdsprcds), parametrupavsp.index("Vyzd")],
	"vyzdpietūs": [[vdpietus], "vyzdp", srcvyzdsppcds.data, make_lin(p1, srcvyzdsppcds), parametrupavsp.index("Vyzd")],
	"vyzdvakaras": [[vdvakaras], "vyzdv", srcvyzdspvcds.data, make_lin(p1, srcvyzdspvcds), parametrupavsp.index("Vyzd")],

	"tremrytas": [[trrytas], "tremr", srctremrcds.data, make_lin(p1, srctremrcds), parametrupavsp.index("Trem")],
	"trempietūs": [[trpietus], "tremp", srctrempcds.data, make_lin(p1, srctrempcds), parametrupavsp.index("Trem")],
	"tremvakaras": [[trvakaras], "tremv", srctremvcds.data, make_lin(p1, srctremvcds), parametrupavsp.index("Trem")],

	"nosrytas": [[surytas], "nosr", srcnosrcds.data, make_lin(p1, srcnosrcds), parametrupavsp.index("Nos")],
	"nospietūs": [[supietus], "nosp", srcnospcds.data, make_lin(p1, srcnospcds), parametrupavsp.index("Nos")],
	"nosvakaras": [[suvakaras], "nosv", srcnosvcds.data, make_lin(p1, srcnosvcds), parametrupavsp.index("Nos")],

	"sargrytas": [[slrytas], "sargr", srcsargrcds.data, make_lin(p1, srcsargrcds), parametrupavsp.index("Sarg")],
	"sargpietūs": [[slpietus], "sargp", srcsargpcds.data, make_lin(p1, srcsargpcds), parametrupavsp.index("Sarg")],
	"sargvakaras": [[slvakaras], "sargv", srcsargvcds.data, make_lin(p1, srcsargvcds), parametrupavsp.index("Sarg")],

	"sklrytas": [[sekrytas], "sklr", srcsklrcds.data, make_lin(p1, srcsklrcds), parametrupavsp.index("S-kl")],
	"sklpietūs": [[sekpietus], "sklp", srcsklpcds.data, make_lin(p1, srcsklpcds), parametrupavsp.index("S-kl")],
	"sklvakaras": [[sekvakaras], "sklv", srcsklvcds.data, make_lin(p1, srcsklvcds), parametrupavsp.index("S-kl")]}

# Ketogeninis|gliukogeninis

ketogliuko = {
	"Norma KT": [15, 1001, 1002, 6, 5, 1, -0.28],
	"Norma AP": [1000, 1001, 1002, 8, 0, -1, -0.18],
	"Pagrindas": [2, 1.2, 2.5, 2, 2, 1.1, 1.2]}

parametrupavkg = ["KD", "t(ksi)", "P4", "KpHi", "D2-P4", "U-šv", "U-put"]
lentelekg = pd.DataFrame(ketogliuko, index=parametrupavkg)
lentelekg = lentelekg[["Norma KT", "Norma AP", "Pagrindas"]]


srckdkgrcds = CDS.srckdkgrcds()
srckdkgpcds = CDS.srckdkgpcds()
srckdkgvcds = CDS.srckdkgvcds()

srctksikgrcds = CDS.srctksikgrcds()
srctksikgpcds = CDS.srctksikgpcds()
srctksikgvcds = CDS.srctksikgvcds()

srcp4rcds = CDS.srcp4rcds()
srcp4pcds = CDS.srcp4pcds()
srcp4vcds = CDS.srcp4vcds()

srckphikgrcds = CDS.srckphikgrcds()
srckphikgpcds = CDS.srckphikgpcds()
srckphikgvcds = CDS.srckphikgvcds()

srcd2p4rcds = CDS.srcd2p4rcds()
srcd2p4pcds = CDS.srcd2p4pcds()
srcd2p4vcds = CDS.srcd2p4vcds()

srcusvkgrcds = CDS.srcusvkgrcds()
srcusvkgpcds = CDS.srcusvkgpcds()
srcusvkgvcds = CDS.srcusvkgvcds()

srcuputkgrcds = CDS.srcuputkgrcds()
srcuputkgpcds = CDS.srcuputkgpcds()
srcuputkgvcds = CDS.srcuputkgvcds()

srcuputkg1rcds = CDS.srcuputkg1rcds()
srcuputkg1pcds = CDS.srcuputkg1pcds()
srcuputkg1vcds = CDS.srcuputkg1vcds()

parametkg = {
	"kdrytas": [[kdrytas, slatankrytas, serrytas], "kdr", srckdkgrcds.data, make_lin(p2, srckdkgrcds), parametrupavkg.index("KD")],
	"kdpietūs": [[kdpietus, slatankpietus, serpietus], "kdp", srckdkgpcds.data, make_lin(p2, srckdkgpcds), parametrupavkg.index("KD")],
	"kdvakaras": [[kdvakaras, slatankvakaras, servakaras], "kdv", srckdkgvcds.data, make_lin(p2, srckdkgvcds), parametrupavkg.index("KD")],

	"tksirytas": [[ksirytas, slatankrytas, serrytas], "tksir", srctksikgrcds.data, make_lin(p2, srctksikgrcds), parametrupavkg.index("t(ksi)")],
	"tksipietūs": [[ksipietus, slatankpietus, serpietus], "tksip", srctksikgpcds.data, make_lin(p2, srctksikgpcds), parametrupavkg.index("t(ksi)")],
	"tksivakaras": [[ksivakaras, slatankvakaras, servakaras], "tksiv", srctksikgvcds.data, make_lin(p2, srctksikgvcds), parametrupavkg.index("t(ksi)")],

	"p4rytas": [[pa45rytas, slatankrytas, serrytas], "p4r", srcp4rcds.data, make_lin(p2, srcp4rcds), parametrupavkg.index("P4")],
	"p4pietūs": [[pa45pietus, slatankpietus, serpietus], "p4p", srcp4pcds.data, make_lin(p2, srcp4pcds), parametrupavkg.index("P4")],
	"p4vakaras": [[pa45vakaras, slatankvakaras, servakaras], "p4v", srcp4vcds.data, make_lin(p2, srcp4vcds), parametrupavkg.index("P4")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", srckphikgrcds.data, make_lin(p2, srckphikgrcds), parametrupavkg.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", srckphikgpcds.data, make_lin(p2, srckphikgpcds), parametrupavkg.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", srckphikgvcds.data, make_lin(p2, srckphikgvcds), parametrupavkg.index("KpHi")],

	"d2p(4)rytas": [[dkarytas, pa45rytas], "d2p(4)r", srcd2p4rcds.data, make_lin(p2, srcd2p4rcds), parametrupavkg.index("D2-P4")],
	"d2p(4)pietūs": [[dkapietus, pa45pietus], "d2p(4)p", srcd2p4pcds.data, make_lin(p2, srcd2p4pcds), parametrupavkg.index("D2-P4")],
	"d2p(4)vakaras": [[dkavakaras, pa45vakaras], "d2p(4)v", srcd2p4vcds.data, make_lin(p2, srcd2p4vcds), parametrupavkg.index("D2-P4")],

	"usvrytas": [[slasvrytas], "usvr", srcusvkgrcds.data, make_lin(p2, srcusvkgrcds), parametrupavkg.index("U-šv")],
	"usvpietūs": [[slasvpietus], "usvp", srcusvkgpcds.data, make_lin(p2, srcusvkgpcds), parametrupavkg.index("U-šv")],
	"usvvakaras": [[slasvvakaras], "usvv", srcusvkgvcds.data, make_lin(p2, srcusvkgvcds), parametrupavkg.index("U-šv")],

	"uputrytas": [[slaputrytas], "uputr", [srcuputkgrcds.data, srcuputkg1rcds.data], make_lin(p2, srcuputkgrcds, srcuputkg1rcds), parametrupavkg.index("U-put")],
	"uputpietūs": [[slaputpietus], "uputp", [srcuputkgpcds.data, srcuputkg1pcds.data], make_lin(p2, srcuputkgpcds, srcuputkg1pcds), parametrupavkg.index("U-put")],
	"uputvakaras": [[slaputvakaras], "uputv", [srcuputkgvcds.data, srcuputkg1vcds.data], make_lin(p2, srcuputkgvcds, srcuputkg1vcds), parametrupavkg.index("U-put")]}

# Disaerobinis|anaerobinis

disaeanae = {
	"Norma KT": [18, 6.1, 6.8, 1, 1, 0.75],
	"Norma AP": [14, 6.3, 6.6, 2, -1, -0.5],
	"Pagrindas": [1.5, 2, 2, 1.5, 1.3, 1.1]}

parametrupavda = ["d(tank)", "U-pHK", "S-pHK", "Derm", "U-šv", "U-put"]
lenteleda = pd.DataFrame(disaeanae, index=parametrupavda)
lenteleda = lenteleda[["Norma KT", "Norma AP", "Pagrindas"]]

srcdtankrcds = CDS.srcdtankrcds()
srcdtankpcds = CDS.srcdtankpcds()
srcdtankvcds = CDS.srcdtankvcds()

srcuphkdarcds = CDS.srcuphkdarcds()
srcuphkdapcds = CDS.srcuphkdapcds()
srcuphkdavcds = CDS.srcuphkdavcds()

srcsphkdarcds = CDS.srcsphkdarcds()
srcsphkdapcds = CDS.srcsphkdapcds()
srcsphkdavcds = CDS.srcsphkdavcds()

srcdermdarcds = CDS.srcdermdarcds()
srcdermdapcds = CDS.srcdermdapcds()
srcdermdavcds = CDS.srcdermdavcds()

srcusvdarcds = CDS.srcusvdarcds()
srcusvdapcds = CDS.srcusvdapcds()
srcusvdavcds = CDS.srcusvdavcds()

srcuputdarcds = CDS.srcuputdarcds()
srcuputdapcds = CDS.srcuputdapcds()
srcuputdavcds = CDS.srcuputdavcds()

parametda = {
	"dtankrytas": [[slatankrytas], "dtankr", srcdtankrcds.data, make_lin(p3, srcdtankrcds), parametrupavda.index("d(tank)")],
	"dtankpietūs": [[slatankpietus], "dtankp", srcdtankpcds.data, make_lin(p3, srcdtankpcds), parametrupavda.index("d(tank)")],
	"dtankvakaras": [[slatankvakaras], "dtankv", srcdtankvcds.data, make_lin(p3, srcdtankvcds), parametrupavda.index("d(tank)")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", srcuphkdarcds.data, make_lin(p3, srcuphkdarcds), parametrupavda.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", srcuphkdapcds.data, make_lin(p3, srcuphkdapcds), parametrupavda.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", srcuphkdavcds.data, make_lin(p3, srcuphkdavcds), parametrupavda.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", srcsphkdarcds.data, make_lin(p3, srcsphkdarcds), parametrupavda.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", srcsphkdapcds.data, make_lin(p3, srcsphkdapcds), parametrupavda.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", srcsphkdavcds.data, make_lin(p3, srcsphkdavcds), parametrupavda.index("S-pHK")],

	"dermrytas": [[drrytas], "dermr", srcdermdarcds.data, make_lin(p3, srcdermdarcds), parametrupavda.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", srcdermdapcds.data, make_lin(p3, srcdermdapcds), parametrupavda.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", srcdermdavcds.data, make_lin(p3, srcdermdavcds), parametrupavda.index("Derm")],

	"usvrytas": [[slasvrytas], "usvr", srcusvdarcds.data, make_lin(p3, srcusvdarcds), parametrupavda.index("U-šv")],
	"usvpietūs": [[slasvpietus], "usvp", srcusvdapcds.data, make_lin(p3, srcusvdapcds), parametrupavda.index("U-šv")],
	"usvvakaras": [[slasvvakaras], "usvv", srcusvdavcds.data, make_lin(p3, srcusvdavcds), parametrupavda.index("U-šv")],

	"uputrytas": [[slaputrytas], "uputr", srcuputdarcds.data, make_lin(p3, srcuputdarcds), parametrupavda.index("U-put")],
	"uputpietūs": [[slaputpietus], "uputp", srcuputdapcds.data, make_lin(p3, srcuputdapcds), parametrupavda.index("U-put")],
	"uputvakaras": [[slaputvakaras], "uputv", srcuputdavcds.data, make_lin(p3, srcuputdavcds), parametrupavda.index("U-put")]}

# Metabolinė alkalozė|acidozė

alkaacid = {
	"Norma KT": [13, 65, 5, 6.3, 6.6, 67, 0],
	"Norma AP": [19, 40, 10, 5.9, 6.8, 75, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.5, 2]}

parametrupavalac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "P1", "P4–P1"]
lentelealac = pd.DataFrame(alkaacid, index=parametrupavalac)
lentelealac = lentelealac[["Norma KT", "Norma AP", "Pagrindas"]]

srckdalacrcds = CDS.srckdalacrcds()
srckdalacpcds = CDS.srckdalacpcds()
srckdalacvcds = CDS.srckdalacvcds()

srctksialacrcds = CDS.srctksialacrcds()
srctksialacpcds = CDS.srctksialacpcds()
srctksialacvcds = CDS.srctksialacvcds()

srckphialacrcds = CDS.srckphialacrcds()
srckphialacpcds = CDS.srckphialacpcds()
srckphialacvcds = CDS.srckphialacvcds()

srcuphkalacrcds = CDS.srcuphkalacrcds()
srcuphkalacpcds = CDS.srcuphkalacpcds()
srcuphkalacvcds = CDS.srcuphkalacvcds()

srcsphkalacrcds = CDS.srcsphkalacrcds()
srcsphkalacpcds = CDS.srcsphkalacpcds()
srcsphkalacvcds = CDS.srcsphkalacvcds()

srcp1alacrcds = CDS.srcp1alacrcds()
srcp1alacpcds = CDS.srcp1alacpcds()
srcp1alacvcds = CDS.srcp1alacvcds()

srcp4p1alacrcds = CDS.srcp4p1alacrcds()
srcp4p1alacpcds = CDS.srcp4p1alacpcds()
srcp4p1alacvcds = CDS.srcp4p1alacvcds()

parametalac = {
	"kdrytas": [[kdrytas], "kdr", srckdalacrcds.data, make_lin(p4, srckdalacrcds), parametrupavalac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", srckdalacpcds.data, make_lin(p4, srckdalacpcds), parametrupavalac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", srckdalacvcds.data, make_lin(p4, srckdalacvcds), parametrupavalac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", srctksialacrcds.data, make_lin(p4, srctksialacrcds), parametrupavalac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", srctksialacpcds.data, make_lin(p4, srctksialacpcds), parametrupavalac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", srctksialacvcds.data, make_lin(p4, srctksialacvcds), parametrupavalac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", srckphialacrcds.data, make_lin(p4, srckphialacrcds), parametrupavalac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", srckphialacpcds.data, make_lin(p4, srckphialacpcds), parametrupavalac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", srckphialacvcds.data, make_lin(p4, srckphialacvcds), parametrupavalac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", srcuphkalacrcds.data, make_lin(p4, srcuphkalacrcds), parametrupavalac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", srcuphkalacpcds.data, make_lin(p4, srcuphkalacpcds), parametrupavalac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", srcuphkalacvcds.data, make_lin(p4, srcuphkalacvcds), parametrupavalac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", srcsphkalacrcds.data, make_lin(p4, srcsphkalacrcds), parametrupavalac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", srcsphkalacpcds.data, make_lin(p4, srcsphkalacpcds), parametrupavalac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", srcsphkalacvcds.data, make_lin(p4, srcsphkalacvcds), parametrupavalac.index("S-pHK")],

	"p(1)rytas": [[pgrytas], "p1r", srcp1alacrcds.data, make_lin(p4, srcp1alacrcds), parametrupavalac.index("P1")],
	"p(1)pietūs": [[pgpietus], "p1p", srcp1alacpcds.data, make_lin(p4, srcp1alacpcds), parametrupavalac.index("P1")],
	"p(1)vakaras": [[pgvakaras], "p1v", srcp1alacvcds.data, make_lin(p4, srcp1alacvcds), parametrupavalac.index("P1")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", srcp4p1alacrcds.data, make_lin(p4, srcp4p1alacrcds), parametrupavalac.index("P4–P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", srcp4p1alacpcds.data, make_lin(p4, srcp4p1alacpcds), parametrupavalac.index("P4–P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", srcp4p1alacvcds.data, make_lin(p4, srcp4p1alacvcds), parametrupavalac.index("P4–P1")]}

# Elektrolitų trūkumas|perteklius

elektroltp = {
	"Norma KT": [16, 16, 10, 180, -8],
	"Norma AP": [8, 22, 10, 220, 2],
	"Pagrindas": [2, 2, 1.2, 1.001, 1.4]}

parametrupavetp = ["Pm1-S21", "Pm1+S21", "Pm1-Pm4", "Sm+Dm", "S-D"]
lenteleetp = pd.DataFrame(elektroltp, index=parametrupavetp)
lenteleetp = lenteleetp[["Norma KT", "Norma AP", "Pagrindas"]]


srcpm1ms21rcds = CDS.srcpm1ms21rcds()
srcpm1ms21pcds = CDS.srcpm1ms21pcds()
srcpm1ms21vcds = CDS.srcpm1ms21vcds()

srcpm1ps21rcds = CDS.srcpm1ps21rcds()
srcpm1ps21pcds = CDS.srcpm1ps21pcds()
srcpm1ps21vcds = CDS.srcpm1ps21vcds()

srcpm1mpm4rcds = CDS.srcpm1mpm4rcds()
srcpm1mpm4pcds = CDS.srcpm1mpm4pcds()
srcpm1mpm4vcds = CDS.srcpm1mpm4vcds()

src1pm1mpm4rcds = CDS.src1pm1mpm4rcds()
src1pm1mpm4pcds = CDS.src1pm1mpm4pcds()
src1pm1mpm4vcds = CDS.src1pm1mpm4vcds()

srcsmdmrcds = CDS.srcsmdmrcds()
srcsmdmpcds = CDS.srcsmdmpcds()
srcsmdmvcds = CDS.srcsmdmvcds()

srcsmdrcds = CDS.srcsmdrcds()
srcsmdpcds = CDS.srcsmdpcds()
srcsmdvcds = CDS.srcsmdvcds()

srcsmd1rcds = CDS.srcsmd1rcds()
srcsmd1pcds = CDS.srcsmd1pcds()
srcsmd1vcds = CDS.srcsmd1vcds()


parametetp = {
	"pm1-s21rytas": [[pgrytas, parytas, pa15rytas, pa45rytas, skarytas, skgrytas], "pm1-s21r", srcpm1ms21rcds.data, make_lin(p5, srcpm1ms21rcds), parametrupavetp.index("Pm1-S21")],
	"pm1-s21pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus, skapietus, skgpietus], "pm1-s21p", srcpm1ms21pcds.data, make_lin(p5, srcpm1ms21pcds), parametrupavetp.index("Pm1-S21")],
	"pm1-s21vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras, skavakaras, skgvakaras], "pm1-s21v", srcpm1ms21vcds.data, make_lin(p5, srcpm1ms21vcds), parametrupavetp.index("Pm1-S21")],

	"pm1+s21rytas": [[pgrytas, parytas, pa15rytas, pa45rytas, skarytas, skgrytas], "pm1+s21r", srcpm1ps21rcds.data, make_lin(p5, srcpm1ps21rcds), parametrupavetp.index("Pm1+S21")],
	"pm1+s21pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus, skapietus, skgpietus], "pm1+s21p", srcpm1ps21pcds.data, make_lin(p5, srcpm1ps21pcds), parametrupavetp.index("Pm1+S21")],
	"pm1+s21vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras, skavakaras, skgvakaras], "pm1+s21v", srcpm1ps21vcds.data, make_lin(p5, srcpm1ps21vcds), parametrupavetp.index("Pm1+S21")],

	"pm1-pm4rytas": [[pgrytas, parytas, pa15rytas, pa45rytas], "pm1-pm4r", [srcpm1mpm4rcds.data, src1pm1mpm4rcds.data], make_lin(p5, srcpm1mpm4rcds, src1pm1mpm4rcds), parametrupavetp.index("Pm1-Pm4")],
	"pm1-pm4pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus], "pm1-pm4p", [srcpm1mpm4pcds.data, src1pm1mpm4pcds.data], make_lin(p5, srcpm1mpm4pcds, src1pm1mpm4pcds), parametrupavetp.index("Pm1-Pm4")],
	"pm1-pm4vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras], "pm1-pm4v", [srcpm1mpm4vcds.data, src1pm1mpm4vcds.data], make_lin(p5, srcpm1mpm4vcds, src1pm1mpm4vcds), parametrupavetp.index("Pm1-Pm4")],

	"smdmrytas": [[skgrytas, skarytas, dkgrytas, dkarytas], "smdmr", srcsmdmrcds.data, make_lin(p5, srcsmdmrcds), parametrupavetp.index("Sm+Dm")],
	"smdmpietūs": [[skgpietus, skapietus, dkgpietus, dkapietus], "smdmp", srcsmdmpcds.data, make_lin(p5, srcsmdmpcds), parametrupavetp.index("Sm+Dm")],
	"smdmvakaras": [[skgvakaras, skavakaras, dkgvakaras, dkavakaras], "smdmv", srcsmdmvcds.data, make_lin(p5, srcsmdmvcds), parametrupavetp.index("Sm+Dm")],

	"s-drytas": [[skgrytas, skarytas, dkgrytas, dkarytas], "s-dr", [srcsmdrcds.data, srcsmd1rcds.data], make_lin(p5, srcsmdrcds, srcsmd1rcds), parametrupavetp.index("S-D")],
	"s-dpietūs": [[skgpietus, skapietus, dkgpietus, dkapietus], "s-dp", [srcsmdpcds.data, srcsmd1pcds.data], make_lin(p5, srcsmdpcds, srcsmd1pcds), parametrupavetp.index("S-D")],
	"s-dvakaras": [[skgvakaras, skavakaras, dkgvakaras, dkavakaras], "s-dv", [srcsmdvcds.data, srcsmd1vcds.data], make_lin(p5, srcsmdvcds, srcsmd1vcds), parametrupavetp.index("S-D")]}

# Kalio trūkumo alkalozė|pertekliaus acidozė

kaliotalpac = {
	"Norma KT": [13, 65, 5, 5.9, 6.6, 1, 1, 0],
	"Norma AP": [19, 40, 10, 6.3, 6.8, -1, 2, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.001, 1.2, 2]}

parametrupavktalpac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "Vyzd", "Derm", "P4-P1"]
lentelektalpac = pd.DataFrame(kaliotalpac, index=parametrupavktalpac)
lentelektalpac = lentelektalpac[["Norma KT", "Norma AP", "Pagrindas"]]

srckdktalpacrcds = CDS.srckdktalpacrcds()
srckdktalpacpcds = CDS.srckdktalpacpcds()
srckdktalpacvcds = CDS.srckdktalpacvcds()

srctksiktalpacrcds = CDS.srctksiktalpacrcds()
srctksiktalpacpcds = CDS.srctksiktalpacpcds()
srctksiktalpacvcds = CDS.srctksiktalpacvcds()

srckphiktalpacrcds = CDS.srckphiktalpacrcds()
srckphiktalpacpcds = CDS.srckphiktalpacpcds()
srckphiktalpacvcds = CDS.srckphiktalpacvcds()

srcuphkktalpacrcds = CDS.srcuphkktalpacrcds()
srcuphkktalpacpcds = CDS.srcuphkktalpacpcds()
srcuphkktalpacvcds = CDS.srcuphkktalpacvcds()

srcsphkktalpacrcds = CDS.srcsphkktalpacrcds()
srcsphkktalpacpcds = CDS.srcsphkktalpacpcds()
srcsphkktalpacvcds = CDS.srcsphkktalpacvcds()

srcvyzdktalpacrcds = CDS.srcvyzdktalpacrcds()
srcvyzdktalpacpcds = CDS.srcvyzdktalpacpcds()
srcvyzdktalpacvcds = CDS.srcvyzdktalpacvcds()

srcdermktalpacrcds = CDS.srcdermktalpacrcds()
srcdermktalpacpcds = CDS.srcdermktalpacpcds()
srcdermktalpacvcds = CDS.srcdermktalpacvcds()

srcp4p1ktalpacrcds = CDS.srcp4p1ktalpacrcds()
srcp4p1ktalpacpcds = CDS.srcp4p1ktalpacpcds()
srcp4p1ktalpacvcds = CDS.srcp4p1ktalpacvcds()

parametktalpac = {
	"kdrytas": [[kdrytas], "kdr", srckdktalpacrcds.data, make_lin(p6, srckdktalpacrcds), parametrupavktalpac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", srckdktalpacpcds.data, make_lin(p6, srckdktalpacpcds), parametrupavktalpac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", srckdktalpacvcds.data, make_lin(p6, srckdktalpacvcds), parametrupavktalpac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", srctksiktalpacrcds.data, make_lin(p6, srctksiktalpacrcds), parametrupavktalpac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", srctksiktalpacpcds.data, make_lin(p6, srctksiktalpacpcds), parametrupavktalpac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", srctksiktalpacvcds.data, make_lin(p6, srctksiktalpacvcds), parametrupavktalpac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", srckphiktalpacrcds.data, make_lin(p6, srckphiktalpacrcds), parametrupavktalpac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", srckphiktalpacpcds.data, make_lin(p6, srckphiktalpacpcds), parametrupavktalpac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", srckphiktalpacvcds.data, make_lin(p6, srckphiktalpacvcds), parametrupavktalpac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", srcuphkktalpacrcds.data, make_lin(p6, srcuphkktalpacrcds), parametrupavktalpac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", srcuphkktalpacpcds.data, make_lin(p6, srcuphkktalpacpcds), parametrupavktalpac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", srcuphkktalpacvcds.data, make_lin(p6, srcuphkktalpacvcds), parametrupavktalpac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", srcsphkktalpacrcds.data, make_lin(p6, srcsphkktalpacrcds), parametrupavktalpac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", srcsphkktalpacpcds.data, make_lin(p6, srcsphkktalpacpcds), parametrupavktalpac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", srcsphkktalpacvcds.data, make_lin(p6, srcsphkktalpacvcds), parametrupavktalpac.index("S-pHK")],

	"vyzdrytas": [[vdrytas], "vyzdr", srcvyzdktalpacrcds.data, make_lin(p6, srcvyzdktalpacrcds), parametrupavktalpac.index("Vyzd")],
	"vyzdpietūs": [[vdpietus], "vyzdp", srcvyzdktalpacpcds.data, make_lin(p6, srcvyzdktalpacpcds), parametrupavktalpac.index("Vyzd")],
	"vyzdvakaras": [[vdvakaras], "vyzdv", srcvyzdktalpacvcds.data, make_lin(p6, srcvyzdktalpacvcds), parametrupavktalpac.index("Vyzd")],

	"dermrytas": [[drrytas], "dermr", srcdermktalpacrcds.data, make_lin(p6, srcdermktalpacrcds), parametrupavktalpac.index("Derm")],
	"dermpietūs": [[drpietus], "dermp", srcdermktalpacpcds.data, make_lin(p6, srcdermktalpacpcds), parametrupavktalpac.index("Derm")],
	"dermvakaras": [[drvakaras], "dermv", srcdermktalpacvcds.data, make_lin(p6, srcdermktalpacvcds), parametrupavktalpac.index("Derm")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", srcp4p1ktalpacrcds.data, make_lin(p6, srcp4p1ktalpacrcds), parametrupavktalpac.index("P4-P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", srcp4p1ktalpacpcds.data, make_lin(p6, srcp4p1ktalpacpcds), parametrupavktalpac.index("P4-P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", srcp4p1ktalpacvcds.data, make_lin(p6, srcp4p1ktalpacvcds), parametrupavktalpac.index("P4-P1")]}

# Respiracinė alkalozė|acidozė

respialac = {
	"Norma KT": [13, 65, 5, 6.3, 6.8, 67, 0],
	"Norma AP": [19, 40, 10, 5.9, 6.6, 75, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.5, 2]}

parametrupavralac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "P1", "P4-P1"]
lenteleralac = pd.DataFrame(respialac, index=parametrupavralac)
lenteleralac = lenteleralac[["Norma KT", "Norma AP", "Pagrindas"]]

srckdralacrcds = CDS.srckdralacrcds()
srckdralacpcds = CDS.srckdralacpcds()
srckdralacvcds = CDS.srckdralacvcds()

srctksiralacrcds = CDS.srctksiralacrcds()
srctksiralacpcds = CDS.srctksiralacpcds()
srctksiralacvcds = CDS.srctksiralacvcds()

srckphiralacrcds = CDS.srckphiralacrcds()
srckphiralacpcds = CDS.srckphiralacpcds()
srckphiralacvcds = CDS.srckphiralacvcds()

srcuphkralacrcds = CDS.srcuphkralacrcds()
srcuphkralacpcds = CDS.srcuphkralacpcds()
srcuphkralacvcds = CDS.srcuphkralacvcds()

srcsphkralacrcds = CDS.srcsphkralacrcds()
srcsphkralacpcds = CDS.srcsphkralacpcds()
srcsphkralacvcds = CDS.srcsphkralacvcds()

srcp1ralacrcds = CDS.srcp1ralacrcds()
srcp1ralacpcds = CDS.srcp1ralacpcds()
srcp1ralacvcds = CDS.srcp1ralacvcds()

srcp4p1ralacrcds = CDS.srcp1ralacrcds()
srcp4p1ralacpcds = CDS.srcp1ralacpcds()
srcp4p1ralacvcds = CDS.srcp1ralacvcds()

parametralac = {
	"kdrytas": [[kdrytas], "kdr", srckdralacrcds.data, make_lin(p7, srckdralacrcds), parametrupavralac.index("KD")],
	"kdpietūs": [[kdpietus], "kdp", srckdralacpcds.data, make_lin(p7, srckdralacpcds), parametrupavralac.index("KD")],
	"kdvakaras": [[kdvakaras], "kdv", srckdralacvcds.data, make_lin(p7, srckdralacvcds), parametrupavralac.index("KD")],

	"tksirytas": [[ksirytas], "tksir", srctksiralacrcds.data, make_lin(p7, srctksiralacrcds), parametrupavralac.index("t(ksi)")],
	"tksipietūs": [[ksipietus], "tksip", srctksiralacpcds.data, make_lin(p7, srctksiralacpcds), parametrupavralac.index("t(ksi)")],
	"tksivakaras": [[ksivakaras], "tksiv", srctksiralacvcds.data, make_lin(p7, srctksiralacvcds), parametrupavralac.index("t(ksi)")],

	"kphirytas": [[kdrytas, ksirytas], "kphir", srckphiralacrcds.data, make_lin(p7, srckphiralacrcds), parametrupavralac.index("KpHi")],
	"kphipietūs": [[kdpietus, ksipietus], "kphip", srckphiralacpcds.data, make_lin(p7, srckphiralacpcds), parametrupavralac.index("KpHi")],
	"kphivakaras": [[kdvakaras, ksivakaras], "kphiv", srckphiralacvcds.data, make_lin(p7, srckphiralacvcds), parametrupavralac.index("KpHi")],

	"uphkrytas": [[slatankrytas, slarugrytas], "uphkr", srcuphkralacrcds.data, make_lin(p7, srcuphkralacrcds), parametrupavralac.index("U-pHK")],
	"uphkpietūs": [[slatankpietus, slarugpietus], "uphkp", srcuphkralacpcds.data, make_lin(p7, srcuphkralacpcds), parametrupavralac.index("U-pHK")],
	"uphkvakaras": [[slatankvakaras, slarugvakaras], "uphkv", srcuphkralacvcds.data, make_lin(p7, srcuphkralacvcds), parametrupavralac.index("U-pHK")],

	"sphkrytas": [[slatankrytas, serrytas], "sphkr", srcsphkralacrcds.data, make_lin(p7, srcsphkralacrcds), parametrupavralac.index("S-pHK")],
	"sphkpietūs": [[slatankpietus, serpietus], "sphkp", srcsphkralacpcds.data, make_lin(p7, srcsphkralacpcds), parametrupavralac.index("S-pHK")],
	"sphkvakaras": [[slatankvakaras, servakaras], "sphkv", srcsphkralacvcds.data, make_lin(p7, srcsphkralacvcds), parametrupavralac.index("S-pHK")],

	"p(1)rytas": [[pgrytas], "p1r", srcp1ralacrcds.data, make_lin(p7, srcp1ralacrcds), parametrupavralac.index("P1")],
	"p(1)pietūs": [[pgpietus], "p1p", srcp1ralacpcds.data, make_lin(p7, srcp1ralacpcds), parametrupavralac.index("P1")],
	"p(1)vakaras": [[pgvakaras], "p1v", srcp1ralacvcds.data, make_lin(p7, srcp1ralacvcds), parametrupavralac.index("P1")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", srcp4p1ralacrcds.data, make_lin(p7, srcp4p1ralacrcds), parametrupavralac.index("P4-P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", srcp4p1ralacpcds.data, make_lin(p7, srcp4p1ralacpcds), parametrupavralac.index("P4-P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", srcp4p1ralacvcds.data, make_lin(p7, srcp4p1ralacvcds), parametrupavralac.index("P4-P1")]}

hidracind = {
	"hidrindrytas": [[slarugrytas, serrytas, slatankrytas]],
	"hidrindpietūs": [[slarugpietus, serpietus, slatankpietus]],
	"hidrindvakaras": [[slarugvakaras, servakaras, slatankvakaras]]}

dictlytis = {"lytis": [[lytis]]}


def pagr_update(attr, old, new):
	simparasimr = {}
	simparasimp = {}
	simparasimv = {}
	dictpav1 = {"simparasim": 5}

	ketogliukor = {}
	ketogliukop = {}
	ketogliukov = {}
	dictpav2 = {"ketogliuko": 4}

	disaeanaer = {}
	disaeanaep = {}
	disaeanaev = {}
	dictpav3 = {"disaeanae": 3}

	alkaacidr = {}
	alkaacidp = {}
	alkaacidv = {}
	dictpav4 = {"alkaacid": None}

	elektroltpr = {}
	elektroltpp = {}
	elektroltpv = {}
	dictpav5 = {"elektroltp": 3}

	kaliotalpacr = {}
	kaliotalpacp = {}
	kaliotalpacv = {}
	dictpav6 = {"kaliotalpac": None}

	respialacr = {}
	respialacp = {}
	respialacv = {}
	dictpav7 = {"respialac": None}

	for key in parametsp.keys():
		if "ps1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2 = verte(n)
			formule = (v1 - v2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp, key)

	# taip bokeh atnaujinama x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)
			# print(key, sourcedata)

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

		if "rytas" in str(key):
			simparasimr[key] = karareiksme
		elif "pietūs" in str(key):
			simparasimp[key] = karareiksme
		elif "vakaras" in str(key):
			simparasimv[key] = karareiksme

		if len(simparasimr) == len(simparasimp) == len(simparasimv) == 12:
			spktareiksme = buklnustat(simparasimr, simparasimp, simparasimv, dictpav1)

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

		if "rytas" in str(key):
			if key == "uputrytas":
				key1 = "uputrytas1"
				ketogliukor[key] = karareiksme
				ketogliukor[key1] = -karareiksme
			else:
				ketogliukor[key] = karareiksme
		elif "pietūs" in str(key):
			if key == "uputpietūs":
				key1 = "uputpietūs1"
				ketogliukop[key] = karareiksme
				ketogliukop[key1] = -karareiksme
			else:
				ketogliukop[key] = karareiksme
		elif "vakaras" in str(key):
			if key == "uputvakaras":
				key1 = "uputvakaras1"
				ketogliukov[key] = karareiksme
				ketogliukov[key1] = -karareiksme
			else:
				ketogliukov[key] = karareiksme

		if len(ketogliukor) == len(ketogliukop) == len(ketogliukov) == 8:
			kgktareiksme = buklnustat(ketogliukor, ketogliukop, ketogliukov, dictpav2)

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

		if "rytas" in str(key):
			disaeanaer[key] = karareiksme
		elif "pietūs" in str(key):
			disaeanaep[key] = karareiksme
		elif "vakaras" in str(key):
			disaeanaev[key] = karareiksme

		if len(disaeanaer) == len(disaeanaep) == len(disaeanaev) == 6:
			daktareiksme = buklnustat(disaeanaer, disaeanaep, disaeanaev, dictpav3)

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

		if "rytas" in str(key):
			alkaacidr[key] = karareiksme
		elif "pietūs" in str(key):
			alkaacidp[key] = karareiksme
		elif "vakaras" in str(key):
			alkaacidv[key] = karareiksme
		if len(alkaacidr) == len(alkaacidp) == len(alkaacidv) == 7:
			maaktareiksme = buklnustat(alkaacidr, alkaacidp, alkaacidv, dictpav4)

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

		if "rytas" in str(key):
			if key == "pm1-pm4rytas":
				key1 = "pm1-pm4rytas1"
				elektroltpr[key] = karareiksme
				elektroltpr[key1] = -karareiksme
			elif key == "s-drytas":
				if karareiksme < 0:
					key1 = "s-drytas1"
					elektroltpr[key] = karareiksme
					elektroltpr[key1] = -karareiksme
				else:
					key1 = "s-drytas1"
					elektroltpr[key] = 0
					elektroltpr[key1] = karareiksme
			else:
				elektroltpr[key] = karareiksme
		elif "pietūs" in str(key):
			if key == "pm1-pm4pietūs":
				key1 = "pm1-pm4pietūs1"
				elektroltpp[key] = karareiksme
				elektroltpp[key1] = -karareiksme
			elif key == "s-dpietūs":
				if karareiksme < 0:
					key1 = "s-dpietūs1"
					elektroltpp[key] = karareiksme
					elektroltpp[key1] = -karareiksme
				else:
					key1 = "s-dpietūs1"
					elektroltpp[key] = 0
					elektroltpp[key1] = karareiksme
			else:
				elektroltpp[key] = karareiksme
		elif "vakaras" in str(key):
			if key == "pm1-pm4vakaras":
				key1 = "pm1-pm4vakaras1"
				elektroltpv[key] = karareiksme
				elektroltpv[key1] = -karareiksme
			elif key == "s-dvakaras":
				if karareiksme < 0:
					key1 = "s-dvakaras1"
					elektroltpv[key] = karareiksme
					elektroltpv[key1] = -karareiksme
				else:
					key1 = "s-dvakaras1"
					elektroltpv[key] = 0
					elektroltpv[key1] = karareiksme
			else:
				elektroltpv[key] = karareiksme

		if len(elektroltpr) == len(elektroltpp) == len(elektroltpv) == 7:
			etpktareiksme = buklnustat(elektroltpr, elektroltpp, elektroltpv, dictpav5)

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

		if "rytas" in str(key):
			kaliotalpacr[key] = karareiksme
		elif "pietūs" in str(key):
			kaliotalpacp[key] = karareiksme
		elif "vakaras" in str(key):
			kaliotalpacv[key] = karareiksme

	if len(kaliotalpacr) == len(kaliotalpacp) == len(kaliotalpacv) == 8:
		ktktareiksme = buklnustat(kaliotalpacr, kaliotalpacp, kaliotalpacv, dictpav6)

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
			formule = serugv + (0.033333 * tankindx) - 0.533603
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

		if "rytas" in str(key):
			respialacr[key] = karareiksme
		elif "pietūs" in str(key):
			respialacp[key] = karareiksme
		elif "vakaras" in str(key):
			respialacv[key] = karareiksme

		if len(respialacr) == len(respialacp) == len(respialacv) == 7:
			raaktareiksme = buklnustat(respialacr, respialacp, respialacv, dictpav7)

	for d in [spktareiksme, kgktareiksme, daktareiksme, maaktareiksme, etpktareiksme, ktktareiksme, raaktareiksme]:
		for k, v in d.items():
			if k == "simparasim":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						sptnk = v1
					else:
						sptna = v1
			elif k == "ketogliuko":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						kgtnk = v1
					else:
						kgtna = v1
			elif k == "disaeanae":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						datnk = v1
					else:
						datna = v1
			elif k == "alkaacid":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						maatnk = v1
					else:
						maatna = v1
			elif k == "elektroltp":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						etptnk = v1
					else:
						etptna = v1
			elif k == "kaliotalpac":
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						ktptnk = v1
					else:
						ktptna = v1
			else:
				for k1, v1 in v.items():
					if k1 == "Katabolizmas":
						raatnk = v1
					else:
						raatna = v1

	reik = ["-"]
	avrl = []
	for v in hidracind.values():
		n = v[0]
		v1, v2, v3 = verte(n)
		hdi = v1 + v2 - (v3 * 1000 - 1000) / 5
		avrl.append(hdi)

	# Geriamas vanduo
	if avrl:
		if mean(avrl) <= 8.5:
			gervandfm.text_color = "green"
			gervandfm.font_style = "bold"
			new_data = {'grupe': [*vandulist], 'reiksmes': reik * len(vandulist)}
			vanduocds.data.update(new_data)
		elif mean(avrl) >= 12.0:
			gervandfm.text_color = "red"
			gervandfm.font_style = "bold"
			new_data = {'grupe': [*vandulist], 'reiksmes': reik * len(vandulist)}
			vanduocds.data.update(new_data)
		else:
			gervandfm.text_color = None
			gervandfm.font_style = "bold"
			new_data = {'grupe': [*vandulist], 'reiksmes': reik * len(vandulist)}
			vanduocds.data.update(new_data)

	# Organinės rūgštys
	if (maatnk == "T") or (maatna == "T"):
		orgrugfm.text_color = "red"
		orgrugfm.font_style = "bold"
		new_data = {'grupe': [*orgruglist], 'reiksmes': reik * len(orgruglist)}
		orgrugcds.data.update(new_data)
	else:
		orgrugfm.text_color = None
		orgrugfm.font_style = "bold"
		new_data = {'grupe': [* orgruglist], 'reiksmes': reik * len(orgruglist)}
		orgrugcds.data.update(new_data)

	# Hidrokarbonatai
	if raatna == "T":
		hidrokarbofm.text_color = "red"
		hidrokarbofm.font_style = "bold"
		new_data = {'grupe': [*hidrokarbolist], 'reiksmes': reik * len(hidrokarbolist)}
		hidrokarbocds.data.update(new_data)
	else:
		hidrokarbofm.text_color = None
		hidrokarbofm.font_style = "bold"
		new_data = {'grupe': [*hidrokarbolist], 'reiksmes': reik * len(hidrokarbolist)}
		hidrokarbocds.data.update(new_data)

	# Natris, chloras, fluoras
	if (etptnk == "T") and (etptna == "T"):
		natchlofluofm.text_color = None
		natchlofluofm.font_style = "bold"
		new_data = {'grupe': [*natchlofluolist], 'reiksmes': reik * len(natchlofluolist)}
		natchlofluocds.data.update(new_data)
	else:
		if etptnk == "T":
			natchlofluofm.text_color = "green"
			natchlofluofm.font_style = "bold"
			new_data = {'grupe': [*natchlofluolist], 'reiksmes': reik * len(natchlofluolist)}
			natchlofluocds.data.update(new_data)
		else:
			if etptna == "T":
				natchlofluofm.text_color = "red"
				natchlofluofm.font_style = "bold"
				new_data = {'grupe': [*natchlofluolist], 'reiksmes': reik * len(natchlofluolist)}
				natchlofluocds.data.update(new_data)
			else:
				natchlofluofm.text_color = None
				natchlofluofm.font_style = "bold"
				new_data = {'grupe': [*natchlofluolist], 'reiksmes': reik * len(natchlofluolist)}
				natchlofluocds.data.update(new_data)

	# Sulfatai
	if (etptnk == "T") and (etptna == "T"):
		sulfatfm.text_color = "green"
		sulfatfm.font_style = "bold"
		new_data = {'grupe': [*sulfatlist], 'reiksmes': reik * len(sulfatlist)}
		sulfatcds.data.update(new_data)
	else:
		if etptna == "T":
			sulfatfm.text_color = "green"
			sulfatfm.font_style = "bold"
			new_data = {'grupe': [*sulfatlist], 'reiksmes': reik * len(sulfatlist)}
			sulfatcds.data.update(new_data)
		else:
			sulfatfm.text_color = None
			sulfatfm.font_style = "bold"
			new_data = {'grupe': [*sulfatlist], 'reiksmes': reik * len(sulfatlist)}
			sulfatcds.data.update(new_data)

	# Krakmolo šaltiniai
	if (sptna == "T") or (kgtna == "T") or (datna == "T"):
		krakmolfm.text_color = "red"
		krakmolfm.font_style = "bold"
		new_data = {'grupe': [*krakmollist], 'reiksmes': reik * len(krakmollist)}
		krakmolcds.data.update(new_data)
	else:
		krakmolfm.text_color = "#CCCC00"
		krakmolfm.font_style = "bold"
		new_data = {'grupe': [*krakmollist], 'reiksmes': reik * len(krakmollist)}
		krakmolcds.data.update(new_data)

	# Polinesotieji riebalai
	if datnk == "T":
		poliriebfm.text_color = "red"
		poliriebfm.font_style = "bold"
		new_data = {'grupe': [*polirieblist], 'reiksmes': reik * len(polirieblist)}
		poliriebcds.data.update(new_data)
	else:
		poliriebfm.text_color = "#CCCC00"
		poliriebfm.font_style = "bold"
		new_data = {'grupe': [*polirieblist], 'reiksmes': reik * len(polirieblist)}
		poliriebcds.data.update(new_data)

	# Mononesotieji riebalai
	if (kgtnk == "T") or (datnk == "T"):
		monoriebfm.text_color = "green"
		monoriebfm.font_style = "bold"
		new_data = {'grupe': [*monorieblist], 'reiksmes': reik * len(monorieblist)}
		monoriebcds.data.update(new_data)
	else:
		monoriebfm.text_color = None
		monoriebfm.font_style = "bold"
		new_data = {'grupe': [*monorieblist], 'reiksmes': reik * len(monorieblist)}
		monoriebcds.data.update(new_data)

	# Sotieji riebalai
	if kgtnk == "T":
		sotriebfm.text_color = "red"
		sotriebfm.font_style = "bold"
		new_data = {'grupe': [*sotrieblist], 'reiksmes': reik * len(sotrieblist)}
		sotriebcds.data.update(new_data)
	else:
		if kgtna == "T":
			sotriebfm.text_color = "green"
			sotriebfm.font_style = "bold"
			new_data = {'grupe': [*sotrieblist], 'reiksmes': reik * len(sotrieblist)}
			sotriebcds.data.update(new_data)
		else:
			sotriebfm.text_color = None
			sotriebfm.font_style = "bold"
			new_data = {'grupe': [*sotrieblist], 'reiksmes': reik * len(sotrieblist)}
			sotriebcds.data.update(new_data)

	# Stipriai pakitę baltymai ir riebalai
	if (sptnk == "T") or (sptna == "T") or (kgtnk == "T") or (datnk == "T"):
		spbaltirriebfm.text_color = "red"
		spbaltirriebfm.font_style = "bold"
		new_data = {'grupe': [*spbaltirrieblist], 'reiksmes': reik * len(spbaltirrieblist)}
		spbaltirriebcds.data.update(new_data)
	else:
		spbaltirriebfm.text_color = None
		spbaltirriebfm.font_style = "bold"
		new_data = {'grupe': [*spbaltirrieblist], 'reiksmes': reik * len(spbaltirrieblist)}
		spbaltirriebcds.data.update(new_data)

	# Kiaušiniai
	if (kgtnk == "T") or (datnk == "T"):
		kiausiniaifm.text_color = "green"
		kiausiniaifm.font_style = "bold"
		new_data = {'grupe': [*kiausiniailist], 'reiksmes': reik * len(kiausiniailist)}
		kiausiniaicds.data.update(new_data)
	else:
		kiausiniaifm.text_color = None
		kiausiniaifm.font_style = "bold"
		new_data = {'grupe': [*kiausiniailist], 'reiksmes': reik * len(kiausiniailist)}
		kiausiniaicds.data.update(new_data)

	# Organai
	if kgtnk == "T":
		organaifm.text_color = "red"
		organaifm.font_style = "bold"
		new_data = {'grupe': [*organailist], 'reiksmes': reik * len(organailist)}
		organaicds.data.update(new_data)
	else:
		if kgtna == "T":
			organaifm.text_color = "green"
			organaifm.font_style = "bold"
			new_data = {'grupe': [*organailist], 'reiksmes': reik * len(organailist)}
			organaicds.data.update(new_data)
		else:
			organaifm.text_color = None
			organaifm.font_style = "bold"
			new_data = {'grupe': [*organailist], 'reiksmes': reik * len(organailist)}
			organaicds.data.update(new_data)

	# Pieno baltymai
	if (sptnk == "T") or (sptna == "T"):
		pienbaltfm.text_color = "red"
		pienbaltfm.font_style = "bold"
		new_data = {'grupe': [*pienbaltlist], 'reiksmes': reik * len(pienbaltlist)}
		pienbaltcds.data.update(new_data)
	else:
		if kgtnk == "T":
			pienbaltfm.text_color = "green"
			pienbaltfm.font_style = "bold"
			new_data = {'grupe': [*pienbaltlist], 'reiksmes': reik * len(pienbaltlist)}
			pienbaltcds.data.update(new_data)
		else:
			pienbaltfm.text_color = None
			pienbaltfm.font_style = "bold"
			new_data = {'grupe': [*pienbaltlist], 'reiksmes': reik * len(pienbaltlist)}
			pienbaltcds.data.update(new_data)

	# Moliuskai ir vėžiagyviai
	if kgtnk == "T":
		moliuvezfm.text_color = "red"
		moliuvezfm.font_style = "bold"
		new_data = {'grupe': [*moliuvezlist], 'reiksmes': reik * len(moliuvezlist)}
		moliuvezcds.data.update(new_data)
	else:
		if kgtna == "T":
			moliuvezfm.text_color = "green"
			moliuvezfm.font_style = "bold"
			new_data = {'grupe': [*moliuvezlist], 'reiksmes': reik * len(moliuvezlist)}
			moliuvezcds.data.update(new_data)
		else:
			moliuvezfm.text_color = None
			moliuvezfm.font_style = "bold"
			new_data = {'grupe': [*moliuvezlist], 'reiksmes': reik * len(moliuvezlist)}
			moliuvezcds.data.update(new_data)

	# Balta mėsa
	if kgtnk == "T":
		baltamesafm.text_color = "green"
		baltamesafm.font_style = "bold"
		new_data = {'grupe': [*baltamesalist], 'reiksmes': reik * len(baltamesalist)}
		baltamesacds.data.update(new_data)
	else:
		if kgtna == "T":
			baltamesafm.text_color = "#CCCC00"
			baltamesafm.font_style = "bold"
			new_data = {'grupe': [*baltamesalist], 'reiksmes': reik * len(baltamesalist)}
			baltamesacds.data.update(new_data)
		else:
			baltamesafm.text_color = None
			baltamesafm.font_style = "bold"
			new_data = {'grupe': [*baltamesalist], 'reiksmes': reik * len(baltamesalist)}
			baltamesacds.data.update(new_data)

	# Raudona mėsa
	if kgtnk == "T":
		raudomesafm.text_color = "red"
		raudomesafm.font_style = "bold"
		new_data = {'grupe': [*raudomesalist], 'reiksmes': reik * len(raudomesalist)}
		raudomesacds.data.update(new_data)
	else:
		if kgtna == "T":
			raudomesafm.text_color = "green"
			raudomesafm.font_style = "bold"
			new_data = {'grupe': [*raudomesalist], 'reiksmes': reik * len(raudomesalist)}
			raudomesacds.data.update(new_data)
		else:
			raudomesafm.text_color = None
			raudomesafm.font_style = "bold"
			new_data = {'grupe': [*raudomesalist], 'reiksmes': reik * len(raudomesalist)}
			raudomesacds.data.update(new_data)

	# Grybai
	if (sptnk == "T") or (sptnk == "T") or (kgtnk == "T"):
		grybaifm.text_color = "red"
		grybaifm.font_style = "bold"
		new_data = {'grupe': [*grybailist], 'reiksmes': reik * len(grybailist)}
		grybaicds.data.update(new_data)
	else:
		grybaifm.text_color = "green"
		grybaifm.font_style = "bold"
		new_data = {'grupe': [*grybailist], 'reiksmes': reik * len(grybailist)}
		grybaicds.data.update(new_data)

	# Augaliniai baltymai
	if (sptnk == "T") or (sptna == "T"):
		augalbaltfm.text_color = "red"
		augalbaltfm.font_style = "bold"
		new_data = {'grupe': [*augalbaltlist], 'reiksmes': reik * len(augalbaltlist)}
		augalbaltcds.data.update(new_data)
	else:
		if kgtnk == "T":
			augalbaltfm.text_color = "green"
			augalbaltfm.font_style = "bold"
			new_data = {'grupe': [*augalbaltlist], 'reiksmes': reik * len(augalbaltlist)}
			augalbaltcds.data.update(new_data)
		else:
			augalbaltfm.text_color = "#CCCC00"
			augalbaltfm.font_style = "bold"
			new_data = {'grupe': [*augalbaltlist], 'reiksmes': reik * len(augalbaltlist)}
			augalbaltcds.data.update(new_data)

	# Pakeistų savybių vanduo
	if (etptnk == "T") or (etptna == "T"):
		paksavyvanduofm.text_color = "red"
		paksavyvanduofm.font_style = "bold"
		new_data = {'grupe': [*paksavyvanduolist], 'reiksmes': reik * len(paksavyvanduolist)}
		paksavyvanduocds.data.update(new_data)
	else:
		paksavyvanduofm.text_color = "#CCCC00"
		paksavyvanduofm.font_style = "bold"
		new_data = {'grupe': [*paksavyvanduolist], 'reiksmes': reik * len(paksavyvanduolist)}
		paksavyvanduocds.data.update(new_data)

	# Slopikliai
	if sptna == "T":
		slopikaifm.text_color = "red"
		slopikaifm.font_style = "bold"
		new_data = {'grupe': [*slopikailist], 'reiksmes': reik * len(slopikailist)}
		slopikaicds.data.update(new_data)
	else:
		slopikaifm.text_color = "#CCCC00"
		slopikaifm.font_style = "bold"
		new_data = {'grupe': [*slopikailist], 'reiksmes': reik * len(slopikailist)}
		slopikaicds.data.update(new_data)

	# Stimuliatoriai
	if ((((sptnk == "T") or (kgtnk == "T") or (datnk == "T") or (etptnk == "T") or (etptna == "T")) or (mean(avrl) >= 12)) and 
		(((sptnk == "T") or (kgtnk == "T") or (datnk == "T") or (etptnk == "T") or (etptna == "T") or (mean(avrl) <= 8.5)))):
		stimuliatfm.text_color = "red"
		stimuliatfm.font_style = "bold"
		new_data = {'grupe': [*stimuliatlist], 'reiksmes': reik * len(stimuliatlist)}
		stimuliatcds.data.update(new_data)
	else:
		stimuliatfm.text_color = "#CCCC00"
		stimuliatfm.font_style = "bold"
		new_data = {'grupe': [*stimuliatlist], 'reiksmes': reik * len(stimuliatlist)}
		stimuliatcds.data.update(new_data)

	# Rūkalai
	if (sptnk == "T") or (datnk == "T") or (raatna == "T"):
		rukalaifm.text_color = "red"
		rukalaifm.font_style = "bold"
		new_data = {'grupe': [*rukalailist], 'reiksmes': reik * len(rukalailist)}
		rukalaicds.data.update(new_data)
	else:
		rukalaifm.text_color = "#CCCC00"
		rukalaifm.font_style = "bold"
		new_data = {'grupe': [*rukalailist], 'reiksmes': reik * len(rukalailist)}
		rukalaicds.data.update(new_data)

	# Didelio intensyvumo trumpos trukmės fizinė veikla
	if (kgtnk == "T") or (datnk == "T"):
		didintesyvfm.text_color = "green"
		didintesyvfm.font_style = "bold"
		new_data = {'grupe': [*didintesyvlist], 'reiksmes': reik * len(didintesyvlist)}
		didintesyvcds.data.update(new_data)
	else:
		didintesyvfm.text_color = None
		didintesyvfm.font_style = "bold"
		new_data = {'grupe': [*didintesyvlist], 'reiksmes': reik * len(didintesyvlist)}
		didintesyvcds.data.update(new_data)

	# Mažo intensyvumo ilgos trukmės fizinė veikla
	if (kgtnk == "T") or (datnk == "T"):
		mazointesyvfm.text_color = "red"
		mazointesyvfm.font_style = "bold"
		new_data = {'grupe': [*mazointesyvlist], 'reiksmes': reik * len(mazointesyvlist)}
		mazointesyvcds.data.update(new_data)
	else:
		mazointesyvfm.text_color = None
		mazointesyvfm.font_style = "bold"
		new_data = {'grupe': [*mazointesyvlist], 'reiksmes': reik * len(mazointesyvlist)}
		mazointesyvcds.data.update(new_data)

	# Hipoventiliacija
	if raatna == "T":
		hipoventilfm.text_color = "red"
		hipoventilfm.font_style = "bold"
		new_data = {'grupe': [*hipoventillist], 'reiksmes': reik * len(hipoventillist)}
		hipoventilcds.data.update(new_data)
	else:
		hipoventilfm.text_color = "#CCCC00"
		hipoventilfm.font_style = "bold"
		new_data = {'grupe': [*hipoventillist], 'reiksmes': reik * len(hipoventillist)}
		hipoventilcds.data.update(new_data)

	# Grūdinimasis
	if (sptnk == "T") or (kgtnk == "T") or (datnk == "T"):
		grudinimasfm.text_color = "red"
		grudinimasfm.font_style = "bold"
		new_data = {'grupe': [*grudinimaslist], 'reiksmes': reik * len(grudinimaslist)}
		grudinimascds.data.update(new_data)
	else:
		grudinimasfm.text_color = "#CCCC00"
		grudinimasfm.font_style = "bold"
		new_data = {'grupe': [*grudinimaslist], 'reiksmes': reik * len(grudinimaslist)}
		grudinimascds.data.update(new_data)

	# Kaitinimasis
	if (sptna == "T") or (kgtna == "T") or (datna == "T"):
		kaitinimasfm.text_color = "red"
		kaitinimasfm.font_style = "bold"
		new_data = {'grupe': [*kaitinimaslist], 'reiksmes': reik * len(kaitinimaslist)}
		kaitinimascds.data.update(new_data)
	else:
		kaitinimasfm.text_color = "#CCCC00"
		kaitinimasfm.font_style = "bold"
		new_data = {'grupe': [*kaitinimaslist], 'reiksmes': reik * len(kaitinimaslist)}
		kaitinimascds.data.update(new_data)

	# Galūnių laikymas šiltai
	if sptnk == "T":
		galuniulsilfm.text_color = "green"
		galuniulsilfm.font_style = "bold"
		new_data = {'grupe': [*galuniulsillist], 'reiksmes': reik * len(galuniulsillist)}
		galuniulsilcds.data.update(new_data)
	else:
		galuniulsilfm.text_color = None
		galuniulsilfm.font_style = "bold"
		new_data = {'grupe': [*galuniulsillist], 'reiksmes': reik * len(galuniulsillist)}
		galuniulsilcds.data.update(new_data)

	# Galūnių laikymas šaltai
	if sptnk == "T":
		galuniulsalfm.text_color = "red"
		galuniulsalfm.font_style = "bold"
		new_data = {'grupe': [*galuniulsallist], 'reiksmes': reik * len(galuniulsallist)}
		galuniulsalcds.data.update(new_data)
	else:
		galuniulsalfm.text_color = None
		galuniulsalfm.font_style = "bold"
		new_data = {'grupe': [*galuniulsallist], 'reiksmes': reik * len(galuniulsallist)}
		galuniulsalcds.data.update(new_data)

	# Buvimas šiltesnėje aplinkoje
	if sptnk == "T":
		buvsilaplfm.text_color = "green"
		buvsilaplfm.font_style = "bold"
		new_data = {'grupe': [*buvsilapllist], 'reiksmes': reik * len(buvsilapllist)}
		buvsilaplcds.data.update(new_data)
	else:
		buvsilaplfm.text_color = None
		buvsilaplfm.font_style = "bold"
		new_data = {'grupe': [*buvsilapllist], 'reiksmes': reik * len(buvsilapllist)}
		buvsilaplcds.data.update(new_data)

	# Buvimas šaltesnėje aplinkoje
	if sptnk == "T":
		buvsalaplfm.text_color = "red"
		buvsalaplfm.font_style = "bold"
		new_data = {'grupe': [*buvsalapllist], 'reiksmes': reik * len(buvsalapllist)}
		buvsalaplcds.data.update(new_data)
	else:
		buvsalaplfm.text_color = None
		buvsalaplfm.font_style = "bold"
		new_data = {'grupe': [*buvsalapllist], 'reiksmes': reik * len(buvsalapllist)}
		buvsalaplcds.data.update(new_data)

	# Atidėta ejakuliacija (vyrams)
	if (sptnk == "T") and (lytis.value == "Vyras"):
		atidejakulfm.text_color = "green"
		atidejakulfm.font_style = "bold"
		new_data = {'grupe': [*atidejakullist], 'reiksmes': reik * len(atidejakullist)}
		atidejakulcds.data.update(new_data)
	else:
		atidejakulfm.text_color = None
		atidejakulfm.font_style = "bold"
		new_data = {'grupe': [*atidejakullist], 'reiksmes': reik * len(atidejakullist)}
		atidejakulcds.data.update(new_data)

	# Pakartotinis orgazmas (moterims)
	if (sptna == "T") and (lytis.value == "Moteris"):
		pakartotorgfm.text_color = "green"
		pakartotorgfm.font_style = "bold"
		new_data = {'grupe': [*pakartotorglist], 'reiksmes': reik * len(pakartotorglist)}
		pakartotorgcds.data.update(new_data)
	else:
		pakartotorgfm.text_color = None
		pakartotorgfm.font_style = "bold"
		new_data = {'grupe': [*pakartotorglist], 'reiksmes': reik * len(pakartotorglist)}
		pakartotorgcds.data.update(new_data)

	# Limfotakos aktyvavimas
	if (etptna == "T") or (etptna == "T"):
		limfoaktyvfm.text_color = "green"
		limfoaktyvfm.font_style = "bold"
		new_data = {'grupe': [*limfoaktyvlist], 'reiksmes': reik * len(limfoaktyvlist)}
		limfoaktyvcds.data.update(new_data)
	else:
		limfoaktyvfm.text_color = None
		limfoaktyvfm.font_style = "bold"
		new_data = {'grupe': [*limfoaktyvlist], 'reiksmes': reik * len(limfoaktyvlist)}
		limfoaktyvcds.data.update(new_data)


for k in [parametsp, parametkg, parametda, parametalac, parametetp, parametktalpac, parametralac, hidracind, dictlytis]:
	for w in list(itertools.chain.from_iterable([b[0] for b in [i for i in k.values()]])):
		w.on_change("value", pagr_update)


def reko_update(attr, old, new):
	# print("kitosrekolentel", kitosrekolentel.value)
	print("old", old)
	print("new", new)


kitosrekolentel.on_change("value", reko_update)


# def exportpng(a):
# 	grafikailist = [p1, p2, p3, p4, p5, p6, p7, dt1, dt2]
# 	for i in a:
# 		export_png(i, filename=f"{i}.png")


def ataskaitapdf():
	# exportpng(grafikailist)
	export_png(p1, filename="p1.png")
	export_png(p2, filename="p2.png")
	export_png(p3, filename="p3.png")
	export_png(p4, filename="p4.png")
	export_png(p5, filename="p5.png")
	export_png(p6, filename="p6.png")
	export_png(p7, filename="p7.png")
	export_png(dt1, filename="p8.png")
	export_png(dt2, filename="p9.png")

	font1 = ImageFont.truetype("LiberationSansNarrow-Bold.ttf", 24)
	font2 = ImageFont.truetype("LiberationSansNarrow-Bold.ttf", 26)
	font3 = ImageFont.truetype("LiberationSansNarrow-Bold.ttf", 32)
	font4 = ImageFont.truetype("LiberationSansNarrow-Regular.ttf", 22)

	# kitosrekolentel.value

	image_list = []

	for filename in glob.glob("/home/andrejusa/zintis/zintistyrimas/*.png"):
		image_list.append(filename)

	image_list = sorted(image_list)
	image_list.insert(0, "/home/andrejusa/zintis/Zintistyrimasasdasd/kodas/logo/zintislogo.png")
	print("image_list", image_list)

	width = 1300
	sumsh = []

	for i in image_list:
		img = Image.open(i)
		sumsh.append(img.size[1])

	totalh = sum(sumsh) - sumsh[-1] - 400
	new_i = Image.new("RGB", (width, totalh), "white")
	draw = ImageDraw.Draw(new_i)
	rekotext = '''Kategorijos išdėstytos svarbos mažėjimo tvarka, tad jei prioritetai dėl tam
tikrų maisto produktų vienas kitam prieštarauja, vadovautis tuo, kuris yra
aukščiau.
Prioritetų žymėjimas:
Žalia spalva - rekomenduojama vartoti daugiau,
Raudona spalva - vartoti nerekomenduojama,
Tamsiai geltona spalva - vartoti saikingai
(taip retai, kad būtų sunku prisiminti ankstesnio vartojimo datą),
Jokios spalvos - papildomų rekomendacijų nėra.'''
	# tyrimo pagridnasss
	text_coo_x = 100
	draw.text(xy=(400, 105), text="KŪNO BŪKLĖS TYRIMO ATASKAITA", fill=(0, 0, 0), font=font3)
	draw.text(xy=(text_coo_x, 225), text="Vardas:", fill=(0, 0, 0), font=font2)
	draw.text(xy=(text_coo_x, 265), text="Pavardė:", fill=(0, 0, 0), font=font2)
	draw.text(xy=(text_coo_x, 305), text="Lytis:", fill=(0, 0, 0), font=font2)
	draw.text(xy=(text_coo_x, 345), text="Data:", fill=(0, 0, 0), font=font2)
	draw.text(xy=(1100, 135), text="www.zintis.lt", fill=(0, 0, 0), font=font2)
	draw.text(xy=(1000, 175), text="sveikatingumas@zintis.lt", fill=(0, 0, 0), font=font2)

	draw.text(xy=(250, 225), text=invard.value, fill=(0, 0, 0), font=font2)
	draw.text(xy=(250, 265), text=inpavard.value, fill=(0, 0, 0), font=font2)
	draw.text(xy=(250, 305), text=lytis.value, fill=(0, 0, 0), font=font2)
	draw.text(xy=(250, 345), text="2018-01-20", fill=(0, 0, 0), font=font2)
	draw.text(xy=(5, 1955), text=rekotext, fill=(0, 0, 0), font=font4)
	draw.text(xy=(1000, 2000), text=kitosrekolentel.value, fill=(0, 0, 0), font=font4)

	begin = 10
	begin1 = 0

	for idx, img in enumerate(image_list):
		print(img)
		images = Image.open(img)
		sizeh = images.size[0]
		sizev = images.size[1]
		if idx == 0:
			sizeh = int(sizeh * 0.5)
			sizev = int(sizev * 0.5)
			images = images.convert("RGB")
			images = images.resize([sizeh, sizev], Image.ANTIALIAS)
			new_i.paste(images, (50, begin, (sizeh + 50), (begin + sizev)))
			begin += sizev
		elif 1 <= int(idx) <= 7:
			images = images.convert("RGB")
			new_i.paste(images, (700, begin, 1300, (begin + sizev)))
			begin += sizev
		else:
			if idx == 8:
				images = images.crop([0, 0, sizeh, 2000])
				sizev = images.size[1]
			images = images.convert("RGBA")
			alpha = images.convert('RGBA').split()[-1]
			new_i.paste(images, (begin1, begin, (begin1 + sizeh), (begin + sizev)), mask=alpha)
			begin1 += sizeh

	# kadangi ši dalis kodinta pyhon 3.5, todėl naujomas OrderedDict, bet nuo 3.6,1 versijos galima naudoti dict, nes duomenys
	# išlaiko vietą
	parametrai = ["Šlapimo parametrai", "Seilių parametrai", "Refleksai", "Kraujotakos parametrai", "Kvėpavimo parametrai"]
	duomenys = [[["Rūgštingumas", slarugrytas.value, slarugpietus.value, slarugvakaras.value],
					["Tankis", slasvrytas.value, slasvpietus.value, slasvvakaras.value],
					["Šviesumas", slasvrytas.value, slasvpietus.value, slasvvakaras.value],
					["Putojimas", slaputrytas.value, slaputpietus.value, slaputvakaras.value]],
					[["Rūgštingumas", serrytas.value, serpietus.value, servakaras.value],
					["Klampumas", sekrytas.value, sekpietus.value, sekvakaras.value]],
					[["Kūno temperatūra", ktrytas.value, ktpietus.value, ktvakaras.value],
					["Dermografizmas", drrytas.value, drpietus.value, drvakaras.value],
					["Vasomotorinis", vrrytas.value, vrpietus.value, vrvakaras.value],
					["Vyzdžio dydis", vdrytas.value, vdpietus.value, vdvakaras.value],
					["Tremoras (drebulys)", trrytas.value, trpietus.value, trvakaras.value],
					["Šnervių užgulimas", surytas.value, supietus.value, suvakaras.value],
					["Sargento linija", slrytas.value, slpietus.value, slvakaras.value]],
					[["Pulsas sėdinti",psrytas.value, pspietus.value, psvakaras.value],
					["Pulsas gulint", pgrytas.value, pgpietus.value, pgvakaras.value],
					["Sistolinis kraujospūdis gulint", skgrytas.value, skgpietus.value, skgvakaras.value],
					["Diastolinis kraujospūdis gulint", dkgrytas.value, dkgpietus.value, dkgvakaras.value],
					["Pulsas tik ką atsistojus",parytas.value, papietus.value, pavakaras.value],
					["Pulsas atsistojus po 15 s", pa15rytas.value, pa15pietus.value, pa15vakaras.value],
					["Sistolinis kraujospūdis atsistojus", skarytas.value, skapietus.value, skavakaras.value],
					["Diastolinis kraujospūdis atsistojus", dkarytas.value, dkapietus.value, dkavakaras.value],
					["Pulsas atsistojus po 45 s", pa45rytas.value, pa45pietus.value, pa45vakaras.value]],
					[["Kvėpavimo dažnis", kdrytas.value, kdpietus.value, kdvakaras.value],
					["Kvėpavimo sulaikymas įkvėpus", ksirytas.value, ksipietus.value, ksivakaras.value]]]

	parametruduomenys = OrderedDict()

	for duo, par in zip(duomenys, parametrai):
		parametruduomenys[par] = duo

	lis = []
	for i in duomenys:
		for j in i:
			lis.append(j[0])

	max_para_length = int(len(max(lis, key=len)))

	prad = 50
	pabaig = 400
	parametruh = 30

	for k, v in parametruduomenys.items():
		draw.text(xy=(prad, pabaig), text=k, fill=(0, 0, 0), font=font1)
		draw.text(xy=(395, pabaig), text="Rytas", fill=(0, 0, 0), font=font1)
		draw.text(xy=(470, pabaig), text="Pietūs", fill=(0, 0, 0), font=font1)
		draw.text(xy=(550, pabaig), text="Vakaras", fill=(0, 0, 0), font=font1)
		rytash = font1.getsize("Rytas")[0]
		pietush = font1.getsize("Pietūs")[0]
		vakarash = font1.getsize("Vakaras")[0]
		for j in v:
			pararytash = font1.getsize(j[1])[0]
			parapietush = font1.getsize(j[2])[0]
			paravakarash = font1.getsize(j[3])[0]
			draw.text(xy=(prad, pabaig + parametruh), text=j[0], fill=(0, 0, 0), font=font4)
			draw.text(xy=((rytash - pararytash) / 2 + 400, pabaig + parametruh), text=j[1], fill=(0, 0, 0), font=font4)
			draw.text(xy=((pietush - parapietush) / 2 + 480, pabaig + parametruh), text=j[2], fill=(0, 0, 0), font=font4)
			draw.text(xy=((vakarash - paravakarash) / 2 + 560, pabaig + parametruh), text=j[3], fill=(0, 0, 0), font=font4)
			draw.rectangle((((prad - 5), (pabaig + parametruh)), ((390 - 5), (pabaig + parametruh * 2))), outline="black")
			draw.rectangle((((470 - 5), (pabaig + parametruh)), ((390 - 5), (pabaig + parametruh * 2))), outline="black")
			draw.rectangle((((550 - 5), (pabaig + parametruh)), ((390 - 5), (pabaig + parametruh * 2))), outline="black")
			draw.rectangle((((640 - 5), (pabaig + parametruh)), ((390 - 5), (pabaig + parametruh * 2))), outline="black")
			pabaig = pabaig + parametruh + 10
		pabaig = pabaig + parametruh + 40

	new_i.save("p10.pdf", "PDF", resoliution=100.0)


rekomendmyg.on_click(ataskaitapdf)

# visi elementai sujungiami į norimą layout
lay1 = row(protok, invard, inpavard, lytis, inamz)
lay2 = layout(
	[slapimo],
	[aprslarugs, slarugrytas, slarugpietus, slarugvakaras],
	[aprslatank, slatankrytas, slatankpietus, slatankvakaras],
	[aprslasvies, slasvrytas, slasvpietus, slasvvakaras],
	[aprslaputo, slaputrytas, slaputpietus, slaputvakaras],
	[prikseil],
	[seiliu],
	[aprseilrugst, serrytas, serpietus, servakaras],
	[aprseilklamp, sekrytas, sekpietus, sekvakaras],
	[tiriam],
	[kraujot],
	[aprpulsed, psrytas, pspietus, psvakaras],
	[refleksu],
	[aprkunotemp, ktrytas, ktpietus, ktvakaras],
	[aprdermoref, drrytas, drpietus, drvakaras],
	[aprvasomref, vrrytas, vrpietus, vrvakaras],
	[aprvyzdyd, vdrytas, vdpietus, vdvakaras],
	[aprtremoref, trrytas, trpietus, trvakaras],
	[aprsneruzgu, surytas, supietus, suvakaras],
	[tiriam1],
	[aprsarglinref, slrytas, slpietus, slvakaras],
	[tiriam2],
	[kvepparmat10],
	[aprkvepdaz, kdrytas, kdpietus, kdvakaras],
	[tiriam3],
	[kraujparmat],
	[aprpulgul, pgrytas, pgpietus, pgvakaras],
	[aprsiskraujgul, skgrytas, skgpietus, skgvakaras],
	[aprdiakraujgul, dkgrytas, dkgpietus, dkgvakaras],
	[ortatest],
	[aprpulsatsi15],
	[atsist, parytas, papietus, pavakaras],
	[po15, pa15rytas, pa15pietus, pa15vakaras],
	[aprkraujpulsatsi45],
	[siskraujatsi, skarytas, skapietus, skavakaras],
	[diaskraujatsi, dkarytas, dkapietus, dkavakaras],
	[pulsatsi45, pa45rytas, pa45pietus, pa45vakaras],
	[tiriam4],
	[kvepparmat14],
	[aprkvepsu, ksirytas, ksipietus, ksivakaras])

grid = gridplot([p1, spacer_2, p2, spacer_3, p3, spacer_4, p4, spacer_5, p5, spacer_6, p6, spacer_7, p7], ncols=1)
lay3 = row(spacer_0, rekomendmyg)
lay4 = row(lay2, grid)

dt1 = column(
	maistproduk,
	gervandtable,
	orgrugtable,
	hidrokarbotable,
	natchlofluotable,
	sulfattable,
	krakmoltable,
	augalinerttable,
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

dt2 = column(
	kitumedz,
	paksavyvanduotable,
	slopikaitable,
	stimuliattable,
	rukalaitable,
	kitielgsen,
	didintesyvtable,
	mazointesyvtable,
	kvepasulaiktable,
	hipoventiltable,
	grudinimastable,
	kaitinimastable,
	galuniulsiltable,
	galuniulsaltable,
	buvsilapltable,
	buvsalapltable,
	atidejakultable,
	pakartotorgtable,
	limfoaktyvtable,
	subalanmiegtable,
	kitosreko
)
lay5 = column(kitosrekolentel, lay3, rekokatego, rekotipai)
lay6 = column(dt2, lay5)
lay7 = row(dt1, spacer_8, lay6)
lay8 = column(lay1, pagrapras, lay4, lay7)

# add the layout to curdoc
curdoc().add_root(lay8)
