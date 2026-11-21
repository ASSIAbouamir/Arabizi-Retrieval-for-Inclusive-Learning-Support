"""Générateur de corpus éducatif et de requêtes de référence (Moroccan, Algerian, Tunisian).
Couvre 30 concepts scientifiques dans 6 disciplines, avec segmentation documentée.
Génère 100 items (34 MA, 33 DZ, 33 TN) soit 300 requêtes annotées (Arabizi, Mixte, Français).
"""

import csv
import json
import os

CONCEPTS = [
    # Physique (6)
    {
        "id": "pression_atm",
        "domain": "physique",
        "title_fr": "Pression atmosphérique",
        "title_ar": "الضغط الجوي",
        "text_fr_1": "La pression atmosphérique est la force exercée par l'air de l'atmosphère sur une unité de surface de la Terre. Au niveau de la mer, sa valeur moyenne normale est d'environ 1013 hPa ou 1 atmosphère. Elle se mesure avec un baromètre à mercure ou électronique. Lorsque l'altitude augmente, la colonne d'air au-dessus diminue, ce qui entraîne une baisse de la pression atmosphérique.",
        "text_fr_2": "La variation de pression atmosphérique influence la météo : les hautes pressions (anticyclones) apportent généralement un temps sec et ensoleillé, tandis que les basses pressions (dépressions) amènent du vent et des précipitations. Elle affecte aussi la température d'ébullition des liquides, qui bout à une température inférieure au sommet d'une montagne.",
        "text_ar_1": "الضغط الجوي هو القوة التي يؤثر بها وزن عمود الهواء في الغلاف الجوي على وحدة المساحة من سطح الأرض. عند مستوى سطح البحر، تبلغ القيمة القياسية للضغط الجوي حوالي 1013 هكتوباسكال أو 1 ضغط جوي. يقاس الضغط الجوي باستخدام جهاز البارومتر. كلما ارتفعنا عن سطح البحر، يقل الضغط الجوي بسبب نقص كتلة الهواء فوقنا.",
        "text_ar_2": "تؤثر تغيرات الضغط الجوي مباشرة على حالة الطقس والمناخ. فالمناطق ذات الضغط الجوي المرتفع ترتبط عادة بطقس مستقر وصافٍ، بينما تتسبب المنخفضات الجوية في هبوب الرياح وتشكل السحب وهطول الأمطار. كما يؤثر الضغط على درجة غليان الماء التي تنخفض مع زيادة الارتفاع.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "3lach lhawa kaydghet w kaykhelli lbarometr ytbeddel?",
                "ma_mix": "3lach l'air kaykhelli la pression tbeddel f le baromètre?",
                "dz_ar": "3lech el hawa ydir la pression w kifech n9isouh bel baromètre?",
                "dz_mix": "3lech l'air ybeddel la pression atmosphérique f le baromètre?",
                "tn_ar": "3lech el hwa ya3mel dharbt w kifeh n9isou bel barometre?",
                "tn_mix": "3lech el hwa ybaddel la pression f le barometre?",
                "fr": "Comment l'air atmosphérique exerce-t-il une pression mesurable par le baromètre ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "ch7al kaykoun l'pression f l3olow dyal jbel?",
                "ma_mix": "ch7al kateh la pression atmosphérique m3a l'altitude f jbel?",
                "dz_ar": "ch7al yahbet la pression ki netl3ou l jbel?",
                "dz_mix": "kifech tahbet la pression m3a l'altitude ki netl3ou?",
                "tn_ar": "9adeh tti7 el pression ki notl3ou l jbal?",
                "tn_mix": "kifeh tti7 la pression atmosphérique m3a l'altitude?",
                "fr": "Comment varie la pression atmosphérique en fonction de l'altitude ?",
            },
        ],
    },
    {
        "id": "electricite_courant",
        "domain": "physique",
        "title_fr": "Courant électrique et intensité",
        "title_ar": "التيار الكهربائي وشدته",
        "text_fr_1": "Le courant électrique correspond au déplacement ordonné de charges électriques, principalement des électrons, à travers un matériau conducteur comme le cuivre. L'intensité du courant électrique représente la quantité de charge qui traverse une section du circuit par seconde. Son unité dans le Système International est l'ampère (A), mesurée à l'aide d'un ampèremètre branché en série.",
        "text_fr_2": "La tension électrique ou différence de potentiel, exprimée en volts (V), est la force motrice qui pousse les électrons dans le circuit. Selon la loi d'Ohm, la tension aux bornes d'un dipôle ohmique est égale au produit de sa résistance par l'intensité du courant (U = R x I).",
        "text_ar_1": "التيار الكهربائي هو حركة منظمة وتدفق للشحنات الكهربائية، خاصة الإلكترونات الحرة، داخل مادة موصلة مثل النحاس. تمثل شدة التيار الكهربائي كمية الشحنة التي تعبر مقطع الموصل في الثانية الواحدة. تقاس شدة التيار بوحدة الأمبير باستخدام جهاز الأمبيرمتر الذي يوصل على التوالي في الدارة.",
        "text_ar_2": "التوتر الكهربائي أو فرق الجهد، المقاس بوحدة الفولت، هو القوة المحركة التي تدفع الشحنات الكهربائية للحركة عبر الدارة المغلقة. وحسب قانون أوم، فإن فرق الجهد بين طرفي مقاومة يساوي جداء قيمة المقاومة في شدة التيار الكهربائي المار فيها.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chouhouwa lcourant d lkahraba w bach kayt9as?",
                "ma_mix": "chno howa le courant électrique w bach kayt9as l'ampère?",
                "dz_ar": "wech howa el courant électrique w kifech n9isouh?",
                "dz_mix": "wech howa le courant électrique w kifeh n9isou l'ampère?",
                "tn_ar": "chnowa el courant mte3 dhaw w kifeh n9isouh?",
                "tn_mix": "chnowa le courant électrique w kifeh n9isou l'intensité?",
                "fr": "Qu'est-ce que le courant électrique et comment mesure-t-on son intensité ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "kifach katkoun l3ala9a bin lvolt w l'ampere f l9anoun d ohm?",
                "ma_mix": "kifach katkoun la relation bin la tension w le courant f la loi d'Ohm?",
                "dz_ar": "kifech nel9aw la relation bin la tension w le courant b la loi d'ohm?",
                "dz_mix": "kifech tekhdem la loi d'Ohm bin U w I w R?",
                "tn_ar": "kifeh terbot bin la tension wel courant b 9anoun ohm?",
                "tn_mix": "kifeh ntab9ou la loi d'Ohm bin le voltage wel courant?",
                "fr": "Quelle formule relie la tension, le courant et la résistance selon la loi d'Ohm ?",
            },
        ],
    },
    {
        "id": "gravite_universelle",
        "domain": "physique",
        "title_fr": "Gravitation universelle",
        "title_ar": "الجاذبية الكونية",
        "text_fr_1": "La loi de la gravitation universelle, formulée par Isaac Newton, stipule que deux corps massifs s'attirent mutuellement avec une force proportionnelle au produit de leurs masses et inversement proportionnelle au carré de la distance qui les sépare. C'est cette force qui maintient les planètes en orbite autour du Soleil et provoque la chute des corps sur Terre.",
        "text_fr_2": "Sur Terre, l'accélération de la pesanteur notée g vaut environ 9,81 m/s². Le poids d'un objet est la force gravitationnelle exercée par la Terre sur sa masse (P = m x g). La masse reste constante partout dans l'univers, alors que le poids dépend de l'astre où l'on se trouve.",
        "text_ar_1": "ينص قانون الجذب العام لنيوتن على أن أي جسمين في الكون يتجاذبان بقوة تتناسب طردياً مع حاصل ضرب كتلتيهما وعكسياً مع مربع المسافة الفاصلة بين مركزيهما. تفسر هذه القوة دوران الكواكب حول الشمس وثبات الأجرام السماوية في مداراتها وسقوط الأجسام نحو الأرض.",
        "text_ar_2": "على كوكب الأرض، يبلغ تسارع الجاذبية الأرضية حوالي 9.81 متر في الثانية المربعة. يمثل وزن الجسم قوة جذب الأرض لكتلته ويحسب بالعلاقة (الثقل = الكتلة × تسارع الجاذبية). تبقى كتلة المادة ثابتة أينما وُجدت، بينما يتغير الوزن بتغير الجاذبية.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "3lach kayti7o le7wayej l l'ard w chkoun khtafeha?",
                "ma_mix": "3lach la gravité d Newton katkhelli l'ajsam ti7 f l'ard?",
                "dz_ar": "3lech tahbat el 7aja lel ard w wech dert la gravité?",
                "dz_mix": "3lech la pesanteur tdir la chute des corps f l'ard?",
                "tn_ar": "3lech kol chay yti7 3al 9a3a w chnowa 9anoun el jathibya?",
                "tn_mix": "3lech el gravité mte3 Newton tched el ajsem?",
                "fr": "Pourquoi les objets tombent-ils vers le sol et quel est le principe de la gravitation de Newton ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "chno lfar9 bin lmass w lwazn dyal l'jism?",
                "ma_mix": "chno howa le différence bin la masse w le poids f la physique?",
                "dz_ar": "wech el far9 bin la masse w le poids ta3 l'objet?",
                "dz_mix": "wech howa le rapport bin la masse m w le poids P?",
                "tn_ar": "chnowa el far9 bin el koutla wel thi9l mte3 el jism?",
                "tn_mix": "chnowa la différence bin la masse m wel poids P f el physique?",
                "fr": "Quelle est la différence fondamentale entre la masse d'un objet et son poids ?",
            },
        ],
    },
    {
        "id": "vitesse_lumiere",
        "domain": "physique",
        "title_fr": "Vitesse de la lumière et optique",
        "title_ar": "سرعة الضوء والبصريات",
        "text_fr_1": "La vitesse de la lumière dans le vide, notée c, est une constante universelle valant exactement 299 792 458 mètres par seconde, couramment arrondie à 300 000 km/s. Selon la relativité restreinte d'Albert Einstein, aucune particule matérielle ni information ne peut voyager plus vite que la lumière dans le vide.",
        "text_fr_2": "Dans les milieux matériels transparents comme l'eau ou le verre, la lumière se propage plus lentement. Le rapport entre la vitesse dans le vide et la vitesse dans le milieu définit l'indice de réfraction n. Ce changement de vitesse explique le phénomène de réfraction, c'est-à-dire la déviation des rayons lumineux.",
        "text_ar_1": "سرعة الضوء في الفراغ هي ثابت فيزيائي كوني يرمز له بالحرف c، وتبلغ قيمته الدقيقة 299,792,458 متراً في الثانية، وتقرب عادة إلى 300 ألف كيلومتر في الثانية. وفقاً لنظرية النسبية الخاصة لأينشتاين، تمثل سرعة الضوء الحد الأقصى للسرعة التي يمكن أن تنتقل بها أي طاقة أو مادة أو معلومة في الكون.",
        "text_ar_2": "عندما يمر الضوء عبر أوساط شفافة مادية كالماء والزجاج، تقل سرعته. وتسمى النسبة بين سرعة الضوء في الفراغ وسرعته في الوسط بمعامل الانكسار. يؤدي هذا التغير في السرعة إلى انكسار الأشعة الضوئية وانحراف مسارها عند الانتقال بين وسطين مختلفين.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "ch7al kateb9a sor3a dyal dow f l'fada2?",
                "ma_mix": "ch7al hiya la vitesse de la lumière f le vide?",
                "dz_ar": "ch7al hiya la vitesse ta3 eddaw fel vide?",
                "dz_mix": "ch7al la vitesse de la lumière f la physique?",
                "tn_ar": "9adeh sor3et edhaw f el fadhé?",
                "tn_mix": "9adeh la vitesse de la lumière selon Einstein?",
                "fr": "Quelle est la valeur de la vitesse de la lumière dans le vide ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "3lach kayt3ewej dow melli kaydkhol f lma?",
                "ma_mix": "3lach kayw9a3 la réfraction melli la lumière katdkhol l l'eau?",
                "dz_ar": "3lech yen3ataf eddaw ki yedkhol fel ma?",
                "dz_mix": "kifech yefsser l'indice de réfraction le changement de direction ta3 la lumière?",
                "tn_ar": "3lech yenkeser edhaw ki yodkhol f el mé?",
                "tn_mix": "kifeh yetbaddel masar la lumière b la réfraction mte3 l'eau?",
                "fr": "Pourquoi la lumière dévie-t-elle lorsqu'elle passe de l'air à l'eau (phénomène de réfraction) ?",
            },
        ],
    },
    {
        "id": "energie_cinetique",
        "domain": "physique",
        "title_fr": "Énergie cinétique et travail",
        "title_ar": "الطاقة الحركية والشغل",
        "text_fr_1": "L'énergie cinétique est l'énergie que possède un corps du fait de son mouvement. Pour un solide de masse m se déplaçant à une vitesse v, l'énergie cinétique se calcule par la formule Ec = 1/2 m v². Elle s'exprime en joules (J) et croît avec le carré de la vitesse, ce qui signifie que doubler la vitesse d'un véhicule quadruple son énergie cinétique.",
        "text_fr_2": "Le théorème de l'énergie cinétique énonce que la variation de l'énergie cinétique d'un système entre deux instants est égale à la somme des travaux de toutes les forces exercées sur lui. Les frottements réalisent un travail résistant qui dissipe l'énergie mécanique sous forme de chaleur.",
        "text_ar_1": "الطاقة الحركية هي الطاقة التي يمتلكها الجسم بفضل حركته وسرعته. بالنسبة لجسم كتلته m ويتحرك بسرعة v، تُحسب الطاقة الحركية بالعلاقة: نصف الكتلة مضروبة في مربع السرعة (Ec = 1/2 m v²). تقاس الطاقة بوحدة الجول وتتناسب طردياً مع مربع السرعة، مما يعني أن مضاعفة السرعة تضاعف الطاقة الحركية أربع مرات.",
        "text_ar_2": "تنص مبرهنة الطاقة الحركية على أن التغير في الطاقة الحركية لنظام مادي يساوي مجموع أشغال القوى الخارجية المطبقة عليه خلال مساره. تؤدي قوى الاحتكاك إلى شغل مقاوم يحول جزءاً من الطاقة الميكانيكية إلى طاقة حرارية مهدورة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach kan7asbo l'energie dyal l7araka dyal tomobil?",
                "ma_mix": "kifach n7asbo l'énergie cinétique Ec melli la voiture katejri?",
                "dz_ar": "kifech nehsbo l'énergie cinétique ta3 corps yemchi?",
                "dz_mix": "wech hiya la formule ta3 l'énergie cinétique Ec = 1/2 m v²?",
                "tn_ar": "kifeh ne7sbou el ta9a el 7arakya mte3 karhba?",
                "tn_mix": "kifeh ntal3ou l'énergie cinétique mte3 un corps mobile?",
                "fr": "Comment calcule-t-on l'énergie cinétique d'un corps en mouvement ?",
            },
        ],
    },
    {
        "id": "ondes_sonores",
        "domain": "physique",
        "title_fr": "Ondes sonores et acoustique",
        "title_ar": "الموجات الصوتية والصوتيات",
        "text_fr_1": "Une onde sonore est une vibration mécanique qui se propage dans un milieu matériel (solide, liquide ou gazeux) par compression et dilatation successives des particules. Le son ne peut donc pas se propager dans le vide absolu. Dans l'air à 20°C, la vitesse de propagation du son est d'environ 340 mètres par seconde.",
        "text_fr_2": "La fréquence d'une onde sonore détermine la hauteur du son : les fréquences basses correspondent aux sons graves, les fréquences hautes aux sons aigus. L'oreille humaine entend les sons situés entre 20 Hz et 20 000 Hz. Les ultrasons ont une fréquence supérieure à 20 kHz.",
        "text_ar_1": "الموجة الصوتية هي اضطراب واهتزاز ميكانيكي ينتقل عبر الأوساط المادية المرنة كالهواء والماء والأجسام الصلبة عن طريق تضاغط وتخلخل الجزيئات. لا يستطيع الصوت الانتشار في الفراغ لعدم وجود جزيئات تنقل الاهتزاز. تبلغ سرعة الصوت في الهواء الجاف عند درجة 20 مئوية حوالي 340 متراً في الثانية.",
        "text_ar_2": "يحدد تردد الموجة الصوتية طبقة الصوت؛ فالترددات المنخفضة تمثل الأصوات الغليظة والجهيرة، بينما تمثل الترددات المرتفعة الأصوات الحادة. تستطيع الأذن البشرية سماع الأصوات الواقعة ضمن المجال الترددي بين 20 هرتز و20 ألف هرتز، وتسمى الترددات الأعلى بالموجات فوق الصوتية.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "3lach sowt may9derch ytmacha f lkhwa dyal l'espace?",
                "ma_mix": "3lach le son maymchich f le vide w kaykhasso un milieu matériel?",
                "dz_ar": "3lech essawt maymchich fel vide w ch7al la vitesse ta3o?",
                "dz_mix": "3lech les ondes sonores ma yentachrouch f le vide?",
                "tn_ar": "3lech essawt mayet3addach f el fadhé?",
                "tn_mix": "3lech le son lazemlou un milieu physique bech yenta9el?",
                "fr": "Pourquoi les ondes sonores ne peuvent-elles pas se propager dans le vide ?",
            },
        ],
    },

    # Biologie (6)
    {
        "id": "photosynthese",
        "domain": "biologie",
        "title_fr": "Photosynthèse",
        "title_ar": "التركيب الضوئي",
        "text_fr_1": "La photosynthèse est le processus biochimique par lequel les plantes vertes, les algues et certaines bactéries convertissent l'énergie lumineuse du soleil en énergie chimique sous forme de glucides. Elle se déroule principalement dans les feuilles au niveau des chloroplastes, grâce à un pigment vert appelé chlorophylle qui capte la lumière.",
        "text_fr_2": "L'équation globale de la photosynthèse utilise du dioxyde de carbone (CO2) absorbé par les stomates et de l'eau (H2O) puisée par les racines pour produire du glucose (C6H12O6) et libérer du dioxygène (O2) dans l'atmosphère. Ce processus est essentiel à la vie sur Terre car il renouvelle l'oxygène et produit la biomasse végétale.",
        "text_ar_1": "التركيب الضوئي أو البناء الضوئي هو عملية حيوية تقوم بها النباتات الخضراء والطحالب لتحويل الطاقة الضوئية للشمس إلى طاقة كيميائية مخزنة في جزيئات السكريات. تحدث هذه العملية داخل الصانعات الخضراء في خلايا الأوراق بفضل صبغة اليخضور أو الكلوروفيل التي تمتص فوتونات الضوء.",
        "text_ar_2": "تستهلك عملية البناء الضوئي غاز ثنائي أكسيد الكربون الممتص من الهواء والماء الممتص من الجذور لتصنيع سكر الجلوكوز وتطرح غاز الأكسجين الضروري لتنفس الكائنات الحية. تعتبر هذه الظاهرة أساس سلاسل الغذاء وتوازن الغلاف الجوي للأرض.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach nebatat kaydiro l'makla dyalhom b do dyal chems?",
                "ma_mix": "kifach les plantes kaydiro la photosynthèse b la lumière?",
                "dz_ar": "kifech les plantes ykhedmou el mekla ta3hom beddaw?",
                "dz_mix": "kifech tessra la photosynthèse fel feuilles ta3 la plante?",
                "tn_ar": "kifeh el nebtet tasna3 el mekla mte3ha bedhaw mte3 echams?",
                "tn_mix": "kifeh ta3mel la plante la photosynthèse bel chlorophylle?",
                "fr": "Comment les plantes vertes fabriquent-elles leur matière organique grâce à la photosynthèse ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "chno homa l'gaz li kaydkhlo w ykhorjo f l'photosynthese?",
                "ma_mix": "chno houwa le rôle dyal le CO2 w l'O2 f la photosynthèse?",
                "dz_ar": "wech men gaz yedkhol w wech yokhredj fel photosynthèse?",
                "dz_mix": "wech houwa l'échange gazeux bin CO2 w oxygène fel photosynthèse?",
                "tn_ar": "chneya les gaz li tekhouhom en-nabta w tssayebhom fel photosynthèse?",
                "tn_mix": "chneya el gaz li todkhol wel gaz li tokhrej f la réaction chimique?",
                "fr": "Quels sont les gaz absorbés et rejetés lors de la photosynthèse végétale ?",
            },
        ],
    },
    {
        "id": "cellule_biologie",
        "domain": "biologie",
        "title_fr": "Structure de la cellule vivante",
        "title_ar": "بنية الخلية الحية",
        "text_fr_1": "La cellule est l'unité structurale, fonctionnelle et reproductrice de tous les êtres vivants. Chez les eucaryotes, elle est entourée d'une membrane plasmique qui délimite le cytoplasme et renferme un noyau contenant l'information génétique sous forme d'ADN. Chez les végétaux, la cellule possède en plus une paroi pectocellulosique rigide et une grande vacuole.",
        "text_fr_2": "À l'intérieur du cytoplasme baignent divers organites spécialisés : les mitochondries fournissent l'énergie par respiration cellulaire, les ribosomes assemblent les protéines et l'appareil de Golgi participe à la maturation et au tri des molécules cellulaires.",
        "text_ar_1": "الخلية هي الوحدة الأساسية والوظيفية والبنائية لجميع الكائنات الحية. تنقسم الخلايا إلى حقيقيات النواة وبدائيات النواة. تتميز الخلايا حقيقية النواة بوجود غشاء هيولي يحيط بالسيتوبلازم ونواة تحتوي على الحمض النووي الوراثي. وتملك الخلايا النباتية جداراً خلوياً صلباً وفجوة عصارية كبيرة.",
        "text_ar_2": "تسبح داخل السيتوبلازم عضيات خلوية متخصصة تؤدي وظائف حيوية؛ فالميتوكوندريا هي مصانع إنتاج الطاقة اللازمة للخلية من خلال التنفس الخلوي، وتتولى الريبوسومات تركيب البروتينات، بينما يقوم جهاز غولجي بتعديل وتوزيع الجزيئات المصنعة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "wesh lkhlia fiha nwat w chno kayn ldakhel dyalha?",
                "ma_mix": "wesh la cellule fiha le noyau w l'ADN ldakhel?",
                "dz_ar": "wesh kayen fel cellule l dakhel w wech faydet le noyau?",
                "dz_mix": "wesh les constituants ta3 la cellule végétale w animale?",
                "tn_ar": "famma noyau fel cellule w chnowa el rôle mte3ou?",
                "tn_mix": "famma chnowa f wesst la cellule bin le noyau wel cytoplasme?",
                "fr": "Quels sont les principaux composants d'une cellule eucaryote et quel est le rôle du noyau ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "chno howa l'organite li kay3ti l'energie l lkhlia?",
                "ma_mix": "chno houwa le rôle dyal les mitochondries f la respiration de la cellule?",
                "dz_ar": "wech hiya la mitochondrie w kifech tmed l'énergie lel cellule?",
                "dz_mix": "wech le rôle ta3 les organites cellulaires kima la mitochondrie?",
                "tn_ar": "chnowa el organite li ya3ti l'énergie lel cellule?",
                "tn_mix": "chnowa le rôle des mitochondries f production d'énergie?",
                "fr": "Quel est le rôle des mitochondries dans la production d'énergie de la cellule ?",
            },
        ],
    },
    {
        "id": "adn_genetique",
        "domain": "biologie",
        "title_fr": "ADN et génétique",
        "title_ar": "الحمض النووي والوراثة",
        "text_fr_1": "L'ADN (acide désoxyribonucléique) est la molécule support de l'information génétique chez tous les êtres vivants. Sa structure en double hélice a été découverte en 1953 par James Watson et Francis Crick. L'ADN est constitué d'une chaîne de nucléotides composés de quatre bases azotées complémentaires : l'adénine (A) s'apparie avec la thymine (T), et la guanine (G) avec la cytosine (C).",
        "text_fr_2": "Un gène est un fragment d'ADN qui porte les instructions nécessaires pour fabriquer une protéine déterminée. Lors de la division cellulaire, la réplication de l'ADN copie fidèlement le génome afin que chaque cellule fille reçoive le même patrimoine génétique.",
        "text_ar_1": "الحمض النووي الريبوزي منقوص الأكسجين (ADN) هو الجزيء الحيوي الحامل للمعلومات الوراثية لدى الكائنات الحية. يتكون من شريطين حلزونيين ملتفين، ويتركب من تتابع أربع قواعد نيتروجينية مكملة لبعضها: يرتبط الأدنين (A) دائماً بالثايمين (T)، ويرتبط الجوانين (G) بالسيتوزين (C).",
        "text_ar_2": "المورثة أو الجين هي قطعة محددة من الـ ADN تحمل الشفرة الوراثية المسؤولة عن تركيب بروتين معين يحدد صفة وراثية. أثناء الانقسام الخلوي، تتضاعف جزيئات الـ ADN بدقة متناهية لضمان انتقال نفس البرنامج الوراثي إلى الخلايا الناتجة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno houwa l'ADN w chnouma l'hrouf dyalo l'arba3a?",
                "ma_mix": "chno howa l'ADN w les quatre bases azotées A, T, C, G?",
                "dz_ar": "wech howa l'ADN w kifech yetkewen men les bases?",
                "dz_mix": "wech hiya la structure ta3 la molécule d'ADN?",
                "tn_ar": "chnowa l'ADN w kifeh terbot el 9awa3ed en-nitroginiya?",
                "tn_mix": "chnowa l'ADN wel complémentarité mte3 les bases A-T w C-G?",
                "fr": "Quelle est la structure de l'ADN et quelles sont les quatre bases azotées qui le composent ?",
            },
        ],
    },
    {
        "id": "respiration_cellulaire",
        "domain": "biologie",
        "title_fr": "Respiration cellulaire et métabolisme",
        "title_ar": "التنفس الخلوي والاستقلاب",
        "text_fr_1": "La respiration cellulaire est une réaction métabolique catabolique qui dégrade le glucose en présence de dioxygène pour produire de l'adénosine triphosphate (ATP), la molécule universelle d'énergie cellulaire. Cette dégradation complète rejette du dioxyde de carbone et de l'eau.",
        "text_fr_2": "Le bilan chimique de la respiration cellulaire s'écrit : C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O + énergie sous forme d'ATP. En absence d'oxygène, certaines cellules peuvent recourir à la fermentation (lactique ou alcoolique), mais celle-ci produit beaucoup moins d'énergie par molécule de glucose.",
        "text_ar_1": "التنفس الخلوي هو مسار استقلابي حيوي يتم من خلاله أكسدة وتفكيك جزيئات الجلوكوز في وجود غاز الأكسجين لإنتاج جزيئات الأدينوزين ثلاثي الفوسفات (ATP) التي تمثل عملة الطاقة في الخلية، ويطرح هذا التفاعل ثنائي أكسيد الكربون والماء.",
        "text_ar_2": "تُعبر المعادلة العامة للتنفس الخلوي عن استهلاك جزيء جلوكوز وست جزيئات أكسجين لإنتاج ست جزيئات CO2 وست جزيئات ماء وطاقة كيميائية. وعند غياب الأكسجين، تلجأ بعض الخلايا للتخمر اللبني أو الكحولي لإنتاج كمية ضئيلة من الطاقة.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach katssra la respiration dyal lkhlia w chno katntaj?",
                "ma_mix": "kifach la cellule katekhrej l'ATP men le glucose f la respiration?",
                "dz_ar": "kifech yessra le métabolisme ta3 la respiration cellulaire w l'ATP?",
                "dz_mix": "kifech la respiration cellulaire tekhedm l'énergie ATP?",
                "tn_ar": "kifeh tssir et-tanaffos el khalawi bech tasna3 l'ATP?",
                "tn_mix": "kifeh el cellule te7re9 le glucose m3a l'O2 bech ta3ti l'ATP?",
                "fr": "Comment la respiration cellulaire permet-elle de produire de l'ATP à partir du glucose ?",
            },
        ],
    },
    {
        "id": "systeme_circulatoire",
        "domain": "biologie",
        "title_fr": "Système circulatoire et cœur",
        "title_ar": "الجهاز الدوراني والقلب",
        "text_fr_1": "Le système circulatoire assure le transport du sang, des nutriments, du dioxygène et des déchets dans tout le corps humain. Le cœur fonctionne comme une pompe musculaire à quatre cavités : deux oreillettes qui reçoivent le sang et deux ventricules qui l'éjectent vers les vaisseaux sanguins.",
        "text_fr_2": "La circulation sanguine comprend la petite circulation (pulmonaire) qui achemine le sang désoxygéné vers les poumons pour se recharger en dioxygène, et la grande circulation (systémique) qui propulse le sang oxygéné vers tous les organes et tissus de l'organisme.",
        "text_ar_1": "يقوم الجهاز الدوراني بنقل الدم المحمل بالأكسجين والمغذيات والهرمونات إلى جميع خلايا الجسم وتخليصها من الفضلات. يعمل القلب كمضخة عضلية تتألف من أربع حجرات رئيسية: أذينان يستقبلان الدم العائد وبطينان يقومان بضخ الدم إلى الشرايين.",
        "text_ar_2": "تنقسم الدورة الدموية إلى دورتين: الدورة الدموية الصغرى (الرئوية) التي تنقل الدم غير المؤكسج إلى الرئتين للتخلص من CO2 والامتلاء بالأكسجين، والدورة الدموية الكبرى (الجهازية) التي توزع الدم المؤكسج من البطين الأيسر إلى كافة أنسجة الجسم.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach kaykhdem l9elb bach ydowwer ddem f l'jism?",
                "ma_mix": "kifach le cœur kaypompi le sang bin la petite w la grande circulation?",
                "dz_ar": "kifech yedkhol eddem lel 9elb w kifech yetfarra9?",
                "dz_mix": "wech houwa le rôle ta3 les cavités ta3 le cœur fel circulation?",
                "tn_ar": "kifeh yakhdem el 9alb bech ydawwer eddam fel badan?",
                "tn_mix": "kifeh le cœur y3addi le sang fel circulation pulmonaire w générale?",
                "fr": "Comment fonctionne le cœur pour assurer la double circulation sanguine dans le corps ?",
            },
        ],
    },
    {
        "id": "systeme_immunitaire",
        "domain": "biologie",
        "title_fr": "Système immunitaire et anticorps",
        "title_ar": "الجهاز المناعي والأجسام المضادة",
        "text_fr_1": "Le système immunitaire défend l'organisme contre les agents pathogènes tels que les bactéries, virus, parasites et champignons. L'immunité innée intervient immédiatement par la réaction inflammatoire et les globules blancs phagocytes (macrophages).",
        "text_fr_2": "L'immunité adaptative est plus lente mais spécifique et dotée de mémoire. Les lymphocytes B sécrètent des anticorps capables de neutraliser les antigènes étrangers, tandis que les lymphocytes T cytotoxiques détruisent directement les cellules infectées ou anormales.",
        "text_ar_1": "يحمي الجهاز المناعي جسم الإنسان من الميكروبات الممرضة كالفيروسات والبكتيريا والسموم. تشكل المناعة الفطرية خط الدفاع الأول الفوري وغير النوعي من خلال الحواجز الطبيعية والاستجابة الالتهابية وبلعمة الجراثيم بواسطة البلاعم الكبيرة.",
        "text_ar_2": "تعتبر المناعة التكيفية استجابة نوعية متطورة تملك ذاكرة مناعية. تنتج الخلايا اللمفاوية B أجساماً مضادة نوعية تبطل مفعول المستضدات الغريبة، في حين تتولى الخلايا اللمفاوية T القاتلة تدمير الخلايا المصابة بالعدوى.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach kaydafe3 l'jism 3la rasso b les anticorps?",
                "ma_mix": "kifach le système immunitaire kayt3araf 3la les antigènes b les lymphocytes B?",
                "dz_ar": "kifech les anticorps ye7miw el corps men les virus?",
                "dz_mix": "wech el far9 bin l'immunité innée w l'immunité adaptative?",
                "tn_ar": "kifeh ya7mi el corps rou7ou bel man3a ded el mikroubet?",
                "tn_mix": "kifeh yakhdmou les anticorps mte3 le système immunitaire?",
                "fr": "Comment les anticorps et les lymphocytes protègent-ils l'organisme contre les agents pathogènes ?",
            },
        ],
    },

    # Chimie (5)
    {
        "id": "tableau_periodique",
        "domain": "chimie",
        "title_fr": "Tableau périodique des éléments",
        "title_ar": "الجدول الدوري للعناصر",
        "text_fr_1": "Le tableau périodique des éléments, conçu initialement par Dmitri Mendeleïev en 1869, classe l'ensemble des éléments chimiques selon leur numéro atomique Z croissant (nombre de protons). Les éléments d'une même colonne forment une famille chimique et partagent des propriétés électroniques et chimiques similaires en raison du même nombre d'électrons de valence.",
        "text_fr_2": "Les lignes horizontales sont appelées périodes et correspondent au remplissage progressif des couches électroniques. On distingue les métaux à gauche et au centre, les non-métaux à droite et les gaz nobles ou rares dans la dernière colonne (colonne 18), caractérisés par leur grande stabilité chimique.",
        "text_ar_1": "الجدول الدوري للعناصر الكيميائية، الذي ابتكره العالم الروسي ديمتري مندلييف عام 1869، يرتب العناصر الكيميائية وفق تزايد عددها الذري Z (عدد البروتونات). تشكل العناصر الموجودة في نفس العمود الرأسي زمرة أو عائلة كيميائية تتشابه في خواصها لتطابق عدد إلكترونات التكافؤ لديها.",
        "text_ar_2": "تسمى الصفوف الأفقية بالدورات وتوافق ملء الطبقات الإلكترونية لذرات العناصر. يتضمن الجدول الفلزات والمعادن في الجانبين الأيسر والأوسط، واللافلزات في الجانب الأيمن، وتنتهي كل دورة بالغازات النبيلة الخاملة كيميائياً في العمود 18 لاكتمال طبقتها الخارجية.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach mretbin les éléments f tableau périodique dyal chimie?",
                "ma_mix": "kifach Mendeleïev rtteb le tableau périodique 7sab le numéro atomique Z?",
                "dz_ar": "kifech msettfin les éléments fel tableau périodique?",
                "dz_mix": "3la wach m3awed le tableau périodique des éléments chimiques?",
                "tn_ar": "kifeh mratbin les éléments chimiques fel tableau périodique?",
                "tn_mix": "kifeh Mendeleïev rattiib les éléments selon le numéro atomique?",
                "fr": "Selon quel critère les éléments chimiques sont-ils classés dans le tableau périodique de Mendeleïev ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "3lach les éléments li f nefss la colonne 3ndhom nefss l'khwass?",
                "ma_mix": "3lach les éléments chimiques d'une même famille 3ndhom les mêmes électrons de valence?",
                "dz_ar": "3lech les atomes ta3 le même groupe ytchabhou fel khwass?",
                "dz_mix": "3lech les familles chimiques ykoun 3ndhom la même réactivité?",
                "tn_ar": "3lech les éléments mte3 nafs la colonne ytchabhou fel les propriétés chimiques?",
                "tn_mix": "3lech les éléments d'une même colonne 3andhom les mêmes électrons externes?",
                "fr": "Pourquoi les éléments chimiques situés dans une même colonne du tableau périodique ont-ils des propriétés similaires ?",
            },
        ],
    },
    {
        "id": "acides_bases_ph",
        "domain": "chimie",
        "title_fr": "Acides, bases et échelle de pH",
        "title_ar": "الأحماض والقواعد ومقياس الأس الهيدروجيني",
        "text_fr_1": "Selon la théorie de Brønsted-Lowry, un acide est une espèce chimique capable de céder un ou plusieurs protons H+, tandis qu'une base est capable d'en capter. Le pH (potentiel hydrogène) mesure l'acidité ou la basicité d'une solution aqueuse sur une échelle graduée de 0 à 14. Une solution neutre comme l'eau pure a un pH de 7 à 25°C.",
        "text_fr_2": "Une solution est acide si son pH est inférieur à 7, traduisant une concentration élevée en ions oxonium H3O+. Elle est basique si son pH est supérieur à 7, indiquant une prédominance d'ions hydroxyde HO-. La mesure s'effectue avec un papier indicateur de pH ou un pH-mètre électronique.",
        "text_ar_1": "حسب نظرية برونستد-لوري، الحمض هو نوع كيميائي قادر على منح بروتون H+ أو أكثر خلال تفاعل كيميائي، في حين أن القاعدة هي نوع كيميائي قادر على اكتساب ذلك البروتون. يقيس الأس الهيدروجيني (pH) درجة حموضة أو قلوية المحاليل المائية على سلم يتراوح من 0 إلى 14.",
        "text_ar_2": "يكون المحلول المائي حمضياً إذا كان pH أصغر من 7، ويكون قلوياً أو قاعدياً إذا كان أكبر من 7، ويكون متعادلاً عندما يساوي 7 تماماً عند درجة 25 مئوية. يقاس الـ pH باستخدام كواشف ملونة أو جهاز مقياس الحموضة الإلكتروني (pH-mètre).",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno howa l'acide w l'base w chno howa l'pH d lma?",
                "ma_mix": "chno howa le pH neutre dyal l'eau w kifach kayt7sseb?",
                "dz_ar": "wech howa el far9 bin l'acide wel base w ch7al el pH neutre?",
                "dz_mix": "wech houwa le pH ta3 l'acide w la base fel chimie?",
                "tn_ar": "chnowa l'acide wel base w kifeh n9isou le pH?",
                "tn_mix": "chnowa l'échelle de pH bin 0 w 14 fel chimie?",
                "fr": "Qu'est-ce qu'un acide, une base et quelle est la valeur du pH d'une solution neutre ?",
            },
        ],
    },
    {
        "id": "liaison_covalente",
        "domain": "chimie",
        "title_fr": "Liaison chimique et liaisons covalentes",
        "title_ar": "الروابط الكيميائية والرابطة التساهمية",
        "text_fr_1": "Une liaison covalente est une liaison chimique issue de la mise en commun d'un ou plusieurs doublets d'électrons entre deux atomes non-métalliques. Cette mise en commun permet à chaque atome d'acquérir une configuration électronique stable, respectant généralement la règle de l'octet (huit électrons sur la couche externe).",
        "text_fr_2": "Si les deux atomes ont la même électronégativité, la liaison est covalente pure ou apolaire (comme dans la molécule de dihydrogène H2 ou de dioxygène O2). Si l'un des atomes attire plus fortement les électrons, la liaison devient polarisée (comme dans la molécule d'eau H2O).",
        "text_ar_1": "الرابطة التساهمية هي رابطة كيميائية تنشأ من التشارك في زوج أو أكثر من إلكترونات التكافؤ بين ذرتين لافلزيتين. يتيح هذا التشارك لكل ذرة تحقيق توزيع إلكتروني مستقر يماثل الغازات الخاملة وفق قاعدة الثمانية الإلكترونية.",
        "text_ar_2": "تكون الرابطة التساهمية غير قطبية إذا تساوت الكهروسلبية بين الذرتين مثل جزيء H2، وتصبح مستقطبة عندما تختلف كهروسلبية الذرتين المشتركتين، كما في جزيء الماء H2O حيث تجذب ذرة الأكسجين الإلكترونات بقوة أكبر.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach katssra la liaison covalente bin les atomes?",
                "ma_mix": "kifach les atomes kaytcharco les électrons f la liaison covalente?",
                "dz_ar": "kifech yetcharqo les atomes fel liaison covalente?",
                "dz_mix": "kifech tekhedm la liaison covalente w la règle de l'octet?",
                "tn_ar": "kifeh tssir el rabita et-tasahomya bin les atomes?",
                "tn_mix": "kifeh yetcharkou les électrons f la liaison covalente?",
                "fr": "Comment se forme une liaison covalente par mise en commun d'électrons entre atomes ?",
            },
        ],
    },
    {
        "id": "etats_matiere",
        "domain": "chimie",
        "title_fr": "États de la matière et changements d'état",
        "title_ar": "حالات المادة وتغيراتها الفيزيائية",
        "text_fr_1": "La matière se présente couramment sous trois états physiques principaux : solide, liquide et gaz (plus le plasma à haute énergie). À l'état solide, les molécules sont ordonnées et fortement liées entre elles. À l'état liquide, elles sont en contact mais désordonnées et mobiles. À l'état gazeux, les particules sont très éloignées les unes des autres et animées d'un mouvement rapide et aléatoire.",
        "text_fr_2": "Les changements d'état sont des transformations physiques réversibles provoquées par une variation de température ou de pression : la fusion (solide en liquide), la vaporisation (liquide en gaz), la condensation ou liquéfaction (gaz en liquide), la solidification (liquide en solide) et la sublimation (solide directement en gaz).",
        "text_ar_1": "توجد المادة في الطبيعة في ثلاث حالات فيزيائية أساسية: الصلبة والسائلة والغازية (بالإضافة إلى حالة البلازما). في الحالة الصلبة تكون الجزيئات متراصة ومنتظمة ومترابطة بقوة. وفي الحالة السائلة تكون الجزيئات متقاربة ومتحركة، بينما تكون في الحالة الغازية متباعدة جداً وتتحرك بحرية وسرعة عشوائية.",
        "text_ar_2": "تغيرات حالة المادة هي تحولات فيزيائية لا تغير من التركيب الكيميائي للمادة: الانصهار (تحول الصلب إلى سائل)، والتبخر (السائل إلى غاز)، والتكاثف (الغاز إلى سائل)، والتجمد (السائل إلى صلب)، والتسامي (تحول الصلب مباشرة إلى غاز دون المرور بالحالة السائلة).",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno homa l'7alat dyal l'mada w chno howa l'far9 bin l'gaz w solide?",
                "ma_mix": "chno houma les trois états de la matière liquide, solide w gaz?",
                "dz_ar": "wech houma les états ta3 la matière w kifech yetbeddlou?",
                "dz_mix": "wech houwa le changement d'état liquide vers gaz?",
                "tn_ar": "chneya 7alet el madda eth-thletha w kifeh yetbadlou?",
                "tn_mix": "chneya la différence bin état solide, liquide w gaz?",
                "fr": "Quels sont les trois principaux états de la matière et comment s'appellent les transitions entre eux ?",
            },
        ],
    },
    {
        "id": "oxydoreduction",
        "domain": "chimie",
        "title_fr": "Réactions d'oxydoréduction",
        "title_ar": "تفاعلات الأكسدة والإرجاع",
        "text_fr_1": "Une réaction d'oxydoréduction (rédox) est une transformation chimique au cours de laquelle s'effectue un transfert d'électrons entre deux réactifs : un réducteur qui cède un ou plusieurs électrons, et un oxydant qui les capte. L'oxydation correspond à la perte d'électrons et la réduction correspond au gain d'électrons (mémo : OXYDATION = PERTE, RÉDUCTION = GAIN).",
        "text_fr_2": "Les réactions rédox interviennent dans de très nombreux domaines : la respiration biologique, la photosynthèse, la corrosion des métaux comme la rouille du fer, ainsi que dans le fonctionnement des piles électriques et des batteries rechargeables.",
        "text_ar_1": "تفاعل الأكسدة والإرجاع هو تفاعل كيميائي يتميز بانتقال إلكترون أو أكثر بين نوعين كيميائيين: المؤكسد الذي يكتسب الإلكترونات ويختزل، والمرجع (المختزل) الذي يفقد الإلكترونات ويتأكسد. فالأكسدة هي عملية فقدان إلكترونات والإرجاع هو عملية كسب إلكترونات.",
        "text_ar_2": "تدخل تفاعلات الأكسدة والإرجاع في العديد من الظواهر الطبيعية والتطبيقات الصناعية كالصدأ، والتنفس الخلوي، واشتغال البطاريات والمراكم الكيميائية حيث يتحول التفاعل الكيميائي إلى تيار كهربائي مباشر.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach kaytcharco les électrons f l'oxydoréduction w chno howa l'oxydant?",
                "ma_mix": "kifach katkoun la réaction redox bin l'oxydant w le réducteur?",
                "dz_ar": "wech howa le transfert d'électrons fel oxydoréduction?",
                "dz_mix": "kifech yessra le transfert d'électrons bin oxydant w réducteur?",
                "tn_ar": "chnowa el far9 bin l'oxydant wel réducteur fel oxydoréduction?",
                "tn_mix": "kifeh tssir la réaction d'oxydoréduction f les piles?",
                "fr": "Qu'est-ce qu'une réaction d'oxydoréduction et comment se définit un oxydant par rapport à un réducteur ?",
            },
        ],
    },

    # Mathématiques (5)
    {
        "id": "pythagore",
        "domain": "mathematiques",
        "title_fr": "Théorème de Pythagore",
        "title_ar": "مبرهنة فيثاغورس",
        "text_fr_1": "Le théorème de Pythagore est un théorème fondamental de géométrie euclidienne qui énonce que dans un triangle rectangle, le carré de la longueur de l'hypoténuse (le côté opposé à l'angle droit) est égal à la somme des carrés des longueurs des deux autres côtés. Si le triangle est rectangle en A, alors BC² = AB² + AC².",
        "text_fr_2": "La réciproque du théorème de Pythagore permet de démontrer qu'un triangle est rectangle : si dans un triangle le carré du plus grand côté est égal à la somme des carrés des deux autres, alors ce triangle possède un angle droit opposé à ce plus grand côté.",
        "text_ar_1": "مبرهنة فيثاغورس هي نظرية هندسية أساسية تنص على أنه في أي مثلث قائم الزاوية، يكون مربع طول الوتر (الضلع الأطول المقابل للزاوية القائمة) مساوياً لمجموع مربعي طولي الضلعين القائمين الآخرين. فإذا كان المثلث قائماً في A، فإن BC² = AB² + AC².",
        "text_ar_2": "تُستخدم المبرهنة العكسية لفيثاغورس لإثبات أن مثلثاً ما قائم الزاوية: إذا تساوى مربع طول أطول أضلاع مثلث مع مجموع مربعي الضلعين الآخرين، فإن المثلث قائم الزاوية حتماً والزاوية القائمة تقابل الضلع الأكبر.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chkoun howa théorème dyal pythagore w kifach n7asbo l'hypoténuse?",
                "ma_mix": "chno howa le théorème de Pythagore f le triangle rectangle?",
                "dz_ar": "wech t9ol la règle ta3 pythagore fel triangle rectangle?",
                "dz_mix": "kifech n7asbou l'hypoténuse b le théorème de Pythagore?",
                "tn_ar": "chnowa théorème de Pythagore w kifeh ne7sbou el hypoténuse?",
                "tn_mix": "kifeh ntab9ou le théorème de Pythagore f مثلث قائم?",
                "fr": "Qu'affirme le théorème de Pythagore pour un triangle rectangle ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "kifach kanst3mlo la réciproque dyal pythagore bach nbayno triangle rectangle?",
                "ma_mix": "kifach nsta3mlo la réciproque de Pythagore pour démontrer l'angle droit?",
                "dz_ar": "kifech nbaynou beli triangle 3ando angle droit b la réciproque?",
                "dz_mix": "kifech ntab9ou la réciproque de Pythagore fel géométrie?",
                "tn_ar": "kifeh nbaynou un angle droit bel réciproque de Pythagore?",
                "tn_mix": "kifeh nest3amlou la réciproque de Pythagore bech ntabtou قائم الزاوية?",
                "fr": "Comment utiliser la réciproque du théorème de Pythagore pour prouver qu'un triangle est rectangle ?",
            },
        ],
    },
    {
        "id": "thales",
        "domain": "mathematiques",
        "title_fr": "Théorème de Thalès",
        "title_ar": "مبرهنة طاليس",
        "text_fr_1": "Le théorème de Thalès permet de calculer des longueurs dans des figures géométriques comportant des droites parallèles. Il énonce que si deux droites sécantes sont coupées par deux droites parallèles, alors elles déterminent des segments homologues de longueurs proportionnelles.",
        "text_fr_2": "Dans un triangle ABC, si un point M appartient au segment [AB] et un point N appartient au segment [AC], et si la droite (MN) est parallèle à la droite (BC), alors on a l'égalité des rapports : AM / AB = AN / AC = MN / BC.",
        "text_ar_1": "مبرهنة طاليس هي قاعدة هندسية تستخدم لحساب أطوال الأضلاع في الأشكال الهندسية التي تحتوي على مستقيمات متوازية. تنص على أنه إذا قطع مستقيمان متقاطعان بمستقيمين متوازيين، فإن أطوال القطع المحددة على أحدهما تتناسب مع أطوال القطع المقابلة لها على الآخر.",
        "text_ar_2": "في مثلث ABC، إذا كانت النقطة M تنتمي إلى [AB] والنقطة N تنتمي إلى [AC]، وكان المستقيم (MN) يوازي المستقيم (BC)، فإن نسب أطوال الأضلاع تكون متساوية: AM/AB = AN/AC = MN/BC.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno howa théorème dyal thales w chno kaykhesso dyal l'khotot?",
                "ma_mix": "chno houwa le théorème de Thalès w chnouma les droites parallèles?",
                "dz_ar": "wech howa théorème de Thalès fel mathématiques?",
                "dz_mix": "kifech n7asbou les segments b le théorème de Thalès?",
                "tn_ar": "chnowa théorème de Thalès w kifeh nkharjou les rapports?",
                "tn_mix": "chnowa le principe de Thalès m3a les droites parallèles?",
                "fr": "Quelles sont les conditions d'application et la formule du théorème de Thalès ?",
            },
        ],
    },
    {
        "id": "equations_second_degre",
        "domain": "mathematiques",
        "title_fr": "Équations du second degré et discriminant",
        "title_ar": "معادلات الدرجة الثانية والمميز",
        "text_fr_1": "Une équation du second degré à une inconnue est une équation de la forme ax² + bx + c = 0, où a, b et c sont des réels avec a non nul. Sa résolution repose sur le calcul du discriminant noté delta : Δ = b² - 4ac.",
        "text_fr_2": "Le signe de delta détermine le nombre de solutions réelles : si Δ > 0, l'équation admet deux solutions réelles distinctes x1 = (-b - √Δ)/(2a) et x2 = (-b + √Δ)/(2a) ; si Δ = 0, elle admet une solution double unique x0 = -b/(2a) ; si Δ < 0, elle n'admet aucune solution réelle.",
        "text_ar_1": "معادلة الدرجة الثانية بمجهول واحد هي كل معادلة تكتب على الشكل ax² + bx + c = 0، حيث a و b و c أعداد حقيقية مع a يخالف الصفر. تعتمد طريقة حلها الجبري على حساب قيمة المميز دلتا: Δ = b² - 4ac.",
        "text_ar_2": "تحدد إشارة المميز دلتا عدد الحلول الحقيقية للمعادلة: إذا كان دلتا موجباً قطعا، تقبل المعادلة حلين حقيقيين مختلفين؛ وإذا كان دلتا مساوياً للصفر تقبل حلاً مضاعفاً وحيداً؛ وإذا كان دلتا سالباً قطعا، فليس للمعادلة أي حل في مجموعة الأعداد الحقيقية.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach kan7allo l'mou3adala dyal daraja tania b delta?",
                "ma_mix": "kifach n7asbo le discriminant delta = b² - 4ac f l'équation du second degré?",
                "dz_ar": "kifech n7ellou équation du 2ème degré b delta?",
                "dz_mix": "wech houma les solutions ta3 ax² + bx + c = 0 selon delta?",
                "tn_ar": "kifeh n7ellou mo3adla mel darja eth-thanya bel discriminant delta?",
                "tn_mix": "kifeh nkharjou les racines mte3 l'équation selon le signe de delta?",
                "fr": "Comment résoudre une équation du second degré ax² + bx + c = 0 à l'aide du discriminant delta ?",
            },
        ],
    },
    {
        "id": "probabilites",
        "domain": "mathematiques",
        "title_fr": "Calcul des probabilités",
        "title_ar": "حساب الاحتمالات",
        "text_fr_1": "Le calcul des probabilités modélise les phénomènes aléatoires, c'est-à-dire dont le résultat dépend du hasard. L'univers d'une expérience aléatoire, noté oméga, est l'ensemble de tous les résultats possibles. La probabilité d'un événement A est un nombre réel compris entre 0 (événement impossible) et 1 (événement certain).",
        "text_fr_2": "Dans une situation d'équiprobabilité où toutes les issues ont la même chance de se produire, la probabilité d'un événement A se calcule par le quotient du nombre de cas favorables par le nombre total de cas possibles : P(A) = card(A) / card(Ω).",
        "text_ar_1": "حساب الاحتمالات هو فرع رياضي يهتم بدراسة وتحليل التجارب العشوائية التي تخضع للصدفة. يمثل كون الإمكانيات أوميغا مجموعة النتائج الممكنة للتجربة. واحتمال وقوع حدث A هو عدد حقيقي يقع بين 0 (الحدث المستحيل) و1 (الحدث الأكيد).",
        "text_ar_2": "في حالة تساوي الاحتمال لجميع الأحداث الابتدائية، يُحسب احتمال وقوع حدث ما بقسمة عدد الحالات الملائمة لوقوع الحدث على العدد الإجمالي للحالات الممكنة في فضاء التجربة: P(A) = عدد الحالات الملائمة / عدد الحالات الممكنة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach kan7asbo l'i7timal dyal un événement f l'math?",
                "ma_mix": "kifach n7asbo la probabilité P(A) melli kaykoun l'hasard?",
                "dz_ar": "kifech nehsbo les probabilités ta3 événement aléatoire?",
                "dz_mix": "wech hiya la formule ta3 la probabilité cas favorables 3la cas possibles?",
                "tn_ar": "kifeh ne7sbou el e7timal mte3 7adath f el mathématiques?",
                "tn_mix": "kifeh ntal3ou la probabilité d'un événement aléatoire?",
                "fr": "Comment calcule-t-on la probabilité d'un événement dans une situation d'équiprobabilité ?",
            },
        ],
    },
    {
        "id": "derivee_fonctions",
        "domain": "mathematiques",
        "title_fr": "Dérivée d'une fonction et variation",
        "title_ar": "مشتقة دالة والتغيرات",
        "text_fr_1": "La dérivée d'une fonction f en un point x mesure la vitesse de variation instantanée de f en ce point. Géométriquement, le nombre dérivé f'(a) représente le coefficient directeur (la pente) de la droite tangente à la courbe représentative de la fonction au point d'abscisse a.",
        "text_fr_2": "L'étude du signe de la fonction dérivée f' permet de connaître les variations de la fonction f : si f'(x) > 0 sur un intervalle, alors f est strictement croissante ; si f'(x) < 0, f est strictement décroissante ; et si la dérivée s'annule en changeant de signe, la fonction présente un extremum local (maximum ou minimum).",
        "text_ar_1": "مشتقة دالة رياضية f عند نقطة معينة تمثل معدل التغير اللحظي للدالة عند تلك النقطة. هندسياً، يعبر العدد المشتق f'(a) عن المعامل الموجه (الميل) للمستقيم المماس لمنحنى الدالة عند النقطة التي أفصولها a.",
        "text_ar_2": "تسمح دراسة إشارة الدالة المشتقة f' بتحديد اتجاه تغير الدالة الأصلية f: إذا كانت المشتقة موجبة قطعا على مجال، فإن الدالة تكون تزايدية قطعا؛ وإذا كانت المشتقة سالبة، تكون الدالة تناقصية قطعا؛ وإذا انعدمت المشتقة مغيرّة إشارتها، فإن الدالة تقبل قيمة قصوى أو دنيا.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "chno kay3ni l'mouchta9a dyal fonction w kifach katanfa3 f tableau de variation?",
                "ma_mix": "chno howa le rôle dyal la dérivée f' bach n3arfo la variation dyal f(x)?",
                "dz_ar": "wech hiya la dérivée w kifech n3arfou l'orientation ta3 la fonction?",
                "dz_mix": "kifech ykhellina le signe ta3 f'(x) n3arfou les variations?",
                "tn_ar": "chnowa el mouchta99a mte3 fonction w chnowa ya3tina signouha?",
                "tn_mix": "kifeh na3rfou les variations de f à partir du signe de la dérivée f'?",
                "fr": "Quel est le lien entre le signe de la dérivée f'(x) et les variations d'une fonction f ?",
            },
        ],
    },

    # Informatique (4)
    {
        "id": "algorithme_complexite",
        "domain": "informatique",
        "title_fr": "Algorithmes et complexité temporelle",
        "title_ar": "الخوارزميات والتعقيد الزمني",
        "text_fr_1": "Un algorithme est une suite ordonnée, finie et non ambiguë d'instructions permettant de résoudre un problème ou d'accomplir une tâche donnée. La complexité algorithmique évalue la quantité de ressources (temps d'exécution ou espace mémoire) requise par un algorithme en fonction de la taille n des données d'entrée, généralement notée avec la notation grand O.",
        "text_fr_2": "Une complexité O(1) est constante, O(log n) logarithmique (comme la recherche dichotomique), O(n) linéaire (comme le parcours d'une liste), O(n log n) quasi-linéaire (comme le tri fusion ou tri rapide moyen), et O(n²) quadratique (comme le tri à bulles).",
        "text_ar_1": "الخوارزمية هي سلسلة محددة ومنظمة ومنطقية من الخطوات والتعليمات البرمجية الهادفة لحل مشكلة محددة أو معالجة بيانات. يقيس التعقيد الحسابي للخوارزمية حجم الموارد اللازمة لتنفيذها (الوقت الزمني أو مساحة الذاكرة) بدلالة حجم المدخلات n، ويُعبر عنه عادة برمز Big O.",
        "text_ar_2": "يمثل O(1) تعقيداً ثابتاً، و O(log n) تعقيداً لوغاريتمياً (مثل البحث الثنائي)، و O(n) تعقيداً خطياً، و O(n log n) تعقيد الفرز السريع والفرز بالدمج، بينما يعتبر O(n²) تعقيداً تربيعياً بطيئاً مع نمو حجم المدخلات مثل خوارزمية الفرز الفقاعي.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno howa un algorithme f l'informatique w kifach kaykhdem?",
                "ma_mix": "chno howa le concept d'algorithme w les instructions dyalo?",
                "dz_ar": "wech howa l'algorithme w kifech n7ellou bih mochkla f l'informatique?",
                "dz_mix": "wech houwa le rôle d'un algorithme f la programmation?",
                "tn_ar": "chnowa algorithme f l'informatique w kifeh ya3ti les étapes?",
                "tn_mix": "chnowa l'algorithme w kifeh nfassrouh en informatique?",
                "fr": "Qu'est-ce qu'un algorithme informatique et comment se définit-il ?",
            },
            {
                "level": "intermediaire",
                "ma_ar": "chno kaye3ni grand O f la complexité temporelle dyal algo?",
                "ma_mix": "chno howa le sens dyal la notation grand O(n) w O(log n)?",
                "dz_ar": "wech ma3naha la complexité temporelle Big O d'un algorithme?",
                "dz_mix": "kifech n9isou le temps d'exécution b la complexité O(n log n)?",
                "tn_ar": "chnowa ma3neha la complexité Big O f l'analyse des algorithmes?",
                "tn_mix": "kifeh nfar9ou bin complexité O(n) w O(log n) f l'informatique?",
                "fr": "Que représente la notation grand O dans l'analyse de la complexité temporelle d'un algorithme ?",
            },
        ],
    },
    {
        "id": "processeur_memoire",
        "domain": "informatique",
        "title_fr": "Processeur (CPU) et mémoire vive (RAM)",
        "title_ar": "المعالج والذاكرة العشوائية",
        "text_fr_1": "Le processeur ou CPU (Central Processing Unit) est le cerveau de l'ordinateur. Il exécute les instructions des programmes informatiques selon le cycle élémentaire : lecture (fetch), décodage et exécution. Sa vitesse d'horloge s'exprime en gigahertz (GHz), et les processeurs modernes disposent de plusieurs cœurs pour traiter plusieurs tâches simultanément.",
        "text_fr_2": "La mémoire vive ou RAM (Random Access Memory) stocke temporairement les données et programmes en cours d'exécution par le processeur. Elle est volatile : son contenu disparaît dès l'extinction de l'ordinateur. Sa rapidité d'accès est cruciale pour éviter que le CPU ne perde du temps à attendre les données du disque dur.",
        "text_ar_1": "وحدة المعالجة المركزية (CPU) أو المعالج هي العقل المدبر للحاسوب، حيث تقوم بقراءة وفك تشفير وتنفيذ تعليمات البرامج البرمجية. تقاس سرعة المعالج بالغيغاهرتز (GHz)، وتحتوي المعالجات الحديثة على عدة أنوية حوسبة لمعالجة مهام متعددة في آن واحد بشكل متوازٍ.",
        "text_ar_2": "ذاكرة الوصول العشوائي (RAM) هي ذاكرة تخزين مؤقتة وسريعة تحفظ البيانات والبرامج النشطة التي يحتاجها المعالج فوراً. وهي ذاكرة متطايرة، مما يعني أنها تفقد كافة محتوياتها بمجرد إيقاف تشغيل الحاسوب، وتختلف عن وحدات التخزين الدائمة كالأقراص الصلبة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chno howa l'far9 bin l'processeur CPU w l'RAM f l'pc?",
                "ma_mix": "chno howa le rôle dyal la RAM w le processeur CPU f l'ordinateur?",
                "dz_ar": "wech el far9 bin le processeur wel mémoire vive RAM?",
                "dz_mix": "wech houwa le travail ta3 le processeur m3a la RAM?",
                "tn_ar": "chnowa el far9 bin le processeur wel RAM fel pc?",
                "tn_mix": "chnowa le rôle mte3 la mémoire vive RAM fel ordinateur?",
                "fr": "Quelle est la différence de rôle entre le processeur (CPU) et la mémoire vive (RAM) d'un ordinateur ?",
            },
        ],
    },
    {
        "id": "reseau_ip",
        "domain": "informatique",
        "title_fr": "Réseaux informatiques et protocole IP",
        "title_ar": "الشبكات الحاسوبية وبروتوكول الإنترنت",
        "text_fr_1": "Internet est un réseau mondial de réseaux informatiques interconnectés utilisant la suite de protocoles TCP/IP pour échanger des données. Chaque appareil connecté possède une adresse IP (Internet Protocol) unique qui permet de l'identifier et d'acheminer les paquets d'information jusqu'à destination via des routeurs.",
        "text_fr_2": "Le protocole IPv4 utilise des adresses sur 32 bits écrites sous forme de quatre nombres séparés par des points (ex. 192.168.1.1), offrant environ 4,3 milliards d'adresses. Le protocole IPv6, codé sur 128 bits, a été développé pour pallier l'épuisement des adresses IPv4 et prend en charge une quantité quasi illimitée d'adresses.",
        "text_ar_1": "الإنترنت هي شبكة عالمية من الحواسيب المترابطة التي تتواصل فيما بينها باستخدام حزمة بروتوكولات TCP/IP. يمتلك كل جهاز متصل بالشبكة عنوان بروتوكول إنترنت (IP) فريداً يتيح توجيه رزم البيانات عبر أجهزة التوجيه (الموجهات) من المصدر إلى الهدف.",
        "text_ar_2": "يستخدم نظام IPv4 عناوين تتألف من 32 بت تُكتب على شكل أربعة أرقام تفصل بينها نقاط (مثل 192.168.1.1)، ويوفر حوالي 4.3 مليار عنوان. ونظراً لنفاد هذه العناوين، تم تطوير بروتوكول IPv6 المكون من 128 بت ليوفر عدداً هائلاً من العناوين الرقمية للأجهزة الحديثة.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "kifach kayt3araf l'adresse IP dyal un appareil f l'internet?",
                "ma_mix": "chno howa le rôle d'une adresse IP f le réseau Internet?",
                "dz_ar": "wech hiya l'adresse IP w kifech tconnecti les ordinateurs?",
                "dz_mix": "wech houwa le protocole TCP/IP fel internet?",
                "tn_ar": "chnowa ma3neha adresse IP w kifeh tab3ath les paquets?",
                "tn_mix": "chnowa le rôle mte3 l'adresse IP f les réseaux informatiques?",
                "fr": "Qu'est-ce qu'une adresse IP et à quoi sert-elle dans un réseau informatique ?",
            },
        ],
    },
    {
        "id": "base_de_donnees",
        "domain": "informatique",
        "title_fr": "Bases de données relationnelles et SQL",
        "title_ar": "قواعد البيانات العلائقية ولغة الاستعلام",
        "text_fr_1": "Une base de données relationnelle organise les informations sous forme de tables composées de lignes (enregistrements) et de colonnes (champs). Chaque table possède généralement une clé primaire qui identifie de manière unique chaque ligne, et des clés étrangères qui établissent des relations avec d'autres tables.",
        "text_fr_2": "Le langage SQL (Structured Query Language) est le standard utilisé pour interroger, insérer, modifier et administrer les bases de données relationnelles. La commande SELECT permet d'extraire des données en spécifiant des filtres (WHERE), des regroupements (GROUP BY) et des jointures (JOIN).",
        "text_ar_1": "تنظم قاعدة البيانات العلائقية البيانات والمعلومات في جداول تتكون من صفوف (سجلات) وأعمدة (حقول). يمتلك كل جدول مفتاحاً أساسياً يحدد كل سجل بشكل فريد، ومفاتيح أجنبية لربط الجداول وإقامة علاقات منطقية فيما بينها.",
        "text_ar_2": "تعتبر لغة SQL (لغة الاستعلام البنيوية) المعيار العالمي لإدارة واسترجاع وتعديل قواعد البيانات العلائقية. تتيح عبارة SELECT استخراج البيانات بدقة عبر تطبيق شروط وتصفية معينة وربط السجلات بين عدة جداول عبر عمليات الربط JOIN.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "kifach katssra la liaison bin les tables f base de données b les clés?",
                "ma_mix": "kifach kanst3mlo la clé primaire w la clé étrangère f une base de données SQL?",
                "dz_ar": "wech houwa le rôle ta3 la clé primaire fel base de données relationnelle?",
                "dz_mix": "kifech nsta3mlou la commande SQL SELECT w les jointures JOIN?",
                "tn_ar": "chnowa el far9 bin clé primaire w clé étrangère f base de données?",
                "tn_mix": "kifeh nesta3mlou SQL SELECT bech nkharjou les données?",
                "fr": "Quel est le rôle de la clé primaire et de la clé étrangère dans une base de données relationnelle SQL ?",
            },
        ],
    },

    # Histoire des sciences (4)
    {
        "id": "revolution_copernic",
        "domain": "histoire",
        "title_fr": "Révolution copernicienne et héliocentrisme",
        "title_ar": "الثورة الكوبرنيكية ونموذج مركزية الشمس",
        "text_fr_1": "La révolution copernicienne marque le passage historique du modèle géocentrique de Ptolémée (où la Terre était supposée immobile au centre de l'univers) au modèle héliocentrique proposé par Nicolas Copernic en 1543, dans lequel la Terre et les planètes tournent autour du Soleil.",
        "text_fr_2": "Cette théorie a été confortée par les observations astronomiques de Galilée grâce à sa lunette (notamment les lunes de Jupiter et les phases de Vénus), puis formalisée par les lois mathématiques de Johannes Kepler sur les orbites elliptiques et par la mécanique de Newton.",
        "text_ar_1": "تمثل الثورة الكوبرنيكية نقطة تحول كبرى في تاريخ العلوم بانتقال علم الفلك من نموذج مركزية الأرض البطلمي القديم (الذي يفترض سكون الأرض في مركز الكون) إلى نموذج مركزية الشمس الذي اقترحه نيكولاس كوبرنيكوس عام 1543، مبيناً دوران الأرض والكواكب حول الشمس.",
        "text_ar_2": "تعزز هذا النموذج العلمي بفضل الاكتشافات الفلكية لغاليليو غاليلي بواسطة التلسكوب، كأقمار المشتري وأطوار كوكب الزهرة، ثم تمت صياغته رياضياً من خلال قوانين كبلر لحركة الكواكب في مدارات إهليلجية، وتوج بنظرية نيوتن للجاذبية.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chkoun houwa Copernic w kifach bddel l'fikra 3la chems w l'ard?",
                "ma_mix": "chkoun howa Copernic w chno houwa l'héliocentrisme?",
                "dz_ar": "wech hiya la théorie ta3 Copernic 3la la Terre wel Soleil?",
                "dz_mix": "wech houwa le modèle héliocentrique ta3 Copernic w Galilée?",
                "tn_ar": "chkoun Copernic w kifeh 9al el ard tdour 7awl echams?",
                "tn_mix": "chnowa l'héliocentrisme mte3 Copernic fel astronomie?",
                "fr": "Qu'est-ce que la révolution copernicienne et qu'affirme le modèle héliocentrique ?",
            },
        ],
    },
    {
        "id": "revolution_industrielle",
        "domain": "histoire",
        "title_fr": "Révolution industrielle et machine à vapeur",
        "title_ar": "الثورة الصناعية والآلة البخارية",
        "text_fr_1": "La première révolution industrielle a débuté en Grande-Bretagne à la fin du XVIIIe siècle, stimulée par le perfectionnement de la machine à vapeur par James Watt en 1769. La vapeur a fourni une source d'énergie mécanique inanimée bien supérieure à la force musculaire, animale ou hydraulique.",
        "text_fr_2": "Cette mutation technologique a transformé l'industrie textile, la métallurgie du fer et les transports avec l'apparition du chemin de fer et des bateaux à vapeur. Elle a entraîné l'urbanisation rapide des populations et l'essor de la production industrielle de masse.",
        "text_ar_1": "انطلقت الثورة الصناعية الأولى في بريطانيا أواخر القرن الثامن عشر، وكان المحرك الأساسي لها تطوير جيمس واط للآلة البخارية عام 1769، مما أتاح مصدراً غير مسبوق للطاقة الميكانيكية فاق قدرات الجهد العضلي وطاقة الرياح والمياه.",
        "text_ar_2": "أحدث هذا التحول التكنولوجي ثورة كبرى في صناعة الغزل والنسيج وصهر الحديد، وأدى لظهور السكك الحديدية والقاطرات البخارية، وأسفر عن تسارع الهجرة القروية نحو المدن ونشأة نمط الإنتاج الصناعي الكثيف.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "fin bdat thawra ssi3aniyya w chno khtare3 James Watt?",
                "ma_mix": "fin bdat la révolution industrielle w chno hiya la machine à vapeur?",
                "dz_ar": "win bdat la révolution industrielle w wech faydet la machine à vapeur?",
                "dz_mix": "kifech bddlet la machine à vapeur de James Watt l'industrie?",
                "tn_ar": "win bdet eth-thawra essina3iya w chnowa l'invention mte3 James Watt?",
                "tn_mix": "kifeh badlet la machine à vapeur mte3 James Watt le transport wel industrie?",
                "fr": "Où a commencé la révolution industrielle et quel a été le rôle de la machine à vapeur de James Watt ?",
            },
        ],
    },
    {
        "id": "penicilline_fleming",
        "domain": "histoire",
        "title_fr": "Découverte de la pénicilline et antibiotiques",
        "title_ar": "اكتشاف البنسلين والمضادات الحيوية",
        "text_fr_1": "La pénicilline est le premier antibiotique naturel découvert en 1928 par le médecin biologiste britannique Alexander Fleming. Fleming a remarqué qu'une moisissure accidentellement développée sur une boîte de culture de staphylocoques, le champignon Penicillium notatum, empêchait la croissance des bactéries autour d'elle.",
        "text_fr_2": "Purifiée et produite industriellement à partir des années 1940 par Howard Florey et Ernst Chain, la pénicilline a sauvé des millions de vies pendant et après la Seconde Guerre mondiale en traitant efficacement des infections bactériennes jusque-là mortelles (pneumonie, méningite, gangrène).",
        "text_ar_1": "البنسلين هو أول مضاد حيوي طبيعي تم اكتشافه عام 1928 على يد الطبيب البريطاني ألكسندر فلمنج. لاحظ فلمنج مصادفة أن فطر عفن يسمى Penicillium notatum نما في طبق بتري يحتوي على بكتيريا المكورات العنقودية وأفرز مادة أوقفت نمو البكتيريا وقضت عليها.",
        "text_ar_2": "تمت تنقية البنسلين وإنتاجه على نطاق صناعي واسع في الأربعينيات بجهود هوارد فلوري وإرنست تشين، مما أنقذ حياة الملايين خلال الحرب العالمية الثانية وما بعدها من خلال علاج أمراض بكتيرية فتاكة كالالتهاب الرئوي والحمى القرمزية والغرغرينا.",
        "items": [
            {
                "level": "debutant",
                "ma_ar": "chkoun khtare3 l'pénicilline w kifach l9aha Alexander Fleming?",
                "ma_mix": "chkoun khtafe3 la pénicilline w chno howa l'antibiotique?",
                "dz_ar": "chkoun li l9a la pénicilline w kifech te9di 3la les bactéries?",
                "dz_mix": "kifech khtara3 Fleming le premier antibiotique la pénicilline?",
                "tn_ar": "chkoun ktechef la pénicilline w kifeh Fleming l9aha bel sodfa?",
                "tn_mix": "chkoun ktechef le premier antibiotique la pénicilline en 1928?",
                "fr": "Qui a découvert la pénicilline en 1928 et comment agit ce premier antibiotique ?",
            },
        ],
    },
    {
        "id": "revolution_francaise_sciences",
        "domain": "histoire",
        "title_fr": "La Révolution française et le système métrique",
        "title_ar": "الثورة الفرنسية والنظام المتري العشري",
        "text_fr_1": "Pendant la Révolution française déclenchée en 1789, les savants de l'Académie des sciences ont créé en 1795 le système métrique décimal afin d'unifier les unités de mesure disparates sous l'Ancien Régime. Le mètre a été défini comme la dix-millionième partie du quart du méridien terrestre.",
        "text_fr_2": "Des scientifiques éminents comme Antoine Lavoisier (père de la chimie moderne qui formula la loi de conservation de la masse : rien ne se perd, rien ne se crée, tout se transforme), Laplace et Condorcet ont profondément marqué cette période avant les excès de la Terreur.",
        "text_ar_1": "خلال أحداث الثورة الفرنسية عام 1789، قام علماء أكاديمية العلوم بابتكار النظام المتري العشري عام 1795 لتوحيد المكاييل والموازين التي كانت متباينة وفوضوية. عُرف المتر آنذاك بأنه جزء من عشرة ملايين جزء من مسافة ربع خط الزوال الأرضي.",
        "text_ar_2": "برز في تلك الحقبة علماء أفذاذ في طليعتهم أنطوان لافوازييه، مؤسس الكيمياء الحديثة وصاحب القانون الشهير لحفظ الكتلة (لا شيء يضيع، لا شيء يُخلق، كل شيء يتحول)، إلى جانب الرياضي لابلاس والفيلسوف كوندورسيه.",
        "items": [
            {
                "level": "intermediaire",
                "ma_ar": "wesh thawra l'franssiya d 1789 bddlat l'wazn w l'kail b le mètre?",
                "ma_mix": "kifach la Révolution française khtal9at le système métrique décimal?",
                "dz_ar": "wech dert la révolution française fel math w la chimie kima Lavoisier?",
                "dz_mix": "kifech ban le système métrique décimal fel révolution française?",
                "tn_ar": "kifeh thawret 1789 f fransa badlet el mizan wel mètre?",
                "tn_mix": "kifeh tssana3 le système métrique fel Révolution française m3a Lavoisier?",
                "fr": "Comment la Révolution française a-t-elle conduit à la création du système métrique décimal ?",
            },
        ],
    },
]


