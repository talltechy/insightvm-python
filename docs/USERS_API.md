# Users API Documentation

## Overview

The Users API module provides comprehensive user account management and access control operations for InsightVM. This includes user CRUD operations, role assignment, site/asset group access control, password management, account locking/unlocking, and two-factor authentication management.

**Key Features:**
- User CRUD operations (create, read, update, delete)
- Site access management (grant, revoke, bulk operations)
- Asset group access management (grant, revoke, bulk operations)
- Role-based access control
- Password reset and management
- Account locking/unlocking
- Two-factor authentication (2FA) management
- Search and filter by login, role, status

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# List all users
users = client.users.list()

# Get specific user
user = client.users.get_user(user_id=42)
print(f"User: {user['name']} ({user['login']})")
print(f"Role: {user['role']['name']}")

# Create new user
new_user = client.users.create(
    login="john.doe",
    name="John Doe",
    email="john.doe@example.com",
    password="SecurePassword123!",
    role_id="user"
)

# Grant site access
client.users.grant_site_access(user_id=42, site_id=10)

# Update user
client.users.update(
    user_id=42,
    email="newemail@example.com",
    enabled=True
)
```

## Core Operations

### List Users

Retrieve paginated list of all users:

```python
# Basic listing
users = client.users.list(page=0, size=50)

# Sort by login name
sorted_users = client.users.list(
    sort=["login,ASC"]
)

# Access pagination info
page_info = users['page']
print(f"Page {page_info['number']} of {page_info['totalPages']}")
print(f"Total users: {page_info['totalResources']}")

# Iterate through users
for user in users['resources']:
    print(f"{user['login']} - {user['name']}")
    print(f"  Role: {user['role']['name']}")
    print(f"  Enabled: {user['enabled']}")
    print(f"  Locked: {user['locked']}")
```

### Get User Details

Retrieve comprehensive information for a specific user:

```python
user = client.users.get_user(user_id=42)

# Access basic info
print(f"ID: {user['id']}")
print(f"Login: {user['login']}")
print(f"Name: {user['name']}")
print(f"Email: {user['email']}")

# Account status
print(f"Enabled: {user['enabled']}")
print(f"Locked: {user['locked']}")

# Role information
role = user['role']
print(f"Role ID: {role['id']}")
print(f"Role Name: {role['name']}")
print(f"All Sites Access: {role['allSites']}")
print(f"All Asset Groups Access: {role['allAssetGroups']}")

# Authentication details
auth = user['authentication']
print(f"Auth Type: {auth['type']}")
if 'id' in auth:
    print(f"Auth Source ID: {auth['id']}")

# Locale preferences
if 'locale' in user:
    locale = user['locale']
    print(f"Default Locale: {locale.get('default', 'Not set')}")
    print(f"Reports Locale: {locale.get('reports', 'Not set')}")
```

### Create User

Create new user accounts with various authentication types:

```python
# Create local user
local_user = client.users.create(
    login="john.doe",
    name="John Doe",
    email="john.doe@example.com",
    password="SecurePassword123!",
    role_id="user",
    enabled=True
)

# Create LDAP user
ldap_user = client.users.create(
    login="jane.smith",
    name="Jane Smith",
    email="jane.smith@example.com",
    role_id="security-manager",
    authentication_type="ldap",
    authentication_id=1
)

# Create user with locale preferences
user_with_locale = client.users.create(
    login="bob.jones",
    name="Bob Jones",
    email="bob.jones@example.com",
    password="SecurePassword123!",
    role_id="user",
    locale_default="en-US",
    locale_reports="en-GB"
)

# Create user requiring password reset on first login
temp_user = client.users.create(
    login="temp.user",
    name="Temporary User",
    email="temp@example.com",
    password="TempPassword123!",
    role_id="user",
    password_reset_on_login=True
)

# Create administrator
admin = client.users.create_admin(
    login="admin.user",
    name="Admin User",
    password="AdminPassword123!",
    email="admin@example.com"
)
```

### Update User

Modify existing user accounts:

```python
# Update email and name
client.users.update(
    user_id=42,
    email="newemail@example.com",
    name="John M. Doe"
)

# Change user role
client.users.update(
    user_id=42,
    role={'id': 'security-manager'}
)

# Disable user account
client.users.update(user_id=42, enabled=False)

# Enable user account
client.users.update(user_id=42, enabled=True)

