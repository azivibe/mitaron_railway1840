You are adjudicating whether a Parliamentary railway authorisation corresponds to a constructed/opened railway line in GIS data.

Return only valid JSON. Base your decision on company name, route endpoints, intermediate places, counties, authorised length, GIS length, act year, and opening year. Do not assume a match solely from company name.

Required JSON schema:
{
  "decision": "matched" | "partial_matched" | "not_found" | "ambiguous" | "not_applicable",
  "best_gis_segment_id": string | null,
  "match_confidence": number,
  "reason": string,
  "key_evidence": [string],
  "needs_manual_review": boolean
}
