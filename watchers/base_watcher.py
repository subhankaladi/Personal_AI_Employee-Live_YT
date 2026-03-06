"""
Base Watcher Module

Abstract base class for all watcher scripts in the AI Employee system.
All watchers inherit from this class and implement the check_for_updates()
and create_action_file() methods.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher scripts.
    
    Watchers are lightweight Python scripts that run continuously in the
    background, monitoring external systems (Gmail, WhatsApp, file system, etc.)
    and creating actionable .md files in the /Needs_Action folder when changes
    are detected.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            check_interval: Time in seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        
        # Ensure the Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Track processed items to avoid duplicates
        self.processed_ids: set = set()
        
    def _setup_logging(self) -> None:
        """Configure logging for the watcher."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'watcher_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check the external system for new items.
        
        Returns:
            List of new items that need processing
            
        This method must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created file, or None if creation failed
            
        This method must be implemented by subclasses.
        """
        pass
    
    def run(self) -> None:
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    for item in items:
                        filepath = self.create_action_file(item)
                        if filepath:
                            self.logger.info(f'Created action file: {filepath.name}')
                except Exception as e:
                    self.logger.error(f'Error during check: {e}', exc_info=True)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise
    
    def generate_filename(self, prefix: str, unique_id: str) -> str:
        """
        Generate a standardized filename for action files.
        
        Args:
            prefix: Type prefix (e.g., 'EMAIL', 'WHATSAPP', 'FILE')
            unique_id: Unique identifier for the item
            
        Returns:
            Formatted filename string
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'{prefix}_{unique_id}_{timestamp}.md'
    
    def create_frontmatter(self, **kwargs) -> str:
        """
        Create YAML frontmatter for action files.
        
        Args:
            **kwargs: Key-value pairs for frontmatter
            
        Returns:
            Formatted YAML frontmatter string
        """
        lines = ['---']
        for key, value in kwargs.items():
            lines.append(f'{key}: {value}')
        lines.append('---')
        return '\n'.join(lines)
