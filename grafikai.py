# -*- coding: utf-8 -*-

from bokeh.plotting import figure
from bokeh.models import Span, BoxAnnotation, FixedTicker
from bokeh.models.ranges import FactorRange

# grafikai
pavadin = [
	"<-Simpatinis|Parasimpatinis->",
	"<-Ketogeniniss|Gliukogeninis->",
	"<-Disaerobinis|Anaerobinis->",
	"<-Rūgščių trūkumas|Rūgščių perteklius->",
	"<-Elektrolitų trūkumas|Elektrolitų perteklius->",
	"<-Kalio trūkumas|Kalio perteklius->",
	"<-Anglies dvideginio trūkumas|Anglies dvideginio perteklius->"]

plist = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]

# categorical tipo duomenys, kad būtų galima atvaziduoti grafike, atitinaktys kiekvieno tyrimo ryto, pietų ir vakaro
factorssp = [
	"sklv", "sargv", "nosv", "tremv", "vyzdv", "vasov", "dermv", "tempv", "kriv", "pm1+pm4v", "s+dv", "ps1v",
	"sklp", "sargp", "nosp", "tremp", "vyzdp", "vasop", "dermp", "tempp", "krip", "pm1+pm4p", "s+dp", "ps1p",
	"sklr", "sargr", "nosr", "tremr", "vyzdr", "vasor", "dermr", "tempr", "krir", "pm1+pm4r", "s+dr", "ps1r"]

factorskg = [
	"uputv", "usvv", "d2p(4)v", "kphiv", "p4v", "tksiv", "kdv",
	"uputp", "usvp", "d2p(4)p", "kphip", "p4p", "tksip", "kdp",
	"uputr", "usvr", "d2p(4)r", "kphir", "p4r", "tksir", "kdr"]

factorsda = [
	"uputv", "usvv", "dermv", "sphkv", "uphkv", "dtankv",
	"uputp", "usvp", "dermp", "sphkp", "uphkp", "dtankp",
	"uputr", "usvr", "dermr", "sphkr", "uphkr", "dtankr"]

factorsmalac = [
	"p4p1v", "p1v", "sphkv", "uphkv", "kphiv", "tksiv", "kdv",
	"p4p1p", "p1p", "sphkp", "uphkp", "kphip", "tksip", "kdp",
	"p4p1r", "p1r", "sphkr", "uphkr", "kphir", "tksir", "kdr"]

factorsetp = [
	"s-dv", "smdmv", "pm1-pm4v", "pm1+s21v", "pm1-s21v",
	"s-dp", "smdmp", "pm1-pm4p", "pm1+s21p", "pm1-s21p",
	"s-dr", "smdmr", "pm1-pm4r", "pm1+s21r", "pm1-s21r"]

factorsktp = [
	"p4p1v", "dermv", "vyzdv", "sphkv", "uphkv", "kphiv", "tksiv", "kdv",
	"p4p1p", "dermp", "vyzdp", "sphkp", "uphkp", "kphip", "tksip", "kdp",
	"p4p1r", "dermr", "vyzdr", "sphkr", "uphkr", "kphir", "tksir", "kdr"]

factorsralac = [
	"p4p1v", "p1v", "sphkv", "uphkv", "kphiv", "tksiv", "kdv",
	"p4p1p", "p1p", "sphkp", "uphkp", "kphip", "tksip", "kdp",
	"p4p1r", "p1r", "sphkr", "uphkr", "kphir", "tksir", "kdr"]

# skaičiuojam atitinakamų categorical skaičių, kad
# 1) automatiškai grafike nusistatytų ribos tarp ryto, pietų ir vakaro
# 2) tekstas atskiriantis juos
# 3) y categorical axis range'as
countsp = len(factorssp)
countkg = len(factorskg)
countda = len(factorsda)
countmalac = len(factorsmalac)
countetp = len(factorsetp)
countktp = len(factorsktp)
countralac = len(factorsralac)


def heigth_count(h):
	if h < 36:
		h_c = 165 + h * 5
	else:
		h_c = 220 + h * 5
	return h_c


def make_graf(p, pav, count, factor):
	p = figure(x_range=[-5, 5], y_range=FactorRange(factors=factor), height=heigth_count(count), tools="save", toolbar_location="above")
	p.title.text = "<-Katabolizmas|Anabolizmas->"
	p.title.align = "center"
	# p.output_backend = "svg"
	p.text(x=[-4.7], y=[(count - (count - 3) / 3 - 1)], text=["Rytas"], text_font_size='10pt', text_font_style="bold", angle=1.56)
	p.text(x=[-4.7], y=[(count - (count - 3) / 3 * 2 - 2)], text=["Pietūs"], text_font_size='10pt', text_font_style="bold", angle=1.56)
	p.text(x=[-4.7], y=[(count - count)], text=["Vakaras"], text_font_size='10pt', text_font_style="bold", angle=1.56)
	p.x_range.bounds = 'auto'
	p.y_range.bounds = 'auto'
	p.xaxis.axis_label = pav
	p.yaxis.visible = False
	p.xaxis.ticker = FixedTicker(ticks=[-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5])
	p.xaxis.major_label_overrides = {-3.5: "Didelis", -2.5: "Vidutinis", -1.5: "Mažas", -0.5: "Norma", 0.5: "Norma", 1.5: "Mažas", 2.5: "Vidutinis", 3.5: "Didelis"}
	p.xaxis.major_tick_line_color = None
	# p.output_backend = "svg"

	p.add_layout(Span(location=0, dimension='height', line_color='black', line_dash='solid', line_width=4))
	p.add_layout(Span(location=1, dimension='height', line_color='green', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=-1, dimension='height', line_color='green', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=2, dimension='height', line_color='orange', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=-2, dimension='height', line_color='orange', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=3, dimension='height', line_color='red', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=-3, dimension='height', line_color='red', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=4, dimension='height', line_color='darkred', line_dash='dashed', line_width=4))
	p.add_layout(Span(location=-4, dimension='height', line_color='darkred', line_dash='dashed', line_width=4))
	p.add_layout(BoxAnnotation(top=(count - 3) / 3 + 1, fill_alpha=0.1, fill_color='black'))
	p.add_layout(BoxAnnotation(bottom=(count - 3) / 3 + 1, top=(count - 3) / 3 * 2 + 2, fill_alpha=0.1, fill_color='cyan'))
	p.add_layout(BoxAnnotation(top=count, fill_alpha=0.1, fill_color='yellow'))
	return p
