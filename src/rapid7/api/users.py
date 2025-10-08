"""
User API Module for Rapid7 InsightVM

This module provides comprehensive user account management and access control operations
for the InsightVM platform.

Examples:
    Basic usage::

        from rapid7 import InsightVMClient

        # Initialize client
        client = InsightVMClient()

        # List all users
        users = client.users.list()

        # Get specific user
        user = client.users.get_user(user_id=42)

        # Create new user
        new_user = client.users.create(
            login="john.doe",
            name="John Doe",
            email="john.doe@example.com",
            password="SecurePassword123!",
            role_id="global-admin"
        )

        # Grant site access
        client.users.grant_site_access(user_id=42, site_id=10)

Author: InsightVM-Python Development Team
Version: 2.0.0
"""

from typing import Dict, List, Optional, Any, Tuple
from .base import BaseAPI


class UserAPI(BaseAPI):
    """
    User API client for managing user accounts and access control in InsightVM.
    
    This class provides methods for:
    - User CRUD operations (list, get, create, update, delete)
    - Site access management (grant, revoke, bulk operations)
    - Asset group access management (grant, revoke, bulk operations)
    - User privilege management
    - Password operations
    - Account locking/unlocking
    - Two-factor authentication management
    
    All methods require appropriate permissions, typically Global Administrator.
    """

    def __init__(self, auth, verify_ssl: Optional[bool] = None,
                 timeout: Tuple[int, int] = (10, 90)):
        """
        Initialize the User API client.
        
        Args:
            auth: Authentication object (InsightVMAuth)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout as (connect_timeout, read_timeout)
        """
        super().__init__(auth, verify_ssl, timeout)

    # ============================================================================
    # Core CRUD Operations
    # ============================================================================

    def list(self, page: int = 0, size: int = 10,
             sort: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retrieve a paginated list of all users.
        
        Requires Global Administrator privilege.
        
        Args:
            page: Page number (zero-based)
            size: Number of records per page (max 500)
            sort: Sort criteria in format ['property,ASC|DESC']
        
        Returns:
            Dictionary containing resources, page info, and links
        
        Example:
            >>> users = client.users.list(page=0, size=50)
            >>> for user in users['resources']:
            ...     print(f"{user['login']} - {user['name']}")
        """
        params: Dict[str, Any] = {
            'page': page,
            'size': min(size, 500),
        }
        if sort:
            params['sort'] = sort
        
        return self._request('GET', 'users', params=params)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve details for a specific user.
        
        Accessible by Global Admin or the current user (own details).
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            User object with id, login, name, email, enabled, locked,
            role, authentication, and locale information
        
        Example:
            >>> user = client.users.get_user(user_id=42)
            >>> print(f"User: {user['name']} ({user['login']})")
            >>> print(f"Role: {user['role']['name']}")
        """
        return self._request('GET', f'users/{user_id}')

    def create(self, 
               login: str,
               name: str,
               role_id: str,
               password: Optional[str] = None,
               email: Optional[str] = None,
               enabled: bool = True,
               authentication_id: Optional[int] = None,
               authentication_type: str = "normal",
               locale_default: Optional[str] = None,
               locale_reports: Optional[str] = None,
               password_reset_on_login: bool = False,
               **kwargs) -> Dict[str, Any]:
        """
        Create a new user account.
        
        Requires Global Administrator privilege.
        
        Args:
            login: Username for the account
            name: Full name of the user
            role_id: Role ID (e.g., 'global-admin', 'user')
            password: Initial password (required for normal auth)
            email: Email address
            enabled: Whether the account is enabled
            authentication_id: Authentication source ID (external auth)
            authentication_type: Type ('normal', 'kerberos', 'ldap',
                'saml')
            locale_default: Default locale (e.g., 'en-US')
            locale_reports: Report locale
            password_reset_on_login: Force password change on login
            **kwargs: Additional user properties
        
        Returns:
            Dictionary with links to the created user
        
        Example:
            >>> # Create local user
            >>> new_user = client.users.create(
            ...     login="john.doe",
            ...     name="John Doe",
            ...     email="john.doe@example.com",
            ...     password="SecurePassword123!",
            ...     role_id="user"
            ... )
            
            >>> # Create LDAP user
            >>> ldap_user = client.users.create(
            ...     login="jane.smith",
            ...     name="Jane Smith",
            ...     email="jane.smith@example.com",
            ...     role_id="security-manager",
            ...     authentication_type="ldap",
            ...     authentication_id=1
            ... )
        """
        data: Dict[str, Any] = {
            'login': login,
            'name': name,
            'enabled': enabled,
            'authentication': {
                'type': authentication_type
            },
            'role': {
                'id': role_id
            },
            'passwordResetOnLogin': password_reset_on_login
        }
        
        if password:
            data['password'] = password
        if email:
            data['email'] = email
        if authentication_id:
            data['authentication']['id'] = authentication_id
        if locale_default or locale_reports:
            data['locale'] = {}
            if locale_default:
                data['locale']['default'] = locale_default
            if locale_reports:
                data['locale']['reports'] = locale_reports
        
        # Add any additional properties
        data.update(kwargs)
        
        return self._request('POST', 'users', json=data)

    def update(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update an existing user account.
        
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
            **kwargs: User properties to update (login, name, email,
                enabled, role, etc.)
        
        Returns:
            Dictionary with links to the updated user
        
        Example:
            >>> # Update user email and name
            >>> client.users.update(
            ...     user_id=42,
            ...     email="new.email@example.com",
            ...     name="John M. Doe"
            ... )
            
            >>> # Change user role
            >>> client.users.update(
            ...     user_id=42,
            ...     role={'id': 'security-manager'}
            ... )
            
            >>> # Disable user account
            >>> client.users.update(user_id=42, enabled=False)
        """
        return self._request('PUT', f'users/{user_id}', json=kwargs)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Delete a user account.
        
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user to delete
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.delete_user(user_id=42)
        """
        return self._request('DELETE', f'users/{user_id}')

    # ============================================================================
    # Site Access Management
    # ============================================================================

    def get_sites(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve the sites to which a user has access.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary containing site IDs and links
        
        Example:
            >>> sites = client.users.get_sites(user_id=42)
            >>> print(f"User has access to {len(sites['resources'])} sites")
        """
        return self._request('GET', f'users/{user_id}/sites')

    def set_sites(self, user_id: int,
                  site_ids: List[int]) -> Dict[str, Any]:
        """
        Update the sites to which a user has access (bulk operation).
        
        Individual site access cannot be granted to users with the
        allSites permission. Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
            site_ids: List of site identifiers to grant access to
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> # Grant access to specific sites
            >>> client.users.set_sites(
            ...     user_id=42, site_ids=[10, 20, 30])
            
            >>> # Remove all site access (empty list)
            >>> client.users.set_sites(user_id=42, site_ids=[])
        """
        # API expects JSON array of site IDs
        return self._request(
            'PUT', f'users/{user_id}/sites',
            json={'ids': site_ids})

    def grant_site_access(self, user_id: int,
                          site_id: int) -> Dict[str, Any]:
        """
        Grant a user access to a specific site.
        
        Individual site access cannot be granted to users with the
        allSites permission. Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
            site_id: The identifier of the site
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.grant_site_access(
            ...     user_id=42, site_id=10)
        """
        return self._request('PUT', f'users/{user_id}/sites/{site_id}')

    def revoke_site_access(self, user_id: int,
                           site_id: int) -> Dict[str, Any]:
        """
        Revoke a user's access to a specific site.
        
        Individual site access cannot be revoked from users with the
        allSites permission. Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
            site_id: The identifier of the site
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.revoke_site_access(
            ...     user_id=42, site_id=10)
        """
        return self._request('DELETE', f'users/{user_id}/sites/{site_id}')

    def revoke_all_site_access(self, user_id: int) -> Dict[str, Any]:
        """
        Revoke a user's access to all sites.
        
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.revoke_all_site_access(user_id=42)
        """
        return self._request('DELETE', f'users/{user_id}/sites')

    # ============================================================================
    # Asset Group Access Management
    # ============================================================================

    def get_asset_groups(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve the asset groups to which a user has access.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary containing asset group IDs and links
        
        Example:
            >>> groups = client.users.get_asset_groups(user_id=42)
            >>> count = len(groups['resources'])
            >>> print(f"User has access to {count} asset groups")
        """
        return self._request('GET', f'users/{user_id}/asset_groups')

    def set_asset_groups(self, user_id: int,
                         asset_group_ids: List[int]) -> Dict[str, Any]:
        """
        Update the asset groups to which a user has access (bulk op).
        
        Individual asset group access cannot be granted to users with
        allAssetGroups permission. Requires Global Admin privilege.
        
        Args:
            user_id: The identifier of the user
            asset_group_ids: List of asset group IDs to grant access
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> # Grant access to specific asset groups
            >>> client.users.set_asset_groups(
            ...     user_id=42, asset_group_ids=[5, 10, 15])
            
            >>> # Remove all asset group access (empty list)
            >>> client.users.set_asset_groups(
            ...     user_id=42, asset_group_ids=[])
        """
        # API expects JSON array of asset group IDs
        return self._request(
            'PUT', f'users/{user_id}/asset_groups',
            json={'ids': asset_group_ids})

    def grant_asset_group_access(self, user_id: int,
                                  asset_group_id: int) -> Dict[str, Any]:
        """
        Grant a user access to a specific asset group.
        
        Individual asset group access cannot be granted to users with
        allAssetGroups permission. Requires Global Admin privilege.
        
        Args:
            user_id: The identifier of the user
            asset_group_id: The identifier of the asset group
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.grant_asset_group_access(
            ...     user_id=42, asset_group_id=5)
        """
        return self._request(
            'PUT', f'users/{user_id}/asset_groups/{asset_group_id}')

    def revoke_asset_group_access(self, user_id: int,
                                   asset_group_id: int) -> Dict[str, Any]:
        """
        Revoke a user's access to a specific asset group.
        
        Individual asset group access cannot be revoked from users
        with allAssetGroups permission. Requires Global Admin.
        
        Args:
            user_id: The identifier of the user
            asset_group_id: The identifier of the asset group
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.revoke_asset_group_access(
            ...     user_id=42, asset_group_id=5)
        """
        endpoint = f'users/{user_id}/asset_groups/{asset_group_id}'
        return self._request('DELETE', endpoint)

    def revoke_all_asset_group_access(self, user_id: int) -> Dict[str, Any]:
        """
        Revoke a user's access to all asset groups.
        
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.revoke_all_asset_group_access(user_id=42)
        """
        return self._request('DELETE', f'users/{user_id}/asset_groups')

    # ============================================================================
    # User Management Operations
    # ============================================================================

    def get_privileges(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve the privileges granted to a user by their role.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary containing list of privilege strings
        
        Example:
            >>> privs = client.users.get_privileges(user_id=42)
            >>> print(f"Privileges: {', '.join(privs['resources'])}")
        """
        return self._request('GET', f'users/{user_id}/privileges')

    def reset_password(self, user_id: int,
                       new_password: str) -> Dict[str, Any]:
        """
        Change the password for a user.
        
        Users may only change their own password.
        
        Args:
            user_id: The identifier of the user
            new_password: The new password to set
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.reset_password(
            ...     user_id=42,
            ...     new_password="NewSecurePassword123!")
        """
        data: Dict[str, str] = {'password': new_password}
        return self._request('PUT', f'users/{user_id}/password', json=data)

    def unlock_user(self, user_id: int) -> Dict[str, Any]:
        """
        Unlock a locked user account.
        
        Accounts are locked after too many failed auth attempts.
        Disabled accounts cannot be unlocked.
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.unlock_user(user_id=42)
        """
        return self._request('DELETE', f'users/{user_id}/lock')

    def get_2fa_key(self, user_id: int) -> Dict[str, Any]:
        """
        Retrieve the 2FA token seed (key) for a user.
        
        Returns the key only if 2FA is configured for the user.
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary containing:
            - key: The 2FA token seed
            - links: Hypermedia links
        
        Example:
            >>> twofa = client.users.get_2fa_key(user_id=42)
            >>> print(f"2FA Key: {twofa.get('key', 'Not configured')}")
        """
        return self._request('GET', f'users/{user_id}/2FA')

    def remove_2fa(self, user_id: int) -> Dict[str, Any]:
        """
        Remove two-factor authentication for a user.
        
        Requires Global Administrator privilege.
        
        Args:
            user_id: The identifier of the user
        
        Returns:
            Dictionary with confirmation links
        
        Example:
            >>> client.users.remove_2fa(user_id=42)
        """
        return self._request('DELETE', f'users/{user_id}/2FA')

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def get_all(self,
                sort: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all users using automatic pagination.
        
        Convenience method that handles pagination automatically.
        Requires Global Administrator privilege.
        
        Args:
            sort: Sort criteria in format ['property,ASC|DESC']
        
        Returns:
            List of all user objects
        
        Example:
            >>> all_users = client.users.get_all()
            >>> print(f"Total users: {len(all_users)}")
            >>> for user in all_users:
            ...     if user['enabled']:
            ...         print(f"Active: {user['login']}")
        """
        all_users = []
        page = 0
        page_size = 500
        
        while True:
            response = self.list(page=page, size=page_size, sort=sort)
            users = response.get('resources', [])
            
            if not users:
                break
            
            all_users.extend(users)
            
            # Check if we've retrieved all users
            page_info = response.get('page', {})
            if page >= page_info.get('totalPages', 1) - 1:
                break
            
            page += 1
        
        return all_users

    def get_by_login(self, login: str,
                     users: Optional[List[Dict[str, Any]]] = None
                     ) -> Optional[Dict[str, Any]]:
        """
        Find a user by their login username.
        
        Args:
            login: The username to search for
            users: Optional pre-fetched list of users (for caching)
        
        Returns:
            User object if found, None otherwise
        
        Example:
            >>> user = client.users.get_by_login("john.doe")
            >>> if user:
            ...     print(f"Found user: {user['name']}")
            
            >>> # With caching to avoid redundant API calls
            >>> all_users = client.users.get_all()
            >>> user1 = client.users.get_by_login(
            ...     "john.doe", users=all_users)
            >>> user2 = client.users.get_by_login(
            ...     "jane.smith", users=all_users)
        """
        all_users = users if users is not None else self.get_all()
        for user in all_users:
            if user.get('login', '').lower() == login.lower():
                return user
        return None

    def get_enabled_users(self,
                          users: Optional[List[Dict[str, Any]]] = None
                          ) -> List[Dict[str, Any]]:
        """
        Retrieve all enabled user accounts.
        
        Args:
            users: Optional pre-fetched list of users (for caching)
        
        Returns:
            List of enabled user objects
        
        Example:
            >>> enabled = client.users.get_enabled_users()
            >>> print(f"Active users: {len(enabled)}")
            
            >>> # With caching to avoid redundant API calls
            >>> all_users = client.users.get_all()
            >>> enabled = client.users.get_enabled_users(
            ...     users=all_users)
            >>> locked = client.users.get_locked_users(
            ...     users=all_users)
        """
        all_users = users if users is not None else self.get_all()
        return [user for user in all_users if user.get('enabled', False)]

    def get_locked_users(self,
                         users: Optional[List[Dict[str, Any]]] = None
                         ) -> List[Dict[str, Any]]:
        """
        Retrieve all locked user accounts.
        
        Args:
            users: Optional pre-fetched list of users (for caching)
        
        Returns:
            List of locked user objects
        
        Example:
            >>> locked = client.users.get_locked_users()
            >>> for user in locked:
            ...     print(f"Locked: {user['login']}")
            ...     client.users.unlock_user(user['id'])
            
            >>> # With caching to avoid redundant API calls
            >>> all_users = client.users.get_all()
            >>> locked = client.users.get_locked_users(
            ...     users=all_users)
        """
        all_users = users if users is not None else self.get_all()
        return [user for user in all_users if user.get('locked', False)]

    def get_users_by_role(self, role_id: str,
                          users: Optional[List[Dict[str, Any]]] = None
                          ) -> List[Dict[str, Any]]:
        """
        Retrieve all users with a specific role.
        
        Args:
            role_id: Role identifier (e.g., 'global-admin', 'user')
            users: Optional pre-fetched list of users (for caching)
        
        Returns:
            List of user objects with the specified role
        
        Example:
            >>> admins = client.users.get_users_by_role(
            ...     'global-admin')
            >>> print(f"Administrators: {len(admins)}")
            >>> for admin in admins:
            ...     print(f"- {admin['name']} ({admin['login']})")
            
            >>> # With caching to avoid redundant API calls
            >>> all_users = client.users.get_all()
            >>> admins = client.users.get_users_by_role(
            ...     'global-admin', users=all_users)
            >>> regular = client.users.get_users_by_role(
            ...     'user', users=all_users)
        """
        all_users = users if users is not None else self.get_all()
        return [
            user for user in all_users
            if user.get('role', {}).get('id', '') == role_id
        ]

    def create_admin(self, 
                     login: str,
                     name: str,
                     password: str,
                     email: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new global administrator user.
        
        Convenience method for creating admin users.
        Requires Global Administrator privilege.
        
        Args:
            login: Username for the account
            name: Full name of the user
            password: Initial password
            email: Email address
        
        Returns:
            Dictionary with links to the created user
        
        Example:
            >>> admin = client.users.create_admin(
            ...     login="admin.user",
            ...     name="Admin User",
            ...     password="SecureAdminPass123!",
            ...     email="admin@example.com"
            ... )
        """
        return self.create(
            login=login,
            name=name,
            password=password,
            email=email,
            role_id='global-admin',
            enabled=True
        )
