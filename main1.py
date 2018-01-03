
# -*- coding: utf-8 -*-
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models.widgets import TextInput, Div, Select
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
	<title>{{ title if title else "Bokeh Plot" }} </title>
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
			margin-bottom:3%;
			}

			th,td {
			border: 1px solid #c6c7cc;
			padding: 10px 15px;
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
			width: 80%;
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
	return Div(text="""<br><b>ORGANIZMO BŪKLĖS TYRIMO PROTOKOLAS</b>""", width=330, height=None)


invard = TextInput(name="vard", value="", title="Vardas", width=130)
inpavard = TextInput(name="pavard", value="", title="Pavardė", width=160)
lytis = Select(name="lyt", title="Lytis:", options=["Vyras", "Moteris"], width=130)
inamz = TextInput(name="amz", value="", title="Amžius", width=80)


def tikslus():
	return Div(text="""Tikslūs organizmo tyrimo metu atliekamų testų rezultatai padeda geriau suprasti organizme vykstančius procesus,
	todėl tinkamas pasirengimas tyrimui yra labai svarbus tikrajai Jūsų organizmo būklei nustatyti:""", width=780)


def eiga():
	return Div(text="""<b>ORGANIZMO BŪKLĖS TYRIMO EIGA</b>
<br><br>Organizmo būklės nustatymo tikslumui lemiamos įtakos turi tikslūs organizmo parametrų išmatavimai.
Šiuos parametrus stipriai veikia tiriamojo psichologinė būklė tyrimo metu, taip pat matavimų eilės tvarka.
Svarbu, kad organizmo būklės tyrimas būtų vykdomas griežtai pagal nurodytą seką.
Taip pat rekomenduotina kelias dienas iki tyrimo pasipraktikuoti jį atlikti, kad tyrimo dieną viskas vyktų sklandžiai.
Tyrimo trukmė apie 45 minutės. Pamatuoti duomenys rašomi į <b>„Organizmo būklės tyrimo formos“ </b>skiltį<b><i> „Tyrimo protokolas“</i></b>.
<br><br><b>PRIEMONĖS</b>:
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
<br><b>1.</b> 2 valandos iki tyrimo<b><i>nevalgyti</b></i>, jei norisi,<b><i>galima gerti negazuoto vandens</b></i>.
<br><b>2.</b> 30 minučių iki tyrimo<b><i>nieko negerti ir nekramtyti</b></i>.""", width=780)


def slapimo():
	return Div(text="""<b>3. Šlapimo parametrų matavimas:</b>""", width=780)


def prikseil():
	return Div(text="""<b > 4.</b><i>Tiriamojo paprašoma prikaupti seilių ir įspjauti į valgomąjį šaukštą. Seilių turi būti
maždaug mažojo piršto galinio narelio dydžio lašas.</i>""", width=780)


def seiliu():
	return Div(text="""<b>5. Seilių parametrų matavimas:</b>""", width=780)


def tiriam():
	return Div(text="""<b>6.</b><i>Tiriamojo paprašoma atsisėsti ant sofos arba lovos per vidurį.</i>""", width=780)


def kraujot():
	return Div(text="""<b>7. Kraujotakos parametrų matavimas:</b>""", width=780)


def refleksu():
	return Div(text="""<b>8. Refleksų tyrimas:</b>""", width=780)


def tiriam1():
	return Div(text="""<i>Tiriamojo paprašoma atsigulti ant sofos ar lovos ant kurios sėdi. Gulamasi
ištiestomis kojomis, galvą dedant taip, kad prie sofos ar lovos krašto būtų tiriamojo kairė
pusė. Paliekamas toks tarpas nuo sofos ar lovos krašto, kad tiriamojo kairė ranka laisvai
gulėtų šalia delnu į viršų. Paprašoma atsipalaiduoti, nekalbėti ir nusiraminti. Taip
tiriamasis turi pagulėti daugiau nei 1 minutę.</i>""", width=780)


def tiriam2():
	return Div(text="""<b>9.</b><i>Tiriamajam pranešama, kad jis jau gali užsidengti pilvą ir paprašoma atsipalaiduoti,
nekalbėti ir nusiraminti. Taip tiriamasis turi pagulėti daugiau nei 1 minutę.</i></b>""", width=780)


def kvepparmat10():
	return Div(text="""<b>10. Kvėpavimo parametrų matavimas:</b>""", width=780)


def tiriam3():
	return Div(text="""<b>11.</b><i>Tiriamajam ant kairės rankos žasto uždedama kraujospūdžio matavimo manžetė.</i>""", width=780)


def kraujparmat():
	return Div(text="""<b>12. Kraujotakos parametrų matavimas:</b>""", width=780)


def ortatest():
	return Div(text="""<b>Ortostatinis testas.</b> Tiriamajam atsistojus, kraujospūdžio matuoklio žarnelė neturi
būti tempiama, todėl matuoklį reikia<i>padėti ant paaukštinimo, pritvirtinti prie manžetės
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
Tiriamajam besistojant, Jūs turite likti sėdėti.""", width=780)


def atsist():
	return Div(text="""<br>Atsistojus<br>(dūžių skaičius per pirmas 15 s,×4)""", width=300)


def po15():
	return Div(text="""<br>Po 15 s.<br>(dūžių skaičius tarp 15-tos ir 45-tos sekundės,×2)""", width=300)


def siskraujatsi():
	return Div(text="""<br>Sistolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „SYS“ po 45 s)""", width=300)


def diaskraujatsi():
	return Div(text="""<br>Diastolinis kraujospūdis atsistojus<br>(rodmuo ekrane ties „DIA“)""", width=300)


def pulsatsi45():
	return Div(text="""<br>Pulsas atsistojus po 45 s<br>(rodmuo ekrane ties „PULS“)""", width=300)


def tiriam4():
	return Div(text="""<b>13.</b><i> Nuimama manžetė nuo tiriamojo žasto.</i>""", width=780)


def kvepparmat14():
	return Div(text="""<b>14. Kvėpavimo parametrų matavimas:</b>""", width=780)


def kataanab():
	return Div(text="""<b>KATABOLIZMAS|ANABOLIZMAS</b>""", width=780)


def pav1():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup1">3-2 SAVAITĖS IKI TYRIMŲ DIENOS</a>
</div>

<div id="popup1" class="overlay">
	<div class="popup" id="showpopup">
		<h2>3-2 SAVAITĖS IKI TYRIMŲ DIENOS</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
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
<br><b>Krakmolo šaltinius:</b><i>Bulves ir jų produktus (traškučius, lietuviškas mišraines, tirštas
sriubas, kisielių ir pan.), miltų gaminius (duoną, batoną, bandeles, pyragus, blynus,
makaronus ir pan.), grūdus (kviečius, rugius, ryžius, grikius, avižas, miežius, soras ir pan.),
visas kruopas, dribsnius, ankštinius (pupas, pupeles, lęšius, žirnius). GALIMA VARTOTI
žaliuosius žirnelis ir visas daržoves neribotais kiekiais.</i>
<br><b>Saldžius produktus:</b><i>Saldainius, tortus, pyragėlius, sausainius, šokoladą, ledus, medų,
uogienes, sirupus, sultis, limonadus, vaisius, uogas, alų, likerį, saldų bei pusiau sausą vyną,
saldų bei pusiau sausą putojantį vyną.</i>
<br><b>Polinesočiuosius riebalus:</b><i>Saulėgrąžų, rapsų, sezamų, linų sėmenų, moliūgų sėklų,
nakvišų aliejus, žuvų taukus, saulėgrąžas, sėmenis, sezamų sėklas, visus riešutus (išskyrus
kokosų, migdolų ir lazdyno), pistacijas, soją ir jos produktus, margariną, majonezą, picų
padažus, „tepamus riebalų mišinius", „grietinės ir augalinių riebalų mišinius", „sūrio
produktus“. GALIMA VARTOTI alyvuogių, avokadų, kokosų, migdolų, lazdyno riešutų aliejus,
kakavos sviestą, pieno sviestą, lašinius.</i>
<br><b>Stipriai pakitusius baltymus ir riebalus:</b><i>Savo sultis atidavusią kaitintą mėsą, kietai
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
<br>• Graikiškos salotos
		</div>
	</div>
</div>
	""")


def pav2():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup2">MAŽIAUSIAI 2 DIENOS IKI TYRIMŲ DIENOS</a>
</div>

<div id="popup2" class="overlay">
	<div class="popup" id="showpopup">
		<h2>MAŽIAUSIAI 2 DIENOS IKI TYRIMŲ DIENOS</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Nuo ryto nustojamos vartoti šios medžiagos:
<br><b>Kava, arbata, kakava, šokoladas, energiniai gėrimai, rūkalai, alkoholis, gazuoti
gėrimai, maisto papildai ir vaistai </b>(IŠSKIRTINIAIS ATVEJAIS, kai vaistų nutraukimas tokiam ilgam periodui gali sukelti pavojų gyvybei,<b> vaistų
nevartoti bent 1 dieną prieš tyrimą)</b>.<i>GALIMA VARTOTI žolelių arbatas, rooibos arbatą</i>.
<br>Iki tyrimo neužsiimama intensyvia arba ilgalaike fizine veikla.
		</div>
	</div>
</div>
	""")


