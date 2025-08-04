from flask import Blueprint, jsonify, request
from src.models.user import User, UserSession, UserPreference, db
from datetime import datetime, timedelta
import json
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Quick user registration - "We girls have no time" for complex signups
    Minimal required fields with smart defaults
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({
                'error': 'Username, email, and password are required',
                'message': 'Quick signup needs just the basics!'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'error': 'Username already exists',
                'message': 'Try a different username - we need you to be unique!'
            }), 409
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'error': 'Email already registered',
                'message': 'This email is already in use. Try logging in instead!'
            }), 409
        
        # Create new user with smart defaults
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age_range=data.get('age_range', '18-22'),  # Default to college age
            style_preference=data.get('style_preference', 'trendy'),  # Default for young users
            privacy_level=data.get('privacy_level', 'private'),  # Safe default
            marketing_consent=data.get('marketing_consent', False)
        )
        
        user.set_password(data['password'])
        
        # Set quick color preferences if provided
        if data.get('color_preferences'):
            user.color_preferences = json.dumps(data['color_preferences'])
        
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create default preferences for quick AI styling
        preferences = UserPreference(
            user_id=user.id,
            occasion_preferences=json.dumps(['casual', 'work', 'social']),  # Common occasions
            weather_sensitivity='medium',
            comfort_priority=7,  # High comfort priority for busy lifestyle
            trend_following=6,  # Moderate trend following
            budget_range=data.get('budget_range', 'medium'),
            conversation_style='friendly',
            notification_frequency='daily'
        )
        
        db.session.add(preferences)
        db.session.commit()
        
        # Generate auth token for immediate login
        token = user.generate_auth_token(expires_in=86400)  # 24 hours
        
        # Create session
        session = UserSession(
            user_id=user.id,
            session_token=str(uuid.uuid4()),
            device_info=json.dumps({
                'user_agent': request.headers.get('User-Agent', ''),
                'platform': 'web'
            }),
            ip_address=request.remote_addr,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Welcome to Tanvi! Ready to save time on styling?',
            'tagline': 'We girls have no time - let\'s get you styled quickly!',
            'user': user.to_dict(),
            'token': token,
            'session_id': session.session_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Quick login - "We girls have no time" for slow authentication
    """
    try:
        data = request.json
        
        if not data.get('username') and not data.get('email'):
            return jsonify({
                'error': 'Username or email required',
                'message': 'Quick login needs your username or email!'
            }), 400
            
        if not data.get('password'):
            return jsonify({
                'error': 'Password required',
                'message': 'Don\'t forget your password!'
            }), 400
        
        # Find user by username or email
        user = None
        if data.get('email'):
            user = User.query.filter_by(email=data['email']).first()
        elif data.get('username'):
            user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username/email or password is incorrect'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'error': 'Account inactive',
                'message': 'Your account has been deactivated. Contact support.'
            }), 403
        
        # Update last login
        user.update_last_login()
        
        # Generate new auth token
        token = user.generate_auth_token(expires_in=86400)  # 24 hours
        
        # Create new session
        session = UserSession(
            user_id=user.id,
            session_token=str(uuid.uuid4()),
            device_info=json.dumps({
                'user_agent': request.headers.get('User-Agent', ''),
                'platform': 'web'
            }),
            ip_address=request.remote_addr,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': f'Welcome back, {user.first_name or user.username}!',
            'tagline': 'We girls have no time - let\'s get you styled!',
            'user': user.to_dict(),
            'token': token,
            'session_id': session.session_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Quick logout - clean session termination
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Deactivate current session
        session_id = request.json.get('session_id') if request.json else None
        if session_id:
            session = UserSession.query.filter_by(
                user_id=user.id,
                session_token=session_id,
                is_active=True
            ).first()
            
            if session:
                session.is_active = False
                db.session.commit()
        
        return jsonify({
            'message': 'Logged out successfully',
            'tagline': 'See you soon - we\'ll be here when you need quick styling!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Logout failed',
            'message': str(e)
        }), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Quick token verification for maintaining sessions
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        
        if not user:
            return jsonify({
                'error': 'Invalid or expired token',
                'message': 'Please log in again'
            }), 401
        
        return jsonify({
            'message': 'Token valid',
            'user': user.to_dict(),
            'tagline': 'We girls have no time - you\'re still logged in!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Token verification failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """
    Refresh authentication token for extended sessions
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        
        if not user:
            return jsonify({
                'error': 'Invalid token',
                'message': 'Please log in again'
            }), 401
        
        # Generate new token
        new_token = user.generate_auth_token(expires_in=86400)  # 24 hours
        
        return jsonify({
            'message': 'Token refreshed',
            'token': new_token,
            'user': user.to_dict(),
            'tagline': 'We girls have no time - your session is extended!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500


@auth_bp.route('/quick-setup', methods=['POST'])
def quick_setup():
    """
    Quick profile setup after registration - "We girls have no time"
    Streamlined onboarding with smart defaults
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        token = auth_header.split(' ')[1]
        user = User.verify_auth_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        data = request.json
        
        # Update user profile with quick setup data
        if data.get('style_preference'):
            user.style_preference = data['style_preference']
        
        if data.get('color_preferences'):
            user.color_preferences = json.dumps(data['color_preferences'])
        
        if data.get('size_info'):
            user.size_info = json.dumps(data['size_info'])
        
        if data.get('age_range'):
            user.age_range = data['age_range']
        
        # Update preferences
        preferences = user.preferences
        if not preferences:
            preferences = UserPreference(user_id=user.id)
            db.session.add(preferences)
        
        if data.get('occasion_preferences'):
            preferences.occasion_preferences = json.dumps(data['occasion_preferences'])
        
        if data.get('budget_range'):
            preferences.budget_range = data['budget_range']
        
        if data.get('comfort_priority'):
            preferences.comfort_priority = data['comfort_priority']
        
        if data.get('trend_following'):
            preferences.trend_following = data['trend_following']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quick setup complete! Ready for AI styling.',
            'tagline': 'We girls have no time - you\'re all set for instant styling!',
            'user': user.to_dict(),
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Quick setup failed',
            'message': str(e)
        }), 500

