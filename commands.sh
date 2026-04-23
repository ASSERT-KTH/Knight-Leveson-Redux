# Oracle verification
pytest oracle/ -v

# Full pipeline
python -m pipeline.generate_versions  --config config/main.yaml  --output results/pilot/versions/
python -m pipeline.run_acceptance     --versions results/pilot/versions/ --output results/pilot/accepted.json
python -m pipeline.run_campaign       --accepted results/pilot/accepted.json --config config/main.yaml --output results/pilot/campaign.csv
python -m analysis.analyze_results    --campaign results/pilot/campaign.csv --output results/pilot/ --report report.md