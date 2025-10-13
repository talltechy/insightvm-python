# Palo Alto Cortex XDR Integration

## Status: Moved to Separate Development Branch

As of version 2.1, the Palo Alto Cortex XDR integration has been moved to a dedicated development branch to keep the main repository focused on Rapid7 InsightVM functionality.

## Accessing the Palo Alto XDR Code

### Option 1: Check Out from Git History

The Palo Alto XDR code is available in the git history. You can access it by checking out a commit before the removal:

```bash
# View the last commit that included Palo Alto code
git log --all --full-history -- src/paloalto/

# Check out the specific commit (replace with actual commit hash)
git checkout 559a63e -- src/paloalto/
```

### Option 2: Browse on GitHub

You can view the Palo Alto XDR code in the GitHub repository history:

1. Go to the repository: https://github.com/talltechy/insightvm-python
2. Navigate to `src/paloalto/` in any commit before this change
3. View commit `559a63e` or earlier

### Files Included

The Palo Alto Cortex XDR integration consisted of:

- `src/paloalto/__init__.py` - Package initialization
- `src/paloalto/api_pa_xdr.py` - Main API client with functions for:
  - Incident management
  - Endpoint management
  - Alert management
  - Endpoint isolation/quarantine operations
- `src/paloalto/api_pa_xdr_auth.py` - Authentication helper functions

### Environment Variables Required

If you restore the Palo Alto XDR code, you'll need these environment variables:

```bash
XDR_API_KEY=your_xdr_api_key
XDR_API_KEY_ID=your_xdr_api_key_id
XDR_BASE_URL=https://api-your-region.xdr.us.paloaltonetworks.com
```

## Why Was This Moved?

The Palo Alto Cortex XDR integration was moved to a separate development branch for the following reasons:

1. **Focus**: Keep the main repository focused on Rapid7 InsightVM
2. **Maintainability**: Separate development cycles for different products
3. **Clarity**: Clear separation of concerns between different API integrations
4. **Independence**: Allow each integration to evolve independently

## Future Plans

The Palo Alto Cortex XDR integration may be:
- Developed as a separate package (`paloalto-cortex-xdr-python`)
- Maintained on a long-lived feature branch
- Released as a separate project

## Questions?

For questions about the Palo Alto XDR integration, please:
1. Check the git history for implementation details
2. Open an issue in the repository for discussion
3. Contact the maintainers if you're interested in continuing XDR development

## References

- [Palo Alto Cortex XDR API Documentation](https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-API-Reference/APIs-Overview)
