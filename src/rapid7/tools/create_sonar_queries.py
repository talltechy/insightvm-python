#!/usr/bin/env python3
"""
Create Sonar Discovery Queries from CSV

This tool reads a CSV file containing discovery targets (domains or IP ranges)
and creates InsightVM Sonar queries for each target using the InsightVM API.

CSV Format:
    target
    example.com
    192.168.1.0/24
    test.org

Usage:
    python create_sonar_queries.py <csv_file> [--days N]

Example:
    python create_sonar_queries.py targets.csv --days 7
"""

import argparse
import ipaddress
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

import pandas as pd  # type: ignore

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rapid7.client import InsightVMClient  # noqa: E402


def is_valid_domain(domain: str) -> bool:
    """
    Check if string is a valid domain name.
    
    Args:
        domain: String to validate
    
    Returns:
        True if valid domain, False otherwise
    """
    pattern = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$'
    return bool(re.match(pattern, domain.lower()))


def parse_target(target: str) -> Tuple[str, Dict[str, Any]]:
    """
    Parse a target string and determine its type and filter criteria.
    
    Args:
        target: Target string (domain or IP/CIDR)
    
    Returns:
        Tuple of (target_type, filter_dict)
        
    Raises:
        ValueError: If target format is invalid
    """
    target = target.strip()
    
    # Check if it's a domain
    if is_valid_domain(target):
        return 'domain', {"type": "domain-contains", "domain": target}
    
    # Try to parse as IP or IP range
    try:
        ip_range = ipaddress.ip_network(target, strict=False)
        return 'ip_range', {
            "type": "ip-address-range",
            "lower": str(ip_range.network_address),
            "upper": str(ip_range.broadcast_address)
        }
    except ValueError:
        raise ValueError(f"Invalid target format: {target}")


def load_targets_from_csv(filepath: str) -> pd.DataFrame:
    """
    Load targets from CSV file.
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        DataFrame with targets
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    if not Path(filepath).exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    
    df = pd.read_csv(filepath, skipinitialspace=True)
    
    # Validate CSV format
    if 'target' not in df.columns:
        raise ValueError(
            "CSV file must have a 'target' column. "
            "Found columns: " + ", ".join(df.columns)
        )
    
    # Clean whitespace
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df


def create_queries_from_csv(
    client: InsightVMClient,
    filepath: str,
    days: int = 30
) -> pd.DataFrame:
    """
    Create Sonar queries from CSV file.
    
    Args:
        client: InsightVM client instance
        filepath: Path to CSV file
        days: Number of days for scan recency filter
    
    Returns:
        DataFrame with results (target, status, query_id, message)
    """
    # Load targets
    df = load_targets_from_csv(filepath)
    
    # Add result columns
    df['status'] = ''
    df['query_id'] = ''
    df['message'] = ''
    
    print(f"\nProcessing {len(df)} targets with {days}-day scan filter...")
    print("-" * 80)
    
    # Process each target
    for index, row in df.iterrows():
        target = row['target']
        print(f"\nProcessing: {target}")
        
        try:
            # Parse target
            target_type, filter_dict = parse_target(target)
            
            # Build filters
            filters: List[Dict[str, Any]] = [
                filter_dict,
                {"type": "scan-date-within-the-last", "days": days}
            ]
            
            # Create query
            result = client.sonar_queries.create_sonar_query(
                name=target,
                filters=filters
            )
            
            # Update results
            df.at[index, 'status'] = 'success'
            df.at[index, 'query_id'] = result.get('id', '')
            df.at[index, 'message'] = (
                f"Query created successfully. ID: {result.get('id')}"
            )
            
            print(f"  ✓ Success - Query ID: {result.get('id')}")
            
        except ValueError as e:
            df.at[index, 'status'] = 'error'
            df.at[index, 'message'] = str(e)
            print(f"  ✗ Error: {e}")
            
        except Exception as e:
            df.at[index, 'status'] = 'error'
            df.at[index, 'message'] = f"API Error: {str(e)}"
            print(f"  ✗ API Error: {e}")
    
    return df


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Create InsightVM Sonar queries from CSV file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CSV Format:
  The CSV file must have a 'target' column containing domains or IP ranges.
  
  Example CSV:
    target
    example.com
    192.168.1.0/24
    test.org
    10.0.0.1
    
Examples:
  # Create queries with default 30-day filter
  python create_sonar_queries.py targets.csv
  
  # Create queries with 7-day filter
  python create_sonar_queries.py targets.csv --days 7
  
  # Save results to specific output file
  python create_sonar_queries.py targets.csv --output results.csv
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='Path to CSV file containing targets'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days for scan-date-within-the-last filter (default: 30)'
    )
    parser.add_argument(
        '--output',
        help='Output CSV file path (default: input file with _results suffix)'
    )
    
    args = parser.parse_args()
    
    # Validate days parameter
    if args.days < 1:
        parser.error("--days must be a positive integer")
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        input_path = Path(args.csv_file)
        output_file = (
            input_path.parent /
            f"{input_path.stem}_results{input_path.suffix}"
        )
    
    print("=" * 80)
    print("InsightVM Sonar Query Creator")
    print("=" * 80)
    print(f"Input file:  {args.csv_file}")
    print(f"Output file: {output_file}")
    print(f"Days filter: {args.days}")
    
    try:
        # Create client (uses environment variables)
        print("\nConnecting to InsightVM...")
        client = InsightVMClient()
        print(f"Connected to: {client.auth.base_url}")
        
        # Process CSV
        results_df = create_queries_from_csv(
            client,
            args.csv_file,
            days=args.days
        )
        
        # Save results
        results_df.to_csv(output_file, index=False)
        
        # Print summary
        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        success_count = (results_df['status'] == 'success').sum()
        error_count = (results_df['status'] == 'error').sum()
        print(f"Total targets:  {len(results_df)}")
        print(f"Successful:     {success_count}")
        print(f"Failed:         {error_count}")
        print(f"\nResults saved to: {output_file}")
        
        # Exit with error if any failed
        sys.exit(0 if error_count == 0 else 1)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
