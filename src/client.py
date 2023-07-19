"""
TODO: Update Summary Docstring
"""

import os
import src.rapid7
import src.paloalto

from src.rapid7.api_r7_asset_group import create_high_risk_asset_group

class AssetGroupCreator:
    def __init__(self):
        pass
    
    def create_high_risk_asset_group(self, name):
        create_high_risk_asset_group(name)
