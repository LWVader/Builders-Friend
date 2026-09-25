// Example using Supabase JavaScript SDK in Next.js
const { data, error } = await supabase
  .rpc('match_ldc_chunks', {
    query_embedding: localGeneratedVector, // 384 dimensions from MiniLM
    match_threshold: 0.3,
    match_count: 3
  })
  // Hard metadata filter: Only return chunks where the applicable_zones array contains the property's zone code!
  .contains('metadata', { applicable_zones: [propertyZoningCode] });