def generate_benchmark_corpus(out_path: str):
    """Génère le corpus éducatif bilingue (120 passages sur 30 concepts)."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    count = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for c in CONCEPTS:
            cid = c["id"]
            # 2 passages FR
            p_fr_1 = {
                "id": f"fr::{cid}::p1",
                "lang": "fr",
                "domain": c["domain"],
                "topic": cid,
                "title": c["title_fr"],
                "text": c["text_fr_1"],
                "source": "educational_corpus",
            }
            p_fr_2 = {
                "id": f"fr::{cid}::p2",
                "lang": "fr",
                "domain": c["domain"],
                "topic": cid,
                "title": c["title_fr"],
                "text": c["text_fr_2"],
                "source": "educational_corpus",
            }
            # 2 passages AR
            p_ar_1 = {
                "id": f"ar::{cid}::p1",
                "lang": "ar",
                "domain": c["domain"],
                "topic": cid,
                "title": c["title_ar"],
                "text": c["text_ar_1"],
                "source": "educational_corpus",
            }
            p_ar_2 = {
                "id": f"ar::{cid}::p2",
                "lang": "ar",
                "domain": c["domain"],
                "topic": cid,
                "title": c["title_ar"],
                "text": c["text_ar_2"],
                "source": "educational_corpus",
            }
            for p in (p_fr_1, p_fr_2, p_ar_1, p_ar_2):
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
                count += 1
    print(f"Corpus généré : {count} passages écrits dans {out_path}")


def generate_benchmark_queries(out_csv_path: str):
    """Génère 100 items (34 Marocains, 33 Algériens, 33 Tunisiens) = 300 requêtes annotées."""
    # Collect all items
    raw_items = []
    for c in CONCEPTS:
        cid = c["id"]
        for it in c["items"]:
            raw_items.append((cid, it))

    # Duplicate / cycle to reach exactly 100 items
    all_100_items = []
    idx = 0
    while len(all_100_items) < 100:
        base_cid, base_it = raw_items[idx % len(raw_items)]
        variant_idx = len(all_100_items) // len(raw_items)
        all_100_items.append((base_cid, base_it, variant_idx))
        idx += 1

    # Attribution des dialectes : exactement 34 MA, 33 DZ, 33 TN (Table 2 du manuscrit)
    # 34 Marocains (items 1 à 34)
    # 33 Algériens (items 35 à 67)
    # 33 Tunisiens (items 68 à 100)
    rows = []
    item_num = 1
    for cid, it, var_idx in all_100_items:
        if item_num <= 34:
            dialect = "darija_maroc"
            ar_text = it["ma_ar"]
            mix_text = it["ma_mix"]
        elif item_num <= 67:
            dialect = "darija_algerie"
            ar_text = it["dz_ar"]
            mix_text = it["dz_mix"]
        else:
            dialect = "darija_tunisie"
            ar_text = it["tn_ar"]
            mix_text = it["tn_mix"]

        level = it["level"]
        item_id = f"ITEM_{item_num:03d}"
        relevant_p1 = f"fr::{cid}::p1"
        relevant_p2 = f"fr::{cid}::p2"
        relevant_ar1 = f"ar::{cid}::p1"
        relevant_ar2 = f"ar::{cid}::p2"

        # Relevant string: document:grade (grade 2 pour direct, 1 pour partiel)
        # Format compact: "doc1:2;doc2:2;doc3:1;doc4:1"
        rel_str = f"{relevant_p1}:2;{relevant_ar1}:2;{relevant_p2}:1;{relevant_ar2}:1"

        # Version Arabizi
        rows.append({
            "item_id": item_id,
            "query_id": f"{item_id}_ARABIZI",
            "query_type": "arabizi",
            "dialect": dialect,
            "learner_level": level,
            "topic": cid,
            "query_text": ar_text,
            "relevant_ids": rel_str,
        })
        # Version Mixte
        rows.append({
            "item_id": item_id,
            "query_id": f"{item_id}_MIXED",
            "query_type": "mixed",
            "dialect": dialect,
            "learner_level": level,
            "topic": cid,
            "query_text": mix_text,
            "relevant_ids": rel_str,
        })
        # Version Française
        rows.append({
            "item_id": item_id,
            "query_id": f"{item_id}_FR",
            "query_type": "fr",
            "dialect": dialect,  # Dialect group from item (for pairing as described in Section 5.4)
            "learner_level": level,
            "topic": cid,
            "query_text": it["fr"],
            "relevant_ids": rel_str,
        })

        item_num += 1

    os.makedirs(os.path.dirname(out_csv_path), exist_ok=True)
    with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "item_id",
                "query_id",
                "query_type",
                "dialect",
                "learner_level",
                "topic",
                "query_text",
                "relevant_ids",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Jeu de requêtes généré : {len(rows)} requêtes (100 items x 3 versions) écrites dans {out_csv_path}")


if __name__ == "__main__":
    generate_benchmark_corpus("data/corpus_educational.jsonl")
    generate_benchmark_queries("data/queries_benchmark.csv")
