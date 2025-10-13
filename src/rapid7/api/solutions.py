"""
Rapid7 InsightVM Solutions API Module

This module provides a comprehensive interface for managing remediation solutions in InsightVM.
It supports listing solutions, retrieving detailed solution information, managing prerequisites,
and finding superseding solutions.

Example:
    ```python
    from rapid7 import InsightVMClient

    # Create client
    client = InsightVMClient()

    # List all solutions
    solutions = client.solutions.list(size=100)

    # Get solution details
    solution = client.solutions.get_solution('ubuntu-upgrade-libexpat1')
    print(f"Title: {solution['summary']['text']}")
    print(f"Steps: {solution['steps']['text']}")

    # Get prerequisites
    prereqs = client.solutions.get_prerequisites('solution-id')

    # Get superseding solutions (newer alternatives)
    newer = client.solutions.get_superseding_solutions('solution-id')
    ```
"""

from typing import Dict, List, Optional, Any
from .base import BaseAPI


class SolutionsAPI(BaseAPI):
    """
    API client for InsightVM Solutions operations.

    This class provides methods for managing remediation solutions including:
    - Listing and retrieving solutions
    - Getting solution details (steps, prerequisites, estimates)
    - Managing superseding relationships
    - Finding solutions for vulnerabilities
    - Accessing prerequisite solutions

    All methods follow the BaseAPI pattern and handle authentication,
    SSL verification, and error handling automatically.
    """

    MAX_PAGE_SIZE = 500

    def _validate_page_size(self, size: int) -> int:
        """
        Validate and cap page size to maximum allowed.

        Args:
            size: Requested page size

        Returns:
            Validated page size (capped at MAX_PAGE_SIZE)
        """
        return min(size, self.MAX_PAGE_SIZE)

    def list(
        self,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        List all remediation solutions.

        Returns a paginated list of all solutions available in the
        vulnerability database with support for sorting.

        Args:
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Example: ["id,ASC"]

        Returns:
            Dictionary containing:
                - resources: List of solution objects with:
                    - id: Solution identifier
                    - summary: Solution summary (html and text)
                    - steps: Remediation steps (html and text)
                    - additionalInformation: Additional details
                    - appliesTo: What the solution applies to
                    - estimate: Time estimate (ISO 8601 duration)
                    - type: Solution type (configuration, patch, rollup)
                    - links: HATEOAS links
                - page: Pagination metadata
                - links: HATEOAS links

        Example:
            ```python
            # Get first page of solutions
            solutions = client.solutions.list()

            # Get solutions sorted by ID
            solutions = client.solutions.list(
                sort=["id,ASC"]
            )

            # Get second page
            page2 = client.solutions.list(page=1, size=100)
            ```
        """
        # Validate size parameter
        size = self._validate_page_size(size)

        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }

        if sort:
            params['sort'] = sort

        return self._request('GET', 'solutions', params=params)

    def get_solution(self, solution_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific solution.

        Retrieves comprehensive information about a solution including
        remediation steps, time estimates, and applicability information.

        Args:
            solution_id: The unique identifier of the solution
                        (e.g., 'ubuntu-upgrade-libexpat1')

        Returns:
            Dictionary containing detailed solution information:
                - id: Solution identifier
                - summary: Solution summary
                    - html: HTML-formatted summary
                    - text: Plain text summary
                - steps: Remediation steps
                    - html: HTML-formatted steps
                    - text: Plain text steps
                - additionalInformation: Additional details
                    - html: HTML-formatted information
                    - text: Plain text information
                - appliesTo: Description of what it applies to
                - estimate: Time estimate (ISO 8601 duration,
                           e.g., "PT10M")
                - type: Solution type (configuration, patch, rollup)
                - links: HATEOAS links

        Raises:
            requests.exceptions.HTTPError: If solution not found (404)

        Example:
            ```python
            solution = client.solutions.get_solution(
                'ubuntu-upgrade-libexpat1'
            )

            print(f"Title: {solution['summary']['text']}")
            print(f"Applies To: {solution['appliesTo']}")
            print(f"Steps: {solution['steps']['text']}")
            print(f"Estimate: {solution['estimate']}")
            print(f"Type: {solution['type']}")
            ```
        """
        return self._request('GET', f'solutions/{solution_id}')

    def get_prerequisites(
        self,
        solution_id: str
    ) -> Dict[str, Any]:
        """
        Get prerequisite solutions that must be executed first.

        Returns solutions that must be executed before this solution
        can successfully resolve a vulnerability.

        Args:
            solution_id: The unique identifier of the solution

        Returns:
            Dictionary containing:
                - resources: List of prerequisite solution objects
                - links: HATEOAS links

        Example:
            ```python
            # Get prerequisites for a solution
            prereqs = client.solutions.get_prerequisites('solution-id')

            for prereq in prereqs['resources']:
                print(f"Must execute first: {prereq['summary']['text']}")
            ```
        """
        return self._request(
            'GET',
            f'solutions/{solution_id}/prerequisites'
        )

    def get_superseding_solutions(
        self,
        solution_id: str,
        rollup_only: bool = False
    ) -> Dict[str, Any]:
        """
        Get solutions that supersede this solution.

        Returns newer or better alternative solutions that supersede
        (replace or improve upon) this solution.

        Args:
            solution_id: The unique identifier of the solution
            rollup_only: If True, return only highest-level "rollup"
                        superseding solutions (default: False)

        Returns:
            Dictionary containing:
                - resources: List of superseding solution objects
                - links: HATEOAS links

        Example:
            ```python
            # Get all superseding solutions
            newer = client.solutions.get_superseding_solutions(
                'old-solution-id'
            )

            # Get only rollup superseding solutions
            rollups = client.solutions.get_superseding_solutions(
                'old-solution-id',
                rollup_only=True
            )

            for solution in newer['resources']:
                print(f"Newer alternative: {solution['summary']['text']}")
            ```
        """
        params = {}
        if rollup_only:
            params['rollup'] = 'true'

        return self._request(
            'GET',
            f'solutions/{solution_id}/superseding',
            params=params
        )

    def get_superseded_solutions(
        self,
        solution_id: str
    ) -> Dict[str, Any]:
        """
        Get solutions that are superseded by this solution.

        Returns older solutions that this solution supersedes
        (replaces or improves upon).

        Args:
            solution_id: The unique identifier of the solution

        Returns:
            Dictionary containing:
                - resources: List of superseded solution objects
                - links: HATEOAS links

        Example:
            ```python
            # Get solutions this one supersedes
            older = client.solutions.get_superseded_solutions(
                'new-solution-id'
            )

            for solution in older['resources']:
                print(f"This replaces: {solution['summary']['text']}")
            ```
        """
        return self._request(
            'GET',
            f'solutions/{solution_id}/supersedes'
        )

    def get_all_solutions(
        self,
        sort: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all solutions with automatic pagination.

        Automatically handles pagination to retrieve all solutions in
        the database.

        Args:
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Example: ["id,ASC"]

        Returns:
            List of all solution dictionaries

        Warning:
            This method may return a large dataset. Consider using
            pagination for production use.

        Example:
            ```python
            # Get all solutions
            all_solutions = client.solutions.get_all_solutions(
                sort=["id,ASC"]
            )

            print(f"Total solutions: {len(all_solutions)}")

            for solution in all_solutions[:10]:
                print(f"{solution['id']}: {solution['summary']['text']}")
            ```
        """
        all_solutions = []
        page = 0
        size = self.MAX_PAGE_SIZE

        while True:
            response = self.list(page=page, size=size, sort=sort)
            solutions = response.get('resources', [])
            all_solutions.extend(solutions)

            # Check if we've retrieved all pages
            page_info = response.get('page', {})
            current_page = page_info.get('number', 0)
            total_pages = page_info.get('totalPages', 1)

            if current_page >= total_pages - 1:
                break

            page += 1

        return all_solutions

    def get_by_type(
        self,
        solution_type: str,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get solutions filtered by type.

        Returns solutions matching the specified type.
        Note: This is a client-side filter.

        Args:
            solution_type: Solution type to filter by. Common types:
                          'configuration', 'patch', 'rollup'
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)

        Returns:
            List of solution dictionaries matching the type

        Example:
            ```python
            # Get configuration solutions
            config_solutions = client.solutions.get_by_type(
                'configuration'
            )

            # Get patch solutions
            patches = client.solutions.get_by_type('patch')

            # Get rollup solutions
            rollups = client.solutions.get_by_type('rollup')
            ```
        """
        # Validate size parameter
        size = self._validate_page_size(size)

        # Get solutions for the requested page
        response = self.list(page=page, size=size)

        # Filter by type
        solutions = response.get('resources', [])
        filtered = [
            s for s in solutions
            if s.get('type', '').lower() == solution_type.lower()
        ]

        return filtered

    def search_by_applies_to(
        self,
        search_term: str,
        page: int = 0,
        size: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Search solutions by what they apply to.

        Returns solutions where the 'appliesTo' field contains
        the search term. Note: This is a client-side filter.

        Args:
            search_term: Term to search for in 'appliesTo' field
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)

        Returns:
            List of solution dictionaries matching the search

        Example:
            ```python
            # Find Ubuntu-related solutions
            ubuntu_solutions = client.solutions.search_by_applies_to(
                'Ubuntu'
            )

            # Find Windows solutions
            windows_solutions = client.solutions.search_by_applies_to(
                'Windows'
            )

            for solution in ubuntu_solutions:
                print(f"- {solution['summary']['text']}")
                print(f"  Applies to: {solution['appliesTo']}")
            ```
        """
        # Validate size parameter
        size = self._validate_page_size(size)

        # Get solutions for the requested page
        response = self.list(page=page, size=size)

        # Filter by appliesTo field
        solutions = response.get('resources', [])
        search_lower = search_term.lower()
        matches = [
            s for s in solutions
            if search_lower in s.get('appliesTo', '').lower()
        ]

        return matches
