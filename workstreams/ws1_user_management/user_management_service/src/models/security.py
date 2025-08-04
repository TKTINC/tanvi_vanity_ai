from datetime import datetime, timedelta
import json
import hashlib
import secrets
from enum import Enum

# Import db from user module to avoid circular imports
from src.models.user import db

class SecurityEventType(Enum):
    """Security event types for audit logging"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    ACCOUNT_LOCKED = "account_locked"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    PRIVACY_SETTING_CHANGE = "privacy_setting_change"
    ACCOUNT_DELETION = "account_deletion"
    TOKEN_REFRESH = "token_refresh"
    UNAUTHORIZED_ACCESS = "unauthorized_access"

class PrivacyLevel(Enum):
    """Privacy levels for user data"""
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"
    ANONYMOUS = "anonymous"

class SecurityAuditLog(db.Model):
    """
    Security audit log for tracking all security events
    "We girls have no time" - Automated security monitoring
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Can be null for system events
    
    # Event details
    event_type = db.Column(db.Enum(SecurityEventType), nullable=False)
    event_description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='info')  # info, warning, critical
    
    # Request context
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    request_method = db.Column(db.String(10), nullable=True)
    
    # Additional context
    event_metadata = db.Column(db.Text, nullable=True)  # JSON with additional details
    
    # Status and resolution
    resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<SecurityAuditLog {self.event_type.value}:{self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type.value,
            'event_description': self.event_description,
            'severity': self.severity,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'endpoint': self.endpoint,
            'request_method': self.request_method,
            'metadata': json.loads(self.event_metadata) if self.event_metadata else {},
            'resolved': self.resolved,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


class UserPrivacySettings(db.Model):
    """
    User privacy settings and preferences
    "We girls have no time" - Simple privacy controls with smart defaults
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # Profile visibility settings
    profile_visibility = db.Column(db.Enum(PrivacyLevel), default=PrivacyLevel.PRIVATE)
    wardrobe_visibility = db.Column(db.Enum(PrivacyLevel), default=PrivacyLevel.PRIVATE)
    outfit_history_visibility = db.Column(db.Enum(PrivacyLevel), default=PrivacyLevel.PRIVATE)
    style_insights_visibility = db.Column(db.Enum(PrivacyLevel), default=PrivacyLevel.PRIVATE)
    
    # Data sharing preferences
    allow_analytics_sharing = db.Column(db.Boolean, default=False)
    allow_style_recommendations = db.Column(db.Boolean, default=True)
    allow_social_features = db.Column(db.Boolean, default=False)
    allow_marketing_communications = db.Column(db.Boolean, default=False)
    
    # Data retention preferences
    auto_delete_old_data = db.Column(db.Boolean, default=False)
    data_retention_months = db.Column(db.Integer, default=24)  # 2 years default
    
    # Third-party integrations
    allow_third_party_integrations = db.Column(db.Boolean, default=False)
    approved_integrations = db.Column(db.Text, nullable=True)  # JSON array of approved services
    
    # Notification preferences
    security_notifications = db.Column(db.Boolean, default=True)
    privacy_update_notifications = db.Column(db.Boolean, default=True)
    data_processing_notifications = db.Column(db.Boolean, default=False)
    
    # GDPR/Privacy compliance
    consent_given_at = db.Column(db.DateTime, default=datetime.utcnow)
    consent_version = db.Column(db.String(10), default='1.0')
    data_processing_consent = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserPrivacySettings {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profile_visibility': self.profile_visibility.value,
            'wardrobe_visibility': self.wardrobe_visibility.value,
            'outfit_history_visibility': self.outfit_history_visibility.value,
            'style_insights_visibility': self.style_insights_visibility.value,
            'allow_analytics_sharing': self.allow_analytics_sharing,
            'allow_style_recommendations': self.allow_style_recommendations,
            'allow_social_features': self.allow_social_features,
            'allow_marketing_communications': self.allow_marketing_communications,
            'auto_delete_old_data': self.auto_delete_old_data,
            'data_retention_months': self.data_retention_months,
            'allow_third_party_integrations': self.allow_third_party_integrations,
            'approved_integrations': json.loads(self.approved_integrations) if self.approved_integrations else [],
            'security_notifications': self.security_notifications,
            'privacy_update_notifications': self.privacy_update_notifications,
            'data_processing_notifications': self.data_processing_notifications,
            'consent_given_at': self.consent_given_at.isoformat(),
            'consent_version': self.consent_version,
            'data_processing_consent': self.data_processing_consent,
            'updated_at': self.updated_at.isoformat()
        }


class DataAccessLog(db.Model):
    """
    Log of all data access for transparency and compliance
    "We girls have no time" - Automated data access tracking
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Access details
    data_type = db.Column(db.String(50), nullable=False)  # profile, wardrobe, analytics, etc.
    access_type = db.Column(db.String(20), nullable=False)  # read, write, update, delete
    data_ids = db.Column(db.Text, nullable=True)  # JSON array of specific record IDs
    
    # Access context
    accessed_by = db.Column(db.String(100), nullable=False)  # user, system, api_client, etc.
    purpose = db.Column(db.String(200), nullable=True)  # Why data was accessed
    
    # Request context
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    
    # Compliance tracking
    legal_basis = db.Column(db.String(100), nullable=True)  # consent, legitimate_interest, etc.
    retention_period = db.Column(db.Integer, nullable=True)  # Days to retain this log
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DataAccessLog {self.user_id}:{self.data_type}:{self.access_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'data_type': self.data_type,
            'access_type': self.access_type,
            'data_ids': json.loads(self.data_ids) if self.data_ids else [],
            'accessed_by': self.accessed_by,
            'purpose': self.purpose,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'endpoint': self.endpoint,
            'legal_basis': self.legal_basis,
            'retention_period': self.retention_period,
            'created_at': self.created_at.isoformat()
        }


class UserSecuritySettings(db.Model):
    """
    User security settings and preferences
    "We girls have no time" - Security made simple with smart defaults
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # Authentication settings
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_method = db.Column(db.String(20), nullable=True)  # sms, email, app
    backup_codes_generated = db.Column(db.Boolean, default=False)
    
    # Session management
    session_timeout_minutes = db.Column(db.Integer, default=60)  # 1 hour default
    max_concurrent_sessions = db.Column(db.Integer, default=3)
    logout_inactive_sessions = db.Column(db.Boolean, default=True)
    
    # Password policy
    password_last_changed = db.Column(db.DateTime, nullable=True)
    password_change_required = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    
    # Security notifications
    notify_new_device_login = db.Column(db.Boolean, default=True)
    notify_password_change = db.Column(db.Boolean, default=True)
    notify_suspicious_activity = db.Column(db.Boolean, default=True)
    notify_data_export = db.Column(db.Boolean, default=True)
    
    # Device tracking
    trusted_devices = db.Column(db.Text, nullable=True)  # JSON array of device fingerprints
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserSecuritySettings {self.user_id}>'

    def is_account_locked(self):
        """Check if account is currently locked"""
        if not self.account_locked_until:
            return False
        return datetime.utcnow() < self.account_locked_until

    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0  # Reset counter after locking
        db.session.commit()

    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        db.session.commit()

    def increment_failed_login(self):
        """Increment failed login attempts and lock if threshold reached"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        db.session.commit()

    def reset_failed_login(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'two_factor_enabled': self.two_factor_enabled,
            'two_factor_method': self.two_factor_method,
            'backup_codes_generated': self.backup_codes_generated,
            'session_timeout_minutes': self.session_timeout_minutes,
            'max_concurrent_sessions': self.max_concurrent_sessions,
            'logout_inactive_sessions': self.logout_inactive_sessions,
            'password_last_changed': self.password_last_changed.isoformat() if self.password_last_changed else None,
            'password_change_required': self.password_change_required,
            'failed_login_attempts': self.failed_login_attempts,
            'account_locked': self.is_account_locked(),
            'account_locked_until': self.account_locked_until.isoformat() if self.account_locked_until else None,
            'notify_new_device_login': self.notify_new_device_login,
            'notify_password_change': self.notify_password_change,
            'notify_suspicious_activity': self.notify_suspicious_activity,
            'notify_data_export': self.notify_data_export,
            'trusted_devices': json.loads(self.trusted_devices) if self.trusted_devices else [],
            'updated_at': self.updated_at.isoformat()
        }


class DataExportRequest(db.Model):
    """
    User data export requests for GDPR compliance
    "We girls have no time" - Quick data export with comprehensive coverage
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Request details
    request_type = db.Column(db.String(20), default='full_export')  # full_export, partial_export
    data_types = db.Column(db.Text, nullable=True)  # JSON array of specific data types
    format = db.Column(db.String(10), default='json')  # json, csv, pdf
    
    # Processing status
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    progress_percentage = db.Column(db.Integer, default=0)
    
    # File details
    file_path = db.Column(db.String(500), nullable=True)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    download_token = db.Column(db.String(255), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)  # When download link expires
    
    # Processing details
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Security
    download_count = db.Column(db.Integer, default=0)
    max_downloads = db.Column(db.Integer, default=3)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DataExportRequest {self.user_id}:{self.status}>'

    def generate_download_token(self):
        """Generate secure download token"""
        self.download_token = secrets.token_urlsafe(32)
        self.expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days to download
        db.session.commit()
        return self.download_token

    def is_download_available(self):
        """Check if download is available"""
        if self.status != 'completed':
            return False
        if not self.expires_at or datetime.utcnow() > self.expires_at:
            return False
        if self.download_count >= self.max_downloads:
            return False
        return True

    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'request_type': self.request_type,
            'data_types': json.loads(self.data_types) if self.data_types else [],
            'format': self.format,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'file_size_bytes': self.file_size_bytes,
            'download_available': self.is_download_available(),
            'download_count': self.download_count,
            'max_downloads': self.max_downloads,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat()
        }


class SecurityHelper:
    """
    Helper class for security operations
    "We girls have no time" - Automated security management
    """
    
    @staticmethod
    def log_security_event(user_id, event_type, description, severity='info', ip_address=None, user_agent=None, endpoint=None, metadata=None):
        """Log a security event"""
        log_entry = SecurityAuditLog(
            user_id=user_id,
            event_type=event_type,
            event_description=description,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            event_metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    
    @staticmethod
    def log_data_access(user_id, data_type, access_type, accessed_by='user', purpose=None, data_ids=None, ip_address=None, user_agent=None, endpoint=None):
        """Log data access for transparency"""
        access_log = DataAccessLog(
            user_id=user_id,
            data_type=data_type,
            access_type=access_type,
            accessed_by=accessed_by,
            purpose=purpose,
            data_ids=json.dumps(data_ids) if data_ids else None,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint=endpoint,
            legal_basis='consent',  # Default to consent
            retention_period=365  # Keep logs for 1 year
        )
        db.session.add(access_log)
        db.session.commit()
        return access_log
    
    @staticmethod
    def get_or_create_privacy_settings(user_id):
        """Get or create privacy settings for user"""
        settings = UserPrivacySettings.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserPrivacySettings(user_id=user_id)
            db.session.add(settings)
            db.session.commit()
        return settings
    
    @staticmethod
    def get_or_create_security_settings(user_id):
        """Get or create security settings for user"""
        settings = UserSecuritySettings.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserSecuritySettings(user_id=user_id)
            db.session.add(settings)
            db.session.commit()
        return settings
    
    @staticmethod
    def generate_device_fingerprint(user_agent, ip_address):
        """Generate device fingerprint for tracking"""
        fingerprint_data = f"{user_agent}:{ip_address}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    @staticmethod
    def check_suspicious_activity(user_id, ip_address, user_agent):
        """Check for suspicious activity patterns"""
        # Check for multiple failed logins from different IPs
        recent_failures = SecurityAuditLog.query.filter_by(
            user_id=user_id,
            event_type=SecurityEventType.LOGIN_FAILED
        ).filter(
            SecurityAuditLog.created_at >= datetime.utcnow() - timedelta(hours=1)
        ).count()
        
        if recent_failures >= 3:
            SecurityHelper.log_security_event(
                user_id=user_id,
                event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
                description=f"Multiple failed login attempts: {recent_failures} in last hour",
                severity='warning',
                ip_address=ip_address,
                user_agent=user_agent,
                metadata={'failed_attempts': recent_failures}
            )
            return True
        
        return False

