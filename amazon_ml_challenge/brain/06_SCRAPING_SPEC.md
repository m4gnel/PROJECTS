# 06_SCRAPING_SPEC.md
# Data Analysis Spec (No Scraping — External Data Prohibited)

## ⚠️ External data lookup is STRICTLY PROHIBITED.
## This document covers internal data analysis only.

## Analysis Tasks to Run on Training Data

### 1. Positive Pair Analysis
For each positive pair in ground truth:
- Levenshtein ratio of name pair → histogram
- Token-set ratio of address pair → histogram
- Cosine embedding similarity → histogram
- Are there pairs where name is empty? address is empty?
- Min similarity observed → sets lower bound for threshold search

### 2. Match Cardinality Distribution
- Count S1 entities with 0 matches (singletons)
- Count S1 entities with 1 match
- Count S1 entities with 2+ matches
- This drives negative sampling ratio

### 3. Country Analysis
- Rows per country per source
- GT match rate by country
- Do countries have different noise patterns?

### 4. Name Variation Catalog
For random 100 positive pairs, manually inspect:
- Type of variation: abbreviation, typo, DBA, transliteration, word order
- Frequency of each type
- Guides which features matter most

### 5. Address Variation Catalog
For random 100 positive pairs with address data:
- Type: abbreviation (Rd→Road), missing component, landmark reference
- PIN/ZIP present or missing?
- Partial vs full address
