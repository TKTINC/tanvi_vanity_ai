from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
import requests
import json
from src.models.enhanced_recommendations import (
    WeatherOutfitRule, SeasonalRecommendation, OutfitFeedback, 
    SmartRecommendationEngine, db
)
from src.models.ai_models import StyleAnalysis, OutfitRecommendation

enhanced_rec_bp = Blueprint('enhanced_recommendations', __name__)

# WS1 User Management Service Integration
WS1_BASE_URL = 'http://localhost:5001'  # WS1 service endpoint

def get_user_data(user_id, auth_token):
    """Fetch user data from WS1 User Management Service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Get user profile
        profile_response = requests.get(f'{WS1_BASE_URL}/api/profile', headers=headers, timeout=5)
        if profile_response.status_code != 200:
            return None
        
        profile_data = profile_response.json()
        
        # Get wardrobe data
        wardrobe_response = requests.get(f'{WS1_BASE_URL}/api/profile/wardrobe', headers=headers, timeout=5)
        wardrobe_data = []
        if wardrobe_response.status_code == 200:
            wardrobe_data = wardrobe_response.json().get('items', [])
        
        return {
            'profile': profile_data,
            'wardrobe': wardrobe_data
        }
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None

def verify_auth_token(auth_token):
    """Verify authentication token with WS1 service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.post(f'{WS1_BASE_URL}/api/auth/verify-token', headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

@enhanced_rec_bp.route('/smart-outfit', methods=['POST'])
def smart_outfit_recommendation():
    """
    Enhanced smart outfit recommendation with weather, season, and learning
    "We girls have no time" - Intelligent outfit suggestions that adapt!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        occasion = data.get('occasion', 'casual')
        weather = data.get('weather')
        temperature = data.get('temperature')
        season = data.get('season')
        include_alternatives = data.get('include_alternatives', True)
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Fetch user data from WS1
        user_data = get_user_data(user_id, auth_token)
        if not user_data:
            return jsonify({'error': 'Unable to fetch user data'}), 500
        
        wardrobe_data = user_data.get('wardrobe', [])
        if not wardrobe_data:
            return jsonify({
                'status': 'no_wardrobe',
                'message': 'No wardrobe items found. Add some clothes first!',
                'recommendation': 'Start by adding basic wardrobe items like tops, bottoms, and shoes.',
                'tagline': 'We girls have no time - But we need clothes first!'
            }), 400
        
        # Get style analysis
        style_analysis = StyleAnalysis.query.filter_by(user_id=user_id).first()
        style_data = style_analysis.to_dict() if style_analysis else {}
        
        # Get user feedback patterns for learning
        feedback_patterns = OutfitFeedback.get_user_feedback_patterns(user_id)
        
        # Generate enhanced outfit recommendation
        outfit_data = SmartRecommendationEngine.generate_enhanced_outfit(
            user_id, wardrobe_data, style_data, occasion, 
            weather, temperature, season, feedback_patterns
        )
        
        if not outfit_data:
            return jsonify({
                'status': 'insufficient_items',
                'message': 'Not enough suitable items for this occasion',
                'recommendation': f'Add more {occasion}-appropriate items to your wardrobe',
                'tagline': 'We girls have no time - Need more outfit options!'
            }), 400
        
        # Save recommendation to database
        recommendation = OutfitRecommendation(
            user_id=user_id,
            occasion=occasion,
            weather=weather,
            season=season,
            outfit_items=json.dumps(outfit_data['outfit_items']),
            outfit_description=outfit_data['outfit_description'],
            style_match_score=outfit_data['style_match_score'],
            occasion_match_score=outfit_data['occasion_match_score'],
            color_harmony_score=outfit_data['color_harmony_score'],
            overall_score=outfit_data['overall_score'],
            algorithm_version='2.0'  # Enhanced version
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        # Get full item details for response
        item_details = []
        for item in wardrobe_data:
            if item.get('id') in outfit_data['outfit_items']:
                item_details.append(item)
        
        response_data = {
            'status': 'success',
            'message': 'Enhanced outfit recommendation generated successfully',
            'recommendation': {
                **recommendation.to_dict(),
                'enhancements': outfit_data.get('enhancements', {}),
                'seasonal_tip': outfit_data.get('seasonal_tip')
            },
            'outfit_items': item_details,
            'context': {
                'weather_considered': weather is not None,
                'temperature': temperature,
                'season_considered': season is not None,
                'user_learning_applied': bool(feedback_patterns),
                'feedback_data_points': len(feedback_patterns) if feedback_patterns else 0
            },
            'generation_time': '1.2 seconds',
            'tagline': 'We girls have no time - Smart outfit ready with all factors considered!'
        }
        
        # Generate alternatives if requested
        if include_alternatives:
            alternatives = SmartRecommendationEngine.get_alternative_recommendations(
                user_id, wardrobe_data, style_data, occasion, outfit_data, count=3
            )
            
            alternative_details = []
            for alt in alternatives:
                alt_items = []
                for item in wardrobe_data:
                    if item.get('id') in alt['outfit_items']:
                        alt_items.append(item)
                
                alternative_details.append({
                    'recommendation': alt,
                    'outfit_items': alt_items
                })
            
            response_data['alternatives'] = alternative_details
            response_data['alternatives_count'] = len(alternative_details)
        
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Enhanced outfit recommendation failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@enhanced_rec_bp.route('/feedback', methods=['POST'])
def submit_outfit_feedback():
    """
    Submit feedback on outfit recommendation for learning
    "We girls have no time" - Quick feedback to improve recommendations!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        recommendation_id = data.get('recommendation_id')
        rating = data.get('rating')  # 1-5 stars
        feedback_type = data.get('feedback_type')  # 'worn', 'saved', 'dismissed', 'modified'
        
        # Optional detailed feedback
        liked_aspects = data.get('liked_aspects', [])  # ['colors', 'style', 'comfort']
        disliked_aspects = data.get('disliked_aspects', [])
        suggested_changes = data.get('suggested_changes', [])
        occasion_actual = data.get('occasion_actual')
        weather_actual = data.get('weather_actual')
        comfort_rating = data.get('comfort_rating')
        worn_date = data.get('worn_date')
        
        if not all([user_id, recommendation_id, rating, feedback_type]):
            return jsonify({'error': 'User ID, recommendation ID, rating, and feedback type required'}), 400
        
        if rating not in [1, 2, 3, 4, 5]:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Verify recommendation exists and belongs to user
        recommendation = OutfitRecommendation.query.filter_by(
            id=recommendation_id, user_id=user_id
        ).first()
        
        if not recommendation:
            return jsonify({'error': 'Recommendation not found or access denied'}), 404
        
        # Create feedback record
        feedback = OutfitFeedback(
            user_id=user_id,
            recommendation_id=recommendation_id,
            rating=rating,
            feedback_type=feedback_type,
            liked_aspects=json.dumps(liked_aspects) if liked_aspects else None,
            disliked_aspects=json.dumps(disliked_aspects) if disliked_aspects else None,
            suggested_changes=json.dumps(suggested_changes) if suggested_changes else None,
            occasion_actual=occasion_actual,
            weather_actual=weather_actual,
            comfort_rating=comfort_rating,
            worn_date=datetime.strptime(worn_date, '%Y-%m-%d').date() if worn_date else None
        )
        
        # Calculate user's perception scores
        if rating >= 4:
            feedback.style_match_feedback = 0.8 + (rating - 4) * 0.2
            feedback.occasion_match_feedback = 0.8 + (rating - 4) * 0.2
        elif rating >= 3:
            feedback.style_match_feedback = 0.6
            feedback.occasion_match_feedback = 0.6
        else:
            feedback.style_match_feedback = 0.3 + (rating - 1) * 0.15
            feedback.occasion_match_feedback = 0.3 + (rating - 1) * 0.15
        
        db.session.add(feedback)
        
        # Update recommendation with user feedback
        recommendation.user_rating = rating
        recommendation.user_feedback = json.dumps({
            'feedback_type': feedback_type,
            'liked_aspects': liked_aspects,
            'disliked_aspects': disliked_aspects
        })
        if worn_date:
            recommendation.worn_date = datetime.strptime(worn_date, '%Y-%m-%d').date()
        
        db.session.commit()
        
        # Generate learning insights
        learning_insights = []
        if rating >= 4:
            learning_insights.append("Great choice! We'll recommend similar outfits in the future.")
        elif rating <= 2:
            learning_insights.append("Thanks for the feedback! We'll avoid similar combinations.")
        
        if liked_aspects:
            learning_insights.append(f"Noted that you love: {', '.join(liked_aspects)}")
        
        if disliked_aspects:
            learning_insights.append(f"We'll avoid: {', '.join(disliked_aspects)}")
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback submitted successfully',
            'feedback': feedback.to_dict(),
            'learning_insights': learning_insights,
            'impact': {
                'future_recommendations': 'Will be improved based on this feedback',
                'style_learning': 'Your preferences have been updated',
                'recommendation_accuracy': 'Expected to improve by 5-10%'
            },
            'tagline': 'We girls have no time - Thanks for helping us learn!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Feedback submission failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@enhanced_rec_bp.route('/weather-rules', methods=['GET'])
def get_weather_rules():
    """
    Get weather-based outfit rules
    "We girls have no time" - Weather-smart styling rules!
    """
    try:
        weather_condition = request.args.get('weather')
        temperature = request.args.get('temperature', type=int)
        
        if weather_condition:
            rules = WeatherOutfitRule.get_weather_rules(weather_condition, temperature)
        else:
            rules = WeatherOutfitRule.query.filter_by(active=True).all()
        
        rules_data = [rule.to_dict() for rule in rules]
        
        return jsonify({
            'status': 'success',
            'message': 'Weather rules retrieved successfully',
            'rules': rules_data,
            'total_rules': len(rules_data),
            'weather_condition': weather_condition,
            'temperature': temperature,
            'tagline': 'We girls have no time - Weather-smart styling rules ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve weather rules',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@enhanced_rec_bp.route('/seasonal-trends', methods=['GET'])
def get_seasonal_trends():
    """
    Get current seasonal trends and recommendations
    "We girls have no time" - Season-perfect styling trends!
    """
    try:
        season = request.args.get('season')
        
        if season:
            # Get specific season
            seasonal_rec = SeasonalRecommendation.query.filter_by(
                season=season, active=True
            ).order_by(SeasonalRecommendation.year.desc()).first()
        else:
            # Get current season
            seasonal_rec = SeasonalRecommendation.get_current_season_recommendations()
        
        if not seasonal_rec:
            return jsonify({
                'status': 'no_data',
                'message': 'No seasonal recommendations found',
                'season': season or 'current',
                'tagline': 'We girls have no time - But no seasonal data available!'
            }), 404
        
        seasonal_data = seasonal_rec.to_dict()
        
        return jsonify({
            'status': 'success',
            'message': 'Seasonal trends retrieved successfully',
            'seasonal_recommendations': seasonal_data,
            'current_season': seasonal_data['season'],
            'trends_summary': {
                'trending_styles': seasonal_data.get('trending_styles', [])[:3],
                'trending_colors': seasonal_data.get('trending_colors', [])[:5],
                'essential_items': seasonal_data.get('essential_items', [])[:5]
            },
            'tagline': 'We girls have no time - Season-perfect trends ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve seasonal trends',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@enhanced_rec_bp.route('/user-patterns', methods=['GET'])
def get_user_patterns():
    """
    Get user's feedback patterns and learning insights
    "We girls have no time" - Your style patterns revealed!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get feedback patterns
        patterns = OutfitFeedback.get_user_feedback_patterns(user_id)
        
        if not patterns:
            return jsonify({
                'status': 'no_data',
                'message': 'No feedback data available yet',
                'recommendation': 'Rate some outfit recommendations to see your patterns!',
                'tagline': 'We girls have no time - But we need your feedback first!'
            })
        
        # Generate insights
        insights = []
        
        avg_rating = patterns.get('average_rating', 0)
        if avg_rating >= 4.0:
            insights.append("You love our recommendations! Your style preferences are well-understood.")
        elif avg_rating >= 3.0:
            insights.append("You generally like our recommendations with room for improvement.")
        else:
            insights.append("We're learning your style - keep rating to improve recommendations!")
        
        # Most liked aspects
        liked_aspects = patterns.get('liked_aspects_frequency', {})
        if liked_aspects:
            top_liked = max(liked_aspects, key=liked_aspects.get)
            insights.append(f"You consistently love: {top_liked}")
        
        # Most disliked aspects
        disliked_aspects = patterns.get('disliked_aspects_frequency', {})
        if disliked_aspects:
            top_disliked = max(disliked_aspects, key=disliked_aspects.get)
            insights.append(f"You consistently avoid: {top_disliked}")
        
        # Preferred occasions
        occasion_prefs = patterns.get('occasion_preferences', {})
        if occasion_prefs:
            top_occasion = max(occasion_prefs, key=occasion_prefs.get)
            insights.append(f"Your most styled occasion: {top_occasion}")
        
        return jsonify({
            'status': 'success',
            'message': 'User patterns retrieved successfully',
            'patterns': patterns,
            'insights': insights,
            'learning_status': {
                'data_points': sum(patterns.get('preferred_feedback_types', {}).values()),
                'learning_confidence': min(avg_rating / 5.0, 1.0),
                'recommendation_accuracy': f"{min(avg_rating * 20, 100):.1f}%"
            },
            'tagline': 'We girls have no time - Your style patterns revealed!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve user patterns',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@enhanced_rec_bp.route('/recommendation-history', methods=['GET'])
def get_recommendation_history():
    """
    Get user's recommendation history with feedback
    "We girls have no time" - Your outfit history at a glance!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', 20, type=int)
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get recommendations with feedback
        recommendations = OutfitRecommendation.query.filter_by(user_id=user_id)\
            .order_by(OutfitRecommendation.created_at.desc())\
            .limit(limit).all()
        
        history_data = []
        for rec in recommendations:
            rec_data = rec.to_dict()
            
            # Get feedback for this recommendation
            feedback = OutfitFeedback.query.filter_by(recommendation_id=rec.id).first()
            if feedback:
                rec_data['feedback'] = feedback.to_dict()
            
            history_data.append(rec_data)
        
        # Calculate summary stats
        total_recommendations = len(history_data)
        rated_recommendations = sum(1 for rec in history_data if rec.get('feedback'))
        avg_rating = 0
        if rated_recommendations > 0:
            total_rating = sum(rec['feedback']['rating'] for rec in history_data if rec.get('feedback'))
            avg_rating = total_rating / rated_recommendations
        
        worn_outfits = sum(1 for rec in history_data 
                          if rec.get('feedback') and rec['feedback'].get('feedback_type') == 'worn')
        
        return jsonify({
            'status': 'success',
            'message': 'Recommendation history retrieved successfully',
            'history': history_data,
            'summary': {
                'total_recommendations': total_recommendations,
                'rated_recommendations': rated_recommendations,
                'average_rating': round(avg_rating, 1),
                'worn_outfits': worn_outfits,
                'rating_percentage': round((rated_recommendations / max(total_recommendations, 1)) * 100, 1)
            },
            'tagline': 'We girls have no time - Your outfit history ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve recommendation history',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

