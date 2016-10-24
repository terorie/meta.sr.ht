from flask import request
from flask_login import current_user
from ipaddress import ip_address
from datetime import datetime, timedelta
from meta.types import AuditLogEntry
from meta.db import db

def audit_log(event_type, details=None):
    if not current_user:
        return
    event = AuditLogEntry(current_user.id,
        event_type, ip_address(request.remote_addr),
        details)
    db.add(event)

def expire_audit_logs():
    cutoff = datetime.now() - timedelta(days=14)
    AuditLogEntry.query.filter(AuditLogEntry.created <= cutoff) \
        .delete()
    db.commit()