# Update multiple properties
client.users.update(
    user_id=42,
    email="updated@example.com",
    name="Updated Name",
    enabled=True,
    locale={'default': 'fr-FR', 'reports': 'fr-FR'}
)
```

### Delete User

Remove user accounts:

```python
# Delete user
client.users.delete_user(user_id=42)

# Note: Requires Global Administrator privilege
```

## Site Access Management

### Get User's Sites

Retrieve sites a user has access to:

```python
sites = client.users.get_sites(user_id=42)

print(f"User has access to {len(sites['resources'])} sites")
for site_id in sites['resources']:
    # Get site details if needed
    print(f"Site ID: {site_id}")
```

### Set Sites (Bulk Operation)

Replace all site access for a user:

```python
# Grant access to specific sites
client.users.set_sites(
    user_id=42,
    site_ids=[10, 20, 30, 40]
)

# Remove all site access (empty list)
client.users.set_sites(user_id=42, site_ids=[])

# Note: Cannot grant individual site access to users with
# allSites permission (Global Administrators)
```

### Grant Site Access

Grant access to a single site:

```python
# Grant access to site
client.users.grant_site_access(user_id=42, site_id=10)

# Note: Cannot grant to users with allSites permission
```

### Revoke Site Access

Remove access to a specific site:

```python
# Revoke access to site
client.users.revoke_site_access(user_id=42, site_id=10)

# Note: Cannot revoke from users with allSites permission
```

### Revoke All Site Access

Remove access to all sites:

```python
# Remove all site access
client.users.revoke_all_site_access(user_id=42)
```

## Asset Group Access Management

### Get User's Asset Groups

Retrieve asset groups a user has access to:

```python
groups = client.users.get_asset_groups(user_id=42)

print(f"User has access to {len(groups['resources'])} asset groups")
for group_id in groups['resources']:
    print(f"Asset Group ID: {group_id}")
```

### Set Asset Groups (Bulk Operation)

Replace all asset group access for a user:

```python
# Grant access to specific asset groups
client.users.set_asset_groups(
    user_id=42,
    asset_group_ids=[5, 10, 15, 20]
)

# Remove all asset group access
client.users.set_asset_groups(user_id=42, asset_group_ids=[])

# Note: Cannot grant individual access to users with
# allAssetGroups permission
```

### Grant Asset Group Access

Grant access to a single asset group:

```python
# Grant access to asset group
client.users.grant_asset_group_access(user_id=42, asset_group_id=5)
```

### Revoke Asset Group Access

Remove access to a specific asset group:

```python
# Revoke access to asset group
client.users.revoke_asset_group_access(user_id=42, asset_group_id=5)
```

### Revoke All Asset Group Access

Remove access to all asset groups:

```python
# Remove all asset group access
client.users.revoke_all_asset_group_access(user_id=42)
```

## User Management Operations

### Get User Privileges

Retrieve privileges granted by user's role:

```python
privileges = client.users.get_privileges(user_id=42)

print("User privileges:")
for privilege in privileges['resources']:
    print(f"- {privilege}")

# Common privileges include:
# - all-permissions
# - create-reports
# - manage-sites
# - manage-dynamic-asset-groups
# - manage-policies
# - manage-tags
```

### Reset Password

Change a user's password:

```python
# Reset password
client.users.reset_password(
    user_id=42,
    new_password="NewSecurePassword123!"
)

# Note: Users can only change their own password unless
# they are Global Administrators
```

### Unlock User

Unlock a locked user account:

```python
# Unlock user
client.users.unlock_user(user_id=42)

# Accounts are locked after too many failed authentication attempts
# Disabled accounts cannot be unlocked
# Requires Global Administrator privilege
```

### Get 2FA Key

Retrieve two-factor authentication key:

```python
# Get 2FA key
twofa = client.users.get_2fa_key(user_id=42)

if 'key' in twofa:
    print(f"2FA Key: {twofa['key']}")
else:
    print("2FA not configured")

# Requires Global Administrator privilege
```

### Remove 2FA

Remove two-factor authentication for a user:

```python
# Remove 2FA
client.users.remove_2fa(user_id=42)

# Requires Global Administrator privilege
```

## Advanced Features

### Get All Users

Retrieve all users using automatic pagination:

```python
# Get all users
all_users = client.users.get_all()

print(f"Total users: {len(all_users)}")

# Sort by login
all_users_sorted = client.users.get_all(sort=["login,ASC"])

# Process all users
for user in all_users:
    if user['enabled']:
        print(f"Active: {user['login']} - {user['role']['name']}")