def pav3():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup3">TYRIMŲ DIENOS IŠVAKARĖSE</a>
</div>

<div id="popup3" class="overlay">
	<div class="popup" id="showpopup">
		<h2>TYRIMŲ DIENOS IŠVAKARĖSE</h2>
		<a class="close" href="#showpopup">&times;</a>
		<div class="content">
Jei kitą dieną matavimus atliks sutartu metu atvykęs asmuo, nuo pietų pradedami rinkti 3
šlapimo mėginiai:
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apiepiet – prieš pietus arba bent 2 val. po valgio.</i>
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Vakare – prieš pat miegą, bent 2 val. po valgio.</i>
<br><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ryte – prieš pusryčius, ne vėliau nei 30 min. nuo atsikėlimo.</i>
<br>Šlapimo mėginys imamas į indelius, skirtus šlapimui, jų galima įsigyti vaistinėse. Mėginio
tūris turi būti 60 ml. Mėginius reikia pažymėti, kad jie nebūtų supainioti.
<br><b>Jei kitą dieną matavimai bus atliekami 3 kartus, šlapimo mėginiai imami ir tiriami
tyrimų dieną.</b>
		</div>
	</div>
</div>
	""")


def pav4():
	return Div(text="""
<div class="box">
	<a class="button" href="#popup4">TYRIMŲ DIENĄ</a>
