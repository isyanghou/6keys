# -*- coding: utf-8 -*-
"""
Data I/O utilities for Six Keys Criticality framework.

六鑰臨界數據輸入輸出工具模組：提供數據加載、保存和配置管理功能

This module provides utilities for loading and saving data, configurations,
and analysis results in the Six Keys Criticality framework.
"""

import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import yaml
from datetime import datetime
import warnings


def load_data(file_path: Union[str, Path], 
              format: Optional[str] = None,
              **kwargs) -> Any:
    """
    Load data from various file formats.
    
    Parameters
    ----------
    file_path : str or Path
        Path to the data file
    format : str, optional
        File format ('csv', 'json', 'pickle', 'npy', 'npz', 'mat', 'xlsx')
        If None, inferred from file extension
    **kwargs
        Additional arguments passed to the loading function
        
    Returns
    -------
    data : any
        Loaded data
        
    Examples
    --------
    >>> data = load_data('data.csv')
    >>> config = load_data('config.json')
    >>> results = load_data('results.pickle')
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Infer format from extension if not provided
    if format is None:
        format = file_path.suffix.lower().lstrip('.')
    
    format = format.lower()
    
    try:
        if format == 'csv':
            return pd.read_csv(file_path, **kwargs)
        
        elif format == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f, **kwargs)
        
        elif format in ['pickle', 'pkl']:
            with open(file_path, 'rb') as f:
                return pickle.load(f, **kwargs)
        
        elif format == 'npy':
            return np.load(file_path, **kwargs)
        
        elif format == 'npz':
            return np.load(file_path, allow_pickle=True, **kwargs)
        
        elif format in ['yaml', 'yml']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f, **kwargs)
        
        elif format in ['xlsx', 'xls']:
            return pd.read_excel(file_path, **kwargs)
        
        elif format == 'mat':
            try:
                from scipy.io import loadmat
                return loadmat(file_path, **kwargs)
            except ImportError:
                raise ImportError("scipy is required to load .mat files")
        
        elif format == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            raise ValueError(f"Unsupported file format: {format}")
            
    except Exception as e:
        raise IOError(f"Error loading file {file_path}: {str(e)}")


def save_results(results: Any,
                file_path: Union[str, Path],
                format: Optional[str] = None,
                metadata: Optional[Dict[str, Any]] = None,
                **kwargs) -> None:
    """
    Save analysis results to file.
    
    Parameters
    ----------
    results : any
        Results to save
    file_path : str or Path
        Output file path
    format : str, optional
        File format ('json', 'pickle', 'csv', 'xlsx', 'npz')
        If None, inferred from file extension
    metadata : dict, optional
        Additional metadata to include
    **kwargs
        Additional arguments passed to the saving function
        
    Examples
    --------
    >>> save_results(analysis_results, 'results.json')
    >>> save_results(dataframe, 'data.csv')
    >>> save_results(arrays, 'data.npz')
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Infer format from extension if not provided
    if format is None:
        format = file_path.suffix.lower().lstrip('.')
    
    format = format.lower()
    
    # Add metadata if provided
    if metadata is not None:
        if hasattr(results, '__dict__'):
            # For objects with attributes
            results_dict = results.__dict__.copy()
            results_dict['_metadata'] = metadata
            results_to_save = results_dict
        elif isinstance(results, dict):
            # For dictionaries
            results_to_save = results.copy()
            results_to_save['_metadata'] = metadata
        else:
            # For other types, wrap in dictionary
            results_to_save = {
                'data': results,
                '_metadata': metadata
            }
    else:
        results_to_save = results
    
    # Add timestamp to metadata
    if isinstance(results_to_save, dict) and '_metadata' not in results_to_save:
        results_to_save['_metadata'] = {}
    if isinstance(results_to_save, dict) and '_metadata' in results_to_save:
        results_to_save['_metadata']['saved_at'] = datetime.now().isoformat()
    
    try:
        if format == 'json':
            # Convert to JSON-serializable format
            json_data = _convert_to_json_serializable(results_to_save)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, **kwargs)
        
        elif format in ['pickle', 'pkl']:
            with open(file_path, 'wb') as f:
                pickle.dump(results_to_save, f, **kwargs)
        
        elif format == 'csv':
            if isinstance(results_to_save, pd.DataFrame):
                results_to_save.to_csv(file_path, **kwargs)
            elif isinstance(results_to_save, dict):
                # Try to convert dict to DataFrame
                try:
                    df = pd.DataFrame(results_to_save)
                    df.to_csv(file_path, **kwargs)
                except:
                    # If conversion fails, save as JSON instead
                    warnings.warn(f"Cannot save as CSV, saving as JSON instead")
                    json_path = file_path.with_suffix('.json')
                    save_results(results_to_save, json_path, format='json')
            else:
                raise ValueError("CSV format requires DataFrame or dict input")
        
        elif format in ['xlsx', 'xls']:
            if isinstance(results_to_save, pd.DataFrame):
                results_to_save.to_excel(file_path, **kwargs)
            elif isinstance(results_to_save, dict):
                # Save multiple sheets if dict contains DataFrames
                with pd.ExcelWriter(file_path) as writer:
                    for key, value in results_to_save.items():
                        if isinstance(value, pd.DataFrame):
                            value.to_excel(writer, sheet_name=str(key)[:31])  # Excel sheet name limit
                        elif isinstance(value, dict):
                            try:
                                df = pd.DataFrame(value)
                                df.to_excel(writer, sheet_name=str(key)[:31])
                            except:
                                continue
            else:
                raise ValueError("Excel format requires DataFrame or dict input")
        
        elif format == 'npz':
            if isinstance(results_to_save, dict):
                # Convert non-array values to arrays where possible
                arrays_dict = {}
                for key, value in results_to_save.items():
                    if isinstance(value, np.ndarray):
                        arrays_dict[key] = value
                    elif isinstance(value, (list, tuple)):
                        try:
                            arrays_dict[key] = np.array(value)
                        except:
                            arrays_dict[key] = np.array(value, dtype=object)
                    else:
                        arrays_dict[key] = np.array([value], dtype=object)
                
                np.savez(file_path, **arrays_dict)
            else:
                np.savez(file_path, data=results_to_save)
        
        elif format in ['yaml', 'yml']:
            yaml_data = _convert_to_yaml_serializable(results_to_save)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, **kwargs)
        
        else:
            raise ValueError(f"Unsupported file format: {format}")
            
    except Exception as e:
        raise IOError(f"Error saving file {file_path}: {str(e)}")


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from file.
    
    Parameters
    ----------
    config_path : str or Path
        Path to configuration file
        
    Returns
    -------
    config : dict
        Configuration dictionary
        
    Examples
    --------
    >>> config = load_config('config.json')
    >>> config = load_config('settings.yaml')
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    format = config_path.suffix.lower().lstrip('.')
    
    if format == 'json':
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    elif format in ['yaml', 'yml']:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported configuration format: {format}")
    
    # Validate configuration
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")
    
    return config


