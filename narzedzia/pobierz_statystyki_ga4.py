from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account

OUTPUT = Path("dane_publiczne/statystyki_strony.json")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Brak wymaganej zmiennej środowiskowej: {name}")
    return value


def rows_to_dicts(response):
    dimensions = [h.name for h in response.dimension_headers]
    metrics = [h.name for h in response.metric_headers]
    result = []
    for row in response.rows:
        item = {name: value.value for name, value in zip(dimensions, row.dimension_values)}
        item.update({name: value.value for name, value in zip(metrics, row.metric_values)})
        result.append(item)
    return result


def run_report(client, property_id: str, *, dimensions, metrics, limit=100):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=name) for name in dimensions],
        metrics=[Metric(name=name) for name in metrics],
        date_ranges=[DateRange(start_date="28daysAgo", end_date="yesterday")],
        limit=limit,
    )
    return client.run_report(request)


def main() -> None:
    property_id = require_env("GA4_PROPERTY_ID")
    credentials_json = require_env("GA4_SERVICE_ACCOUNT_JSON")
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    client = BetaAnalyticsDataClient(credentials=credentials)

    summary = run_report(
        client,
        property_id,
        dimensions=[],
        metrics=[
            "totalUsers",
            "newUsers",
            "sessions",
            "screenPageViews",
            "averageSessionDuration",
            "engagementRate",
        ],
        limit=1,
    )

    acquisition = run_report(
        client,
        property_id,
        dimensions=["sessionSourceMedium"],
        metrics=["sessions", "totalUsers"],
        limit=20,
    )
    pages = run_report(
        client,
        property_id,
        dimensions=["pagePath"],
        metrics=["screenPageViews", "totalUsers", "averageSessionDuration"],
        limit=20,
    )
    countries = run_report(
        client,
        property_id,
        dimensions=["country"],
        metrics=["totalUsers", "sessions"],
        limit=20,
    )
    devices = run_report(
        client,
        property_id,
        dimensions=["deviceCategory"],
        metrics=["totalUsers", "sessions"],
        limit=10,
    )
    new_returning = run_report(
        client,
        property_id,
        dimensions=["newVsReturning"],
        metrics=["totalUsers", "sessions"],
        limit=10,
    )

    payload = {
        "source": "Google Analytics 4",
        "property_id": property_id,
        "period": {"start": "28daysAgo", "end": "yesterday"},
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": rows_to_dicts(summary),
        "new_vs_returning": rows_to_dicts(new_returning),
        "traffic_sources": rows_to_dicts(acquisition),
        "top_pages": rows_to_dicts(pages),
        "countries": rows_to_dicts(countries),
        "devices": rows_to_dicts(devices),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
