import pandas as pd

def test_event_catalog():
    events = pd.read_csv('../../data/processed/key_events.csv')
    assert len(events) >= 10, "Catalog must contain ≥10 events"
    assert pd.api.types.is_datetime64_dtype(pd.to_datetime(events['Date']))