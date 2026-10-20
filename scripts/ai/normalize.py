"""Normalise raw AI-conference sponsor names to organisations (parent-group level,
same convention as the HCI data: Google DeepMind -> Google, Facebook -> Meta/Facebook)."""
import re, html

SUFFIX = re.compile(r'(,?\s+(inc\.?|inc|llc\.?|l\.?l\.?c\.?|ltd\.?|limited|corp\.?|corporation|co\.,?\s*ltd\.?|lp|l\.p\.?|llp|gmbh|se|srl|plc|ulc|pte\.? ltd\.?|sp\. z o\.o\.))+\s*$', re.I)

# exact (case-insensitive) prefix rules: first match wins -> canonical org
RULES = [
    (r'^(google|deepmind|kaggle|waymo)', None),  # handled below (Waymo kept separate)
]
ALIAS = {
 # big tech
 'google': 'Google', 'google ai': 'Google', 'google research': 'Google', 'google research dei': 'Google', 'google deepmind': 'Google',
 'deepmind': 'Google', 'deepmind dei': 'Google', 'deepmind technologies': 'Google', 'google x, the moonshot factory': 'Google', 'kaggle': 'Google',
 'google, inc.': 'Google', 'google, inc': 'Google',
 'facebook': 'Meta/Facebook', 'facebook ai': 'Meta/Facebook', 'meta': 'Meta/Facebook', 'meta ai': 'Meta/Facebook', 'meta platforms': 'Meta/Facebook',
 'microsoft': 'Microsoft', 'microsoft research': 'Microsoft', 'microsoft research maluuba': 'Microsoft', 'linkedin': 'Microsoft',
 'maluuba': 'Maluuba', 'amazon': 'Amazon', 'amazon science': 'Amazon', 'amazon.com': 'Amazon',
 'apple': 'Apple', 'apple - leader level': 'Apple', 'apple inc. dei': 'Apple', 'apple inc.': 'Apple',
 'ibm': 'IBM', 'ibm research': 'IBM', 'ibm research ai': 'IBM',
 'intel': 'Intel', 'intel ai': 'Intel', 'intel corporate': 'Intel', 'intel nervana': 'Intel', 'habana labs': 'Intel', 'habana  labs': 'Intel',
 'nvidia': 'NVIDIA', 'qualcomm': 'Qualcomm', 'qualcomm ai research': 'Qualcomm',
 'amd (advance micro devices, inc)': 'AMD', 'advanced micro devices': 'AMD', 'advanced micro devices (amd)': 'AMD', 'xilinx': 'AMD',
 'arm': 'Arm', 'oracle': 'Oracle', 'oracle labs': 'Oracle', 'salesforce': 'Salesforce', 'adobe': 'Adobe', 'adobe research': 'Adobe', 'adobe systems': 'Adobe',
 'netflix': 'Netflix', 'netflix research': 'Netflix', 'uber': 'Uber', 'uber ai solutions': 'Uber', 'uber technologies': 'Uber',
 'twitter': 'Twitter', 'yahoo labs': 'Yahoo', 'yahoo research': 'Yahoo', 'yahoo!': 'Yahoo', 'cisco': 'Cisco', 'cisco systems': 'Cisco',
 'sap': 'SAP', 'sas': 'SAS', 'sas institute': 'SAS', 'snowflake': 'Snowflake', 'snowflake computing canada': 'Snowflake', 'snowflake poland': 'Snowflake',
 'sony': 'Sony', 'sony ai': 'Sony', 'sony ai dei fund': 'Sony', 'sony group': 'Sony',
 'samsung': 'Samsung', 'samsung electronics': 'Samsung', 'samsung sail montreal': 'Samsung', 'samsung - sait ai lab, montreal': 'Samsung',
 'bosch': 'Bosch', 'bosch ai': 'Bosch', 'bosch center for artificial intelligence': 'Bosch', 'bosch rtc': 'Bosch', 'robert bosch': 'Bosch',
 'toyota': 'Toyota', 'toyota research institute': 'Toyota', 'toyota research institute of north america': 'Toyota', 'woven by toyota': 'Toyota',
 'panasonic': 'Panasonic', 'nec': 'NEC', 'nec laboratories': 'NEC', 'nec laboratories america': 'NEC',
 'huawei': 'Huawei', 'huawei technologies': 'Huawei', "noah's ark labs, huawei technologies": 'Huawei',
 'baidu': 'Baidu', 'baidu research': 'Baidu', 'baidu usa': 'Baidu', 'beijing baidu netcom science technology': 'Baidu',
 'alibaba': 'Alibaba', 'alibaba cloud': 'Alibaba', 'alibaba group': 'Alibaba', 'alibaba (china)': 'Alibaba', 'taobao (china) software': 'Alibaba',
 'taobao and tmall group': 'Alibaba', 'ant financial': 'Ant Group', 'ant group': 'Ant Group', 'ant research': 'Ant Group', 'alipay us': 'Ant Group',
 'tencent': 'Tencent', 'tencent ai lab': 'Tencent', 'tencent arc lab': 'Tencent',
 'bytedance': 'ByteDance', 'tiktok': 'ByteDance', 'jd.com': 'JD.com', 'beijing jingdong shangke information technology': 'JD.com',
 'didi': 'DiDi', 'didi chuxing': 'DiDi', 'kuaishou': 'Kuaishou', 'meituan': 'Meituan', 'naver': 'NAVER', 'naver corp.': 'NAVER', 'naver labs': 'NAVER',
 'naver labs europe': 'NAVER', 'naver | line': 'NAVER', 'naver│line': 'NAVER', 'lg ai research': 'LG', 'sk telecom': 'SK Group', 'sk hynix': 'SK Group',
 'yandex': 'Yandex', 'llc yandex': 'Yandex', 'sberbank': 'Sber', 'sber ai': 'Sber', 'sberbank ai': 'Sber', 'sberbank of russia': 'Sber',
 'inspur electronic information industry': 'Inspur', 'sea': 'Sea', 'sea ai lab': 'Sea', 'sea limited': 'Sea',
 'yokogawa digital': 'Yokogawa', 'yokogawa electric': 'Yokogawa', 'expedia': 'Expedia', 'expedia group': 'Expedia',
 'ebay': 'eBay', 'zalando': 'Zalando', 'zillow': 'Zillow', 'zillow group': 'Zillow', 'audi': 'Audi', 'audi of america': 'Audi',
 'kla -tencor': 'KLA', 'kla-tencor': 'KLA', 'western digital': 'Western Digital', 'shopify': 'Shopify', 'figma': 'Figma',
 'atlassian': 'Atlassian', 'atlassian us': 'Atlassian', 'cognizant': 'Cognizant', 'cognizant ai labs': 'Cognizant', 'cognizant al lab': 'Cognizant',
 'lambda': 'Lambda', 'lambda labs': 'Lambda', 'lambda gpu workstations & servers': 'Lambda',
 'cerebras systems': 'Cerebras', 'sambanova': 'SambaNova', 'sambanova systems': 'SambaNova', 'graphcore': 'Graphcore',
 'together': 'Together AI', 'together ai': 'Together AI', 'nebius': 'Nebius', 'nebius ai': 'Nebius', 'runpod': 'RunPod',
 'scale ai': 'Scale AI', 'toloka': 'Toloka', 'toloka ai': 'Toloka', 'superannotate': 'SuperAnnotate', 'superannotate ai': 'SuperAnnotate',
 'weights & biases': 'Weights & Biases', 'weights and biases': 'Weights & Biases', 'comet': 'Comet', 'comet ml': 'Comet',
 'cocalc': 'CoCalc', 'cocalc by sagemath': 'CoCalc', 'sigopt': 'SigOpt', 'petuum': 'Petuum', 'fedml': 'FedML',
 'friendliai': 'FriendliAI', 'cartesia': 'Cartesia', 'cartesia ai': 'Cartesia', 'abridge': 'Abridge', 'abridge ai': 'Abridge', 'absci': 'Absci',
 'aitrics': 'AITRICS', 'hpc-ai technology': 'HPC-AI Tech', 'hpc-ai.com': 'HPC-AI Tech', 'colossal-ai': 'HPC-AI Tech',
 'akash network': 'Akash Network', 'akash network by overclock labs': 'Akash Network', 'bagel': 'Bagel', 'bagel labs': 'Bagel',
 'crusoe cloud': 'Crusoe', 'crusoe energy': 'Crusoe', 'exa': 'Exa', 'exa labs': 'Exa', 'writer': 'Writer', 'liquid': 'Liquid AI', 'liquid ai': 'Liquid AI',
 'openai': 'OpenAI', 'openai, l.p': 'OpenAI', 'boltzbit': 'Boltzbit', 'booster robotics': 'Booster Robotics', 'booster robotics technology': 'Booster Robotics',
 'unitree robotics': 'Unitree', 'unitree robotics/yushu technology': 'Unitree', 'dataoceanai': 'DataOcean AI', 'dataocean ai': 'DataOcean AI',
 'deep genomics': 'Deep Genomics', 'insilico medicine': 'Insilico Medicine', 'recursion': 'Recursion', 'recursion pharmaceuticals': 'Recursion',
 'ouster': 'Ouster', 'element ai': 'Element AI', 'borealis ai': 'RBC', 'rbc borealis': 'RBC', 'rbc': 'RBC',
 'td bank / layer 6': 'TD Bank', 'td bank group - layer6 ai': 'TD Bank', 'commonwealth bank': 'Commonwealth Bank', 'commonwealth bank of australia': 'Commonwealth Bank',
 'quantumblack': 'McKinsey (QuantumBlack)', 'quantumblack, ai by mckinsey': 'McKinsey (QuantumBlack)',
 'cylance': 'Cylance', 'blackberry cylance': 'Cylance', 'doc.ai': 'doc.ai', 'lab41': 'Lab41 (In-Q-Tel)', 'lab41, an in-q-tel lab': 'Lab41 (In-Q-Tel)',
 'wave computing': 'Wave Computing', 'helm.ai': 'Helm.ai', 'neural magic': 'Neural Magic', 'mosaicml': 'Databricks', 'databricks': 'Databricks',
 'nextai': 'NextAI', 'nextai / next canada': 'NextAI', 'ivado': 'IVADO', 'ivado labs': 'IVADO', 'imagia': 'Imagia',
 'thomson reuters': 'Thomson Reuters', 'thomson reuters labs': 'Thomson Reuters', 'united technologies research center': 'UTRC (RTX)',
 'united technologies research centre ireland': 'UTRC (RTX)', 'xerox research centre europe': 'Xerox', 'siemens medical solutions usa': 'Siemens',
 'ralph': 'Ralph', 'ralph dei': 'Ralph', 'vinai research': 'VinAI', 'wadhwani institute for artificial intelligence': 'Wadhwani AI',
 'mistral ai': 'Mistral AI', 'cohere': 'Cohere', 'anthropic': 'Anthropic', 'handshake ai': 'Handshake', 'turing': 'Turing', 'revelo': 'Revelo',
 'appen': 'Appen', 'encord': 'Encord', 'datologyai': 'DatologyAI', 'modal': 'Modal', 'baseten': 'Baseten', 'lightning ai': 'Lightning AI',
 'translated': 'Translated', 'mathworks': 'MathWorks', 'servicenow': 'ServiceNow', 'invenia labs': 'Invenia Labs', 'benevolentai': 'BenevolentAI',
 'preferred networks': 'Preferred Networks', 'pryon': 'Pryon', 'determined ai': 'Determined AI', 'alegion': 'Alegion', 'abaka ai': 'Abaka AI',
 'voxel51': 'Voxel51', 'virtue ai': 'Virtue AI', 'simular': 'Simular', 'obsidian security': 'Obsidian Security', 'mats research': 'MATS',
 'astrazeneca': 'AstraZeneca', 'novartis': 'Novartis', 'gsk.ai': 'GSK', 'johnson & johnson': 'Johnson & Johnson',
 'tesla': 'Tesla', 'cruise': 'Cruise (GM)', 'general motors': 'Cruise (GM)', 'lyft': 'Lyft', 'wayve': 'Wayve', 'waymo': 'Waymo',
 'spotify': 'Spotify', 'wayfair': 'Wayfair', 'snap': 'Snap', 'roblox': 'Roblox', 'unity technologies': 'Unity', 'disney research': 'Disney',
 'intuit': 'Intuit', 'airbnb': 'Airbnb', 'duolingo': 'Duolingo', 'canva': 'Canva', 'datadog': 'Datadog', 'groq': 'Groq', 'imbue': 'Imbue',
 # finance / quant
 'the d. e. shaw group': 'D. E. Shaw', 'the d. e. shaw group dei': 'D. E. Shaw', 'd. e. shaw': 'D. E. Shaw', 'd. e. shaw & co.': 'D. E. Shaw',
 'd. e. shaw research': 'D. E. Shaw', 'd. e. shaw group': 'D. E. Shaw',
 'two sigma': 'Two Sigma', 'two sigma dei': 'Two Sigma', 'two sigma investments': 'Two Sigma',
 'citadel': 'Citadel', 'citadel & citadel securities': 'Citadel', 'citadel and citadel securities': 'Citadel', 'citadel | citadel securities': 'Citadel',
 'citadel|citadel securities': 'Citadel', 'citadel enterprise americas lls': 'Citadel',
 'point72': 'Point72 / Cubist', 'point72 / cubist systematic strategies': 'Point72 / Cubist', 'cubist systematic strategies': 'Point72 / Cubist',
 'hudson river trading': 'Hudson River Trading', 'jane street': 'Jane Street', 'jump trading': 'Jump Trading', 'pdt partners': 'PDT Partners',
 'g-research': 'G-Research', 'g research': 'G-Research', 'drw': 'DRW', 'drw trading group': 'DRW', 'imc': 'IMC', 'imc trading': 'IMC',
 'optiver': 'Optiver', 'xtx markets': 'XTX Markets', 'xtx markets technologies': 'XTX Markets', 'squarepoint': 'Squarepoint',
 'squarepoint capital': 'Squarepoint', 'squarepoint-capital': 'Squarepoint', 'susquehanna': 'Susquehanna (SIG)', 'susquehanna international group': 'Susquehanna (SIG)',
 'tower research capital': 'Tower Research', 'man ahl': 'Man Group', 'the voleon group': 'Voleon', 'voleon': 'Voleon',
 'winton': 'Winton', 'winton capital': 'Winton', 'winton capital management': 'Winton', 'winton group': 'Winton',
 'qube research & technologies': 'Qube RT', 'qube research and technologies': 'Qube RT', 'worldquant': 'WorldQuant',
 'renaissance technologies': 'Renaissance Technologies', 'edgestream partners': 'Edgestream', 'gsa capital': 'GSA Capital', 'gsa capital services': 'GSA Capital',
 'eqvilent': 'Eqvilent', 'vatic labs': 'Vatic Labs', 'virtu financial': 'Virtu', 'trexquant investment': 'Trexquant', 'quadrature capital': 'Quadrature',
 'joinquant': 'JoinQuant', '北京聚宽投资管理有限公司（北京joinquant投资管理有限公司）': 'JoinQuant', 'wizardquant': 'WizardQuant', '宽德投资wizardquant': 'WizardQuant',
 '上海明汯投资管理有限公司': 'Minghong Investment', '明汯投资 minghong investment': 'Minghong Investment',
 'bloomberg': 'Bloomberg', 'bloomberg engineering': 'Bloomberg', 'bloomberg l.p.': 'Bloomberg', 'bloomberg lp': 'Bloomberg',
 'capital one': 'Capital One', 'capital one services': 'Capital One', 'j.p. morgan': 'JPMorgan Chase', 'j.p.  morgan': 'JPMorgan Chase',
 'jpmorgan chase & co.': 'JPMorgan Chase', 'jpmorganchase': 'JPMorgan Chase', 'morgan stanley': 'Morgan Stanley',
 'aig': 'AIG', 'aig science': 'AIG', 'american international group (aig)': 'AIG', 'ketchum trading': 'Ketchum Trading',
 'abu dhabi investment authority': 'ADIA', 'abu dhabi investment authority (adia)': 'ADIA', 'abu dhabi investment authority - adia': 'ADIA',
 'rosetta analytics': 'Rosetta Analytics', 'blackrock systematic': 'BlackRock', 'natwest group': 'NatWest',
 # publishers / academia / gov
 'springer': 'Springer Nature', 'springer nature': 'Springer Nature', 'springer publishing': 'Springer Nature',
 'the mit press': 'MIT Press', 'mit press': 'MIT Press', 'now publishers': 'now publishers', 'cambridge university press': 'Cambridge University Press',
 'artificial intelligence journal': 'AI Journal (AIJ)', 'artificial intelligence journal (aij)': 'AI Journal (AIJ)',
 'intelligent computing': 'Science Partner Journals', 'intelligent computing, a science partner journal': 'Science Partner Journals',
 'health data science, a science partner journal': 'Science Partner Journals', 'health science data, a science partner journal': 'Science Partner Journals',
 'research, a science partner journal': 'Science Partner Journals', 'science partner journals': 'Science Partner Journals',
 'siam': 'SIAM', 'society for industrial & applied mathematics': 'SIAM',
 'tianqiao & chrissy chen institute': 'Chen Institute', 'tianqiao and chrissy chen institute': 'Chen Institute',
 'national security agency': 'NSA', 'national security agency (nsa)': 'NSA', 'mila - montréal': 'Mila', 'mila - quebec ai institute': 'Mila',
 'mila - quebec artificial intelligence institut': 'Mila', 'vector institute': 'Vector Institute', 'the vector institute': 'Vector Institute',
 'kaust': 'KAUST', 'kaust ai initiative ai main navigation': 'KAUST', 'king abdullah university of science and technology': 'KAUST', 'visual computing center at kaust': 'KAUST',
 'mbzuai - institute of foundation models': 'MBZUAI', 'mohamed bin zayed university of artificial intelligence': 'MBZUAI',
 'beijing academy of artificial intelligence': 'BAAI', 'beijing academy of artificial intelligence (baai)': 'BAAI',
 'inception institute of artificial intelligence': 'Inception Institute of AI', 'xprize': 'XPRIZE', 'xprize foundation': 'XPRIZE',
 'elllis': 'ELLIS', 'ellis - european laboratory for learning and intelligent systems': 'ELLIS', 'ellis institute tübingen': 'ELLIS',
 'montréal international': 'Montréal International', 'sportlogiq': 'Sportlogiq', 'insait – institute for computer science, ai & technology': 'INSAIT',
 'cogs &amp; marvel': 'Cogs & Marvel', 'cogs & marvel': 'Cogs & Marvel', 'causalens': 'causaLens', 'neptune.ai': 'neptune.ai',
 'nota ai': 'Nota AI', 'secondmind': 'Secondmind', 'prowler.io': 'Secondmind', 'zeta alpha': 'Zeta Alpha', 'feature x': 'FeatureX', 'featurex': 'FeatureX',
 'sentient technologies': 'Sentient Technologies', 'biomind': 'BioMind', 'cirrascale cloud services': 'Cirrascale', 'centific': 'Centific',
 'deccan ai': 'Deccan AI', 'prior labs': 'Prior Labs', 'rapidata': 'Rapidata', 'sieve': 'Sieve', 'afterquery': 'AfterQuery', 'ahrefs': 'Ahrefs',
 'ollama': 'Ollama', 'elevenlabs': 'ElevenLabs', 'waveforms ai': 'WaveForms AI', 'reflection': 'Reflection AI', 'lawzero': 'LawZero',
 'basis research institute': 'Basis', 'biohub': 'Biohub', 'sonicjobs': 'SonicJobs', 'jetbrains': 'JetBrains', 'flow traders': 'Flow Traders',
 'quadrillion': 'Quadrillion', 'quantco': 'QuantCo', 'snorkel ai': 'Snorkel AI', 'sandboxaq': 'SandboxAQ', 'research in germany': 'Research in Germany',
 'mayo clinic center for individualized medicine': 'Mayo Clinic', 'ukri centre ai for healthcare, imperial college london': 'Imperial College London',
 'shanghai artificial intelligence laboratory': 'Shanghai AI Lab', 'hsbc': 'HSBC', 'upwork': 'Upwork', 'inria': 'Inria',
 'association for computing machinery': 'ACM', 'criteo': 'Criteo', 'criteo ai lab': 'Criteo', 'criteo research': 'Criteo', 'criteo reasearch': 'Criteo',
 'brain corporation': 'Brain Corporation', 'qihoo 360': 'Qihoo 360', '360 international development co. ltd.': 'Qihoo 360', 'ascent_robotics': 'Ascent Robotics', 'computing research association': 'CRA', 'black in ai': 'Black in AI',
}

def key(s):
    s = html.unescape(str(s)).strip()
    s = re.sub(r'\s+', ' ', s)
    k = s.lower()
    if k in ALIAS: return k
    k2 = SUFFIX.sub('', s).strip().lower().rstrip(',. ')
    return k2

def norm(s):
    s0 = re.sub(r'\s+', ' ', html.unescape(str(s))).strip()
    k = key(s0)
    if k in ALIAS: return ALIAS[k]
    if s0.lower() in ALIAS: return ALIAS[s0.lower()]
    return SUFFIX.sub('', s0).strip().rstrip(',')

SKIP = {'TBDTBD'}
