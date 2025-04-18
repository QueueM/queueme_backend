"""
This module provides a dummy implementation for video content analysis.
"""

def analyze_video_content(video_instance):
    if hasattr(video_instance, 'caption') and video_instance.caption and "funny" in video_instance.caption.lower():
        return {"tags": ["humor", "funny"], "confidence": 0.95}
    return {"tags": ["general"], "confidence": 0.70}
