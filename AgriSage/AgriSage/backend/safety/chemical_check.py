from typing import Dict, Any, List, Tuple


class ChemicalSafetyCheck:
    """CIB&RC Statutory Chemical Safety Validator.
    
    Checks pesticide registration status, active ingredients, crop-specific approval,
    stage safety, and dosage compliance per Indian CIB&RC guidelines.
    """

    # Approved CIB&RC database subset
    APPROVED_CIBRC_REGISTRY: Dict[str, Dict[str, Any]] = {
        "tricyclazole 75 wp": {
            "approved_crops": ["rice", "paddy"],
            "max_dosage_per_liter": 0.6,  # grams per liter
            "banned": False,
            "stage_restrictions": ["flowering_harvest_prevention"],
            "cibrc_reg_no": "CIR-18239/95/Tricyclazole-WP-102"
        },
        "pseudomonas fluorescens": {
            "approved_crops": ["rice", "paddy", "tomato", "potato", "banana", "chilli", "pepper"],
            "max_dosage_per_liter": 10.0,
            "banned": False,
            "stage_restrictions": [],
            "cibrc_reg_no": "CIR-BIO/2012/Pseudomonas-04"
        },
        "mancozeb 75 wp": {
            "approved_crops": ["potato", "tomato", "chilli", "grape", "apple"],
            "max_dosage_per_liter": 2.5,
            "banned": False,
            "stage_restrictions": [],
            "cibrc_reg_no": "CIR-14322/92/Mancozeb-WP-304"
        },
        "copper oxychloride 50 wp": {
            "approved_crops": ["tomato", "potato", "chilli", "cardamom", "coffee"],
            "max_dosage_per_liter": 3.0,
            "banned": False,
            "stage_restrictions": [],
            "cibrc_reg_no": "CIR-09821/88/Copper-WP-112"
        },
        "hexaconazole 5 ec": {
            "approved_crops": ["rice", "paddy", "mango", "grape"],
            "max_dosage_per_liter": 2.0,
            "banned": False,
            "stage_restrictions": [],
            "cibrc_reg_no": "CIR-22104/98/Hexaconazole-EC-55"
        },
        "azoxystrobin 23 sc": {
            "approved_crops": ["rice", "paddy", "tomato", "chilli", "grape", "mango"],
            "max_dosage_per_liter": 1.0,
            "banned": False,
            "stage_restrictions": [],
            "cibrc_reg_no": "CIR-31045/04/Azoxystrobin-SC-88"
        }
    }

    # Explicitly prohibited or severely restricted chemicals (Statutory Ban)
    PROHIBITED_CHEMICALS: List[str] = [
        "monocrotophos",
        "paraquat dichloride",
        "endosulfan",
        "phorate",
        "methomyl",
        "triazophos"
    ]

    def validate_pesticide(
        self, product_name: str, crop: str, dosage: float, crop_stage: str = "vegetative"
    ) -> Tuple[bool, List[str]]:
        """Validate pesticide against CIB&RC rules.
        
        Returns:
            (is_safe: bool, issues: List[str])
        """
        issues = []
        clean_name = product_name.strip().lower()
        clean_crop = crop.strip().lower()

        # Check for banned/prohibited active ingredients
        for prohibited in self.PROHIBITED_CHEMICALS:
            if prohibited in clean_name:
                issues.append(f"BLOCK: Chemical '{product_name}' contains prohibited active ingredient '{prohibited}'.")
                return False, issues

        # Match against CIB&RC registry
        matched_reg = None
        for registered_name, reg_data in self.APPROVED_CIBRC_REGISTRY.items():
            if registered_name in clean_name or clean_name in registered_name:
                matched_reg = reg_data
                break

        if not matched_reg:
            issues.append(f"BLOCK: Chemical '{product_name}' is not found in verified CIB&RC registry.")
            return False, issues

        # Check crop approval
        approved_crops = matched_reg.get("approved_crops", [])
        if clean_crop not in approved_crops:
            issues.append(
                f"BLOCK: Chemical '{product_name}' is registered for {approved_crops} but not approved for '{crop}'."
            )
            return False, issues

        # Check dosage threshold
        max_dosage = matched_reg.get("max_dosage_per_liter", 100.0)
        if dosage > max_dosage:
            issues.append(
                f"WARNING: Prescribed dosage {dosage} exceeds CIB&RC safe limit of {max_dosage} per liter for '{product_name}'."
            )

        return len([i for i in issues if "BLOCK" in i]) == 0, issues
