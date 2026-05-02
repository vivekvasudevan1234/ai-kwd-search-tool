# Workflow: Estimate AI Search Volume

## Objective
Given a keyword, country, and relative usage difference, return the estimated monthly AI search volume.

## Inputs
| Input | Source | Example |
|-------|--------|---------|
| Keyword | User | "programming" |
| Country | User (dropdown) | "USA" |
| Relative Usage Difference | User (looked up in SparkToro) | 8 |

## Formula
```
Est AI Monthly Search Vol = KW_Volume × (base_rate/100 × (1 + rel_diff/100)) × avg_ai_market_use
```

## Steps
1. User selects country → `tools/country_rates.py` returns `base_rate`, `avg_ai_market_use`, and `geo_target_id`
2. User enters keyword and relative usage difference (from SparkToro)
3. `tools/dataforseo_keyword.py` calls DataForSEO API with keyword + geo_target_id → returns `avg_monthly_searches`
4. `tools/calculate_ai_volume.py` applies the formula → returns estimated AI search volume
5. Results displayed: Google volume, estimated AI volume, formula breakdown

## Edge Cases
- **Keyword not found**: DataForSEO returns 0 or null — display a warning, show 0 as AI estimate
- **API credentials missing**: Show clear error: "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set in .env"
- **DataForSEO API error**: Show the status_message from the API response
- **Network timeout**: requests timeout is 30s; show "Failed to fetch keyword volume" on timeout

## Updating Country Rates
Edit `tools/country_rates.py` to update or add countries. Each entry needs:
```python
"Country Name": {
    "base_rate": <ChatGPT adoption % as integer>,
    "avg_ai_market_use": <fraction of searches through AI, e.g. 0.20>,
    "geo_target_id": <DataForSEO/Google geo target criterion ID>,
}
```
DataForSEO geo target IDs: https://developers.google.com/google-ads/api/data/geotargets

## Data Sources for Country Rates (last updated 2025)
- ChatGPT adoption rates: Visual Capitalist, Cybernews AI Adoption Index 2025
- Avg AI market use: Microsoft AI Economy Institute, OECD Digital Skills 2025
- Relative usage difference: SparkToro (paid) — topic-level AI affinity vs. baseline

## Running the Tool
```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your DataForSEO credentials
python app.py          # starts Flask at http://127.0.0.1:5000
```
