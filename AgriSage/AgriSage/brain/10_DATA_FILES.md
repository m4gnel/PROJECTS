# AGRI-SAGE — DATA FILES (backend/data/)

## disease_classes.json (22 classes — index order MUST match ONNX model)
[
  {"index":0,"class_name":"rice_blast","common_name":"Rice Blast","ml_name":"നെൽ ബ്ലാസ്റ്റ് രോഗം","crop":"rice"},
  {"index":1,"class_name":"rice_brown_spot","common_name":"Brown Spot","ml_name":"തവിട്ട് പുള്ളി രോഗം","crop":"rice"},
  {"index":2,"class_name":"rice_bacterial_blight","common_name":"Bacterial Blight","ml_name":"ബാക്ടീരിയൽ ഇല കരിച്ചിൽ","crop":"rice"},
  {"index":3,"class_name":"rice_sheath_blight","common_name":"Sheath Blight","ml_name":"കതിർ ആവരണ ജീർണ്ണം","crop":"rice"},
  {"index":4,"class_name":"rice_leaf_folder","common_name":"Leaf Folder","ml_name":"ഇല ചുരുട്ടി പുഴു","crop":"rice"},
  {"index":5,"class_name":"rice_healthy","common_name":"Healthy Rice","ml_name":"ആരോഗ്യകരമായ നെൽ","crop":"rice"},
  {"index":6,"class_name":"banana_fusarium","common_name":"Fusarium Wilt","ml_name":"ഫ്യൂസേറിയം വിൽറ്റ്","crop":"banana"},
  {"index":7,"class_name":"banana_sigatoka","common_name":"Sigatoka Leaf Spot","ml_name":"സിഗറ്റോക്ക ഇലപ്പുള്ളി","crop":"banana"},
  {"index":8,"class_name":"banana_bbtv","common_name":"Banana Bunchy Top Virus","ml_name":"വാഴ ബഞ്ചി ടോപ്പ് വൈറസ്","crop":"banana"},
  {"index":9,"class_name":"banana_healthy","common_name":"Healthy Banana","ml_name":"ആരോഗ്യകരമായ വാഴ","crop":"banana"},
  {"index":10,"class_name":"coconut_wclwd","common_name":"Kerala Wilt WCLWD","ml_name":"തെങ്ങ് മഞ്ഞൾ ഇല കൊഴിച്ചിൽ","crop":"coconut"},
  {"index":11,"class_name":"coconut_bud_rot","common_name":"Bud Rot","ml_name":"ഓലച്ചീർ","crop":"coconut"},
  {"index":12,"class_name":"coconut_healthy","common_name":"Healthy Coconut","ml_name":"ആരോഗ്യകരമായ തെങ്ങ്","crop":"coconut"},
  {"index":13,"class_name":"tomato_early_blight","common_name":"Early Blight","ml_name":"തക്കാളി ആദ്യ ദ്രവം","crop":"tomato"},
  {"index":14,"class_name":"tomato_late_blight","common_name":"Late Blight","ml_name":"തക്കാളി അന്ത്യ ദ്രവം","crop":"tomato"},
  {"index":15,"class_name":"tomato_leaf_curl","common_name":"Leaf Curl Virus","ml_name":"തക്കാളി ഇല ചുരുളൽ","crop":"tomato"},
  {"index":16,"class_name":"tomato_healthy","common_name":"Healthy Tomato","ml_name":"ആരോഗ്യകരമായ തക്കാളി","crop":"tomato"},
  {"index":17,"class_name":"maize_northern_blight","common_name":"Northern Leaf Blight","ml_name":"ചോളം ഇല ദ്രവം","crop":"maize"},
  {"index":18,"class_name":"maize_common_rust","common_name":"Common Rust","ml_name":"ചോളം തുരുമ്പ്","crop":"maize"},
  {"index":19,"class_name":"maize_grey_leaf_spot","common_name":"Grey Leaf Spot","ml_name":"ചോളം ചാര പുള്ളി","crop":"maize"},
  {"index":20,"class_name":"maize_healthy","common_name":"Healthy Maize","ml_name":"ആരോഗ്യകരമായ ചോളം","crop":"maize"},
  {"index":21,"class_name":"out_of_distribution","common_name":"Not a crop image","ml_name":"തിരിച്ചറിയാൻ കഴിഞ്ഞില്ല","crop":"none"}
]

