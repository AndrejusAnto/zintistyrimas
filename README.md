# Žintis tyrimas
Šis projektas turėtų leisti paprastai suvesti organizmo metabolizmo nukrypimo tyrimo duomenis internetiniame puslapyje ir duoti atsakymą apie organizmo būklę bei kitą informaciją (daugiau zintis.lt arba https://www.facebook.com/zintis.lt/). Puslapyje turėtų būti nurodyta visa tyrimo eiga ir prie tų žingsnių, kurie reikalauja duomenų, turėtų būti laukeliai (šiuo atveju Bokeh TextInput), į kuriuos suvedus duomenis, automatiškai grafikuose atsispindėtų organimzo nukrypimai ir (galbūt), pateiktos visos reikiamos išvados be žmogaus įsikišimo.  
Paleidimas (komandinė eilutė): bokeh serve --show main1.py. Turi atsidaryti naršyklės langas ir reikia kantriai palaukti.
Projektas yra workable stadijoje, bet reikia kelių dalykų (multiline textinput ir headless chrome pakeitimo vietoj phantomjs, kad būtų galima grafius paversti į paveiksliukus ir po to įdėti į pdf), kad būtų galima naudoti.

ls main*.py | entr -p -r -s "bokeh serve --show main1.py"
![Alt Text](https://github.com/AndrejusAnto/zintistyrimas/blob/master/demo.gif)
