from datetime import datetime
from flask import request
from functools import wraps
from metasrht.types import OAuthClient, OAuthToken, DelegatedScope
from srht.config import cfgkeys, cfg
from srht.database import db
from srht.oauth import OAuthScope, AbstractOAuthProvider, AbstractOAuthService
from urllib.parse import quote_plus
import hashlib

meta_scopes = {
    'profile': 'profile information',
    'audit': 'audit log',
    'keys': 'SSH and PGP keys',
}

meta_access = {
    'profile': 'read',
    'audit': 'read',
    'keys': 'read',
}

meta_aliases = { "meta.sr.ht": None }
for key in cfgkeys("meta.sr.ht::aliases"):
    meta_aliases[key] = cfg("meta.sr.ht::aliases", key)

class MetaOAuthProvider(AbstractOAuthProvider):
    def get_alias(self, client_id):
        return meta_aliases.get(client_id)

    def resolve_scope(self, scope):
        if scope.client_id:
            client = (OAuthClient.query
                .filter(OAuthClient.client_id == scope.client_id)).one_or_none()
            if not client:
                raise Exception('Unknown client ID {}'.format(scope.client_id))
            scope.client = client
        else:
            scope.client = None

        if not scope.client:
            _scope = scope.scope
            if not _scope in meta_scopes:
                raise Exception('Invalid scope {}'.format(_scope))
            if meta_access[_scope] == 'read' and scope.access == 'write':
                raise Exception(
                        'Write access not permitted for {}'.format(_scope))
            return meta_scopes[scope.scope]
        else:
            _scope = (DelegatedScope.query
                .filter(DelegatedScope.client_id == scope.client.id)
                .filter(DelegatedScope.name == scope.scope)).one_or_none()
            if not _scope:
                raise Exception('Invalid scope {}'.format(scope.scope))
            if not _scope.write and scope.access == 'write':
                raise Exception('Write access not permitted for {}'.format(
                    scope.scope))
            return _scope.description

class MetaOAuthService(AbstractOAuthService):
    def __init__(self):
        super().__init__(None, None)

    def get_token(self, token, token_hash, scopes):
        now = datetime.utcnow()
        oauth_token = (OAuthToken.query
            .filter(OAuthToken.token_hash == token_hash)
            .filter(OAuthToken.expires > now)
        ).first()
        if oauth_token:
            oauth_token.updated = now
            db.session.commit()
        return oauth_token

    def oauth_url(self, return_to, scopes=[]):
        return "/login?return_to={}".format(quote_plus(return_to))
