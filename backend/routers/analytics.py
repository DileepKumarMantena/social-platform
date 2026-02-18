from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database
from typing import Optional, List
from datetime import datetime, timezone
from collections import defaultdict

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


@router.get("/analytics/trends")
def get_trend_analysis(current_user=Depends(get_current_user)):
    """Get trend analysis including best-performing posts, time slots, and channels"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Filter analytics for current tenant
    tenant_analytics = [a for a in database.ANALYTICS if a.get("tenant_id") == tenant_id]
    
    if not tenant_analytics:
        return {"message": "No analytics data available", "trends": {}}
    
    # Best performing posts
    best_posts = sorted(tenant_analytics, key=lambda x: x.get("engagement_rate", 0), reverse=True)[:5]
    
    # Best performing channels
    channel_performance = defaultdict(list)
    for analytic in tenant_analytics:
        channel_id = analytic.get("channel_id")
        channel_performance[channel_id].append(analytic)
    
    best_channels = []
    for channel_id, analytics in channel_performance.items():
        avg_engagement = sum(a.get("engagement_rate", 0) for a in analytics) / len(analytics)
        total_impressions = sum(a.get("impressions", 0) for a in analytics)
        channel = next((c for c in database.CHANNELS if c["id"] == channel_id), None)
        if channel:
            best_channels.append({
                "channel_id": channel_id,
                "channel_name": channel["name"],
                "avg_engagement_rate": round(avg_engagement, 2),
                "total_impressions": total_impressions,
                "post_count": len(analytics)
            })
    
    best_channels.sort(key=lambda x: x.get("avg_engagement_rate", 0), reverse=True)
    
    # Best time slots (hourly analysis)
    hourly_performance = defaultdict(lambda: {"engagement_rates": [], "impressions": []})
    for analytic in tenant_analytics:
        posted_at = analytic.get("posted_at", "")
        if posted_at:
            try:
                hour = datetime.fromisoformat(posted_at.replace("Z", "+00:00")).hour
                hourly_performance[hour]["engagement_rates"].append(analytic.get("engagement_rate", 0))
                hourly_performance[hour]["impressions"].append(analytic.get("impressions", 0))
            except:
                continue
    
    best_time_slots = []
    for hour, data in hourly_performance.items():
        if data["engagement_rates"]:
            avg_engagement = sum(data["engagement_rates"]) / len(data["engagement_rates"])
            total_impressions = sum(data["impressions"])
            best_time_slots.append({
                "hour": hour,
                "time_slot": f"{hour:02d}:00 - {hour:02d}:59",
                "avg_engagement_rate": round(avg_engagement, 2),
                "total_impressions": total_impressions,
                "post_count": len(data["engagement_rates"])
            })
    
    best_time_slots.sort(key=lambda x: x.get("avg_engagement_rate", 0), reverse=True)
    
    return {
        "best_performing_posts": [
            {
                "campaign_id": post.get("campaign_id"),
                "channel_id": post.get("channel_id"),
                "engagement_rate": post.get("engagement_rate"),
                "impressions": post.get("impressions"),
                "clicks": post.get("clicks"),
                "posted_at": post.get("posted_at")
            } for post in best_posts
        ],
        "best_performing_channels": best_channels[:5],
        "best_time_slots": best_time_slots[:5]
    }


@router.get("/analytics/recommendations")
def get_smart_recommendations(current_user=Depends(get_current_user)):
    """Get smart recommendations based on historical engagement data"""
    tenant_id = current_user.get("tenant_id", "")
    
    tenant_analytics = [a for a in database.ANALYTICS if a.get("tenant_id") == tenant_id]
    
    if not tenant_analytics:
        return {"message": "No analytics data available for recommendations", "recommendations": []}
    
    recommendations = []
    
    # Channel recommendations
    channel_performance = defaultdict(list)
    for analytic in tenant_analytics:
        channel_id = analytic.get("channel_id")
        channel_performance[channel_id].append(analytic)
    
    # Find best performing channel
    best_channel = None
    best_avg_engagement = 0
    for channel_id, analytics in channel_performance.items():
        avg_engagement = sum(a.get("engagement_rate", 0) for a in analytics) / len(analytics)
        if avg_engagement > best_avg_engagement:
            best_avg_engagement = avg_engagement
            best_channel = channel_id
    
    if best_channel:
        channel = next((c for c in database.CHANNELS if c["id"] == best_channel), None)
        if channel:
            recommendations.append({
                "type": "channel",
                "priority": "high",
                "title": f"Focus on {channel['name']}",
                "description": f"Your {channel['name']} campaigns have the highest engagement rate ({best_avg_engagement:.1f}%). Consider allocating more budget here.",
                "action": "Increase budget and frequency on this channel"
            })
    
    # Time slot recommendations
    hourly_performance = defaultdict(lambda: {"engagement_rates": []})
    for analytic in tenant_analytics:
        posted_at = analytic.get("posted_at", "")
        if posted_at:
            try:
                hour = datetime.fromisoformat(posted_at.replace("Z", "+00:00")).hour
                hourly_performance[hour]["engagement_rates"].append(analytic.get("engagement_rate", 0))
            except:
                continue
    
    # Find best time slots
    best_hours = []
    for hour, data in hourly_performance.items():
        if data["engagement_rates"]:
            avg_engagement = sum(data["engagement_rates"]) / len(data["engagement_rates"])
            best_hours.append((hour, avg_engagement))
    
    best_hours.sort(key=lambda x: x[1], reverse=True)
    
    if best_hours:
        top_hour, top_engagement = best_hours[0]
        recommendations.append({
            "type": "timing",
            "priority": "medium",
            "title": f"Optimal Posting Time: {top_hour:02d}:00",
            "description": f"Posts made around {top_hour:02d}:00 show {top_engagement:.1f}% average engagement. Schedule important posts during this time.",
            "action": f"Schedule campaigns between {top_hour:02d}:00-{top_hour+1:02d}:00"
        })
    
    # Content performance recommendations
    high_performing_posts = [a for a in tenant_analytics if a.get("engagement_rate", 0) > 5.0]
    low_performing_posts = [a for a in tenant_analytics if a.get("engagement_rate", 0) < 3.0]
    
    if high_performing_posts:
        recommendations.append({
            "type": "content",
            "priority": "medium",
            "title": "Replicate High-Performing Content",
            "description": f"You have {len(high_performing_posts)} posts with >5% engagement. Analyze what makes them successful.",
            "action": "Review successful content patterns and apply to future campaigns"
        })
    
    if low_performing_posts:
        recommendations.append({
            "type": "optimization",
            "priority": "low",
            "title": "Optimize Underperforming Posts",
            "description": f"{len(low_performing_posts)} posts have <3% engagement. Consider revising your content strategy.",
            "action": "Test different content formats, visuals, or messaging"
        })
    
    return {"recommendations": recommendations}


@router.get("/analytics/dashboard")
def get_analytics_dashboard(current_user=Depends(get_current_user)):
    """Get comprehensive analytics dashboard data"""
    tenant_id = current_user.get("tenant_id", "")
    
    tenant_analytics = [a for a in database.ANALYTICS if a.get("tenant_id") == tenant_id]
    tenant_campaigns = [c for c in database.CAMPAIGNS if c.get("tenant_id") == tenant_id]
    
    if not tenant_analytics:
        return {"message": "No analytics data available", "dashboard": {}}
    
    # Overall metrics
    total_impressions = sum(a.get("impressions", 0) for a in tenant_analytics)
    total_clicks = sum(a.get("clicks", 0) for a in tenant_analytics)
    avg_engagement = sum(a.get("engagement_rate", 0) for a in tenant_analytics) / len(tenant_analytics) if tenant_analytics else 0
    
    # Channel breakdown
    channel_metrics = {}
    for analytic in tenant_analytics:
        channel_id = analytic.get("channel_id")
        if channel_id not in channel_metrics:
            channel_metrics[channel_id] = {"impressions": 0, "clicks": 0, "posts": 0}
        channel_metrics[channel_id]["impressions"] += analytic.get("impressions", 0)
        channel_metrics[channel_id]["clicks"] += analytic.get("clicks", 0)
        channel_metrics[channel_id]["posts"] += 1
    
    # Format channel data
    channel_breakdown = []
    for channel_id, metrics in channel_metrics.items():
        channel = next((c for c in database.CHANNELS if c["id"] == channel_id), None)
        if channel:
            engagement_rate = (metrics["clicks"] / metrics["impressions"] * 100) if metrics["impressions"] > 0 else 0
            channel_breakdown.append({
                "channel_name": channel["name"],
                "impressions": metrics["impressions"],
                "clicks": metrics["clicks"],
                "engagement_rate": round(engagement_rate, 2),
                "posts": metrics["posts"]
            })
    
    return {
        "dashboard": {
            "overview": {
                "total_impressions": total_impressions,
                "total_clicks": total_clicks,
                "avg_engagement_rate": round(avg_engagement, 2),
                "total_campaigns": len(tenant_campaigns),
                "total_posts": len(tenant_analytics)
            },
            "channel_breakdown": channel_breakdown,
            "recent_performance": tenant_analytics[-10:] if tenant_analytics else []
        }
    }
