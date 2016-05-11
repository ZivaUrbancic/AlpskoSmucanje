import re
import orodja
tekme=[]
tekmovalci=[]
vse=[]

def grange(st, ime):
    rec=0
    ImamZadetke=True
    #global tekme
    while ImamZadetke:
        orodja.shrani('http://data.fis-ski.com/dynamic/athlete-biography.html?sector=AL&listid=&competitorid={}&type=result&category=WC&rec_start={}&limit=100'.format(st,rec), 'zajete-strani/{}{}.html'.format(ime,rec))
        if rec == 0:
            rezultat = re.search(r'Skis:.*?>[^>]*>(?P<smuci>[^<]*)', orodja.vsebina_datoteke('zajete-strani/{}{}.html'.format(ime,rec)))
            rez=re.search(r'Nation:.*\n\W*.*?>.*?>.*?>.*?>(?P<drzava>.+?)<.span>', orodja.vsebina_datoteke('zajete-strani/{}{}.html'.format(ime,rec)))
            if rezultat is None:
                ski='Ni_podatka'
            else:
                ski = rezultat.group('smuci')
            tekmovalci.append({'id':st, 'ime':ime, 'drzava': rez.group('drzava'), 'smuci': ski})

        tekma = re.compile(
            #r'<tr><td class=.i[01].>(?P<datum>.*?)&nbsp;<.td>'
            r'<tr><td class=.i[01].>(?P<datum>.*?)&nbsp;<.td>\n<td class=.i[01].><a href=.+?>(?P<kraj>.+?)<.a><.td>\n.*\n.*\n.*?>(?P<disciplina>.+?)&.*\n<td class.*?>(?P<uvrstitev>.+?)&nbsp;<.td>\n<td .+?>'
        )
    
        for vnos in re.finditer(tekma, orodja.vsebina_datoteke('zajete-strani/{}{}.html'.format(ime,rec))):
            datum='{}'.format(vnos.group('datum'))
            kraj='{}'.format(vnos.group('kraj'))
            disciplina='{}'.format(vnos.group('disciplina'))
            mesto='{}'.format(vnos.group('uvrstitev'))
            tekme.append({'datum': datum, 'kraj': kraj, 'mesto': mesto, 'disciplina': disciplina})
            vse.append({'datum': datum, 'kraj': kraj, 'mesto': mesto, 'disciplina': disciplina, 'id': st})

        #print (rec)
        rec+=100
        ImamZadetke=(len (tekme) == rec)
        #print (ImamZadetke, len (tekme))
    orodja.zapisi_tabelo(tekme,['datum', 'kraj', 'disciplina', 'mesto'], 'csv-datoteke/{}.csv'.format(ime))
    #print ("Zajel sem stran in naredil csv za {}".format(ime))



#zajemi_flisar()

def zajemi_url():
    global tekme
    orodja.shrani('http://www.fis-ski.com/alpine-skiing/athletes/', 'zajete-strani/sportniki.html')
    #print("Zajemam ulr ... ")
    url = re.compile(
        r'<a href=..alpine-skiing.athletes\D+(?P<id>\d+).. alt=.(?P<ime>[\w| |-]+)'
    )

    smucarji = []
 
    for vnos in re.finditer(url, orodja.vsebina_datoteke('zajete-strani/sportniki.html')):
        st='{}'.format(vnos.group('id'))
        ime='{}'.format(vnos.group('ime'))
        #print (ime, st)
        #print ('1')
        smucarji.append({'id': st, 'ime': ime})
        tekme=[]
        grange(st, ime) #zajame podatke za posameznega smučarja
    #orodja.zapisi_tabelo(smucarji,['id', 'ime'], 'csv-datoteke/smucarji.csv')

    orodja.zapisi_tabelo(tekmovalci, ['id', 'ime', 'drzava', 'smuci'], 'csv-datoteke/smucarji.csv')

zajemi_url()
orodja.zapisi_tabelo(vse, ['id','datum', 'kraj', 'disciplina', 'mesto'], 'csv-datoteke/vse.csv')