```

### Find User by Login

Search for user by username:

```python
# Find user by login
user = client.users.get_by_login("john.doe")

if user:
    print(f"Found: {user['name']}")
    print(f"ID: {user['id']}")
    print(f"Email: {user['email']}")
else:
    print("User not found")
```

### Get Enabled Users

Retrieve only enabled user accounts:

```python
enabled = client.users.get_enabled_users()

print(f"Active users: {len(enabled)}")
for user in enabled:
    print(f"- {user['login']} ({user['name']})")
```

### Get Locked Users

Retrieve all locked user accounts:

```python
locked = client.users.get_locked_users()

print(f"Locked users: {len(locked)}")
for user in locked:
    print(f"Locked: {user['login']}")
    
    # Optionally unlock
    # client.users.unlock_user(user['id'])
```

### Get Users by Role

Filter users by role:

```python
# Get all administrators
admins = client.users.get_users_by_role('global-admin')
print(f"Administrators: {len(admins)}")

# Get security managers
managers = client.users.get_users_by_role('security-manager')
print(f"Security Managers: {len(managers)}")

# Get regular users
regular_users = client.users.get_users_by_role('user')
print(f"Regular Users: {len(regular_users)}")

# Display role breakdown
for admin in admins:
    print(f"Admin: {admin['name']} ({admin['login']})")
```

## Common Use Cases

### 1. User Audit Report

```python
# Generate comprehensive user audit report
all_users = client.users.get_all(sort=["login,ASC"])

print("=" * 80)
print("USER AUDIT REPORT")
print("=" * 80)

# Summary statistics
total = len(all_users)
enabled_count = len([u for u in all_users if u['enabled']])
disabled_count = total - enabled_count
locked_count = len([u for u in all_users if u.get('locked', False)])

print(f"\nSummary:")
print(f"  Total Users: {total}")
print(f"  Enabled: {enabled_count}")
print(f"  Disabled: {disabled_count}")
print(f"  Locked: {locked_count}")

# Role breakdown
role_counts = {}
for user in all_users:
    role = user['role']['name']
    role_counts[role] = role_counts.get(role, 0) + 1

