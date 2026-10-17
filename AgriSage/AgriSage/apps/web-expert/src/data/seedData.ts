import { DiagnosticAdvisory, OutbreakAlert } from '../types';

export const SEED_ADVISORIES: DiagnosticAdvisory[] = [
  {
    id: 'ADV-2026-0924-001',
    farmerId: 'FARMER-KL-0982',
    farmerContext: {
      farmerName: 'Rajan K.',
      phone: '+91 98471 23456',
      district: 'Wayanad',
      village: 'Mananthavady',
      farmAreaHa: 1.8,
      crop: 'Rice',
      cultivar: 'Jyothi (Paddy)',
      plantingDate: '2026-08-12',
      estimatedGrowthStage: 'Tillering (Day 43)',
      estimatedGrowthStageMl: 'കതിരുകൾ പൊട്ടുന്ന ഘട്ടം (43-ാം ദിവസം)',
      gddAccumulated: 345,
      recentIrrigation: true,
      recentFertilizer: true,
      recentPesticide: false
    },
    imageUrl: 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=800&q=80',
    imageThumbnail: 'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=200&q=80',
    createdAt: '2026-09-24T06:45:00+05:30',
    diseaseCode: 'rice_blast',
    diagnosisNameEn: 'Rice Blast (Magnaporthe oryzae)',
    diagnosisNameMl: 'നെല്ല് ബ്ലാസ്റ്റ് രോഗം',
    pronunciationMl: 'Nel Blast Rogam',
    confidence: 'LIKELY',
    confidenceScore: 0.88,
    severityRisk: 'HIGH',
    modelProbabilities: [
      { className: 'rice_blast', commonName: 'Rice Blast', probability: 0.88 },
      { className: 'rice_brown_spot', commonName: 'Brown Spot', probability: 0.08 },
      { className: 'rice_bacterial_blight', commonName: 'Bacterial Blight', probability: 0.03 }
    ],
    weatherIndicators: {
      temperatureC: 24.2,
      humidityPct: 89,
      rainfallPast3DaysMm: 38.4,
      rainForecastNext24hPct: 25,
      windSpeedKmh: 8.5,
      diseaseFavorabilityIndex: 0.84 // Extreme pathogen favorability
    },
    evidenceBundle: [
      {
        id: 'EV-1',
        type: 'image_pattern',
        icon: 'Leaf',
        factor: 'Spindle-shaped necrotic lesions',
        description: 'Leaf lesion morphology displays grey-white center with distinct brown margin characteristic of Magnaporthe oryzae.',
        sourceTier: 'Tier 1 (ICAR/KAU)',
        citation: 'ICAR-NRRI Rice Pathology Field Guide, Section 4.2'
      },
      {
        id: 'EV-2',
        type: 'weather_factor',
        icon: 'CloudRain',
        factor: 'High Relative Humidity (>85%) over 72 hours',
        description: 'Prolonged dew period and daytime humidity (>85%) creates ideal spore germination conditions.',
        sourceTier: 'Tier 2 (Govt Advisory)',
        citation: 'IMD Agricultural Meteorology Advisory No. 38'
      },
      {
        id: 'EV-3',
        type: 'crop_stage',
        icon: 'Calendar',
        factor: 'Tillering Stage (GDD 345°C-d)',
        description: 'Rapid vegetative foliage expansion at tillering makes canopy tissue highly vulnerable to blast sporulation.',
        sourceTier: 'Tier 1 (ICAR/KAU)',
        citation: 'Kerala Agricultural University (KAU) Package of Practices 2024'
      }
    ],
    actionPlan: {
      what: 'Apply Tricyclazole 75 WP protective & curative fungicide',
      whatMl: 'ട്രൈസൈക്ലസോൾ 75 WP കുമിൾനാശിനി തളിക്കുക',
      when: 'Today before afternoon cloud cover (between 7:30 AM – 10:30 AM)',
      whenMl: 'ഇന്ന് ഉച്ചയ്ക്ക് മുൻപ് (രാവിലെ 7:30 നും 10:30 നും ഇടയിൽ)',
      how: 'Foliar spray: Dissolve 0.6g per 1 liter of clean water (120g in 200L water per acre). Ensure thorough coverage of lower tillers.',
      howMl: 'ഒരു ലിറ്റർ വെള്ളത്തിൽ 0.6 ഗ്രാം എന്ന തോതിൽ കലക്കി ഇലകളിൽ തളിക്കുക.',
      sprayWindow: {
        isOptimalToday: true,
        startTime: '07:30 AM',
        endTime: '10:30 AM',
        condition: 'Dry canopy, wind < 12 km/h, rain probability < 20% until 3:00 PM',
        conditionMl: 'മഴസാധ്യത കുറവാണ്, അനുയോജ്യമായ കാലാവസ്ഥ'
      },
      costEstimate: {
        minInr: 450,
        maxInr: 580,
        unit: 'per acre'
      },
      chemicalSafety: {
        activeIngredient: 'Tricyclazole 75% WP',
        commercialBrand: 'Baan / Beam 75WP',
        dosagePerLiter: '0.6 g/L',
        cibrcRegNumber: 'CIR-28,451/98/Tricyclazole(WP)-342',
        cibrcStatus: 'VERIFIED_ACTIVE',
        phytotoxicityWarning: 'Do not tank-mix with highly alkaline fertilizers or Bordeaux mixture.'
      }
    },
    scenarios: [
      {
        id: 'A',
        title: 'Do Nothing (Delay)',
        titleMl: 'ചികിത്സ വൈകിപ്പിക്കുക',
        actionSummary: 'Allow blast spread across tillers',
        actionSummaryMl: 'രോഗം പടരാൻ ഇടയാക്കുന്നു',
        yieldEstimateKgHa: 3100,
        netReturnInrHa: 42500,
        diseaseLossPct: 38,
        isRecommended: false,
        costInr: 0
      },
      {
        id: 'B',
        title: 'Treat Immediately (Tricyclazole)',
        titleMl: 'ഉടൻ മരുന്ന് തളിക്കുക (ശുപാർശ ചെയ്യുന്നത്)',
        actionSummary: 'Apply Tricyclazole 75 WP within morning spray window',
        actionSummaryMl: 'രാവിലെ സമയത്ത് ട്രൈസൈക്ലസോൾ തളിക്കുക',
        yieldEstimateKgHa: 5200,
        netReturnInrHa: 89400,
        diseaseLossPct: 4,
        isRecommended: true,
        costInr: 1250
      },
      {
        id: 'C',
        title: 'Organic Bio-agent (Pseudomonas)',
        titleMl: 'ജൈവ നിയന്ത്രണം (സ്യൂഡോമോണസ്)',
        actionSummary: 'Apply Pseudomonas fluorescens 20g/L',
        actionSummaryMl: 'സ്യൂഡോമോണസ് 20 ഗ്രാം/ലിറ്റർ തളിക്കുക',
        yieldEstimateKgHa: 4400,
        netReturnInrHa: 71200,
        diseaseLossPct: 18,
        isRecommended: false,
        costInr: 600
      }
    ],
    schemesMatched: [
      {
        id: 'PMFBY-2026',
        name: 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
        nameMl: 'പ്രധാനമന്ത്രി ഫസൽ ബീമാ യോജന',
        authority: 'Ministry of Agriculture & Farmers Welfare',
        benefit: 'Covers up to ₹48,000/ha for localized pest/disease calamities',
        benefitMl: 'ഹെക്ടറിന് ₹48,000 വരെ വിള നഷ്ടപരിഹാരം',
        deadline: '2026-10-15',
        isEligible: true
      }
    ],
    whatWouldChangeThis: [
      'If heavy rainfall (>50mm) occurs within 2 hours of spraying, reapplication is necessary.',
      'A soil nitrogen test showing excess urea application would explain heightened blast vulnerability.'
    ],
    triageStatus: 'PENDING_REVIEW'
  },
  {
    id: 'ADV-2026-0924-002',
    farmerId: 'FARMER-KL-0744',
    farmerContext: {
      farmerName: 'Kavitha Unni',
      phone: '+91 97455 88990',
      district: 'Palakkad',
      village: 'Chittur',
      farmAreaHa: 2.2,
      crop: 'Banana',
      cultivar: 'Nendran',
      plantingDate: '2026-03-10',
      estimatedGrowthStage: 'Shooting & Bunch Formation',
      estimatedGrowthStageMl: 'കുല വരുന്ന ഘട്ടം',
      gddAccumulated: 1040,
      recentIrrigation: true,
      recentFertilizer: false,
      recentPesticide: false
    },
    imageUrl: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=800&q=80',
    imageThumbnail: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=200&q=80',
    createdAt: '2026-09-24T07:15:00+05:30',
    diseaseCode: 'banana_sigatoka',
    diagnosisNameEn: 'Black Sigatoka Leaf Spot (Mycosphaerella)',
    diagnosisNameMl: 'സിഗറ്റോക്ക ഇലപ്പുള്ളി രോഗം',
    pronunciationMl: 'Sigatoka Ilappulli',
    confidence: 'CONFIRMED',
    confidenceScore: 0.94,
    severityRisk: 'HIGH',
    modelProbabilities: [
      { className: 'banana_sigatoka', commonName: 'Sigatoka Leaf Spot', probability: 0.94 },
      { className: 'banana_fusarium', commonName: 'Fusarium Wilt', probability: 0.04 },
      { className: 'banana_healthy', commonName: 'Healthy Banana', probability: 0.02 }
    ],
    weatherIndicators: {
      temperatureC: 28.5,
      humidityPct: 82,
      rainfallPast3DaysMm: 14.0,
      rainForecastNext24hPct: 40,
      windSpeedKmh: 11.2,
      diseaseFavorabilityIndex: 0.78
    },
    evidenceBundle: [
      {
        id: 'EV-B1',
        type: 'image_pattern',
        icon: 'Leaf',
        factor: 'Elliptical necrotic spots with yellow halos along secondary veins',
        description: 'Advanced dark streaks coalescing into premature leaf dry-up, directly endangering bunch filling.',
        sourceTier: 'Tier 1 (ICAR/KAU)',
        citation: 'NRCB (National Research Centre for Banana) Disease Atlas'
      }
    ],
    actionPlan: {
      what: 'Apply Propiconazole 25 EC with mineral oil emulsion',
      whatMl: 'പ്രോപ്പികൊണസോൾ 25 EC തളിക്കുക',
      when: 'Tomorrow morning between 7:00 AM – 9:30 AM',
      whenMl: 'നാളെ രാവിലെ 7:00 നും 9:30 നും ഇടയിൽ',
      how: 'Dissolve 1ml Propiconazole per 1 liter of water mixed with 10ml agricultural spray oil.',
      howMl: 'ഒരു ലിറ്റർ വെള്ളത്തിൽ 1 മില്ലി പ്രോപ്പികൊണസോൾ കലക്കി തളിക്കുക.',
      costEstimate: {
        minInr: 650,
        maxInr: 850,
        unit: 'per acre'
      },
      chemicalSafety: {
        activeIngredient: 'Propiconazole 25% EC',
        commercialBrand: 'Tilt 25EC',
        dosagePerLiter: '1.0 ml/L',
        cibrcRegNumber: 'CIR-19,820/94/Propiconazole(EC)-122',
        cibrcStatus: 'VERIFIED_ACTIVE'
      }
    },
    scenarios: [
      {
        id: 'A',
        title: 'Untreated',
        titleMl: 'ചികിത്സിക്കാത്തത്',
        actionSummary: 'Sigatoka defoliates bunch canopy',
        actionSummaryMl: 'ഇലകൾ കരിഞ്ഞുപോകുന്നു',
        yieldEstimateKgHa: 18500,
        netReturnInrHa: 145000,
        diseaseLossPct: 32,
        isRecommended: false,
        costInr: 0
      },
      {
        id: 'B',
        title: 'Systemic Fungicide (Propiconazole)',
        titleMl: 'പ്രോപ്പികൊണസോൾ പ്രയോഗം',
        actionSummary: 'Stops necrotic lesion advancement within 48h',
        actionSummaryMl: 'രോഗം പെട്ടെന്ന് തടയുന്നു',
        yieldEstimateKgHa: 27000,
        netReturnInrHa: 260000,
        diseaseLossPct: 3,
        isRecommended: true,
        costInr: 1800
      },
      {
        id: 'C',
        title: 'Copper Oxychloride (Contact)',
        titleMl: 'കോപ്പർ ഓക്സിക്ലോറൈഡ്',
        actionSummary: 'Slower containment, higher spray volume',
        actionSummaryMl: 'കൂടുതൽ വെള്ളം ആവശ്യമാണ്',
        yieldEstimateKgHa: 22000,
        netReturnInrHa: 195000,
        diseaseLossPct: 15,
        isRecommended: false,
        costInr: 1100
      }
    ],
    schemesMatched: [],
    whatWouldChangeThis: ['Removal and burning of severely spotted lower leaves before chemical application improves efficacy by 40%.'],
    triageStatus: 'PENDING_REVIEW'
  },
  {
    id: 'ADV-2026-0924-003',
    farmerId: 'FARMER-KL-0311',
    farmerContext: {
      farmerName: 'Mathew Thomas',
      phone: '+91 94460 11223',
      district: 'Alappuzha',
      village: 'Kuttanad',
      farmAreaHa: 1.2,
      crop: 'Coconut',
      cultivar: 'West Coast Tall (WCT)',
      plantingDate: '2019-06-15',
      estimatedGrowthStage: 'Bearing Palm (>6 years)',
      estimatedGrowthStageMl: 'വിളവ് തരുന്ന തെങ്ങ്',
      gddAccumulated: 4200,
      recentIrrigation: true,
      recentFertilizer: false,
      recentPesticide: false
    },
    imageUrl: 'https://images.unsplash.com/photo-1544979590-37e9b47eb705?auto=format&fit=crop&w=800&q=80',
    imageThumbnail: 'https://images.unsplash.com/photo-1544979590-37e9b47eb705?auto=format&fit=crop&w=200&q=80',
    createdAt: '2026-09-24T08:00:00+05:30',
    diseaseCode: 'coconut_wclwd',
    diagnosisNameEn: 'Root (Wilt) Disease / WCLWD',
    diagnosisNameMl: 'തെങ്ങിന്റെ കാറ്റുവീഴ്ച രോഗം',
    pronunciationMl: 'Thengu Kattuvizha Rogam',
    confidence: 'UNCERTAIN', // Calibrated state: requires agronomist review
    confidenceScore: 0.54,
    severityRisk: 'CRITICAL',
    modelProbabilities: [
      { className: 'coconut_wclwd', commonName: 'Kerala Root Wilt', probability: 0.54 },
      { className: 'coconut_bud_rot', commonName: 'Bud Rot', probability: 0.32 },
      { className: 'coconut_healthy', commonName: 'Nutrient Deficiency (Mg/K)', probability: 0.14 }
    ],
    weatherIndicators: {
      temperatureC: 29.1,
      humidityPct: 86,
      rainfallPast3DaysMm: 22.0,
      rainForecastNext24hPct: 30,
      windSpeedKmh: 14.0,
      diseaseFavorabilityIndex: 0.65
    },
    evidenceBundle: [
      {
        id: 'EV-C1',
        type: 'image_pattern',
        icon: 'AlertTriangle',
        factor: 'Flaccidity and ribbing of leaflets with general yellowing',
        description: 'Leaflet curvature resembles Phytoplasma Root (Wilt) symptoms, but severe Potassium deficiency produces nearly identical foliar necrosis in sandy loam soils.',
        sourceTier: 'Tier 1 (ICAR/KAU)',
        citation: 'CPCRI (Central Plantation Crops Research Institute) Technical Bulletin 88'
      }
    ],
    actionPlan: {
      what: 'Agronomist physical inspection requested — do not apply indiscriminate fungicide',
      whatMl: 'വിദഗ്ദ്ധ പരിശോധന ആവശ്യമാണ് — അനാവശ്യമായി മരുന്ന് തളിക്കരുത്',
      when: 'Await field inspection within 48 hours',
      whenMl: '48 മണിക്കൂറിനകം വിദഗ്ദ്ധൻ ബന്ധപ്പെടും',
      how: 'Collect soil and leaf samples for CPCRI laboratory diagnosis. Apply balanced NPK + Magnesium Sulphate (500g MgSO4 per palm).',
      howMl: 'മണ്ണ് പരിശോധന നടത്തുക. മഗ്നീഷ്യം സൾഫേറ്റ് 500 ഗ്രാം ചേർക്കുക.',
      costEstimate: {
        minInr: 120,
        maxInr: 250,
        unit: 'per palm'
      },
      chemicalSafety: {
        activeIngredient: 'Nutritional remediation (No chemical pesticide indicated)',
        commercialBrand: 'Agricultural Grade MgSO4 + Borax',
        dosagePerLiter: '500g/palm soil application',
        cibrcRegNumber: 'N/A (Nutrient)',
        cibrcStatus: 'VERIFIED_ACTIVE'
      }
    },
    scenarios: [
      {
        id: 'A',
        title: 'Immediate Eradication',
        titleMl: 'തെങ്ങ് വെട്ടിമാറ്റുക',
        actionSummary: 'Cut down if advanced stage to prevent lace bug vector transmission',
        actionSummaryMl: 'രോഗം പടരുന്നത് തടയാൻ വെട്ടിമാറ്റുക',
        yieldEstimateKgHa: 0,
        netReturnInrHa: -5000,
        diseaseLossPct: 100,
        isRecommended: false,
        costInr: 1500
      },
      {
        id: 'B',
        title: 'Nutrient & Phytoplasma Management',
        titleMl: 'പോഷക പരിപാലനം (ശുപാർശ ചെയ്യുന്നത്)',
        actionSummary: 'Intensive nutrition, green manuring, vector control',
        actionSummaryMl: 'പോഷകങ്ങളും പച്ചിലവളവും നൽകുക',
        yieldEstimateKgHa: 6800,
        netReturnInrHa: 82000,
        diseaseLossPct: 20,
        isRecommended: true,
        costInr: 3200
      }
    ],
    schemesMatched: [
      {
        id: 'CDB-REPLANT',
        name: 'Coconut Development Board Replanting & Rejuvenation Scheme',
        nameMl: 'നാളികേര വികസന ബോർഡ് പുനരുദ്ധാരണ പദ്ധതി',
        authority: 'Coconut Development Board (Govt. of India)',
        benefit: 'Financial assistance of ₹8,000 per palm for removal of disease-advanced palms',
        benefitMl: 'രോഗബാധിതമായ തെങ്ങ് വെട്ടിമാറ്റാൻ ₹8,000 ധനസഹായം',
        deadline: '2026-11-30',
        isEligible: true
      }
    ],
    whatWouldChangeThis: [
      'Leaf tissue analysis confirming Phytoplasma DNA via PCR test.',
      'Checking if symptoms respond to 500g Magnesium Sulphate application after 30 days.'
    ],
    triageStatus: 'ESCALATED'
  }
];

