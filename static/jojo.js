function jojoPortrait(char) {
  const mark = (char.mark || char.name.slice(0, 1)).replace(/[&<>"']/g, "");
  const color = char.color || "#2e7d32";
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 280">
    <defs>
      <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="${color}"/>
        <stop offset="100%" stop-color="#0d1a12"/>
      </linearGradient>
    </defs>
    <rect width="240" height="280" fill="url(#g)"/>
    <circle cx="120" cy="108" r="54" fill="rgba(255,255,255,0.92)"/>
    <text x="120" y="124" text-anchor="middle" font-size="42" font-family="IBM Plex Sans Arabic, sans-serif" fill="${color}">${mark}</text>
    <rect x="24" y="188" width="192" height="6" rx="3" fill="rgba(255,255,255,0.35)"/>
    <text x="120" y="230" text-anchor="middle" font-size="18" font-family="IBM Plex Sans Arabic, sans-serif" fill="#fff">${char.name}</text>
  </svg>`;
  return "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg);
}

const JOJO_DATA = [
  {
    part: "الجزء 1",
    title: "Phantom Blood",
    year: "1880 — إنجلترا",
    color: "#1a237e",
    story: "تبدأ الملحمة في إنجلترا الفيكتورية. جوناثان جوستار النبيل يصطدم بديو براندو، اليتيم الطموح الذي دخل البيت ليسرقه من الداخل. بعد القناع الحجري وتحوّل ديو لمصاص دماء، يتعلّم جوناثان طاقة التموج من زيبيلي ويخوض صراعاً على شرف العائلة ومصير من يحبهم.",
    people: [
      { name: "جوناثان جوستار", mark: "ج", color: "#1565c0", role: "البطل", align: "طيب", stand: "التموج / Hamon", tier: "main", desc: "ابن عائلة جوستار. قلبه نظيف وإرادته ثابتة حتى وهو يخسر. يتعلّم التموج ليحارب الظلام، ويضحّي بنفسه أكثر من مرة من أجل إيرينا ومن أجل ألا يورّث الشر لأجيال بعده." },
      { name: "ديو براندو", mark: "د", color: "#b71c1c", role: "الخصم", align: "شرير", stand: "القناع الحجري", tier: "main", desc: "نشأ فقيراً وقرر أن العالم يُؤخذ بالقوة. يدخل بيت جوستار كابن متبنى، ثم يحوّل نفسه لمصاص دماء. ذكي، متكبّر، ويكره جوناثان لأنه يذكّره بما لا يستطيع أن يكونه." },
      { name: "إيرينا بندلتون", mark: "إ", color: "#ec407a", role: "الحبيبة", align: "طيبة", stand: "—", tier: "main", desc: "خطيبة جوناثان. صلبة وهادئة، وتصير لاحقاً أمّ السلالة التي تكمل القصة بعد نهاية الجزء الأول." },
      { name: "ويل أ. زيبيلي", mark: "ز", color: "#ef6c00", role: "المعلم", align: "طيب", stand: "التموج", tier: "side", desc: "فارس إيطالي ومعلم التموج. يدرّب جوناثان بصرامة، ويموت وهو يمرّر طاقته وتجربته لتلميذه." },
      { name: "روبرت سبيدواغن", mark: "س", color: "#546e7a", role: "الصديق", align: "طيب", stand: "—", tier: "side", desc: "لص شوارع صار أصدق أصدقاء جوناثان. لا يملك قوى خارقة، لكن ولاءه يؤسس لاحقاً مؤسسة سبيدواغن التي تحمي العائلة." },
      { name: "جورج جوستار الأول", mark: "و", color: "#5d4037", role: "الأب", align: "طيب", stand: "—", tier: "side", desc: "والد جوناثان. طيب لدرجة تُستغل. تبنّى ديو بحسن نية ودفع الثمن." },
      { name: "جاك السفاح", mark: "ك", color: "#4a148c", role: "قاتل", align: "شرير", stand: "زومبي", tier: "side", desc: "قاتل متسلسل يستعين به ديو. يمثل الجانب القذر من لندن اللي يختبئ تحت الطبقة النبيلة." },
      { name: "تاركوس و بروفورد", mark: "ف", color: "#37474f", role: "فرسان الظلام", align: "شرير", stand: "زومبي", tier: "side", desc: "فرسان قدامى أُحيوا كزومبي. بروفورد يحتفظ بشرفه حتى بعد الموت، وتاركوس يمثل القوة الغاشمة." },
      { name: "بوكو", mark: "ب", color: "#00838f", role: "طفل القرية", align: "طيب", stand: "—", tier: "side", desc: "صبي ينقذه جوناثان. حضوره يذكّر إن المعركة مو بس بين أبطال، فيها ناس عاديين لازم يعيشون." },
      { name: "داير", mark: "ر", color: "#6a1b9a", role: "معلم تموج", align: "طيب", stand: "التموج", tier: "side", desc: "أحد معلمي التموج الكبار. يظهر ليثبت إن الفن أقدم من جوناثان، وأن الحرب ضد القناع لها تاريخ." }
    ]
  },
  {
    part: "الجزء 2",
    title: "Battle Tendency",
    year: "1938 — أمريكا / أوروبا",
    color: "#2e7d32",
    story: "جوزيف جوستار، حفيد جوناثان، يواجه رجال العمود: كائنات حجرية قديمة أقوى من مصاصي الدماء. السباق على جوهرة أجا المكسوة يدفع جوزيف وسيزار وليزا ليزا لقتال ومو وإيسيديسي وكارس قبل أن يصل أحدهم للكمال ويطفئ الشمس كعدو.",
    people: [
      { name: "جوزيف جوستار", mark: "ج", color: "#43a047", role: "البطل", align: "طيب", stand: "التموج + الحيلة", tier: "main", desc: "مرح، وقح، وماكر. يتوقع جملة الخصم قبل ما يقولها. قوته مو العضلات قد ما هي الارتجال والخداع حتى وهو مرعوب." },
      { name: "كارس", mark: "ك", color: "#6a1b9a", role: "الخصم", align: "شرير", stand: "الكائن المطلق", tier: "main", desc: "زعيم رجال العمود ومخترع القناع الحجري. هدفه يتجاوز الشر العادي: يبي يصير كائناً كاملاً لا تقتله الشمس." },
      { name: "سيزار أ. زيبيلي", mark: "س", color: "#0277bd", role: "الرفيق", align: "طيب", stand: "تموج الفقاعات", tier: "main", desc: "حفيد ويل زيبيلي. أنيق وفخور، يت spar مع جوزيف ثم يصير أخاه في المعركة. تضحيته من أقوى لحظات الجزء." },
      { name: "ليزا ليزا", mark: "ل", color: "#ad1457", role: "المعلمة", align: "طيبة", stand: "التموج", tier: "side", desc: "معلمة صارمة وغامضة. درّبت جوزيف وسيزار على جزيرة نائية، وسرّها العائلي يربط الجزء الثاني بالأول." },
      { name: "رودول فون شترونهيم", mark: "ش", color: "#455a64", role: "حليف مؤقت", align: "رمادي", stand: "الجسد الآلي", tier: "side", desc: "ضابط ألماني يتحوّل لآلة بعد هزيمته. عدو ثم حليف براغماتي ضد رجال العمود." },
      { name: "وامو", mark: "و", color: "#f9a825", role: "محارب", align: "شرير شريف", stand: "الريح", tier: "side", desc: "محارب رجال العمود الأكثر شرفاً. يحترم الخصم القوي، ومعركته مع جوزيف أقرب لمبارزة منها لجريمة." },
      { name: "إيسيديسي", mark: "إ", color: "#bf360c", role: "محارب", align: "شرير", stand: "الدم المغلي", tier: "side", desc: "يتحكم بدمه كسلاح وسخّان. أذكى من مظهره الهمجي، ويحب اللعب النفسي." },
      { name: "سانتانا", mark: "ت", color: "#4e342e", role: "رجل عمود", align: "شرير", stand: "الامتصاص", tier: "side", desc: "أول رجل عمود يظهر في أمريكا. يبتلع الأجساد ويتعلّم بسرعة مخيفة." },
      { name: "سموكي براون", mark: "م", color: "#6d4c41", role: "صديق", align: "طيب", stand: "—", tier: "side", desc: "شاب أمريكي يساعد جوزيف في البداية. يمثل الجانب الإنساني البسيط قبل ما تكبر الحرب." },
      { name: "سوزي كيو", mark: "ي", color: "#8e24aa", role: "حبيبة جوزيف", align: "طيبة", stand: "—", tier: "side", desc: "تكمل بيت جوزيف وليزا ليزا. خفيفة الظل، وتصير جزءاً من عائلة جوستار بعدها." },
      { name: "سترايزو", mark: "ز", color: "#880e4f", role: "خائن", align: "شرير", stand: "التموج + القناع", tier: "side", desc: "رفيق قديم لزيبيلي خان الطريق واستخدم القناع. جسده يربط الماضي بالحاضر." }
    ]
  },
  {
    part: "الجزء 3",
    title: "Stardust Crusaders",
    year: "1989 — اليابان إلى مصر",
    color: "#fbc02d",
    story: "بعد مئة سنة يظهر الستاند. جوتارو كوجو ورفاقه يسافرون من اليابان لمصر لإنقاذ هولي، والدة جوتارو، قبل أن يقتلها حضور ديو العائد بجسد جوناثان. الرحلة سلسلة كمائن ستاند، وكل مدينة تضيف رفيقاً أو تأخذ ثمناً.",
    people: [
      { name: "جوتارو كوجو", mark: "ج", color: "#1565c0", role: "البطل", align: "طيب", stand: "ستار بلاتينوم", tier: "main", desc: "طالب ثانوية يبدو بارداً ووقحاً. ستانده قريب المدى، سريع وقاسٍ، ثم يتعلّم إيقاف الزمن في المواجهة الأخيرة. يكره الظلم أكثر مما يحب الكلام." },
      { name: "ديو / DIO", mark: "د", color: "#c62828", role: "الخصم", align: "شرير", stand: "ذا وورلد", tier: "main", desc: "عاد من التابوت بجسد جوناثان. ستانده يوقف الزمن. لم يعد مجرد مصاص دماء: صار رمزاً للقدر اللي يطارد العائلة جيلاً بعد جيل." },
      { name: "جوزيف جوستار", mark: "و", color: "#2e7d32", role: "الجد", align: "طيب", stand: "هيرميت بيربل", tier: "main", desc: "صار عجوزاً وما زال يحتال. ستانده الشوكي يقرأ الأرواح ويصوّر الخصم. حكمته وصخبه يمسكان الفريق." },
      { name: "نوريأكي كاكيوين", mark: "ك", color: "#6a1b9a", role: "رفيق", align: "طيب", stand: "هايروفانت غرين", tier: "side", desc: "طالب أنيق كان تحت سيطرة ديو ثم انضم للفريق. ستانده بعيد المدى، ومعركته الأخيرة من أكثر المشاهد إخلاصاً." },
      { name: "محمد أفدول", mark: "أ", color: "#ef6c00", role: "رفيق", align: "طيب", stand: "ماجيشانز ريد", tier: "side", desc: "عرّاف مصري صديق جوزيف. ناره تكشف الطريق، وهدوؤه يوازن تهوّر الآخرين." },
      { name: "جان بيير بولناريف", mark: "ب", color: "#546e7a", role: "رفيق", align: "طيب", stand: "سيلفر تشاريوت", tier: "side", desc: "مبارز فرنسي يثأر لأخته. ستانده سيف سريع. كوميدي في السلم، عنيد في الحرب." },
      { name: "إيغي", mark: "ي", color: "#5d4037", role: "الكلب", align: "طيب", stand: "ذا فول", tier: "side", desc: "كلب بوسطن تيرير يكره البشر ويحب القهوة. ستانده رمل. ينضج من أناني صغير إلى رفيق يضحّي." },
      { name: "هولي كوجو", mark: "ه", color: "#ec407a", role: "الأم", align: "طيبة", stand: "ستاند غير متحكم", tier: "side", desc: "ابنة جوزيف وأم جوتارو. روحها طيبة زيادة، فستانده يؤذيها بدل ما يحميها. الرحلة كلها سباق لإنقاذها." },
      { name: "فانيلا آيس", mark: "ف", color: "#311b92", role: "حارس ديو", align: "شرير", stand: "كريم", tier: "side", desc: "أشد أتباع ديو إخلاصاً. ستانده يبتلع المكان ويفتح فراغاً أسود. معركته تكلّف الفريق غالياً." },
      { name: "هول هورس", mark: "ح", color: "#ff8f00", role: "مرتزق", align: "رمادي", stand: "إمبيرور", tier: "side", desc: "مُسدّس حي. جبان وماكر ويحب النجاة أكثر من الولاء. يظهر أكثر من مرة ويكسر توقع «العدو يموت ويختفي»." },
      { name: "ن دول", mark: "ن", color: "#00695c", role: "عدو", align: "شرير", stand: "جيبوغراف", tier: "side", desc: "أعمى يستخدم الماء كرادار وقاتل. من أقوى افتتاحيات أعداء الرحلة." },
      { name: "ماريا", mark: "ر", color: "#8e24aa", role: "عدوة", align: "شريرة", stand: "باستيت", tier: "side", desc: "تحوّل الناس لمغناطيس. معركة مدنية خانقة داخل المدينة." }
    ]
  },
  {
    part: "الجزء 4",
    title: "Diamond is Unbreakable",
    year: "1999 — موريو، اليابان",
    color: "#8e24aa",
    story: "جوسكي هيغاشيكاتا يعيش في بلدة هادئة تخفي مستخدمي ستاند وقاتلاً يريد حياة عادية بأي ثمن. الجزء أقرب لقصص مدينة: جيران، مدرسة، قهوة، ثم فجأة قنبلة في المطبخ. جوتارو يأتي للتحقيق، والبلدة تكشف أسنانها.",
    people: [
      { name: "جوسكي هيغاشيكاتا", mark: "ج", color: "#7b1fa2", role: "البطل", align: "طيب", stand: "كريزي دايموند", tier: "main", desc: "يغضب إذا انمسّت تسريحته. ستانده يصلح الأشياء والأجساد، لكنه يصلح بعنف. طيب الجو، وخطير إذا انهان أحد من مدينته." },
      { name: "يوشيكاغي كيرا", mark: "ق", color: "#f9a825", role: "الخصم", align: "شرير", stand: "كيلر كوين", tier: "main", desc: "موظف يريد الهدوء أكثر من السيطرة على العالم. يقتل ليحافظ على روتينه. ستانده يحوّل أي شيء يلمسه إلى قنبلة، ثم يتطور لشيرا هيم." },
      { name: "أوكوياسو نيجيمورا", mark: "أ", color: "#1565c0", role: "الصديق", align: "طيب", stand: "ذا هاند", tier: "main", desc: "يبدو غبياً وقاسياً، وقلبه أكبر من رأسه. ستانده يمسح المسافة. صداقته مع جوسكي عمود الجزء العاطفي." },
      { name: "كويتشي هيروسي", mark: "ك", color: "#00897b", role: "الصديق", align: "طيب", stand: "إيكو إيكو", tier: "side", desc: "الجبان الذي يكبر أمامنا. ستانده يتطور ثلاث مرات: صوت، وزن، ثم دفاع هجومي. دليل إن القوة تجي من القرار مو من الشكل." },
      { name: "روهان كيشيبي", mark: "ر", color: "#2e7d32", role: "حليف", align: "رمادي", stand: "هيفنز دور", tier: "side", desc: "مانغاكا متعجرف يكتب الناس كصفحات. ستانده يقرأ الذكريات ويكتب أوامر على أجسادهم. مفيد وخطر في نفس الوقت." },
      { name: "جوتارو كوجو", mark: "ت", color: "#283593", role: "المحقّق", align: "طيب", stand: "ستار بلاتينوم", tier: "side", desc: "يرجع لموريو كبالغ هادئ. دوره المرشد أكثر من النجم، ويسلّم المسرح لجوسكي." },
      { name: "يوكاكو ياماغشي", mark: "ي", color: "#c2185b", role: "حبيبة كويتشي", align: "رمادية", stand: "لاف ديلوكس", tier: "side", desc: "هوسها مرعب في البداية، ثم يصير حباً ناضجاً. شعرها سلاح." },
      { name: "شيغيتشي", mark: "ش", color: "#558b2f", role: "حليف", align: "طيب", stand: "هارفست", tier: "side", desc: "طفل مستهتر بستاند من مئات الأجزاء الصغيرة. موته يغيّر نبرة المدينة كلها." },
      { name: "تونو تراتي", mark: "ط", color: "#ef6c00", role: "طبّاخ", align: "طيب", stand: "بيرل جام", tier: "side", desc: "طاهٍ إيطالي طعامه يشفي ويكشف أسرار الجسد. حلقة دافئة وسط التوتر." },
      { name: "هاياتو كاواجيتي", mark: "ه", color: "#5d4037", role: "شاهد", align: "طيب", stand: "—", tier: "side", desc: "ابن عائلة كيرا بالتبني. ذكي ومرعوب، ومفتاح إسقاط القاتل وهو طفل." },
      { name: "أكيرا أوتويشي", mark: "ع", color: "#6a1b9a", role: "عدو", align: "شرير", stand: "ريد هوت تشيلي بيبر", tier: "side", desc: "عازف يسرق الكهرباء. من أقوى أعداء منتصف الجزء." },
      { name: "ميكيتاكا هازيكورا", mark: "م", color: "#0097a7", role: "غريب", align: "غامض", stand: "أو فضائي؟", tier: "side", desc: "شكل آخر للغموض في موريو: هل هو مستخدم ستاند أم شيء لا ينتمي للأرض؟" }
    ]
  },
  {
    part: "الجزء 5",
    title: "Golden Wind",
    year: "2001 — إيطاليا",
    color: "#f9a825",
    story: "جورنو جيوفانا، ابن ديو من جسد جوناثان، يدخل عصابة باسوني لا ليصير مجرماً تقليدياً، بل ليسقط تجارة المخدرات من الداخل. الفريق يصير عائلة، والعدو الأكبر يختبئ حتى عن أقرب الناس له: الزعيم ديافولو.",
    people: [
      { name: "جورنو جيوفانا", mark: "ج", color: "#f9a825", role: "البطل", align: "طيب", stand: "غولد إكسبيرينس", tier: "main", desc: "هادئ وطموح بجملة واحدة: سيصل للقمّة. ستانده يعطي الحياة للجماد. حلمه مو المجد، هو أن يغيّر نوع الجريمة في إيطاليا." },
      { name: "ديافولو", mark: "د", color: "#b71c1c", role: "الخصم", align: "شرير", stand: "كينغ كريمسون", tier: "main", desc: "زعيم لا يريد أن يُرى. يمسح أجزاء من الزمن ويتنبّأ بالضربات. انقسامه مع دوبّيو يجعله عدواً لنفسه أيضاً." },
      { name: "برونو بوتشيلاتي", mark: "ب", color: "#1565c0", role: "القائد", align: "طيب", stand: "ستيكي فينغرز", tier: "main", desc: "السوستة التي تفتح الأماكن والأجساد. قائد عادل، يخون الزعيم يوم يخون الزعيم الناس. موته ومعناه محور الجزء." },
      { name: "غويدو ميستا", mark: "م", color: "#2e7d32", role: "قناص", align: "طيب", stand: "سكس بيستولز", tier: "side", desc: "يخاف الرقم 4 أكثر من الموت. رصاصاته كائنات حيّة. أظرف الجنود وأكثرهم ثباتاً تحت الضغط." },
      { name: "نارانشيا غيرغا", mark: "ن", color: "#6a1b9a", role: "رفيق", align: "طيب", stand: "آيروسميث", tier: "side", desc: "صغير، عصبي، ومخلص. طائرته المصغّرة تمسح الرادار وتقصف. قصته من أقسى قصص الفريق." },
      { name: "ليون أباكيو", mark: "أ", color: "#37474f", role: "رفيق", align: "طيب", stand: "مودي بلوز", tier: "side", desc: "شرطي سابق كسر نفسه ثم انضم لبرونو. ستانده يعيد تمثيل الماضي. كبرياؤه جرح مفتوح." },
      { name: "باناكوت فوغو", mark: "ف", color: "#c62828", role: "رفيق", align: "رمادي", stand: "بيربل هيز", tier: "side", desc: "العبقري الغاضب. فيروسه يذيب اللحم. يترك الفريق في لحظة حاسمة، وهذا القرار جزء من تراجيديا الجزء." },
      { name: "تريش أونا", mark: "ت", color: "#ec407a", role: "ابنة الزعيم", align: "طيبة", stand: "سبايس غيرل", tier: "side", desc: "تبدأ كـ«طرد» يجب إيصاله، وتصير مقاتلة تكسر الأشياء إلى ناعماً وتعيد تجميعها. بحثها عن هوية أقوى من نسبها." },
      { name: "دوبّيو", mark: "و", color: "#8d6e63", role: "الوجه الآخر", align: "مأسوي", stand: "كينغ كريمسون", tier: "side", desc: "الشخصية اللطيفة المنفصلة عن ديافولو. ضحية أكثر مما هو شرير، وجسر لفهم انقسام الزعيم." },
      { name: "ريزوتو نيرو", mark: "ز", color: "#212121", role: "قائد اغتيال", align: "شرير", stand: "ميتاليكا", tier: "side", desc: "يتحكم بحديد الدم. فريقه (فورماggio، جيوتشو، ميلوني...) من أقوى أعداء السلسلة كمجموعة." },
      { name: "بولناريف", mark: "ب", color: "#90a4ae", role: "الحارس", align: "طيب", stand: "سيلفر تشاريوت / ركويم", tier: "side", desc: "ناجي الجزء الثالث. يحرس السهم ويشرح ثمن القوة الجديدة. جسده مكسور وصوته ما زال حادّاً." },
      { name: "جيوتشو", mark: "ش", color: "#0277bd", role: "عدو", align: "شرير", stand: "وايت ألبوم", tier: "side", desc: "درع جليد يقترب من الصفر المطلق. معركة القطار من أشهر معارك الجزء." }
    ]
  },
  {
    part: "الجزء 6",
    title: "Stone Ocean",
    year: "2011 — فلوريدا",
    color: "#1565c0",
    story: "جولين كوجو تُسجن ظلماً في سجن جرين دولفين. تكتشف أن الزنزانة فخ رتبه القس إنريكو بوتشي، تلميذ ديو الروحي، ليسرق ذكريات جوتارو ويعيد ضبط الكون. الصداقة داخل السجن تصير خط الدفاع الأخير.",
    people: [
      { name: "جولين كوجو", mark: "ج", color: "#1565c0", role: "البطلة", align: "طيبة", stand: "ستون فري", tier: "main", desc: "ابنة جوتارو. حادّة اللسان وأصلب مما يظن أبوها. ستاندها يحوّل جسدها لخيوط: هروب، قيد، وخياطة للجروح في آن واحد." },
      { name: "إنريكو بوتشي", mark: "ب", color: "#311b92", role: "الخصم", align: "شرير", stand: "وايتسنيك / مييد هيفن", tier: "main", desc: "قس يؤمن بقدر مكتوب. يسرق الأقراص من الناس (ذكريات وستاند). هدفه ليس المال: إعادة خلق عالم «يعرف نهايته»." },
      { name: "إيرميس كوستيلو", mark: "إ", color: "#e65100", role: "صديقة", align: "طيبة", stand: "كيس", tier: "main", desc: "دخلت السجن للثأر. ملصقاتها تنسخ الأشياء. صداقتها مع جولين نواة الجزء النسائية القوية." },
      { name: "إمبوريو ألنيني", mark: "م", color: "#00838f", role: "طفل السجن", align: "طيب", stand: "بيرنينغ داون ذا هاوس", tier: "side", desc: "يعيش في غرفة مخفية بين الجدران. ستانده يحفظ أشياء من مكان محذوف. في النهاية يصير أهم شاهد على العالم." },
      { name: "فو فايترز", mark: "ف", color: "#2e7d32", role: "رفيقة", align: "طيبة", stand: "هي المستعمرة", tier: "side", desc: "عوالق ذكية لبست جسد سجينة. تتعلّم الإنسانية وهي تشرب ماءً كثيراً. من ألطف شخصيات السلسلة." },
      { name: "ويذر ريبورت", mark: "و", color: "#546e7a", role: "حليف", align: "مأسوي", stand: "ويذر ريبورت", tier: "side", desc: "فاقد ذاكرة يتحكم بالطقس. علاقته ببوتشي عائلية وموجعة. قدرته إذا انفلتت تدمّر أكثر مما تحمي." },
      { name: "ناركيسو أناسوي", mark: "أ", color: "#ad1457", role: "حليف", align: "رمادي", stand: "دايفر داون", tier: "side", desc: "يغوص داخل الأجسام ليعدّل تركيبها. حبه لجولين غريب وعنيف ومخلص في نفس الوقت." },
      { name: "جوتارو كوجو", mark: "ت", color: "#1a237e", role: "الأب", align: "طيب", stand: "ستار بلاتينوم", tier: "side", desc: "يحاول إنقاذ ابنته من خارج القضبان ثم من داخل المصيدة. دور الأب هنا أثقل من دور البطل." },
      { name: "سبورتس ماكس", mark: "س", color: "#4e342e", role: "عدو", align: "شرير", stand: "ليل بوم بوم", tier: "side", desc: "يوقظ الديناصورات من العظام. واحد من أعداء السجن الذين يحوّلون الفناء لمقبرة." },
      { name: "لانغ رانغلر", mark: "ل", color: "#006064", role: "حارس", align: "شرير", stand: "جوفربول", tier: "side", desc: "جاذبية انتقائية. يحوّل الممر العادي لكمّين فيزيائي." },
      { name: "فيرنز", mark: "ر", color: "#6a1b9a", role: "سجينة", align: "رمادية", stand: "ستاند صغير", tier: "side", desc: "تمثل نساء السجن العاديات: خوف، شائعات، وتحالفات قصيرة قبل العاصفة الأكبر." }
    ]
  },
  {
    part: "الجزء 7",
    title: "Steel Ball Run",
    year: "1890 — أمريكا (عالم بديل)",
    color: "#d84315",
    story: "سباق خيول عبر القارة الأمريكية يتحول لحرب على أجزاء جثة قديس. جوني جوستار المشلول يتعلّم الدوران من جايرو زيبيلي، بينما الرئيس فاني فالنتاين يجمع الأجزاء باسم «مصلحة أمريكا». هذا جزء إعادة تأسيس: أسماء مألوفة بأرواح جديدة.",
    people: [
      { name: "جوني جوستار", mark: "ج", color: "#1565c0", role: "البطل", align: "طيب", stand: "تاسك", tier: "main", desc: "فارس سابق سقط من المجد وصار مشلولاً. يتعلّم الدوران ليطلق أظافره كرصاص ويتطور عبر أفعال تاسك. رحلته من الأنانية للكرامة." },
      { name: "فاني فالنتاين", mark: "ف", color: "#b71c1c", role: "الخصم", align: "شرير مبدئي", stand: "ديرتي ديدز", tier: "main", desc: "رئيس أمريكا. ينتقل بين أبعاد موازية. يؤمن إن التضحية بأي أحد مقبولة إذا سلمت الأمة. أخطر نوع خصم: وطني صادق في وحشيته." },
      { name: "جايرو زيبيلي", mark: "ي", color: "#2e7d32", role: "المعلم / الصديق", align: "طيب", stand: "سكان / الدوران", tier: "main", desc: "فارس نابولي يرمي كرات فولاذية. يعلّم جوني التكنيك والفكاهة والشرف. علاقتهما قلب الجزء." },
      { name: "دييغو براندو", mark: "د", color: "#f9a825", role: "منافس", align: "شرير", stand: "سكاري مونستر", tier: "side", desc: "نسخة ديو في هذا العالم: فارس ديناصور، طموح وبارد. يظهر بأكثر من وجه عبر الأبعاد." },
      { name: "لوسي ستيل", mark: "ل", color: "#ec407a", role: "محور السباق", align: "طيبة", stand: "—", tier: "side", desc: "زوجة منظّم السباق. أصغر مما يبدو دورها، وأهم مما يظن المتسابقون. الجثة والقوة تمرّان قربها." },
      { name: "هوت بانتس", mark: "ه", color: "#8e24aa", role: "متسابقة", align: "رمادية", stand: "كريم ستارتر", tier: "side", desc: "تستخدم لحماً رذاذاً لتبديل الوجوه والأجساد. هدفها الشخصي أثقل من الميدالية." },
      { name: "ماونتن تيم", mark: "م", color: "#5d4037", role: "متسابق", align: "طيب", stand: "أوه! لونسام مي", tier: "side", desc: "شرطي سابقاً. ستانده خيط يتعقّب. يمثل القانون وهو يذوب وسط السباق." },
      { name: "رينغو روداغين", mark: "ر", color: "#ef6c00", role: "عدو نبيل", align: "رمادي", stand: "ماندام", tier: "side", desc: "يرجع الزمن ست ثوانٍ. يطلب مبارزة شريفة. من أجمل أعداء أراكي لأنّه يحترم الموت." },
      { name: "ستيفن ستيل", mark: "س", color: "#455a64", role: "منظم السباق", align: "طيب", stand: "—", tier: "side", desc: "حالم يريد أن يربط أمريكا بطريق وخيال. السباق فكرته، والجثة مصيدته." },
      { name: "ساندمان / ساوندمان", mark: "ن", color: "#6d4c41", role: "متسابق", align: "رمادي", stand: "إن أيب شل هير", tier: "side", desc: "عداء أصلي للأرض. يشارك لسبب يخص شعبه لا الكأس. سرعته فلسفة أكثر من رقم." },
      { name: "بوكولوكو", mark: "ب", color: "#00897b", role: "محظوظ", align: "طيب", stand: "الحظ نفسه", tier: "side", desc: "يدخل السباق بلا خطة ويصادفه الحظ كقانون فيزيائي. يذكّر إن العالم البديل يلعب نرداً مختلفاً." }
    ]
  },
  {
    part: "الجزء 8",
    title: "JoJolion",
    year: "2011 — موريو البديلة",
    color: "#e91e63",
    story: "بعد زلزال، يُعثر على شاب مدفون بلا ذاكرة. عائلة هيغاشيكاتا تتبنّاه باسم جوسكي، بينما فاكهة الروكاكاكا و«الصخور البشرية» يفتحون حرباً هادئة تحت بلدة ساحلية. الهوية نفسها سلاح وجرح.",
    people: [
      { name: "جوسكي هيغاشيكاتا (غابي)", mark: "ج", color: "#e91e63", role: "البطل", align: "طيب", stand: "سوفت آند ويت", tier: "main", desc: "اندماج شخصين فقد ذاكرته. فقاعاته تسرق خصائص الأشياء: صوت، بصر، احتكاك. يبحث عن اسمه بينما البلدة تراقبه." },
      { name: "تورو", mark: "ت", color: "#4a148c", role: "الخصم", align: "شرير", stand: "وندر أوف يو", tier: "main", desc: "صخر بشري يعيش بين الناس. أي مطاردة له تجلب «حوادث» كأنها قدر. أهدأ الأشرار وأبردهم." },
      { name: "ياسوهو هيروسي", mark: "ي", color: "#ad1457", role: "الشريكة", align: "طيبة", stand: "بيزلي بارك", tier: "main", desc: "تحقق وتخترق وتتبع. ستاندها يشبه التطبيق القاتل: توجيه، تجسّس، نجاة. هي عقل التحقيق أكثر من جوسكي أحياناً." },
      { name: "نوريسكي هيغاشيكاتا الرابع", mark: "ن", color: "#2e7d32", role: "رب الأسرة", align: "طيب", stand: "كينغ نوثينغ", tier: "side", desc: "يتبنّى جوسكي ويدير ثمار العائلة. ستانده يقتفي الأثر برائحة وغرائز البيت." },
      { name: "جوبين هيغاشيكاتا", mark: "ب", color: "#ef6c00", role: "الابن الأكبر", align: "رمادي", stand: "سبيد كينغ", tier: "side", desc: "يحمي أسرته بطرق توسّخ يديه. الحرارة مخزنه وسلاحه. ليس شريراً كلاسيكياً؛ هو أب محتمل مرعوب." },
      { name: "جوشو هيغاشيكاتا", mark: "ش", color: "#5e35b1", role: "الأخ", align: "رمادي", stand: "نات كينغ كول", tier: "side", desc: "غير محبوب وضروري. مساميره تفكك الأشياء. غيرته من جوسكي تحرك كثيراً من الفوضى المنزلية." },
      { name: "راي ماميزوكو", mark: "ر", color: "#00695c", role: "مزارع", align: "طيب", stand: "دوجي ستايل", tier: "side", desc: "يفكك جسده لأسلاك ويقرأ التربة. حليف عملي لجوسكي في حرب الفاكهة." },
      { name: "تسوروغي هيغاشيكاتا", mark: "غ", color: "#0277bd", role: "حفيد", align: "غامض", stand: "بيب برايم", tier: "side", desc: "طفل أذكى مما ينبغي. ألعابه ورقه يخفيان معلومات البيت والصخور." },
      { name: "هاتو هيغاشيكاتا", mark: "ه", color: "#8e24aa", role: "الأخت", align: "طيبة", stand: "وووكينغ هارت", tier: "side", desc: "حبها يتحوّل قوة ملموسة. تمثل الجانب العاطفي الصريح للعائلة." },
      { name: "دايا هيغاشيكاتا", mark: "د", color: "#6a1b9a", role: "الأخت", align: "طيبة", stand: "كاليفورنيا كينغ بد", tier: "side", desc: "ترى علاقات الناس كخرائط. عيونها أداة تحقيق منزلية." },
      { name: "بور توم", mark: "ط", color: "#4e342e", role: "صخر", align: "شرير", stand: "أوريد هارت أتاك", tier: "side", desc: "من الصخور البشرية. يحوّل المكان لفخ صناعي خانق." },
      { name: "أوربان غيريلا", mark: "ع", color: "#37474f", role: "صخر", align: "شرير", stand: "براين ستورم", tier: "side", desc: "يحارب بأسلوب قذر وجماعي. يوضح إن العدو ليس فرداً واحداً بل نوع حياة." }
    ]
  }
];

let jojoPart = 0;
let jojoQuery = "";

function jojoRender() {
  const tabs = document.getElementById("jojo-tabs");
  const part = JOJO_DATA[jojoPart];
  if (!tabs || !part) return;

  tabs.innerHTML = JOJO_DATA.map((item, index) => `
    <button type="button" class="jojo-tab${index === jojoPart ? " active" : ""}" onclick="jojoSetPart(${index})" style="--part:${item.color}">
      <span>${item.part}</span>
      <small>${item.title}</small>
    </button>
  `).join("");

  document.getElementById("jojo-story").innerHTML = `
    <div class="jojo-story-kicker" style="color:${part.color}">${part.year}</div>
    <h3 style="color:${part.color}">${part.part} · ${part.title}</h3>
    <p>${part.story}</p>
  `;

  const q = jojoQuery.trim();
  const people = part.people.filter((person) => {
    if (!q) return true;
    const blob = `${person.name} ${person.role} ${person.stand} ${person.desc}`.toLowerCase();
    return blob.includes(q.toLowerCase());
  });
  const mains = people.filter((person) => person.tier === "main");
  const sides = people.filter((person) => person.tier !== "main");

  document.getElementById("jojo-chars").innerHTML = mains.map((person) => jojoCard(person, part.people.indexOf(person))).join("") || "<p class='jojo-empty'>ما فيه نتيجة بهالبحث.</p>";
  document.getElementById("jojo-side-chars").innerHTML = sides.map((person) => jojoRow(person, part.people.indexOf(person))).join("") || "<p class='jojo-empty'>ما فيه شخصيات إضافية بهالفلتر.</p>";
}

function jojoCard(person, idx) {
  return `
    <button type="button" class="jojo-card" onclick="openJojoModal(${jojoPart}, ${idx})">
      <img alt="${person.name}" src="${jojoPortrait(person)}">
      <div>
        <strong>${person.name}</strong>
        <span>${person.role}</span>
      </div>
    </button>
  `;
}

function jojoRow(person, idx) {
  return `
    <button type="button" class="jojo-row" onclick="openJojoModal(${jojoPart}, ${idx})">
      <img alt="${person.name}" src="${jojoPortrait(person)}">
      <div>
        <strong>${person.name}</strong>
        <span>${person.role} · ${person.stand}</span>
      </div>
    </button>
  `;
}

function jojoSetPart(index) {
  jojoPart = index;
  jojoRender();
}

function jojoFilter(value) {
  jojoQuery = value;
  jojoRender();
}

function openJojoModal(partIndex, personIndex) {
  const person = JOJO_DATA[partIndex].people[personIndex];
  if (!person) return;
  document.getElementById("modal-char-name").textContent = person.name;
  document.getElementById("modal-char-img").src = jojoPortrait(person);
  document.getElementById("modal-char-role").textContent = person.role;
  document.getElementById("modal-char-align").textContent = person.align;
  document.getElementById("modal-char-stand").textContent = person.stand;
  document.getElementById("modal-char-desc").textContent = person.desc;
  document.getElementById("jojo-modal-body").classList.add("blurred");
  document.getElementById("spoiler-warning").style.display = "flex";
  document.getElementById("jojo-modal").classList.remove("hidden");
  setTimeout(() => document.getElementById("jojo-modal").classList.add("show"), 10);
}

function acceptSpoiler() {
  document.getElementById("spoiler-warning").style.display = "none";
  document.getElementById("jojo-modal-body").classList.remove("blurred");
}

function closeJojoModal() {
  document.getElementById("jojo-modal").classList.remove("show");
  setTimeout(() => document.getElementById("jojo-modal").classList.add("hidden"), 300);
}

const _origToggle = window.toggle;
window.toggle = function (id) {
  if (typeof _origToggle === "function") _origToggle(id);
  if (id === "jojo" && !document.getElementById("jojo").classList.contains("hidden")) jojoRender();
};