print(f"\nRole Distribution:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Authentication type breakdown
auth_counts = {}
for user in all_users:
    auth_type = user['authentication']['type']
    auth_counts[auth_type] = auth_counts.get(auth_type, 0) + 1

print(f"\nAuthentication Types:")
for auth_type, count in sorted(auth_counts.items()):
    print(f"  {auth_type}: {count}")

# Detailed user list
print(f"\nDetailed User List:")
print("-" * 80)
for user in all_users:
    status = "✓" if user['enabled'] else "✗"
    locked = " [LOCKED]" if user.get('locked', False) else ""
    
    print(f"{status} {user['login']:20} {user['name']:30}")
    print(f"   Role: {user['role']['name']:20} "
          f"Auth: {user['authentication']['type']:10}{locked}")
    
    if user.get('email'):
        print(f"   Email: {user['email']}")
```

### 2. Onboard New User with Complete Setup

```python
def onboard_user(login, name, email, role_id, site_ids, asset_group_ids):
    """Complete user onboarding with access setup."""
    
    print(f"Onboarding user: {name} ({login})")
    
    # Create user
    result = client.users.create(
        login=login,
        name=name,
        email=email,
        password="TempPassword123!",
        role_id=role_id,
        password_reset_on_login=True,
        enabled=True
    )
    
    # Extract user ID from response
    user_link = result['links'][0]['href']
    user_id = int(user_link.split('/')[-1])
    
    print(f"  Created user ID: {user_id}")
    
    # Grant site access
    if site_ids:
        client.users.set_sites(user_id, site_ids)
        print(f"  Granted access to {len(site_ids)} sites")
    
    # Grant asset group access
    if asset_group_ids:
        client.users.set_asset_groups(user_id, asset_group_ids)
        print(f"  Granted access to {len(asset_group_ids)} asset groups")
    
    print(f"  ✓ Onboarding complete")
    
    return user_id

# Onboard new security manager
user_id = onboard_user(
    login="new.manager",
    name="New Security Manager",
    email="manager@example.com",
    role_id="security-manager",
    site_ids=[10, 20, 30],
    asset_group_ids=[5, 10, 15]
)
```

### 3. Access Control Audit

```python
def audit_user_access(user_id):
    """Audit a user's complete access."""
    
    # Get user details
    user = client.users.get_user(user_id)
    
    print("=" * 80)
    print(f"ACCESS AUDIT: {user['name']} ({user['login']})")
    print("=" * 80)
    
    # Basic info
    print(f"\nAccount Status:")
    print(f"  Enabled: {user['enabled']}")
    print(f"  Locked: {user.get('locked', False)}")
    print(f"  Role: {user['role']['name']}")
    
    # Privileges
    privileges = client.users.get_privileges(user_id)
    print(f"\nPrivileges ({len(privileges['resources'])}):")
    for priv in sorted(privileges['resources']):
        print(f"  - {priv}")
    
    # Site access
    role = user['role']
    if role.get('allSites'):
        print(f"\nSite Access: ALL SITES")
    else:
        sites = client.users.get_sites(user_id)
        site_count = len(sites['resources'])
        print(f"\nSite Access ({site_count} sites):")
        for site_id in sites['resources'][:10]:  # First 10
            print(f"  - Site ID: {site_id}")
        if site_count > 10:
            print(f"  ... and {site_count - 10} more")
    
    # Asset group access
    if role.get('allAssetGroups'):
        print(f"\nAsset Group Access: ALL ASSET GROUPS")
    else:
        groups = client.users.get_asset_groups(user_id)
        group_count = len(groups['resources'])
        print(f"\nAsset Group Access ({group_count} groups):")
        for group_id in groups['resources'][:10]:  # First 10
            print(f"  - Asset Group ID: {group_id}")
        if group_count > 10:
            print(f"  ... and {group_count - 10} more")

# Audit specific user
audit_user_access(42)
```

### 4. Bulk User Management

```python
# Disable inactive users
def disable_inactive_users(days_inactive=90):
    """Disable users inactive for specified days."""
    
    from datetime import datetime, timedelta
    
    all_users = client.users.get_all()
    threshold = datetime.now() - timedelta(days=days_inactive)
    
    disabled_count = 0
    
    for user in all_users:
        # Skip if already disabled
        if not user['enabled']:
            continue
        
        # Skip administrators
        if user['role']['id'] == 'global-admin':
            continue
        
        # Check last login (if available in your data)
        # This is example logic - adjust based on your needs
        # For now, disable based on other criteria
        
        print(f"Disabling inactive user: {user['login']}")
        client.users.update(user_id=user['id'], enabled=False)
        disabled_count += 1
    
    print(f"\nDisabled {disabled_count} inactive users")

# Unlock all locked users
def unlock_all_locked_users():
    """Unlock all currently locked user accounts."""
    
    locked = client.users.get_locked_users()
    
    print(f"Found {len(locked)} locked users")
    
    for user in locked:
        print(f"Unlocking: {user['login']}")
        client.users.unlock_user(user['id'])
    
    print(f"✓ Unlocked {len(locked)} users")

# Bulk update email domains
def update_email_domain(old_domain, new_domain):
    """Update email addresses from old domain to new domain."""
    
    all_users = client.users.get_all()
    updated = 0
    
    for user in all_users:
        email = user.get('email', '')
        if email.endswith(f"@{old_domain}"):
            new_email = email.replace(f"@{old_domain}", f"@{new_domain}")
            print(f"Updating {user['login']}: {email} -> {new_email}")
            
            client.users.update(
                user_id=user['id'],
                email=new_email
            )
            updated += 1
    
    print(f"\n✓ Updated {updated} email addresses")

# Example usage
update_email_domain("oldcompany.com", "newcompany.com")
```

### 5. Role Migration

```python
def migrate_users_to_new_role(from_role_id, to_role_id):
    """Migrate all users from one role to another."""
    
    users = client.users.get_users_by_role(from_role_id)
    
    print(f"Migrating {len(users)} users from {from_role_id} to "
          f"{to_role_id}")
    
    migrated = 0
    
    for user in users:
        print(f"  Migrating: {user['login']}")
        
        try:
            client.users.update(
                user_id=user['id'],
                role={'id': to_role_id}
            )
            migrated += 1
        except Exception as e:
            print(f"    Error: {e}")
    
    print(f"\n✓ Successfully migrated {migrated}/{len(users)} users")

# Example: Upgrade security managers to global admins
migrate_users_to_new_role('security-manager', 'global-admin')
```

### 6. User Access Provisioning

```python
def provision_user_access_from_template(user_id, template_user_id):
    """Copy access from template user to new user."""
    
    # Get template user's access
    template_sites = client.users.get_sites(template_user_id)
    template_groups = client.users.get_asset_groups(template_user_id)
    
    # Apply to new user
    if template_sites['resources']:
        client.users.set_sites(
            user_id,
            template_sites['resources']
        )
        print(f"Granted access to {len(template_sites['resources'])} sites")
    
    if template_groups['resources']:
        client.users.set_asset_groups(
            user_id,
            template_groups['resources']
        )
        print(f"Granted access to {len(template_groups['resources'])} "
              f"asset groups")

# Create user and copy access from template
new_user = client.users.create(
    login="new.analyst",
    name="New Security Analyst",
    email="analyst@example.com",
    password="TempPassword123!",
    role_id="user"
)

# Extract user ID
user_id = int(new_user['links'][0]['href'].split('/')[-1])

# Copy access from existing analyst
provision_user_access_from_template(user_id, template_user_id=15)
```

## Best Practices

### 1. Use Strong Passwords

```python
import secrets
import string

def generate_secure_password(length=16):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

# Create user with secure password
secure_password = generate_secure_password()
client.users.create(
    login="secure.user",
    name="Secure User",
    password=secure_password,
    role_id="user",
    password_reset_on_login=True  # Force change on first login
)
```

### 2. Validate Before Operations

```python
def safe_delete_user(login):
    """Safely delete user with validation."""
    
    # Find user
    user = client.users.get_by_login(login)
    
    if not user:
        print(f"User not found: {login}")
        return False
    
    # Check if admin
    if user['role']['id'] == 'global-admin':
        # Count admins
        admins = client.users.get_users_by_role('global-admin')
        if len(admins) <= 1:
            print("Cannot delete last administrator")
            return False
    
    # Confirm deletion
    print(f"Deleting user: {user['name']} ({user['login']})")
    print(f"Role: {user['role']['name']}")
    
    confirmation = input("Type 'DELETE' to confirm: ")
    if confirmation != 'DELETE':
        print("Deletion cancelled")
        return False
    
    # Delete user
    client.users.delete_user(user['id'])
    print("✓ User deleted")
    return True

# Safe deletion
safe_delete_user("old.user")
```

### 3. Batch Operations Efficiently

```python
# Grant site access to multiple users at once
def grant_site_to_users(user_ids, site_id):
    """Grant site access to multiple users."""
    
    success = 0
    failed = 0
    
    for user_id in user_ids:
        try:
            client.users.grant_site_access(user_id, site_id)
            success += 1
        except Exception as e:
            print(f"Failed for user {user_id}: {e}")
            failed += 1
    
    print(f"✓ Granted access to {success} users ({failed} failed)")

# Apply to multiple users
user_ids = [10, 20, 30, 40, 50]
grant_site_to_users(user_ids, site_id=100)
```

### 4. Handle Errors Gracefully

```python
from requests.exceptions import HTTPError

def update_user_safe(user_id, **updates):
    """Safely update user with error handling."""
    
    try:
        result = client.users.update(user_id, **updates)
        return True, "Success"
    except HTTPError as e:
        if e.response.status_code == 404:
            return False, "User not found"
        elif e.response.status_code == 400:
            return False, f"Invalid input: {e.response.text}"
        elif e.response.status_code == 403:
            return False, "Permission denied"
        else:
            return False, f"API error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

# Safe update
success, message = update_user_safe(
    42,
    email="newemail@example.com"
)

if success:
    print("User updated successfully")
else:
    print(f"Update failed: {message}")
```

### 5. Cache User Lookups

```python
# Cache user data to avoid repeated API calls
user_cache = {}

def get_user_cached(user_id):
    """Get user with caching."""
    if user_id not in user_cache:
        user_cache[user_id] = client.users.get_user(user_id)
    return user_cache[user_id]

def get_user_by_login_cached(login):
    """Get user by login with caching."""
    # Check cache first
    for user in user_cache.values():
        if user['login'] == login:
            return user
    
    # Not in cache, fetch
    user = client.users.get_by_login(login)
    if user:
        user_cache[user['id']] = user
    return user

# Use cached lookups
user = get_user_cached(42)
user2 = get_user_by_login_cached("john.doe")
```

## Response Examples

### User Object

```json
{
  "id": 42,
  "login": "john.doe",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "enabled": true,
  "locked": false,
  "authentication": {
    "type": "normal"
  },
  "role": {
    "id": "user",
    "name": "User",
    "allSites": false,
    "allAssetGroups": false,
    "superuser": false,
    "privileges": [
      "view-asset-group-data",
      "view-site-data",
      "create-reports",
      "view-reports"
    ]
  },
  "locale": {
    "default": "en-US",
    "reports": "en-US"
  },
  "links": [
    {
      "href": "https://insightvm.example.com/api/3/users/42",
      "rel": "self"
    }
  ]
}
```

### User List Response

```json
{
  "resources": [
    {
      "id": 1,
      "login": "admin",
      "name": "Administrator"
    },
    {
      "id": 42,
      "login": "john.doe",
      "name": "John Doe"
    }
  ],
  "page": {
    "number": 0,
    "size": 10,
    "totalPages": 5,
    "totalResources": 47
  },
  "links": [
    {
      "href": "https://insightvm.example.com/api/3/users?page=0&size=10",
      "rel": "self"
    },
    {
      "href": "https://insightvm.example.com/api/3/users?page=1&size=10",
      "rel": "next"
    }
  ]
}
```

### Role Object

```json
{
  "id": "global-admin",
  "name": "Global Administrator",
  "allSites": true,
  "allAssetGroups": true,
  "superuser": true,
  "privileges": ["all-permissions"]
}
```

## Authentication Types

| Type | Description | Notes |
|------|-------------|-------|
| `normal` | Local authentication | Requires password parameter |
| `kerberos` | Kerberos authentication | Requires authentication_id |
| `ldap` | LDAP authentication | Requires authentication_id |
| `saml` | SAML authentication | Requires authentication_id |

## Common Role IDs

| Role ID | Role Name | Description |
|---------|-----------|-------------|
| `global-admin` | Global Administrator | Full system access |
| `security-manager` | Security Manager | Manage security operations |
| `site-owner` | Site Owner | Manage assigned sites |
| `user` | User | Basic user access |
| `asset-owner` | Asset Owner | Manage assigned assets |

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/3/users` | List all users |
| GET | `/api/3/users/{id}` | Get user details |
| POST | `/api/3/users` | Create new user |
| PUT | `/api/3/users/{id}` | Update user |
| DELETE | `/api/3/users/{id}` | Delete user |
| GET | `/api/3/users/{id}/sites` | Get user's sites |
| PUT | `/api/3/users/{id}/sites` | Set user's sites (bulk) |
| PUT | `/api/3/users/{id}/sites/{siteId}` | Grant site access |
| DELETE | `/api/3/users/{id}/sites/{siteId}` | Revoke site access |
| DELETE | `/api/3/users/{id}/sites` | Revoke all site access |
| GET | `/api/3/users/{id}/asset_groups` | Get user's asset groups |
| PUT | `/api/3/users/{id}/asset_groups` | Set user's asset groups (bulk) |
| PUT | `/api/3/users/{id}/asset_groups/{groupId}` | Grant asset group access |
| DELETE | `/api/3/users/{id}/asset_groups/{groupId}` | Revoke asset group access |
| DELETE | `/api/3/users/{id}/asset_groups` | Revoke all asset group access |
| GET | `/api/3/users/{id}/privileges` | Get user privileges |
| PUT | `/api/3/users/{id}/password` | Reset password |
| DELETE | `/api/3/users/{id}/lock` | Unlock user |
| GET | `/api/3/users/{id}/2FA` | Get 2FA key |
| DELETE | `/api/3/users/{id}/2FA` | Remove 2FA |

## Error Codes

Common HTTP status codes returned by the Users API:

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request - invalid input |
| 401 | Unauthorized - invalid credentials |
| 403 | Forbidden - insufficient permissions |
| 404 | Not found - user does not exist |
| 500 | Internal server error |

## Permissions Required

Most user management operations require **Global Administrator** privilege. Exceptions:

- **Get own user details**: Current user can retrieve their own information
- **Reset own password**: Users can change their own password
- **Get user privileges**: Users can view their own privileges

## Notes

- User IDs are permanent and do not change
- Login usernames must be unique
- Passwords must meet minimum complexity requirements
- Site and asset group access cannot be granted to users with `allSites` or `allAssetGroups` permissions
- Locked accounts must be unlocked before users can authenticate
- Disabled accounts cannot authenticate even if unlocked
- 2FA keys are only returned if 2FA is configured
- External authentication (LDAP, SAML, Kerberos) requires authentication source configuration

## Related Documentation

- [Authentication API](./AUTHENTICATION_API.md)
- [Roles API](./ROLES_API.md)
- [Sites API](./SITES_API.md)
- [Asset Groups API](./ASSET_GROUPS_API.md)

---

**Last Updated**: 2025-01-07
