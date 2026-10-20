"""Sector and country attribution for AI-conference sponsors (organisation level)."""

FIN = set("""Two Sigma|D. E. Shaw|Citadel|Point72 / Cubist|PDT Partners|Bloomberg|Hudson River Trading|Jump Trading|Jane Street|Capital One|
G-Research|Squarepoint|XTX Markets|RBC|Voleon|Optiver|WorldQuant|Susquehanna (SIG)|Morgan Stanley|Tower Research|JPMorgan Chase|IMC|ADIA|DRW|
Eqvilent|Man Group|Winton|AIG|Commonwealth Bank|Qube RT|JoinQuant|TD Bank|Virtu|Vatic Labs|Edgestream|WizardQuant|BlackRock|Trexquant|
Renaissance Technologies|Rosetta Analytics|GSA Capital|Flow Traders|Ketchum Trading|NatWest|Minghong Investment|HSBC|AXQ Capital|Ansatz Capital|
Balyasny Asset Management|Capital Fund Management|Capital Group|Credit Suisse|Crédit Agricole|EG Manager UK|GBM|Hutchin Hill Capital|JQ Investments|
Longqi Scientific Investments|Manteio Capital|Nubank|Quadrature|Robinhood|Tibra Global Services Pty|Tudor Investment|U.S. Bank National Association|
Voloridge Investment Management|Wells Fargo|Westbourne Partners|Temasek|Ramp|Adyen|Stripe|Wecash Holding Limited Company|Khosla Ventures|DCVC|
Data Collective|Flagship Pioneering|IMG Investset""".replace('\n', '').split('|'))

PUB = set("""Springer Nature|MIT Press|Cambridge University Press|now publishers|Science Partner Journals|AI Journal (AIJ)|Frontiers|MDPI|
IOP Publishing|Princeton University Press|KeAi Publishing""".replace('\n', '').split('|'))

NONIND = set("""NSF|AFOSR|NSA|National Reconnaissance Office|Lab41 (In-Q-Tel)|Inria|CNRS|Université de Lille|Métropole Européenne de Lille|
Région Nord-Pas de Calais|EuraTechnologies|CRIStAL|Paris Region Entreprises|Hi! Paris|PR[AI]RIE|Mila|Vector Institute|IVADO|NextAI|
Montréal International|Talent Montréal|MBZUAI|KAUST|KAIST|BAAI|Shanghai AI Lab|Zhongguancun Academy|Beijing Institute of Big Data Research|
The Chinese University of Hong Kong, Shenzhen|PolyU Academy for Artificial Intelligence|Chen Institute|XPRIZE|Future of Life Institute|ELLIS|
Imperial College London|The Alan Turing Institute|Swiss Data Science Center|INSAIT|Smart Nation Singapore|INFOCOMM Media Development Authority|
Mayo Clinic|Research in Germany|Wadhwani AI|Black in AI|ACM|CRA|SIAM|IEEE SA|Knight Foundation|Chan Zuckerberg Initiative|Renaissance Philanthropy|
Arc Institute|Biohub|Basis|LawZero|METR|MATS|Electric Power Research Institute|Cloud Native Computing Foundation/PyTorch Foundation|
Simon Fraser University|The Regents of the University of California, San Diego/ NSF-ACCESS|IARAI|Institute of Advanced Research in Artificial Intelligence|
42|INSTITUTO KUNUMI|Grameen Research""".replace('\n', '').split('|'))

def sector(o):
    if o in FIN: return 'Finance / quant'
    if o in PUB: return 'Publisher'
    if o in NONIND: return 'Government / academic / non-profit'
    return 'Tech & other industry'

def _m(code, names):
    return {n: code for n in names.replace('\n', '').split('|')}