export const REGIONAL_OUTBREAKS: OutbreakAlert[] = [
  {
    id: 'OUT-01',
    district: 'Wayanad',
    crop: 'Rice',
    disease: 'Rice Blast (Magnaporthe oryzae)',
    affectedFarmsReported: 142,
    severity: 'HIGH',
    weatherConditionFactor: 'Persistent canopy wetness > 14 hrs/day',
    coordinates: [11.6854, 76.1320]
  },
  {
    id: 'OUT-02',
    district: 'Palakkad',
    crop: 'Banana',
    disease: 'Black Sigatoka',
    affectedFarmsReported: 89,
    severity: 'HIGH',
    weatherConditionFactor: 'Temperature 28°C + intermittent afternoon showers',
    coordinates: [10.7867, 76.6548]
  },
  {
    id: 'OUT-03',
    district: 'Thrissur',
    crop: 'Tomato',
    disease: 'Early Blight (Alternaria)',
    affectedFarmsReported: 34,
    severity: 'MEDIUM',
    weatherConditionFactor: 'Dew condensation during cool nights',
    coordinates: [10.5276, 76.2144]
  },
  {
    id: 'OUT-04',
    district: 'Alappuzha',
    crop: 'Coconut',
    disease: 'Kerala Root (Wilt)',
    affectedFarmsReported: 67,
    severity: 'CRITICAL',
    weatherConditionFactor: 'Waterlogged soil & nutritional leaching',
    coordinates: [9.4981, 76.3388]
  }
];
