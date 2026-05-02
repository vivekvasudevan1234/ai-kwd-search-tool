def estimate_ai_volume(kw_volume, base_rate, relative_diff, avg_ai_market_use):
    """
    Formula from AI Search Forecast Calculator (SEO for LLMs Course).
    base_rate and avg_ai_market_use are per-country values from country_rates.py.
    relative_diff comes from SparkToro (topic-level AI affinity vs. baseline).
    """
    return kw_volume * (base_rate / 100 * (1 + relative_diff / 100)) * avg_ai_market_use


if __name__ == "__main__":
    # Verify against Excel examples
    cases = [
        ("Programming",         22000, 62, 8,     0.20, 2946.24),
        ("Portfolio web design", 200,  62, 62,    0.20, 40.176),
        ("Minivans",             6400, 62, -15.2, 0.20, 672.9728),
        ("Potatoes",            99000, 62, -15.2, 0.20, 10410.048),
        ("Accident lawyer",     40000, 62, -7.2,  0.20, 4602.88),
    ]
    all_pass = True
    for name, vol, br, rd, aim, expected in cases:
        result = estimate_ai_volume(vol, br, rd, aim)
        ok = abs(result - expected) < 0.01
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"{status}  {name:22s}  expected={expected:.4f}  got={result:.4f}")
    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED.")
