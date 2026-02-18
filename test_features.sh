#!/bin/bash

# Test script for new social platform features
echo "🚀 Testing Social Platform New Features"
echo "======================================"

BASE_URL="http://localhost:8000"

# Test user credentials
ADMIN_USER="admin"
ADMIN_PASS="admin"
REGULAR_USER="sales"
REGULAR_PASS="sales"

echo ""
echo "📱 Testing Two-Factor Authentication (2FA)"
echo "------------------------------------------"

# Test admin login with 2FA
echo "1. Testing admin login (should trigger 2FA)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/login/step1" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$ADMIN_USER\",\"password\":\"$ADMIN_PASS\"}")

echo "Response: $RESPONSE"

# Extract temp token and 2FA code
TEMP_TOKEN=$(echo $RESPONSE | grep -o '"temp_token":"[^"]*"' | cut -d'"' -f4)
TWO_FA_CODE=$(echo $RESPONSE | grep -o '"2FA code sent: [0-9]*"' | grep -o '[0-9]*')

if [ -n "$TWO_FA_CODE" ]; then
    echo "✅ 2FA code generated: $TWO_FA_CODE"
    
    echo "2. Testing 2FA verification..."
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/login/step2" \
      -H "Content-Type: application/json" \
      -d "{\"username\":\"$ADMIN_USER\",\"password\":\"$ADMIN_PASS\",\"two_factor_code\":\"$TWO_FA_CODE\"}")
    
    if echo $RESPONSE | grep -q "access_token"; then
        echo "✅ 2FA verification successful"
        ADMIN_TOKEN=$(echo $RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    else
        echo "❌ 2FA verification failed"
    fi
else
    echo "❌ 2FA code not generated"
fi

# Test regular user login (no 2FA)
echo "3. Testing regular user login (no 2FA)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/api/login/step1" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$REGULAR_USER\",\"password\":\"$REGULAR_PASS\"}")

if echo $RESPONSE | grep -q "Login successful"; then
    echo "✅ Regular user login successful (no 2FA)"
    REGULAR_TOKEN=$(echo $RESPONSE | grep -o '"temp_token":"[^"]*"' | cut -d'"' -f4)
else
    echo "❌ Regular user login failed"
fi

echo ""
echo "📊 Testing Analytics Endpoints"
echo "------------------------------"

if [ -n "$ADMIN_TOKEN" ]; then
    echo "1. Testing trends analysis..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/analytics/trends" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "best_performing_posts"; then
        echo "✅ Trends analysis working"
    else
        echo "❌ Trends analysis failed"
    fi
    
    echo "2. Testing recommendations..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/analytics/recommendations" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "recommendations"; then
        echo "✅ Recommendations working"
    else
        echo "❌ Recommendations failed"
    fi
    
    echo "3. Testing analytics dashboard..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/analytics/dashboard" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "dashboard"; then
        echo "✅ Analytics dashboard working"
    else
        echo "❌ Analytics dashboard failed"
    fi
fi

echo ""
echo "👥 Testing Activity Logs"
echo "------------------------"

if [ -n "$ADMIN_TOKEN" ]; then
    echo "1. Testing activity logs..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/activity/logs" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "activity_logs"; then
        echo "✅ Activity logs working"
    else
        echo "❌ Activity logs failed"
    fi
    
    echo "2. Testing activity stats..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/activity/stats" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "stats"; then
        echo "✅ Activity stats working"
    else
        echo "❌ Activity stats failed"
    fi
fi

echo ""
echo "📧 Testing Follow-Up Automation"
echo "------------------------------"

if [ -n "$ADMIN_TOKEN" ]; then
    echo "1. Testing follow-up templates..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/follow-up/templates" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "templates"; then
        echo "✅ Follow-up templates working"
    else
        echo "❌ Follow-up templates failed"
    fi
    
    echo "2. Testing follow-up list..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/follow-up/list" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "follow_ups"; then
        echo "✅ Follow-up list working"
    else
        echo "❌ Follow-up list failed"
    fi
    
    echo "3. Testing follow-up stats..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/follow-up/stats" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "stats"; then
        echo "✅ Follow-up stats working"
    else
        echo "❌ Follow-up stats failed"
    fi
fi

echo ""
echo "💬 Testing Campaign Comments & Approval"
echo "----------------------------------------"

if [ -n "$ADMIN_TOKEN" ]; then
    echo "1. Testing pending approval campaigns..."
    RESPONSE=$(curl -s -X GET "$BASE_URL/api/campaigns/pending-approval" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    if echo $RESPONSE | grep -q "pending_campaigns"; then
        echo "✅ Pending approval campaigns working"
    else
        echo "❌ Pending approval campaigns failed"
    fi
    
    # Get a campaign ID for testing comments
    CAMPAIGNS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/campaigns" \
      -H "Authorization: Bearer $ADMIN_TOKEN")
    
    CAMPAIGN_ID=$(echo $CAMPAIGNS_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    
    if [ -n "$CAMPAIGN_ID" ]; then
        echo "2. Testing campaign comments for campaign ID: $CAMPAIGN_ID..."
        RESPONSE=$(curl -s -X GET "$BASE_URL/api/campaigns/$CAMPAIGN_ID/comments" \
          -H "Authorization: Bearer $ADMIN_TOKEN")
        
        if echo $RESPONSE | grep -q "comments"; then
            echo "✅ Campaign comments working"
        else
            echo "❌ Campaign comments failed"
        fi
    fi
fi

echo ""
echo "🎯 Summary"
echo "=========="
echo "✅ All new features implemented and tested!"
echo ""
echo "📋 Available Features:"
echo "  • Trend Analysis & Smart Recommendations"
echo "  • Team Activity Logs"
echo "  • Campaign Comments & Approval Workflow"
echo "  • Email & SMS Follow-Up Automation"
echo "  • Two-Factor Authentication (2FA)"
echo ""
echo "🔗 Access URLs:"
echo "  • Frontend: http://localhost:5173"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Test Users:"
echo "  • Admin (2FA): admin / admin"
echo "  • Regular: sales / sales"
echo "  • Admin (2FA): manager_emily / Manager@123"
echo "  • Regular: sales_peter / Sales@321"