def save_config(config: Dict[str, Any],
               config_path: Union[str, Path],
               format: Optional[str] = None) -> None:
    """
    Save configuration to file.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
    config_path : str or Path
        Output configuration file path
    format : str, optional
        File format ('json', 'yaml')
        If None, inferred from file extension
        
    Examples
    --------
    >>> save_config(config, 'config.json')
    >>> save_config(settings, 'settings.yaml')
    """
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Infer format from extension if not provided
    if format is None:
        format = config_path.suffix.lower().lstrip('.')
    
    format = format.lower()
    
    # Add metadata
    config_with_metadata = config.copy()
    config_with_metadata['_metadata'] = {
        'created_at': datetime.now().isoformat(),
        'format': format,
        'version': '1.0'
    }
    
    if format == 'json':
        json_data = _convert_to_json_serializable(config_with_metadata)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    elif format in ['yaml', 'yml']:
        yaml_data = _convert_to_yaml_serializable(config_with_metadata)
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)
    
    else:
        raise ValueError(f"Unsupported configuration format: {format}")


def _convert_to_json_serializable(obj: Any) -> Any:
    """
    Convert objects to JSON-serializable format.
    
    Parameters
    ----------
    obj : any
        Object to convert
        
    Returns
    -------
    serializable_obj : any
        JSON-serializable object
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, (np.complex64, np.complex128)):
        return {'real': float(obj.real), 'imag': float(obj.imag), '_type': 'complex'}
    elif isinstance(obj, dict):
        return {key: _convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, set):
        return {'_type': 'set', 'values': [_convert_to_json_serializable(item) for item in obj]}
    elif hasattr(obj, '__dict__'):
        # Handle custom objects
        return _convert_to_json_serializable(obj.__dict__)
    elif isinstance(obj, (datetime)):
        return obj.isoformat()
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


def _convert_to_yaml_serializable(obj: Any) -> Any:
    """
    Convert objects to YAML-serializable format.
    
    Parameters
    ----------
    obj : any
        Object to convert
        
    Returns
    -------
    serializable_obj : any
        YAML-serializable object
    """
    # YAML can handle more types than JSON, but we still need some conversions
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, dict):
        return {key: _convert_to_yaml_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_to_yaml_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return _convert_to_yaml_serializable(obj.__dict__)
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


def create_data_directory(base_path: Union[str, Path],
                         subdirs: Optional[List[str]] = None) -> Path:
    """
    Create a data directory structure.
    
    Parameters
    ----------
    base_path : str or Path
        Base directory path
    subdirs : list of str, optional
        Subdirectories to create
        
    Returns
    -------
    base_path : Path
        Created base directory path
        
    Examples
    --------
    >>> data_dir = create_data_directory('data', ['raw', 'processed', 'results'])
    """
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)
    
    if subdirs is not None:
        for subdir in subdirs:
            (base_path / subdir).mkdir(exist_ok=True)
    
    return base_path


def list_data_files(directory: Union[str, Path],
                   pattern: str = '*',
                   recursive: bool = False) -> List[Path]:
    """
    List data files in a directory.
    
    Parameters
    ----------
    directory : str or Path
        Directory to search
    pattern : str, default='*'
        File pattern to match
    recursive : bool, default=False
        Whether to search recursively
        
    Returns
    -------
    files : list of Path
        List of matching files
        
    Examples
    --------
    >>> files = list_data_files('data', '*.csv')
    >>> all_files = list_data_files('data', recursive=True)
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if recursive:
        files = list(directory.rglob(pattern))
    else:
        files = list(directory.glob(pattern))
    
    # Filter to only include files (not directories)
    files = [f for f in files if f.is_file()]
    
    return sorted(files)


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Get information about a file.
    
    Parameters
    ----------
    file_path : str or Path
        Path to the file
        
    Returns
    -------
    info : dict
        File information
        
    Examples
    --------
    >>> info = get_file_info('data.csv')
    >>> print(info['size'], info['modified'])
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    stat = file_path.stat()
    
    info = {
        'name': file_path.name,
        'path': str(file_path),
        'size': stat.st_size,
        'size_mb': stat.st_size / (1024 * 1024),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'extension': file_path.suffix,
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir()
    }
    
    return info


def backup_file(file_path: Union[str, Path],
               backup_dir: Optional[Union[str, Path]] = None,
               timestamp: bool = True) -> Path:
    """
    Create a backup of a file.
    
    Parameters
    ----------
    file_path : str or Path
        Path to the file to backup
    backup_dir : str or Path, optional
        Directory to store backup. If None, uses same directory as original
    timestamp : bool, default=True
        Whether to add timestamp to backup filename
        
    Returns
    -------
    backup_path : Path
        Path to the backup file
        
    Examples
    --------
    >>> backup_path = backup_file('important_data.csv')
    >>> backup_path = backup_file('config.json', 'backups')
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if backup_dir is None:
        backup_dir = file_path.parent
    else:
        backup_dir = Path(backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Create backup filename
    if timestamp:
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.stem}_{timestamp_str}{file_path.suffix}"
    else:
        backup_name = f"{file_path.stem}_backup{file_path.suffix}"
    
    backup_path = backup_dir / backup_name
    
    # Copy file
    import shutil
    shutil.copy2(file_path, backup_path)
    
    return backup_path