</div>

<div id="popup4" class="overlay">
	<div class="popup" id="showpopup">
		<h2>TYRIMŲ DIENĄ</h2>
		<a class="close" href="#showpopup"">&times;</a>
		<div class="content">
Tyrimų dieną galima valgyti, bet vis dar laikantis ankstesnių mitybos nurodymų. Iki tyrimo
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
		</div>
	</div>
</div>
	""")


def aprsrugs():
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


def aprstank():
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


def aprsputo():
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


def aprserugst():
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


def aprseklamp():
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


skarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
skapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
skavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

dkarytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
dkapietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
dkavakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)

pa45rytas = TextInput(name="rytas", value="0", title="Rytas", width=60)
pa45pietus = TextInput(name="pietus", value="0", title="Pietūs", width=60)
pa45vakaras = TextInput(name="vakaras", value="0", title="Vakaras", width=60)


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

p1 = grafikai.make_graf(grafikai.plist[0], grafikai.pavadin[0], grafikai.countsp, grafikai.factorssp)
p2 = grafikai.make_graf(grafikai.plist[1], grafikai.pavadin[1], grafikai.countkg, grafikai.factorskg)
p3 = grafikai.make_graf(grafikai.plist[2], grafikai.pavadin[2], grafikai.countda, grafikai.factorsda)
p4 = grafikai.make_graf(grafikai.plist[3], grafikai.pavadin[3], grafikai.countmalac, grafikai.factorsmalac)
p5 = grafikai.make_graf(grafikai.plist[4], grafikai.pavadin[4], grafikai.countetp, grafikai.factorsetp)
p6 = grafikai.make_graf(grafikai.plist[5], grafikai.pavadin[5], grafikai.countktp, grafikai.factorsktp)
p7 = grafikai.make_graf(grafikai.plist[6], grafikai.pavadin[6], grafikai.countralac, grafikai.factorsralac)

prodomas = [p1, p2, p3, p4, p5, p6, p7]


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
	else:
		verte1 = float("".join(str(i) for i in (L[0][0].value)).replace(",", "."))
		verte2 = float("".join(str(i) for i in (L[0][1].value)).replace(",", "."))
		verte3 = float("".join(str(i) for i in (L[0][2].value)).replace(",", "."))
		verte4 = float("".join(str(i) for i in (L[0][-1].value)).replace(",", "."))
		return verte1, verte2, verte3, verte4


def formule_kt_ar_ap(skirtum, lin, ind, lentel, *arg):
	NormaK = lentel.loc[lentel.index[ind], "Norma K"]
	NormaA = lentel.loc[lentel.index[ind], "Norma A"]

	if NormaA == 1000:
		NormaA = arg[0]
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaA, NormaK]) / len([NormaA, NormaK])
	elif NormaK == NormaA == 1001:
		if arg[0] < 6.4:
			NormaK = 67
			NormaA = 52
		elif arg[0] > 7.1:
			NormaK = 46
			NormaA = 31
		else:
			NormaK = (-30 * arg[0]) + 259
			NormaA = (-30 * arg[0]) + 244
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaA, NormaK]) / len([NormaA, NormaK])
	elif NormaK == NormaA == 1002:
		if arg[0] < 6.4:
			NormaK = 64
			NormaA = 68
		elif arg[0] > 7.1:
			NormaK = 92
			NormaA = 96
		else:
			NormaK = (-30 * arg[0]) + 192
			NormaA = (-30 * arg[0]) + 188
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaA, NormaK]) / len([NormaA, NormaK])
	elif NormaK == -0.28 and NormaA == -0.18:
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = -0.1
	else:
		pagrindas = lentel.loc[lentel.index[ind], "Pagrindas"]
		balansas = sum([NormaA, NormaK]) / len([NormaA, NormaK])

	if (NormaK - balansas) < 0:
		kryptis = 1
	else:
		kryptis = -1

	if (skirtum - balansas) * kryptis >= 0:
		zenklas = 1
	else:
		zenklas = -1

# nustatoma alfa  ir beta reikšmės
	if zenklas > 0:
		alfa = (1 - pagrindas) / (balansas - NormaA)
		beta = (pagrindas * balansas - NormaA) / (balansas - NormaA)
	else:
		alfa = (1 - pagrindas) / (balansas - NormaK)
		beta = (pagrindas * balansas - NormaK) / (balansas - NormaK)

# nustatoma ar katabolizmo ar anabolizmo reikšmė
	if zenklas < 0:
		ktarap = (zenklas * math.log(alfa * skirtum + beta, pagrindas))
	else:
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
	logging.info(ktarap)
	return ktarapriba


# simpatinis|parasimpatinis

simparasim = {
	"Norma K": [-2, 11, 25, 6, 36.7, 1, -1, 1, 1, -1, 1, 1],
	"Norma A": [0, 6, 22, 4, 36.5, 2, 1, -1, -1, 1, -1, -1],
	"Pagrindas": [2, 2, 2, 1.001, 2, 1.2, 1.001, 1.001, 1.001, 1.001, 1.001, 1.001]}

parametrupavsp = ["Ps-1", "S+D", "Pm-1+Pm-4", "KRi", "Temp", "Derm", "Vaso", "Vyzd", "Trem", "Nos", "Sarg", "S-kl"]
lentelesp = pd.DataFrame(simparasim, index=parametrupavsp)
lentelesp = lentelesp[["Norma K", "Norma A", "Pagrindas"]]

parametsp = {
	"ps1rytas": [[psrytas, pgrytas], "ps1r", CDS.srcps1r.data, make_lin(p1, CDS.srcps1r), parametrupavsp.index("Ps-1")],
	"ps1pietūs": [[pspietus, pgpietus], "ps1p", CDS.srcps1p.data, make_lin(p1, CDS.srcps1p), parametrupavsp.index("Ps-1")],
	"ps1vakaras": [[psvakaras, pgvakaras], "ps1v", CDS.srcps1v.data, make_lin(p1, CDS.srcps1v), parametrupavsp.index("Ps-1")],

	"s+drytas": [[skarytas, skgrytas, dkarytas, dkgrytas], "s+dr", CDS.srcsdr.data, make_lin(p1, CDS.srcsdr), parametrupavsp.index("S+D")],
	"s+dpietūs": [[skapietus, skgpietus, dkapietus, dkgpietus], "s+dp", CDS.srcsdp.data, make_lin(p1, CDS.srcsdp), parametrupavsp.index("S+D")],
	"s+dvakaras": [[skavakaras, skgvakaras, dkavakaras, dkgvakaras], "s+dv", CDS.srcsdv.data, make_lin(p1, CDS.srcsdv), parametrupavsp.index("S+D")],

	"pm1pm4rytas": [[pgrytas, parytas, pa15rytas, pa45rytas], "pm1pm4r", CDS.srcppr.data, make_lin(p1, CDS.srcppr), parametrupavsp.index("Pm-1+Pm-4")],
	"pm1pm4pietūs": [[pgpietus, papietus, pa15pietus, pa45pietus], "pm1pm4p", CDS.srcppp.data, make_lin(p1, CDS.srcppp), parametrupavsp.index("Pm-1+Pm-4")],
	"pm1pm4vakaras": [[pgvakaras, pavakaras, pa15vakaras, pa45vakaras], "pm1pm4v", CDS.srcppv.data, make_lin(p1, CDS.srcppv), parametrupavsp.index("Pm-1+Pm-4")],

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

	"vyzdrytas": [[vdrytas], "vyzdr", CDS.srcvyzdr.data, make_lin(p1, CDS.srcvyzdr), parametrupavsp.index("Vyzd")],
	"vyzdpietūs": [[vdpietus], "vyzdp", CDS.srcvyzdp.data, make_lin(p1, CDS.srcvyzdp), parametrupavsp.index("Vyzd")],
	"vyzdvakaras": [[vdvakaras], "vyzdv", CDS.srcvyzdv.data, make_lin(p1, CDS.srcvyzdv), parametrupavsp.index("Vyzd")],

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


def ps1_update(attr, old, new):
	for key in parametsp.keys():
		if "ps1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2 = verte(n)
			formule = (v1 - v2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def sd_update(attr, old, new):
	for key in parametsp.keys():
		if "s+d" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2, v3, v4 = verte(n)
			formule = (v1 - v2) + (v3 - v4)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def pm1pm4_update(attr, old, new):
	for key in parametsp.keys():
		if "pm1pm4" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2, v3, v4 = verte(n)
			r1 = max(v1, v2, v3, v4) - v1
			r2 = max(v1, v2, v3, v4) - v4
			formule = (r1 + r2)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def kri_update(attr, old, new):
	for key in parametsp.keys():
		if "kri" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1, v2 = verte(n)
			if v2 != 0:
				formule = (v1 / v2)
				karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
				new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
				sourcedata.update(new_data)


def temp_update(attr, old, new):
	for key in parametsp.keys():
		if "temp" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def dermsp_update(attr, old, new):
	for key in parametsp.keys():
		if "derm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def vaso_update(attr, old, new):
	for key in parametsp.keys():
		if "vaso" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def vyzd_update(attr, old, new):
	for key in parametsp.keys():
		if "vyzd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def trem_update(attr, old, new):
	for key in parametsp.keys():
		if "trem" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def nos_update(attr, old, new):
	for key in parametsp.keys():
		if "nos" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def sarg_update(attr, old, new):
	for key in parametsp.keys():
		if "sarg" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def skl_update(attr, old, new):
	for key in parametsp.keys():
		if "skl" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametsp[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelesp)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametsp.values()]])):
	w.on_change(
		"value",
		ps1_update, sd_update, pm1pm4_update, kri_update, temp_update, dermsp_update,
		vaso_update, vyzd_update, trem_update, nos_update, sarg_update, skl_update)


# ketogeninis|gliukogeninis

ketogliuko = {
	"Norma K": [15, 1001, 1002, 6, 5, 1, -0.28],
	"Norma A": [1000, 1001, 1002, 8, 0, -1, -0.18],
	"Pagrindas": [2, 1.2, 2.5, 2, 2, 1.1, 1.2]}

parametrupavkg = ["KD", "t(ksi)", "P4", "KpHi", "D2-P4", "U-šv", "U-put"]
lentelekg = pd.DataFrame(ketogliuko, index=parametrupavkg)
lentelekg = lentelekg[["Norma K", "Norma A", "Pagrindas"]]

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


def kdkg_update(attr, old, new):
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
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, sphkv)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def tksikg_update(attr, old, new):
	for key in parametkg.keys():
		if "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, stv, serv = verte(n)
			tankindx = (stv * 1000) - 1000
			sphk = serv + (0.033333 * tankindx) - 0.533333
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, sphk)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def p4_update(attr, old, new):
	for key in parametkg.keys():
		if "p4" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, stv, serv = verte(n)
			tankindx = (stv * 1000) - 1000
			sphk = serv + (0.033333 * tankindx) - 0.533333
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg, sphk)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def kphikg_update(attr, old, new):
	for key in parametkg.keys():
		if "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def d2p4_update(attr, old, new):
	for key in parametkg.keys():
		if "d2p(4)" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def usvkg_update(attr, old, new):
	for key in parametkg.keys():
		if "usv" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def uputkg_update(attr, old, new):
	for key in parametkg.keys():
		if "uput" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametkg[key]
			v1 = verte(n)
			sourcedata1, sourcedata2 = sourcedata
			formule = v1
			if formule == -1:
				karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelekg)
			else:
				karareiksme = 0

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data1 = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata1.update(new_data1)
			new_data2 = {'x': [0, -karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata2.update(new_data2)


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametkg.values()]])):
	w.on_change(
		"value", kdkg_update, tksikg_update, p4_update, kphikg_update, d2p4_update, usvkg_update, uputkg_update)

# disaerobinis|anaerobinis

disaeanae = {
	"Norma K": [18, 6.1, 6.8, 1, 1, 0.75],
	"Norma A": [14, 6.3, 6.6, 2, -1, -0.5],
	"Pagrindas": [1.5, 2, 2, 1.5, 1.3, 1.1]}

parametrupavda = ["d(tank)", "U-pHK", "S-pHK", "Derm", "U-šv", "U-put"]
lenteleda = pd.DataFrame(disaeanae, index=parametrupavda)
lenteleda = lenteleda[["Norma K", "Norma A", "Pagrindas"]]

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


def dtank_update(attr, old, new):
	for key in parametda.keys():
		if "dtank" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = (v1 * 1000) - 1000
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def uphkda_update(attr, old, new):
	for key in parametda.keys():
		if "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def sphkda_update(attr, old, new):
	for key in parametda.keys():
		if "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


# derm_update jau anksčiau apibrėžtas
def dermda_update(attr, old, new):
	for key in parametda.keys():
		if "derm" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def usvda_update(attr, old, new):
	for key in parametda.keys():
		if "usv" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def uputda_update(attr, old, new):
	for key in parametda.keys():
		if "uput" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametda[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lenteleda)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametda.values()]])):
	w.on_change(
		"value", dtank_update, uphkda_update, sphkda_update, dermda_update, usvda_update, uputda_update)

alkaacid = {
	"Norma K": [13, 65, 5, 6.3, 6.6, 67, 0],
	"Norma A": [19, 40, 10, 5.9, 6.8, 75, 10],
	"Pagrindas": [1.2, 1.01, 1.5, 2, 2, 1.5, 2]}

parametrupavalac = ["KD", "t(ksi)", "KpHi", "U-pHK", "S-pHK", "P1", "P4–P1"]
lentelealac = pd.DataFrame(alkaacid, index=parametrupavalac)
lentelealac = lentelealac[["Norma K", "Norma A", "Pagrindas"]]

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

	"p(1)rytas": [[pgrytas], "p1r", CDS.srcp1r.data, make_lin(p4, CDS.srcp1r), parametrupavalac.index("P1")],
	"p(1)pietūs": [[pgpietus], "p1p", CDS.srcp1p.data, make_lin(p4, CDS.srcp1p), parametrupavalac.index("P1")],
	"p(1)vakaras": [[pgvakaras], "p1v", CDS.srcp1v.data, make_lin(p4, CDS.srcp1v), parametrupavalac.index("P1")],

	"p4p1rytas": [[pa45rytas, pgrytas], "p4p1r", CDS.srcp4p1r.data, make_lin(p4, CDS.srcp4p1r), parametrupavalac.index("P4–P1")],
	"p4p1pietūs": [[pa45pietus, pgpietus], "p4p1p", CDS.srcp4p1p.data, make_lin(p4, CDS.srcp4p1p), parametrupavalac.index("P4–P1")],
	"p4p1vakaras": [[pa45vakaras, pgvakaras], "p4p1v", CDS.srcp4p1v.data, make_lin(p4, CDS.srcp4p1v), parametrupavalac.index("P4–P1")]}


def kdalac_update(attr, old, new):
	for key in parametalac.keys():
		if "kd" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def tksialac_update(attr, old, new):
	for key in parametalac.keys():
		if "tksi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def kphialac_update(attr, old, new):
	for key in parametalac.keys():
		if "kphi" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1, v2 = verte(n)
			formule = v1 - (v2 / 5)
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def uphkalac_update(attr, old, new):
	for key in parametalac.keys():
		if "uphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			slatv, slarugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = slarugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def sphkalac_update(attr, old, new):
	for key in parametalac.keys():
		if "sphk" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			slatv, serugv = verte(n)
			tankindx = (slatv * 1000) - 1000
			formule = serugv + (0.033333 * tankindx) - 0.533333
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def p1_update(attr, old, new):
	for key in parametalac.keys():
		if "p(1)" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1 = verte(n)
			formule = v1
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


def p4p1_update(attr, old, new):
	for key in parametalac.keys():
		if "p4p1" in str(key):
			n, yreiksme, sourcedata, linija, indx = parametalac[key]
			v1, v2 = verte(n)
			formule = v1 - v2
			karareiksme = formule_kt_ar_ap(formule, linija, indx, lentelealac)
			if karareiksme < 0:
				karareiksme = 0

	# atnaujinamas x ir y reikšmės atvaizdavimui grafike
			new_data = {'x': [0, karareiksme], 'y': [yreiksme, yreiksme]}
			sourcedata.update(new_data)


for w in list(itertools.chain.from_iterable([b[0] for b in [w for w in parametalac.values()]])):
	w.on_change(
		"value", kdalac_update, tksialac_update, kphialac_update, uphkalac_update, sphkalac_update, p1_update, p4p1_update)

# visi elementai sujungiami į norimą layout
lay1 = layout(
	[protok()],
	[invard, inpavard, lytis, inamz],
	[tikslus()],
	[pav1()],
	[pav2()],
	[pav3()],
	[pav4()],
	[eiga()],
	[slapimo()],
	[aprsrugs(), slarugrytas, slarugpietus, slarugvakaras],
	[aprslasvies(), slasvrytas, slasvpietus, slasvvakaras],
	[aprstank(), slatankrytas, slatankpietus, slatankvakaras],
	[aprsputo(), slaputrytas, slaputpietus, slaputvakaras],
	[prikseil()],
	[seiliu()],
	[aprserugst(), serrytas, serpietus, servakaras],
	[aprseklamp(), sekrytas, sekpietus, sekvakaras],
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

lay2 = column(prodomas)
lay3 = row(lay1, lay2)

# add the layout to curdoc
curdoc().add_root(lay3)
