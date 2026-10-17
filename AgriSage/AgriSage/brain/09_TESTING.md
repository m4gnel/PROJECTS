# AGRI-SAGE — TESTING

## Rule: Never modify tests — fix the implementation

## Coverage Requirements
Unit (business logic): 80% | Pydantic schemas: 100%
Safety/critic tests: 100% — block merge if any fail
RLS tests: 100% — block merge if any fail
Vision model: Macro-F1≥0.82, ECE≤0.12 before deploy

## pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py

## GDD Unit Tests
```python
def test_rice_gdd(self):
    assert compute_gdd(tmax=30.0,tmin=22.0,crop='rice') == pytest.approx(16.0,abs=0.1)
def test_gdd_below_base_zero(self):
    assert compute_gdd(tmax=12.0,tmin=8.0,crop='rice') == 0.0
def test_rice_tillering_at_260(self):
    r = agent.estimate_stage(crop='rice',cumulative_gdd=260.0)
    assert r.stage_code=='tillering' and r.disease_vulnerability=='high'
```

## DFI Tests
```python
def test_high_humidity_high_dfi(self):
    assert compute_dfi(humidity_pct=88.0,temperature_c=26.0,wet_days=4) > 0.7
def test_dry_low_dfi(self):
    assert compute_dfi(humidity_pct=45.0,temperature_c=35.0,wet_days=0) < 0.3
def test_dfi_clamped(self):
    dfi = compute_dfi(humidity_pct=100.0,temperature_c=25.0,wet_days=14)
    assert 0.0 <= dfi <= 1.0
```

## Safety Tests — CRITICAL
```python
async def test_unknown_pesticide_blocked(self):
    safe,issues = await checker.run({'product_name':'FakeXYZ','crop':'rice','dosage':1.0})
    assert safe==False and any('BLOCK' in i for i in issues)

async def test_valid_pesticide_passes(self):
    safe,issues = await checker.run({'product_name':'Tricyclazole 75 WP','crop':'rice','dosage':0.6})
    assert safe==True and len(issues)==0

async def test_wrong_crop_blocked(self):
    safe,_ = await checker.run({'product_name':'Tricyclazole 75 WP','crop':'banana','dosage':0.6})
    assert safe==False

async def test_conflicting_evidence_no_treatment(self):
    state = make_conflicting_state(vision_label='rice_blast',dfi=0.1,wet_days=0)
    result = await critic.run(state)
    assert result['critic_result']['confidence_state']=='CONFLICTING_EVIDENCE'
    assert result['critic_result']['safe_to_act']==False

async def test_expired_scheme_not_returned(self):
    state = make_state_with_expired_scheme()
    result = await scheme_agent.run(state)
    assert 'ExpiredScheme2020' not in [s['scheme_name'] for s in result.get('scheme_matches',[])]
```

## RLS Test — CRITICAL
```python
async def test_user_cannot_read_other_users_farm(async_client):
    token_a = await create_test_user_token('+919000000001')
    token_b = await create_test_user_token('+919000000002')
    resp = await async_client.post('/api/v1/farms',
        json={'name':'Farm A','location_lat':10.0,'location_lon':76.0},
        headers={'Authorization':f'Bearer {token_a}'})
    farm_id = resp.json()['id']
    resp = await async_client.get(f'/api/v1/farms/{farm_id}',
        headers={'Authorization':f'Bearer {token_b}'})
    assert resp.status_code == 404  # NOT 403 NOT 200
```

## Vision Model Evaluation
```python
def evaluate(model_path, golden_dir):
    # run inference on all golden images
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    ece = compute_ece(y_true, y_pred, y_prob)
    assert macro_f1 >= 0.82, f'FAIL: F1={macro_f1:.3f}'
    assert ece <= 0.12, f'FAIL: ECE={ece:.3f}'
```

## Performance Targets
POST /diagnose: P95 < 8s | GET /weather: P95 < 500ms
App cold start: < 2.5s | ONNX inference Android: < 4s
