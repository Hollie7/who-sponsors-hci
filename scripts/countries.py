C = {}
def put(cc, names):
    for n in names: C[n] = cc
put('CA',['GRAND NCE','Simon Fraser University','University of Toronto','SAT (Société des arts technologiques)','Nureva','Tactual Labs','Thalmic Labs','Flybits','SMART Technologies','Chatham Labs','Nortel/BNR','TekGear'])
put('GB',['University of Glasgow','SICSA','VisitScotland','Newcastle University','UCL','University of Cambridge','EPSRC','Wellcome Trust','Emteq'])
put('DE',['SAP','Siemens','Bosch','Deutsche Telekom','Stabilo','Ubimax','Hasso Plattner Institute','Springer'])
put('FR',['JCDecaux','Inria','Digiteo','Région Île-de-France','Telecom ParisTech','Université Paris-Dauphine','Technicolor'])
put('US',['Nokia Bell Labs'])
put('FI',['Nokia','TSV (Technology Industries of Finland Centennial Foundation)','City of Espoo','MultiTouch Ltd'])
put('NO',['MediaFutures (UiB)']); put('DK',['University of Copenhagen DIKU','IT University of Copenhagen'])
put('NL',['Philips','Elsevier']); put('SE',['Spotify']); put('ES',['Telefonica']); put('IT',['University of Bari']); put('CH',['Frontiers'])
put('JP',['Canon','Ricoh','Sony CSL','Recruit','NTT','NTT Docomo','KDDI','Rakuten','Panasonic','NEC','Kyocera','Mercari','LY Corporation','Yahoo Japan',
 'CyberAgent','H2L','Fairy Devices','OMRON SINIC X','NICT','Science Council of Japan','City of Yokohama','Kayamori Foundation','Language Grid','Innolab (Japan)',
 'UX-XU','JINS','Wacom','IPSJ','Kansai METI','MIC Kinki Bureau of Telecommunications','Telecom Engineering Center Kinki','TAF (Telecommunications Advancement Foundation)',
 'SCAT','Osaka Convention & Tourism Bureau','CKP (Ubiquitous Forum)','Human Interface Society','VRSJ','ZAI'])
put('KR',['Samsung','Samsung Art and Design Institute','Naver','Kakao','LG','Hyundai','SK Planet','GolfZon','FuturePlay','H9Works','KIPFA','Yonsei University',
 'Yonsei University ICS','Seoul Metropolitan Government','Korea Tourism Organization','ETRI','Busan Tourism Organization','Dong-eui University','JD Lab'])
put('CN',['Alibaba','Baidu','Huawei','Makeblock']); put('TW',['CyberLink','Perfect Corp']); put('SG',['Singapore Tourism Board'])
put('AU',['Monash University','CSIRO Data61','Commonwealth Bank of Australia']); put('AE',['MBZUAI']); put('IN',['Infosys'])
put('EU',['User-Centric Networking (EU project)'])
put('EU',['ERMES','Holden'])
put('FI',['GreenSense'])
put('DE',['Bergsonne Labs'])
put('',['Sustain','One Ring','SparQi Lab','SCI','Eventburn','Marvin','Rent-a-Computer'])
# added with DIS / IUI / FAccT
put('DE',['Gesellschaft für Informatik (GI)','RC Trust']); put('CY',['University of Cyprus','Cyprus Tourism Organisation'])
put('JP',['DAYPLA','LIFULL','Sony']); put('CN',['Ruyi.ai']); put('FI',['Silo AI']); put('CH',['MDPI']); put('FR',['Michelin'])
put('KR',['LG']); put('CA',['Vector Institute','Tourisme Montréal']); put('GB',['Holistic AI','Luminate'])
put('GR',['Archimedes (Athena RC)','Athena Research Center']); put('SG',['TikTok','Grab','Singapore Exhibition & Convention Bureau','NUS Division of Industrial Design'])
put('AU',['Business Events Sydney','Roames (Fugro)','HFESA','Brisbane BMW','Go Digi (Australia Post)','Greater Springfield','Australian Design Alliance','ANAT',
          'Media Architecture Biennale','Airtrain','Visit Brisbane','Queensland University of Technology','Deakin University'])
put('AT',['Media Architecture Institute']); put('PT',['Funchal City Council','Visit Madeira','ITI / LARSyS'])
def country(o): return C.get(o, 'US')

PARENT = {'TikTok':'CN','Roames (Fugro)':'NL','Toyota Research Institute':'JP','FXPAL':'JP','MERL':'JP','Megagon Labs':'JP','Nokia Bell Labs':'FI'}
def parent_country(o): return PARENT.get(o, country(o))
