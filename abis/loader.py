"""
ABI Loader Utility

This module provides utilities to load ABI files from JSON.
Centralizes ABI loading logic and provides caching.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from functools import lru_cache


class ABILoader:
    """Utility class to load and cache ABI files"""
    
    def __init__(self, abis_dir: str = None):
        """
        Initialize ABI loader.
        
        Args:
            abis_dir: Directory containing JSON ABI files. 
                     Defaults to 'abis/json' relative to this file.
        """
        if abis_dir is None:
            # Default to json subdirectory
            current_dir = Path(__file__).parent
            self.abis_dir = current_dir / 'json'
        else:
            self.abis_dir = Path(abis_dir)
        
        if not self.abis_dir.exists():
            raise FileNotFoundError(f"ABIs directory not found: {self.abis_dir}")
    
    @lru_cache(maxsize=32)
    def load_abi(self, contract_name: str) -> List[Dict[str, Any]]:
        """
        Load ABI from JSON file with caching.
        
        Args:
            contract_name: Name of the contract (without .json extension)
            
        Returns:
            ABI as a list of dictionaries
            
        Raises:
            FileNotFoundError: If ABI file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        abi_path = self.abis_dir / f"{contract_name}.json"
        
        if not abi_path.exists():
            raise FileNotFoundError(
                f"ABI file not found: {abi_path}\n"
                f"Available ABIs: {self.list_available_abis()}"
            )
        
        with open(abi_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_available_abis(self) -> List[str]:
        """
        List all available ABI files.
        
        Returns:
            List of contract names (without .json extension)
        """
        return [
            f.stem for f in self.abis_dir.glob('*.json')
        ]
    
    def get_abi_path(self, contract_name: str) -> Path:
        """
        Get full path to an ABI file.
        
        Args:
            contract_name: Name of the contract
            
        Returns:
            Path to the ABI file
        """
        return self.abis_dir / f"{contract_name}.json"


# Global loader instance
_loader = ABILoader()


def load_abi(contract_name: str) -> List[Dict[str, Any]]:
    """
    Convenience function to load an ABI.
    
    Args:
        contract_name: Name of the contract (without .json extension)
        
    Returns:
        ABI as a list of dictionaries
        
    Example:
        >>> erc20_abi = load_abi('ERC20')
        >>> axie_abi = load_abi('Axie')
    """
    return _loader.load_abi(contract_name)


def list_abis() -> List[str]:
    """
    List all available ABIs.
    
    Returns:
        List of contract names
        
    Example:
        >>> available = list_abis()
        >>> print(available)
        ['ERC20', 'Axie', 'Katana', ...]
    """
    return _loader.list_available_abis()


# Pre-load commonly used ABIs for convenience
ERC20_ABI = load_abi('ERC20')
KATANA_FACTORY_ABI = load_abi('KatanaFactory')
RESERVES_ABI = load_abi('Reserves')

# You can add more as you convert them:
# AXIE_ABI = load_abi('Axie')
# MARKETPLACE_ABI = load_abi('MarketplaceGatewayV2')
