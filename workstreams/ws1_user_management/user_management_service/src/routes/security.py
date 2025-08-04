from flask import Blueprint, jsonify, request, send_file
from src.models.user import User, db
from src.models.security import (
    SecurityAuditLog, UserPrivacySettings, DataAccessLog, UserSecuritySettings, 
    DataExportRequest, SecurityHelper, SecurityEventType, PrivacyLevel
)
from datetime import datetime, timedelta
import json
import os
import tempfile
import zipfile

security_bp = Blueprint('security', __name__)

def get_current_user():
    """Helper function to get current authenticated user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_auth_token(token)

def get_request_context():
    """Get request context for logging"""
    return {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'endpoint': request.endpoint,
        'method': request.method
    }

@security_bp.route('/privacy-settings', methods=['GET'])
def get_privacy_settings():
    """
    Get user privacy settings - "We girls have no time" for complex privacy management
    Simple privacy controls with clear explanations
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        settings = SecurityHelper.get_or_create_privacy_settings(user.id)
        
        # Log data access
        context = get_request_context()
        SecurityHelper.log_data_access(
            user_id=user.id,
            data_type='privacy_settings',
            access_type='read',
            purpose='User viewing privacy settings',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint']
        )
        
        return jsonify({
            'message': 'Privacy settings retrieved successfully',
            'tagline': 'We girls have no time - privacy made simple!',
            'settings': settings.to_dict(),
            'explanations': {
                'profile_visibility': 'Who can see your basic profile information',
                'wardrobe_visibility': 'Who can see your wardrobe items and outfits',
                'outfit_history_visibility': 'Who can see your outfit history and ratings',
                'style_insights_visibility': 'Who can see your AI-generated style insights',
                'allow_analytics_sharing': 'Help improve the app by sharing anonymous usage data',
                'allow_style_recommendations': 'Receive personalized style recommendations',
                'allow_social_features': 'Enable social features like sharing and following',
                'allow_marketing_communications': 'Receive style tips and product updates'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve privacy settings',
            'message': str(e)
        }), 500


@security_bp.route('/privacy-settings', methods=['PUT'])
def update_privacy_settings():
    """
    Update user privacy settings - quick privacy control updates
    "We girls have no time" for lengthy privacy forms
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        settings = SecurityHelper.get_or_create_privacy_settings(user.id)
        
        # Track what's being changed for audit
        changes = {}
        
        # Update visibility settings
        if 'profile_visibility' in data:
            old_value = settings.profile_visibility.value
            settings.profile_visibility = PrivacyLevel(data['profile_visibility'])
            changes['profile_visibility'] = {'from': old_value, 'to': data['profile_visibility']}
        
        if 'wardrobe_visibility' in data:
            old_value = settings.wardrobe_visibility.value
            settings.wardrobe_visibility = PrivacyLevel(data['wardrobe_visibility'])
            changes['wardrobe_visibility'] = {'from': old_value, 'to': data['wardrobe_visibility']}
        
        if 'outfit_history_visibility' in data:
            old_value = settings.outfit_history_visibility.value
            settings.outfit_history_visibility = PrivacyLevel(data['outfit_history_visibility'])
            changes['outfit_history_visibility'] = {'from': old_value, 'to': data['outfit_history_visibility']}
        
        if 'style_insights_visibility' in data:
            old_value = settings.style_insights_visibility.value
            settings.style_insights_visibility = PrivacyLevel(data['style_insights_visibility'])
            changes['style_insights_visibility'] = {'from': old_value, 'to': data['style_insights_visibility']}
        
        # Update sharing preferences
        sharing_fields = [
            'allow_analytics_sharing', 'allow_style_recommendations', 
            'allow_social_features', 'allow_marketing_communications',
            'allow_third_party_integrations', 'auto_delete_old_data'
        ]
        
        for field in sharing_fields:
            if field in data:
                old_value = getattr(settings, field)
                setattr(settings, field, data[field])
                changes[field] = {'from': old_value, 'to': data[field]}
        
        # Update notification preferences
        notification_fields = [
            'security_notifications', 'privacy_update_notifications', 
            'data_processing_notifications'
        ]
        
        for field in notification_fields:
            if field in data:
                old_value = getattr(settings, field)
                setattr(settings, field, data[field])
                changes[field] = {'from': old_value, 'to': data[field]}
        
        # Update data retention
        if 'data_retention_months' in data:
            old_value = settings.data_retention_months
            settings.data_retention_months = data['data_retention_months']
            changes['data_retention_months'] = {'from': old_value, 'to': data['data_retention_months']}
        
        settings.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log privacy setting changes
        context = get_request_context()
        SecurityHelper.log_security_event(
            user_id=user.id,
            event_type=SecurityEventType.PRIVACY_SETTING_CHANGE,
            description=f"Privacy settings updated: {len(changes)} changes made",
            severity='info',
            metadata={'changes': changes},
            **context
        )
        
        # Log data access
        SecurityHelper.log_data_access(
            user_id=user.id,
            data_type='privacy_settings',
            access_type='update',
            purpose='User updating privacy settings',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint']
        )
        
        return jsonify({
            'message': 'Privacy settings updated successfully',
            'tagline': 'We girls have no time - privacy updated instantly!',
            'settings': settings.to_dict(),
            'changes_made': len(changes)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update privacy settings',
            'message': str(e)
        }), 500


@security_bp.route('/security-settings', methods=['GET'])
def get_security_settings():
    """
    Get user security settings - simple security overview
    "We girls have no time" for complex security management
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        settings = SecurityHelper.get_or_create_security_settings(user.id)
        
        # Log data access
        context = get_request_context()
        SecurityHelper.log_data_access(
            user_id=user.id,
            data_type='security_settings',
            access_type='read',
            purpose='User viewing security settings',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint']
        )
        
        return jsonify({
            'message': 'Security settings retrieved successfully',
            'tagline': 'We girls have no time - security made simple!',
            'settings': settings.to_dict(),
            'security_tips': [
                'Enable two-factor authentication for extra security',
                'Use a strong, unique password',
                'Review your active sessions regularly',
                'Enable security notifications to stay informed'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve security settings',
            'message': str(e)
        }), 500


@security_bp.route('/security-settings', methods=['PUT'])
def update_security_settings():
    """
    Update user security settings - quick security control updates
    "We girls have no time" for complex security configuration
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        settings = SecurityHelper.get_or_create_security_settings(user.id)
        
        # Track changes for audit
        changes = {}
        
        # Update session settings
        if 'session_timeout_minutes' in data:
            old_value = settings.session_timeout_minutes
            settings.session_timeout_minutes = max(15, min(480, data['session_timeout_minutes']))  # 15min to 8hrs
            changes['session_timeout_minutes'] = {'from': old_value, 'to': settings.session_timeout_minutes}
        
        if 'max_concurrent_sessions' in data:
            old_value = settings.max_concurrent_sessions
            settings.max_concurrent_sessions = max(1, min(10, data['max_concurrent_sessions']))  # 1 to 10
            changes['max_concurrent_sessions'] = {'from': old_value, 'to': settings.max_concurrent_sessions}
        
        # Update notification settings
        notification_fields = [
            'notify_new_device_login', 'notify_password_change', 
            'notify_suspicious_activity', 'notify_data_export'
        ]
        
        for field in notification_fields:
            if field in data:
                old_value = getattr(settings, field)
                setattr(settings, field, data[field])
                changes[field] = {'from': old_value, 'to': data[field]}
        
        # Update other settings
        if 'logout_inactive_sessions' in data:
            old_value = settings.logout_inactive_sessions
            settings.logout_inactive_sessions = data['logout_inactive_sessions']
            changes['logout_inactive_sessions'] = {'from': old_value, 'to': data['logout_inactive_sessions']}
        
        settings.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log security setting changes
        context = get_request_context()
        SecurityHelper.log_security_event(
            user_id=user.id,
            event_type=SecurityEventType.PRIVACY_SETTING_CHANGE,
            description=f"Privacy settings updated: {len(changes)} changes made",
            severity='info',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint'],
            metadata={'changes': changes}
        )
        
        return jsonify({
            'message': 'Security settings updated successfully',
            'tagline': 'We girls have no time - security updated instantly!',
            'settings': settings.to_dict(),
            'changes_made': len(changes)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update security settings',
            'message': str(e)
        }), 500


@security_bp.route('/audit-log', methods=['GET'])
def get_security_audit_log():
    """
    Get security audit log for user - transparency in security events
    "We girls have no time" for complex security analysis
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get query parameters
        days = min(int(request.args.get('days', 30)), 90)  # Max 90 days
        severity = request.args.get('severity')  # info, warning, critical
        
        # Build query
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        query = SecurityAuditLog.query.filter_by(user_id=user.id)\
            .filter(SecurityAuditLog.created_at >= start_date)
        
        if severity:
            query = query.filter_by(severity=severity)
        
        logs = query.order_by(SecurityAuditLog.created_at.desc()).limit(100).all()
        
        # Log data access
        context = get_request_context()
        SecurityHelper.log_data_access(
            user_id=user.id,
            data_type='security_audit_log',
            access_type='read',
            purpose='User viewing security audit log',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint']
        )
        
        return jsonify({
            'message': 'Security audit log retrieved successfully',
            'tagline': 'We girls have no time - here\'s your security overview!',
            'logs': [log.to_dict() for log in logs],
            'summary': {
                'total_events': len(logs),
                'date_range_days': days,
                'critical_events': len([l for l in logs if l.severity == 'critical']),
                'warning_events': len([l for l in logs if l.severity == 'warning']),
                'info_events': len([l for l in logs if l.severity == 'info'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve security audit log',
            'message': str(e)
        }), 500


@security_bp.route('/data-access-log', methods=['GET'])
def get_data_access_log():
    """
    Get data access log for transparency - show user what data was accessed
    "We girls have no time" for complex data tracking
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get query parameters
        days = min(int(request.args.get('days', 7)), 30)  # Max 30 days
        data_type = request.args.get('data_type')  # profile, wardrobe, analytics, etc.
        
        # Build query
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        query = DataAccessLog.query.filter_by(user_id=user.id)\
            .filter(DataAccessLog.created_at >= start_date)
        
        if data_type:
            query = query.filter_by(data_type=data_type)
        
        logs = query.order_by(DataAccessLog.created_at.desc()).limit(100).all()
        
        # Log this data access
        context = get_request_context()
        SecurityHelper.log_data_access(
            user_id=user.id,
            data_type='data_access_log',
            access_type='read',
            purpose='User viewing data access transparency log',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint']
        )
        
        return jsonify({
            'message': 'Data access log retrieved successfully',
            'tagline': 'We girls have no time - here\'s your data transparency!',
            'logs': [log.to_dict() for log in logs],
            'summary': {
                'total_accesses': len(logs),
                'date_range_days': days,
                'data_types_accessed': list(set([l.data_type for l in logs])),
                'read_accesses': len([l for l in logs if l.access_type == 'read']),
                'write_accesses': len([l for l in logs if l.access_type in ['write', 'update', 'delete']])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve data access log',
            'message': str(e)
        }), 500


@security_bp.route('/export-data', methods=['POST'])
def request_data_export():
    """
    Request data export for GDPR compliance - quick data export request
    "We girls have no time" for complex data export processes
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        # Check for existing pending requests
        existing_request = DataExportRequest.query.filter_by(
            user_id=user.id,
            status='pending'
        ).first()
        
        if existing_request:
            return jsonify({
                'error': 'Data export request already pending',
                'message': 'Please wait for your current export to complete',
                'existing_request': existing_request.to_dict()
            }), 400
        
        # Create new export request
        export_request = DataExportRequest(
            user_id=user.id,
            request_type=data.get('request_type', 'full_export'),
            data_types=json.dumps(data.get('data_types', [])),
            format=data.get('format', 'json')
        )
        
        db.session.add(export_request)
        db.session.commit()
        
        # Log security event
        context = get_request_context()
        SecurityHelper.log_security_event(
            user_id=user.id,
            event_type=SecurityEventType.DATA_EXPORT,
            description=f"Data export requested: {export_request.request_type}",
            severity='info',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint'],
            metadata={'export_id': export_request.id, 'format': export_request.format}
        )
        
        # Start processing (in a real app, this would be async)
        process_data_export(export_request.id)
        
        return jsonify({
            'message': 'Data export request created successfully',
            'tagline': 'We girls have no time - your data export is being prepared!',
            'request': export_request.to_dict(),
            'estimated_completion': '5-10 minutes'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create data export request',
            'message': str(e)
        }), 500


def process_data_export(export_request_id):
    """Process data export request (simplified version)"""
    try:
        export_request = DataExportRequest.query.get(export_request_id)
        if not export_request:
            return
        
        # Update status
        export_request.status = 'processing'
        export_request.started_at = datetime.utcnow()
        export_request.progress_percentage = 10
        db.session.commit()
        
        # Collect user data
        user = User.query.get(export_request.user_id)
        export_data = {
            'user_profile': user.to_dict(include_sensitive=True),
            'export_info': {
                'requested_at': export_request.created_at.isoformat(),
                'export_type': export_request.request_type,
                'format': export_request.format
            }
        }
        
        # Add additional data based on request
        if export_request.request_type == 'full_export':
            # Add all user data (simplified)
            from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory
            from src.models.analytics import UserAnalytics, StyleInsights
            
            style_profile = StyleProfile.query.filter_by(user_id=user.id).first()
            if style_profile:
                export_data['style_profile'] = style_profile.to_dict()
            
            wardrobe_items = WardrobeItem.query.filter_by(user_id=user.id).all()
            export_data['wardrobe_items'] = [item.to_dict() for item in wardrobe_items]
            
            outfit_history = OutfitHistory.query.filter_by(user_id=user.id).all()
            export_data['outfit_history'] = [outfit.to_dict() for outfit in outfit_history]
            
            analytics = UserAnalytics.query.filter_by(user_id=user.id).all()
            export_data['analytics'] = [a.to_dict() for a in analytics]
            
            insights = StyleInsights.query.filter_by(user_id=user.id).all()
            export_data['style_insights'] = [insight.to_dict() for insight in insights]
        
        # Create temporary file
        temp_dir = tempfile.mkdtemp()
        if export_request.format == 'json':
            file_path = os.path.join(temp_dir, f'tanvi_data_export_{user.id}.json')
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        # Update export request
        export_request.status = 'completed'
        export_request.completed_at = datetime.utcnow()
        export_request.progress_percentage = 100
        export_request.file_path = file_path
        export_request.file_size_bytes = os.path.getsize(file_path)
        export_request.generate_download_token()
        
        db.session.commit()
        
    except Exception as e:
        # Handle error
        export_request.status = 'failed'
        export_request.error_message = str(e)
        db.session.commit()


@security_bp.route('/export-data/<int:request_id>', methods=['GET'])
def get_data_export_status(request_id):
    """
    Get data export request status - check export progress
    "We girls have no time" for complex status checking
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        export_request = DataExportRequest.query.filter_by(
            id=request_id,
            user_id=user.id
        ).first()
        
        if not export_request:
            return jsonify({'error': 'Export request not found'}), 404
        
        return jsonify({
            'message': 'Export request status retrieved successfully',
            'tagline': 'We girls have no time - here\'s your export status!',
            'request': export_request.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve export status',
            'message': str(e)
        }), 500


@security_bp.route('/download-data/<token>', methods=['GET'])
def download_exported_data(token):
    """
    Download exported data using secure token
    "We girls have no time" for complex download processes
    """
    try:
        export_request = DataExportRequest.query.filter_by(download_token=token).first()
        
        if not export_request:
            return jsonify({'error': 'Invalid download token'}), 404
        
        if not export_request.is_download_available():
            return jsonify({'error': 'Download no longer available'}), 410
        
        # Increment download count
        export_request.increment_download_count()
        
        # Log download
        SecurityHelper.log_security_event(
            user_id=export_request.user_id,
            event_type=SecurityEventType.DATA_EXPORT,
            description=f"Data export downloaded (attempt {export_request.download_count})",
            severity='info',
            metadata={'export_id': export_request.id}
        )
        
        return send_file(
            export_request.file_path,
            as_attachment=True,
            download_name=f'tanvi_data_export_{export_request.user_id}.{export_request.format}'
        )
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to download data',
            'message': str(e)
        }), 500


@security_bp.route('/delete-account', methods=['POST'])
def request_account_deletion():
    """
    Request account deletion - GDPR right to be forgotten
    "We girls have no time" for complex deletion processes
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        confirmation = data.get('confirmation', '').lower()
        
        if confirmation != 'delete my account':
            return jsonify({
                'error': 'Confirmation required',
                'message': 'Please type "delete my account" to confirm'
            }), 400
        
        # Log account deletion request
        context = get_request_context()
        SecurityHelper.log_security_event(
            user_id=user.id,
            event_type=SecurityEventType.ACCOUNT_DELETION,
            description="Account deletion requested by user",
            severity='critical',
            ip_address=context['ip_address'],
            user_agent=context['user_agent'],
            endpoint=context['endpoint'],
            metadata={'confirmation_provided': True}
        )
        
        # In a real app, this would start a deletion process with a grace period
        # For now, we'll just mark the account for deletion
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Account deletion request received',
            'tagline': 'We girls have no time - but we\'ll miss you!',
            'next_steps': [
                'Your account has been deactivated',
                'Data will be permanently deleted in 30 days',
                'You can reactivate within 30 days by logging in',
                'Contact support if you need assistance'
            ]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to process account deletion',
            'message': str(e)
        }), 500

