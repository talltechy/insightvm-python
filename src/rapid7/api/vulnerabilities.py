"""
Rapid7 InsightVM Vulnerabilities API Module

This module provides a comprehensive interface for managing vulnerabilities in InsightVM.
It supports listing, retrieving detailed vulnerability information, finding affected assets,
retrieving exploits and malware kits, and accessing external references like CVEs.

Example:
    ```python
    from rapid7 import InsightVMClient
    
    # Create client
    client = InsightVMClient()
    
    # List all critical vulnerabilities
    critical = client.vulnerabilities.get_by_severity('Critical')
    
    # Get vulnerability details
    vuln = client.vulnerabilities.get_vulnerability('ssh-openssh-cve-2023-1234')
    print(f"Title: {vuln['title']}")
    print(f"CVSS: {vuln['cvss']['v3']['score']}")
    
    # Get affected assets
    assets = client.vulnerabilities.get_affected_assets('ssh-openssh-cve-2023-1234')
    print(f"Affected assets: {len(assets['resources'])}")
    
    # Get available exploits
    exploits = client.vulnerabilities.get_exploits('ssh-openssh-cve-2023-1234')
    ```
"""

from typing import Dict, List, Optional, Any
from .base import BaseAPI


class VulnerabilitiesAPI(BaseAPI):
    """
    API client for InsightVM Vulnerabilities operations.
    
    This class provides methods for managing vulnerabilities including:
    - Listing and retrieving vulnerabilities
    - Getting vulnerability details (CVE, CVSS, descriptions)
    - Finding affected assets
    - Retrieving exploits and malware kits
    - Accessing external references and solutions
    - Filtering by severity, risk score, and other criteria
    
    All methods follow the BaseAPI pattern and handle authentication,
    SSL verification, and error handling automatically.
    """
    
    MAX_PAGE_SIZE = 500
    
    def list(
        self,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        List all vulnerabilities that can be assessed during a scan.
        
        Returns a paginated list of all vulnerabilities in the vulnerability
        database with support for sorting.
        
        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Example: ["riskScore,DESC", "severity,DESC"]
        
        Returns:
            Dictionary containing:
                - resources: List of vulnerability objects with:
                    - id: Vulnerability identifier
                    - title: Vulnerability title
                    - severity: Severity level (Critical, Severe, Moderate)
                    - severityScore: Numeric severity (1-10)
                    - riskScore: Rapid7 risk score
                    - cvss: CVSS v2 and v3 scores
                    - cves: List of CVE identifiers
                    - description: Vulnerability description
                    - published: Publication date
                    - added: Date added to database
                    - modified: Last modification date
                - page: Pagination metadata
                - links: HATEOAS links
        
        Example:
            ```python
            # Get first page of vulnerabilities
            vulns = client.vulnerabilities.list()
            
            # Get vulnerabilities sorted by risk score
            high_risk = client.vulnerabilities.list(
                sort=["riskScore,DESC"]
            )
            
            # Get second page
            page2 = client.vulnerabilities.list(page=1, size=100)
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }
        
        if sort:
            params['sort'] = sort
        
        return self._request('GET', 'vulnerabilities', params=params)
    
    def get_vulnerability(self, vulnerability_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific vulnerability.
        
        Retrieves comprehensive information about a vulnerability including
        CVE identifiers, CVSS scores, descriptions, references, and more.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
                            (e.g., 'ssh-openssh-cve-2023-1234')
        
        Returns:
            Dictionary containing detailed vulnerability information:
                - id: Vulnerability identifier
                - title: Full title
                - severity: Severity level (Critical, Severe, Moderate)
                - severityScore: Numeric severity score (1-10)
                - riskScore: Rapid7 risk score
                - cvss: CVSS v2 and v3 detailed metrics
                    - v2: accessVector, accessComplexity, score, etc.
                    - v3: attackVector, attackComplexity, score, etc.
                - cves: List of CVE identifiers
                - description: HTML and text descriptions
                - published: Publication date
                - added: Date added to database
                - modified: Last modification date
                - categories: List of vulnerability categories
                - pci: PCI compliance information
                - denialOfService: Boolean indicating DoS potential
                - exploits: Number of available exploits
                - malwareKits: Number of associated malware kits
                - links: HATEOAS links
        
        Raises:
            requests.exceptions.HTTPError: If vulnerability not found (404)
        
        Example:
            ```python
            vuln = client.vulnerabilities.get_vulnerability(
                'msft-cve-2017-11804'
            )
            
            print(f"Title: {vuln['title']}")
            print(f"Severity: {vuln['severity']}")
            print(f"CVSS v3: {vuln['cvss']['v3']['score']}")
            print(f"CVEs: {', '.join(vuln['cves'])}")
            print(f"Risk Score: {vuln['riskScore']}")
            ```
        """
        return self._request('GET', f'vulnerabilities/{vulnerability_id}')
    
    def get_affected_assets(
        self,
        vulnerability_id: str
    ) -> Dict[str, Any]:
        """
        Get all assets affected by a specific vulnerability.
        
        Returns a list of asset IDs that are currently vulnerable to the
        specified vulnerability.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
        
        Returns:
            Dictionary containing:
                - resources: List of asset IDs
                - links: HATEOAS links
        
        Example:
            ```python
            # Get affected assets
            result = client.vulnerabilities.get_affected_assets(
                'ssh-openssh-cve-2023-1234'
            )
            
            asset_ids = result['resources']
            print(f"Affected assets: {len(asset_ids)}")
            
            # Get details for each affected asset
            for asset_id in asset_ids:
                asset = client.assets.get_asset(asset_id)
                print(f"- {asset['hostName']}: {asset['ip']}")
            ```
        """
        return self._request(
            'GET',
            f'vulnerabilities/{vulnerability_id}/assets'
        )
    
    def get_exploits(
        self,
        vulnerability_id: str,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get exploits that can be used against a vulnerability.
        
        Returns a paginated list of known exploits that can exploit the
        specified vulnerability.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
        
        Returns:
            Dictionary containing:
                - resources: List of exploit objects with:
                    - id: Exploit identifier
                    - title: Exploit title
                    - source: Exploit source (metasploit, exploit-db, etc.)
                        - name: Source name
                        - key: Source key/identifier
                        - link: URL to exploit
                    - skillLevel: Required skill level (novice, intermediate,
                                 expert)
                    - links: HATEOAS links
                - page: Pagination metadata
                - links: HATEOAS links
        
        Example:
            ```python
            # Get exploits for vulnerability
            exploits = client.vulnerabilities.get_exploits(
                'msft-cve-2017-11804'
            )
            
            for exploit in exploits['resources']:
                print(f"Title: {exploit['title']}")
                print(f"Source: {exploit['source']['name']}")
                print(f"Skill: {exploit['skillLevel']}")
                print(f"URL: {exploit['source']['link']['href']}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }
        
        if sort:
            params['sort'] = sort
        
        return self._request(
            'GET',
            f'vulnerabilities/{vulnerability_id}/exploits',
            params=params
        )
    
    def get_malware_kits(
        self,
        vulnerability_id: str,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get malware kits known to exploit a vulnerability.
        
        Returns a paginated list of malware kits that are known to exploit
        the specified vulnerability.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
        
        Returns:
            Dictionary containing:
                - resources: List of malware kit objects with:
                    - id: Malware kit identifier
                    - name: Malware kit name
                    - popularity: Popularity level (Rare, Occasional,
                                 Favored, Popular)
                    - links: HATEOAS links
                - page: Pagination metadata
                - links: HATEOAS links
        
        Example:
            ```python
            # Get malware kits for vulnerability
            kits = client.vulnerabilities.get_malware_kits(
                'msft-cve-2017-11804'
            )
            
            for kit in kits['resources']:
                print(f"Name: {kit['name']}")
                print(f"Popularity: {kit['popularity']}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }
        
        if sort:
            params['sort'] = sort
        
        return self._request(
            'GET',
            f'vulnerabilities/{vulnerability_id}/malware_kits',
            params=params
        )
    
    def get_references(
        self,
        vulnerability_id: str
    ) -> Dict[str, Any]:
        """
        Get external references for a vulnerability.
        
        Returns external references such as CVE, OSVDB, BID, and vendor
        advisories for the specified vulnerability.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
        
        Returns:
            Dictionary containing:
                - resources: List of reference objects
                - links: HATEOAS links
        
        Example:
            ```python
            refs = client.vulnerabilities.get_references(
                'msft-cve-2017-11804'
            )
            
            for ref in refs['resources']:
                print(f"Source: {ref['source']}")
                print(f"Reference: {ref['reference']}")
            ```
        """
        return self._request(
            'GET',
            f'vulnerabilities/{vulnerability_id}/references'
        )
    
    def get_solutions(
        self,
        vulnerability_id: str
    ) -> Dict[str, Any]:
        """
        Get remediation solutions for a vulnerability.
        
        Returns available remediation solutions that address the specified
        vulnerability.
        
        Args:
            vulnerability_id: The unique identifier of the vulnerability
        
        Returns:
            Dictionary containing:
                - resources: List of solution IDs
                - links: HATEOAS links
        
        Example:
            ```python
            solutions = client.vulnerabilities.get_solutions(
                'ssh-openssh-cve-2023-1234'
            )
            
            for solution_id in solutions['resources']:
                # Get solution details using Solutions API
                solution = client.solutions.get_solution(solution_id)
                print(f"Solution: {solution['summary']['text']}")
            ```
        """
        return self._request(
            'GET',
            f'vulnerabilities/{vulnerability_id}/solutions'
        )
    
    def get_all_vulnerabilities(
        self,
        sort: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all vulnerabilities with automatic pagination.
        
        Automatically handles pagination to retrieve all vulnerabilities in
        the database.
        
        Args:
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Example: ["riskScore,DESC"]
        
        Returns:
            List of all vulnerability dictionaries
        
        Warning:
            This method may return a very large dataset (10,000+ vulnerabilities).
            Consider using filters or pagination for production use.
        
        Example:
            ```python
            # Get all vulnerabilities (may take time)
            all_vulns = client.vulnerabilities.get_all_vulnerabilities(
                sort=["riskScore,DESC"]
            )
            
            print(f"Total vulnerabilities: {len(all_vulns)}")
            
            # Get top 10 highest risk
            top_10 = all_vulns[:10]
            for vuln in top_10:
                print(f"{vuln['id']}: {vuln['riskScore']}")
            ```
        """
        all_vulns = []
        page = 0
        size = self.MAX_PAGE_SIZE
        
        while True:
            response = self.list(page=page, size=size, sort=sort)
            vulns = response.get('resources', [])
            all_vulns.extend(vulns)
            
            # Check if we've retrieved all pages
            page_info = response.get('page', {})
            current_page = page_info.get('number', 0)
            total_pages = page_info.get('totalPages', 1)
            
            if current_page >= total_pages - 1:
                break
            
            page += 1
        
        return all_vulns
    
    def get_by_severity(
        self,
        severity: str,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerabilities filtered by severity level.
        
        Returns vulnerabilities matching the specified severity level.
        Note: This is a client-side filter - it retrieves all vulnerabilities
        and filters locally.
        
        Args:
            severity: Severity level to filter by. Valid values:
                     - 'Critical' (severityScore 9-10)
                     - 'Severe' (severityScore 7-8)
                     - 'Moderate' (severityScore 4-6)
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of vulnerability dictionaries matching the severity
        
        Example:
            ```python
            # Get critical vulnerabilities
            critical = client.vulnerabilities.get_by_severity('Critical')
            print(f"Critical vulnerabilities: {len(critical)}")
            
            # Get severe vulnerabilities
            severe = client.vulnerabilities.get_by_severity('Severe')
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter by severity
        vulns = response.get('resources', [])
        filtered = [
            v for v in vulns
            if v.get('severity', '').lower() == severity.lower()
        ]
        
        return filtered
    
    def get_critical(
        self,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get all critical vulnerabilities.
        
        Convenience method to retrieve only critical severity vulnerabilities.
        
        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of critical vulnerability dictionaries
        
        Example:
            ```python
            critical = client.vulnerabilities.get_critical()
            
            print(f"Critical vulnerabilities: {len(critical)}")
            for vuln in critical[:10]:
                print(f"- {vuln['title']}")
                print(f"  Risk: {vuln['riskScore']}")
                print(f"  CVSS: {vuln['cvss']['v3']['score']}")
            ```
        """
        return self.get_by_severity('Critical', page=page, size=size)
    
    def get_exploitable(
        self,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerabilities that have known exploits.
        
        Returns vulnerabilities where exploits field is not empty,
        indicating public exploits are available.
        
        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of exploitable vulnerability dictionaries
        
        Example:
            ```python
            exploitable = client.vulnerabilities.get_exploitable()
            
            print(f"Exploitable vulnerabilities: {len(exploitable)}")
            for vuln in exploitable:
                print(f"- {vuln['title']}")
                print(f"  Exploits available: Yes")
                print(f"  Risk: {vuln['riskScore']}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter for vulnerabilities with exploits
        vulns = response.get('resources', [])
        exploitable = [
            v for v in vulns
            if v.get('exploits') not in [None, '', 0]
        ]
        
        return exploitable
    
    def get_with_malware(
        self,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerabilities associated with malware kits.
        
        Returns vulnerabilities where malwareKits field is not empty,
        indicating known malware actively exploits this vulnerability.
        
        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of vulnerability dictionaries with malware associations
        
        Example:
            ```python
            malware_vulns = client.vulnerabilities.get_with_malware()
            
            print(f"Vulnerabilities with malware: {len(malware_vulns)}")
            for vuln in malware_vulns:
                print(f"- {vuln['title']}")
                print(f"  Risk: {vuln['riskScore']}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter for vulnerabilities with malware kits
        vulns = response.get('resources', [])
        with_malware = [
            v for v in vulns
            if v.get('malwareKits') not in [None, '', 0]
        ]
        
        return with_malware
    
    def get_by_cvss_score(
        self,
        min_score: float,
        max_score: float = 10.0,
        cvss_version: str = 'v3',
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerabilities filtered by CVSS score range.
        
        Returns vulnerabilities with CVSS scores within the specified range.
        Note: This is a client-side filter.
        
        Args:
            min_score: Minimum CVSS score (0.0-10.0)
            max_score: Maximum CVSS score (0.0-10.0, default: 10.0)
            cvss_version: CVSS version to filter by ('v2' or 'v3', default: 'v3')
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of vulnerability dictionaries matching the CVSS criteria
        
        Example:
            ```python
            # Get high CVSS v3 vulnerabilities (7.0-10.0)
            high_cvss = client.vulnerabilities.get_by_cvss_score(
                min_score=7.0,
                cvss_version='v3'
            )
            
            # Get medium CVSS v2 vulnerabilities (4.0-6.9)
            medium_cvss = client.vulnerabilities.get_by_cvss_score(
                min_score=4.0,
                max_score=6.9,
                cvss_version='v2'
            )
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter by CVSS score
        vulns = response.get('resources', [])
        filtered = []
        
        for vuln in vulns:
            cvss_data = vuln.get('cvss', {})
            version_data = cvss_data.get(cvss_version, {})
            score = version_data.get('score')
            
            if score is not None and min_score <= score <= max_score:
                filtered.append(vuln)
        
        return filtered
    
    def get_pci_failing(
        self,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerabilities that cause PCI compliance failures.
        
        Returns vulnerabilities where PCI status indicates a failure.
        
        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of PCI-failing vulnerability dictionaries
        
        Example:
            ```python
            pci_fails = client.vulnerabilities.get_pci_failing()
            
            print(f"PCI-failing vulnerabilities: {len(pci_fails)}")
            for vuln in pci_fails:
                print(f"- {vuln['title']}")
                pci = vuln['pci']
                print(f"  Status: {pci['status']}")
                print(f"  CVSS: {pci['adjustedCVSSScore']}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter for PCI failures
        vulns = response.get('resources', [])
        pci_failing = [
            v for v in vulns
            if v.get('pci', {}).get('fail') is True
        ]
        
        return pci_failing
    
    def search_by_cve(
        self,
        cve_id: str,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Search vulnerabilities by CVE identifier.
        
        Returns vulnerabilities that are associated with the specified CVE ID.
        Note: This is a client-side filter.
        
        Args:
            cve_id: CVE identifier (e.g., 'CVE-2017-11804')
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
        
        Returns:
            List of vulnerability dictionaries matching the CVE
        
        Example:
            ```python
            # Search for specific CVE
            results = client.vulnerabilities.search_by_cve('CVE-2017-11804')
            
            for vuln in results:
                print(f"- {vuln['title']}")
                print(f"  ID: {vuln['id']}")
                print(f"  CVEs: {', '.join(vuln['cves'])}")
            ```
        """
        # Validate size parameter
        size = min(size, self.MAX_PAGE_SIZE)
        
        # Normalize CVE ID
        cve_id = cve_id.upper()
        
        # Get vulnerabilities for the requested page
        response = self.list(
            page=page,
            size=size,
            sort=["riskScore,DESC"]
        )
        
        # Filter by CVE ID
        vulns = response.get('resources', [])
        matches = [
            v for v in vulns
            if cve_id in [cve.upper() for cve in v.get('cves', [])]
        ]
        
        return matches
