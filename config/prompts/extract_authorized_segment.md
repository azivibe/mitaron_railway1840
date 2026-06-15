You are extracting structured data from a nineteenth-century British Parliamentary Paper about railway acts.

Return only valid JSON. Do not infer values that are not present. If a value is unclear, use null and explain in notes.
Preserve raw company and route names exactly, and also provide cleaned versions if possible.

Required JSON schema:
{
  "act_title_raw": string | null,
  "company_name_raw": string | null,
  "act_year": integer | null,
  "session_year": integer | null,
  "route_start_raw": string | null,
  "route_end_raw": string | null,
  "intermediate_places_raw": [string],
  "counties_raw": [string],
  "authorized_miles": number | null,
  "authorized_chains": number | null,
  "authorized_capital_pounds": number | null,
  "loan_power_pounds": number | null,
  "segment_type": "new_line" | "branch" | "extension" | "deviation" | "capital_only" | "amalgamation_or_lease" | "abandonment" | "unknown",
  "is_eligible_for_construction_rate": boolean,
  "evidence_text": string,
  "notes": string,
  "confidence": number
}