## gdd_thresholds.json (key structure)
{
  "base_temperatures": {"rice":10,"maize":10,"tomato":10,"banana":15,"coconut":20},
  "thresholds": {
    "rice": {
      "germination":        {"gdd_from":0,  "gdd_to":50,  "vulnerability":"low",     "diseases_expected":[]},
      "seedling":           {"gdd_from":50, "gdd_to":200, "vulnerability":"low",     "diseases_expected":["rice_leaf_folder"]},
      "tillering":          {"gdd_from":200,"gdd_to":400, "vulnerability":"high",    "diseases_expected":["rice_blast","rice_brown_spot","rice_leaf_folder"]},
      "panicle_initiation": {"gdd_from":400,"gdd_to":600, "vulnerability":"high",    "diseases_expected":["rice_blast","rice_sheath_blight"]},
      "flowering":          {"gdd_from":600,"gdd_to":750, "vulnerability":"critical","diseases_expected":["rice_blast","rice_bacterial_blight"]},
      "grain_fill":         {"gdd_from":750,"gdd_to":900, "vulnerability":"medium",  "diseases_expected":["rice_sheath_blight","rice_brown_spot"]},
      "maturity":           {"gdd_from":900,"gdd_to":1100,"vulnerability":"low",     "diseases_expected":[]}
    }
  }
}

## offline_templates_ml.json
{
  "disease_detected":{"text":"നിങ്ങളുടെ {crop} വിളയിൽ {disease} ന്റെ ലക്ഷണങ്ങൾ കാണുന്നു. ആത്മവിശ്വാസം: {confidence}. ഇന്ന് {action} ചെയ്യുക.","slots":["crop","disease","confidence","action"]},
  "insufficient_data":{"text":"ഫോട്ടോ കൂടുതൽ വ്യക്തമല്ല. ഇലയുടെ അടുത്ത് നിന്ന് നല്ല വെളിച്ചത്തിൽ ഫോട്ടോ എടുക്കുക.","slots":[]},
  "conflicting_evidence":{"text":"ഫോട്ടോയും കാലാവസ്ഥ ഡേറ്റയും വ്യത്യസ്ത ഫലങ്ങൾ കാണിക്കുന്നു. ഒരു കൃഷി വിദഗ്ദ്ധനെ സമീപിക്കുക.","slots":[]},
  "all_clear":{"text":"ഇന്ന് നിങ്ങളുടെ {crop} ആരോഗ്യകരമായി കാണുന്നു. കാലാവസ്ഥ: {weather}.","slots":["crop","weather"]},
  "offline_notice":{"text":"ഇന്റർനെറ്റ് ഇല്ല — ഇത് ഒരു ഓഫ്‌ലൈൻ വിശകലനമാണ്. ഇന്റർനെറ്റ് ലഭ്യമാകുമ്പോൾ കൂടുതൽ കൃത്യമായ ഉത്തരം ലഭിക്കും.","slots":[]},
  "spray_window":{"text":"ഇന്ന് {time} മുതൽ {time_end} വരെ കൃഷിമരുന്ന് തളിക്കാൻ അനുയോജ്യമായ സമയമാണ്.","slots":["time","time_end"]},
  "high_risk_alert":{"text":"⚠ {crop} വിളയ്ക്ക് ഇന്ന് {risk_type} അപകടം കൂടുതലാണ്. {action} ചെയ്യുക.","slots":["crop","risk_type","action"]}
}

## intent_keywords_ml.json
{
  "നെൽ":{"field":"crop","value":"rice"},
  "നെല്ല്":{"field":"crop","value":"rice"},
  "വാഴ":{"field":"crop","value":"banana"},
  "തക്കാളി":{"field":"crop","value":"tomato"},
  "ചോളം":{"field":"crop","value":"maize"},
  "തെങ്ങ്":{"field":"crop","value":"coconut"},
  "ബ്ലാസ്റ്റ്":{"field":"problem","value":"blast"},
  "പുള്ളി":{"field":"symptom","value":"spots"},
  "ഇല":{"field":"body_part","value":"leaf"},
  "ചുരുളൽ":{"field":"symptom","value":"curling"},
  "മഞ്ഞ":{"field":"symptom","value":"yellowing"},
  "കരിച്ചിൽ":{"field":"symptom","value":"burning"},
  "ദ്രവം":{"field":"symptom","value":"rot"},
  "നനഞ്ഞ":{"field":"irrigation_status","value":"irrigated"},
  "വരൾ":{"field":"irrigation_status","value":"dry"}
}