COUNTRY = {}
for code, names in [
 ('CN', """Baidu|ByteDance|Alibaba|Ant Group|Tencent|Huawei|Meituan|DiDi|Kuaishou|JoinQuant|WizardQuant|Minghong Investment|Inspur|Zhipu|JD.com|
Unitree|Booster Robotics|DataOcean AI|Shanghai AI Lab|BAAI|Linkerbot Beijing Technology|Moqi Technology (Beijing)|Beijing Institute of Big Data Research|
NetEase Fuxi Lab|Xiaomi|rednote|SenseTime Group|Horizon Robotics|Happy Elements|Zhongguancun Academy|Wecash Holding Limited Company|Squirrel AI Learning|
Longqi Scientific Investments|Datatang Technology|Nexdata|Cheetah Mobile America|The Chinese University of Hong Kong, Shenzhen|Graviti Technologies|maadaa.ai|
KeAi Publishing|Lenovo|Qihoo 360|PolyU Academy for Artificial Intelligence|JQ Investments|Qifei International Development Co."""),
 ('GB', """G-Research|XTX Markets|Man Group|Winton|Squarepoint|GSA Capital|Quadrature|BenevolentAI|Invenia Labs|Secondmind|Wayve|causaLens|Encord|V7|
Prolific|Boltzbit|NatWest|HSBC|AstraZeneca|GSK|Imperial College London|The Alan Turing Institute|Cambridge University Press|Relation Therapeutics|
EG Manager UK|ElevenLabs|Westbourne Partners|Qube RT|IOP Publishing|SonicJobs|Arm|Graphcore|McKinsey (QuantumBlack)|Credit Suisse"""),
 ('FR', """Criteo|Mistral AI|Owkin|Capital Fund Management|Crédit Agricole|Inria|CNRS|Université de Lille|
Métropole Européenne de Lille|Région Nord-Pas de Calais|EuraTechnologies|MFG Labs|Numberly|CRIStAL|Technicolor|Paris Region Entreprises|Capgemini|
Lithosquare|Humanis|Hi! Paris|PR[AI]RIE|Probabl|Bioptimus|42|White Circle"""),
 ('DE', """Springer Nature|Bosch|SAP|Siemens|Audi|Zalando|Automotive Safety Technologies|Celonis|Pupil Labs|Research in Germany|ELLIS|Aleph Alpha|Prior Labs|Pruna AI|
Avira|Twenty Billion Neurons|ai-coustics"""),
 ('NL', "Optiver|IMC|Booking.com|Flow Traders|Adyen|Zeta Alpha|Nebius|Toloka"),
 ('CH', "Rapidata|Swiss Data Science Center|Lightly|QuantCo|Credit Suisse"),
 ('RU', "Yandex|Sber|OOO Sentium"),
 ('JP', """Toyota|Sony|Panasonic|NEC|Yokogawa|Preferred Networks|Hitachi|NTT|Bridgestone|Recruit Communications|Cogent Labs|GHELIA|Ascent Robotics|Atmanity"""),
 ('KR', """Samsung|LG|NAVER|SK Group|AITRICS|FriendliAI|Nota AI|SqueezeBits|HyperAccel|FuriosaAI|VESSL AI|RLWRLD|TESOLLO|KAIST|Datumo"""),
 ('CA', """Element AI|RBC|TD Bank|Maluuba|Mila|Vector Institute|IVADO|Imagia|NextAI|Sportlogiq|Montréal International|Talent Montréal|Shopify|Cohere|
Deep Genomics|Stradigi AI|Sanctuary AI|TELUS Digital|Simon Fraser University|Boson AI|xBrain"""),
 ('AE', "MBZUAI|ADIA|Inception Institute of AI"),
 ('SA', "KAUST"),
 ('SG', "Sea|HPC-AI Tech|Smart Nation Singapore|INFOCOMM Media Development Authority|Temasek|UNIPATAI|Ahrefs"),
 ('AU', "Commonwealth Bank|Tibra Global Services Pty|Canva|Neara|Appen|Atlassian"),
 ('IN', "Wadhwani AI|Firstsource"),
 ('IL', "Deci|Alice (formerly ActiveFence)"),
 ('VN', "VinAI|VINTECH Technology Development Joint Stock Company"),
 ('TH', "Typhoon l SCB 10X"),
 ('BR', "Nubank|INSTITUTO KUNUMI"),
 ('MX', "GBM"),
 ('BG', "INSAIT"),
 ('IT', "Translated"),
 ('SE', "Peltarion"),
 ('NO', "Schibsted Media Group|Iris.ai"),
 ('FI', "Nokia"),
 ('IE', "ACCENTURE"),
 ('ES', "Telefonca I+D"),
 ('AT', "Emmi AI|NXAI|IARAI|Institute of Advanced Research in Artificial Intelligence"),
 ('BE', "imec AI labs | imec France"),
 ('ZA', "Naspers"),
 ('CZ', "JetBrains"),
 ('??', "Eqvilent|Abaka AI|TerraQuanta|Tynapse|Quadrillion|SSFAM|Karavela|Seven Research|Silicon Dreams|Conway|Sherlock Robotics|Cantina Labs|Lighthouse|Rora|AtlaSense|Taste Labs|Vetto|Fundamental Technologies|SoTALab|Xyla|Astrus|Theremia|Sovrano AI|Goaly AI|Miso Labs|Mirage|Meter|hillclimb|Tynapse|Embo|DVC|SCAI|ACTAVA|Humanis|Cogs & Marvel"),
]:
    COUNTRY.update(_m(code, names))

PARENT = {'Mercedes-Benz Research and Development North America': 'DE', 'Cheetah Mobile America': 'CN', 'Samsung': 'KR',
          'imec AI labs | imec France': 'BE', 'Siemens': 'DE', 'Audi': 'DE'}
HQ_OVERRIDE = {'Mercedes-Benz Research and Development North America': 'US', 'Audi': 'DE'}

def country(o):
    return COUNTRY.get(o, 'US')

def parent_country(o):
    return PARENT.get(o, country(o))
