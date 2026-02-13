#!/bin/bash

echo "🧪 Testing Feature Flag Integration..."
echo ""

API_URL="http://localhost:30080"

echo "═══════════════════════════════════════════════════"
echo "  TEST 1: Health Check"
echo "═══════════════════════════════════════════════════"
curl -s $API_URL/health | jq .
echo ""

echo "═══════════════════════════════════════════════════"
echo "  TEST 2: App Info"
echo "═══════════════════════════════════════════════════"
curl -s $API_URL/api/info | jq .
echo ""

echo "═══════════════════════════════════════════════════"
echo "  TEST 3: Price Calculation (10 requests)"
echo "═══════════════════════════════════════════════════"
echo "Sending 10 requests to /price?amount=100..."
echo ""

for i in {1..10}; do
  RESPONSE=$(curl -s "$API_URL/price?amount=100")
  FINAL_PRICE=$(echo $RESPONSE | jq -r '.final_price')
  METHOD=$(echo $RESPONSE | jq -r '.pricing_method')
  FLAG_ACTIVE=$(echo $RESPONSE | jq -r '.feature_flag_active')
  
  echo "Request $i: Price=$FINAL_PRICE | Method=$METHOD | Flag=$FLAG_ACTIVE"
  sleep 0.5
done

echo ""
echo "═══════════════════════════════════════════════════"
echo "  TEST 4: Feature Flag Metrics"
echo "═══════════════════════════════════════════════════"
echo "Feature flag usage:"
curl -s $API_URL/metrics | grep "app_feature_flag_usage_total"
echo ""
echo "Pricing method distribution:"
curl -s $API_URL/metrics | grep "app_price_calculation_total"
echo ""

echo "═══════════════════════════════════════════════════"
echo "  ✅ Tests Complete!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "💡 TIP: Toggle the flag in Unleash UI and run this script again"
echo "   to see the behavior change in real-time!"
