# 07_API_CONTRACT.md
# Internal Module API Contracts

## 1. data_loader.py

```python
def load_sources(train_dir: str, mode: str = "train") -> Dict[str, pd.DataFrame]:
    """
    Load all source TSV files.
    
    Args:
        train_dir: path to directory containing source TSVs
        mode: "train" or "test"
    
    Returns:
        {
            "s1": DataFrame,  # columns: entity_id, business_name, business_address, country
            "s2": DataFrame,
            "s3": DataFrame,
            "gt": DataFrame,  # only if mode="train"; columns: source1_entity_id, matched_entity_ids
        }
    
    Raises:
        FileNotFoundError: if any expected TSV is missing
        ValueError: if required columns are absent
    """

def validate_entity_ids(sources: Dict[str, pd.DataFrame]) -> None:
    """
    Check:
    - S1 IDs start with "S1-"
    - S2 IDs start with "S2-"
    - S3 IDs start with "S3-"
    - No duplicates within each source
    Raises ValueError with details if any check fails.
    """
```

---

## 2. normalizer.py

```python
def normalize_text(text: str, field: str = "name") -> str:
    """
    Normalize a raw text field.
    
    Args:
        text: raw string (may be None/NaN)
        field: "name" or "address" — selects abbreviation dict
    
    Returns:
        normalized string (lowercase, expanded, punctuation-stripped)
        Returns "" if text is None/NaN
    
    Steps applied in order:
    1. Handle None/NaN → return ""
    2. unicodedata.normalize("NFC", text)
    3. text.lower()
    4. Expand abbreviations using abbreviation dict
    5. re.sub(r'[^a-z0-9\s]', ' ', text)   # keep alphanumeric + space
    6. re.sub(r'\s+', ' ', text).strip()
    """

def build_combined_text(norm_name: str, norm_address: str) -> str:
    """
    Concatenate name and address for embedding.
    Returns: f"{norm_name} {norm_address}".strip()
    """
```

---

## 3. blocker.py

```python
def build_blocking_index(
    s1_records: List[RecordDict],
    s23_records: List[RecordDict],
    config: BlockingConfig
) -> Dict[str, List[str]]:
    """
    Generate candidate pairs via multiple blocking strategies.
    
    Returns:
        {s1_entity_id: [candidate_entity_id, ...]}
        Every S1 entity appears as a key (empty list for no candidates).
    
    Guarantees:
        - Union of all blocking keys used
        - Deduplication within each list
        - len(candidates_per_s1) <= config.max_candidates_per_s1
    """

def compute_blocking_recall(
    candidates: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]]
) -> float:
    """
    Fraction of GT positive pairs present in candidates.
    A value < 0.98 is a pipeline warning.
    """
```

---

## 4. embedder.py

```python
def encode_records(
    texts: List[str],
    model_name: str,
    batch_size: int = 256,
    device: str = "auto"
) -> np.ndarray:
    """
    Encode list of texts to embeddings.
    
    Args:
        texts: list of combined (name + address) strings
        model_name: HuggingFace model identifier
        batch_size: encoding batch size
        device: "cuda" / "cpu" / "auto"
    
    Returns:
        np.ndarray of shape (len(texts), embedding_dim), dtype=float32
        L2-normalized embeddings (for cosine via dot product).
    """

def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """Build a FAISS IndexFlatIP (inner product = cosine on L2-normed vectors)."""

def search_faiss(
    index: faiss.Index,
    query_embeddings: np.ndarray,
    top_k: int = 20
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns (distances, indices) arrays of shape (n_queries, top_k).
    """
```

---

## 5. feature_engineer.py

```python
def compute_pair_features(
    s1_record: RecordDict,
    candidate_record: RecordDict
) -> Dict[str, float]:
    """
    Compute all similarity features for one (S1, candidate) pair.
    Returns feature dict matching CandidatePair schema (minus label/match_prob).
    """

def build_feature_matrix(
    s1_records: Dict[str, RecordDict],
    candidate_records: Dict[str, RecordDict],
    candidate_pairs: Dict[str, List[str]],
    ground_truth: Optional[Dict[str, List[str]]] = None
) -> pd.DataFrame:
    """
    Build full feature DataFrame for all candidate pairs.
    If ground_truth provided, adds 'label' column.
    Columns: s1_id, candidate_id, [features...], [label]
    """
```

---

## 6. matcher.py

```python
def train_matcher(
    feature_df: pd.DataFrame,
    config: MatchingConfig
) -> lgb.LGBMClassifier:
    """
    Train LightGBM on feature_df with 'label' column.
    Uses stratified sampling, scale_pos_weight for class imbalance.
    Returns trained model.
    """

def predict_scores(
    model: lgb.LGBMClassifier,
    feature_df: pd.DataFrame
) -> pd.Series:
    """
    Returns series of match probabilities, same index as feature_df.
    """

def calibrate_threshold(
    val_feature_df: pd.DataFrame,
    val_ground_truth: Dict[str, List[str]],
    model: lgb.LGBMClassifier
) -> float:
    """
    Grid-search threshold [0.1, 0.95] in steps of 0.01.
    Returns threshold that maximizes macro-F₀.₅ on validation set.
    """
```

---

## 7. evaluator.py

```python
def compute_f05_per_entity(
    predicted: List[str],
    ground_truth: List[str]
) -> float:
    """
    F₀.₅ for a single S1 entity.
    
    predicted: list of matched S2/S3 IDs predicted
    ground_truth: list of true S2/S3 IDs
    
    Returns F₀.₅ in [0, 1]
    Edge cases:
    - Both empty → 1.0 (correct singleton)
    - GT empty, predicted non-empty → 0.0 (false merge)
    - GT non-empty, predicted empty → 0.0 (missed all)
    """

def compute_macro_f05(
    predictions: Dict[str, List[str]],
    ground_truth: Dict[str, List[str]]
) -> Dict[str, float]:
    """
    Returns {
        "macro_f05": float,
        "macro_precision": float,
        "macro_recall": float,
        "n_entities": int,
        "n_singletons": int,
        "n_correct_singletons": int,
    }
    """
```

---

## 8. postprocessor.py

```python
def apply_threshold(
    feature_df: pd.DataFrame,
    scores: pd.Series,
    threshold: float
) -> Dict[str, List[str]]:
    """
    Returns {s1_id: [matched_ids]} where match_prob >= threshold.
    """

def write_output_files(
    candidates: Dict[str, List[str]],
    matches: Dict[str, List[str]],
    s1_ids: List[str],
    output_dir: str
) -> None:
    """
    Write candidate_pairs.tsv and matching_results.tsv.
    Guarantees every s1_id has exactly one row.
    Guarantees no duplicate IDs in any list.
    """
```
