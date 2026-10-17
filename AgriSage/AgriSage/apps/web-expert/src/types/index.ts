/**
 * Agri-SAGE Master Type Definitions
 * Adheres 100% to PRD, TRD, and Backend Schema specifications.
 */

export type ConfidenceState =
  | 'CONFIRMED'
  | 'LIKELY'
  | 'POSSIBLE'
  | 'UNCERTAIN'
  | 'INSUFFICIENT_DATA'
  | 'CONFLICTING_EVIDENCE'
  | 'OUT_OF_SCOPE';

export type RiskLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export type CropType = 'Rice' | 'Banana' | 'Coconut' | 'Tomato' | 'Maize';

export interface EvidenceItem {
  id: string;
  type: 'image_pattern' | 'weather_factor' | 'crop_stage' | 'scientific_literature' | 'historical_precedent';
  icon: string;
  factor: string;
  description: string;
  sourceTier?: 'Tier 1 (ICAR/KAU)' | 'Tier 2 (Govt Advisory)' | 'Tier 3 (Academic)';
  citation?: string;
}

export interface ActionPlan {
  what: string;
  whatMl: string;
  when: string;
  whenMl: string;
  how: string;
  howMl: string;
  sprayWindow?: {
    isOptimalToday: boolean;
    startTime: string;
    endTime: string;
    condition: string;
    conditionMl: string;
  };
  costEstimate: {
    minInr: number;
    maxInr: number;
    unit: string;
  };
  chemicalSafety: {
    activeIngredient: string;
    commercialBrand: string;
    dosagePerLiter: string;
    cibrcRegNumber: string;
    cibrcStatus: 'VERIFIED_ACTIVE' | 'RESTRICTED' | 'UNVERIFIED';
    phytotoxicityWarning?: string;
  };
}

export interface SimulationScenario {
  id: 'A' | 'B' | 'C';
  title: string;
  titleMl: string;
  actionSummary: string;
  actionSummaryMl: string;
  yieldEstimateKgHa: number;
  netReturnInrHa: number;
  diseaseLossPct: number;
  isRecommended: boolean;
  costInr: number;
}

export interface GovernmentScheme {
  id: string;
  name: string;
  nameMl: string;
  authority: string;
  benefit: string;
  benefitMl: string;
  deadline: string;
  applicationUrl?: string;
  isEligible: boolean;
}

export interface FarmerContext {
  farmerName: string;
  phone: string;
  district: string;
  village: string;
  farmAreaHa: number;
  crop: CropType;
  cultivar: string;
  plantingDate: string;
  estimatedGrowthStage: string;
  estimatedGrowthStageMl: string;
  gddAccumulated: number;
  recentIrrigation: boolean;
  recentFertilizer: boolean;
  recentPesticide: boolean;
}

export interface DiagnosticAdvisory {
  id: string;
  farmerId: string;
  farmerContext: FarmerContext;
  imageUrl: string;
  imageThumbnail: string;
  createdAt: string;
  
  // Diagnostic Findings
  diseaseCode: string;
  diagnosisNameEn: string;
  diagnosisNameMl: string;
  pronunciationMl: string;
  confidence: ConfidenceState;
  confidenceScore: number; // 0.0 - 1.0
  severityRisk: RiskLevel;
  
  // Model & Sensor Analytics
  modelProbabilities: Array<{
    className: string;
    commonName: string;
    probability: number;
  }>;
  weatherIndicators: {
    temperatureC: number;
    humidityPct: number;
    rainfallPast3DaysMm: number;
    rainForecastNext24hPct: number;
    windSpeedKmh: number;
    diseaseFavorabilityIndex: number; // 0.0 - 1.0
  };
  
  // Core Deliverables
  evidenceBundle: EvidenceItem[];
  actionPlan: ActionPlan;
  scenarios: SimulationScenario[];
  schemesMatched: GovernmentScheme[];
  whatWouldChangeThis: string[];
  
  // Review & Triage State
  triageStatus: 'PENDING_REVIEW' | 'VERIFIED_APPROVED' | 'OVERRIDDEN' | 'ESCALATED';
  expertReview?: {
    reviewerName: string;
    verdict: 'AGREE' | 'DISAGREE' | 'PARTIAL';
    reviewedAt: string;
    safetyApproved: boolean;
    expertNotes: string;
    correctedDiseaseCode?: string;
  };
}

export interface OutbreakAlert {
  id: string;
  district: string;
  crop: CropType;
  disease: string;
  affectedFarmsReported: number;
  severity: RiskLevel;
  weatherConditionFactor: string;
  coordinates: [number, number]; // [lat, lng]
}
