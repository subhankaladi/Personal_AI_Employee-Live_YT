"""
File System Watcher

Monitors a designated "drop folder" for new files and creates action files
in the Obsidian vault's /Needs_Action folder.

This is the Bronze Tier watcher - simple, reliable, and doesn't require
external API credentials.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import shutil
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file creation events in the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        """
        Initialize the handler.
        
        Args:
            watcher: The parent FileSystemWatcher instance
        """
        self.watcher = watcher
        self.logger = watcher.logger
    
    def on_created(self, event) -> None:
        """
        Handle file creation events.
        
        Args:
            event: The file system event
        """
        if event.is_directory:
            return
        
        source_path = Path(event.src_path)
        
        # Skip hidden files and temporary files
        if source_path.name.startswith('.') or source_path.suffix == '.tmp':
            return
        
        self.logger.info(f'New file detected: {source_path.name}')
        
        # Create action file for this new file
        self.watcher.process_new_file(source_path)


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a new file is detected, it:
    1. Copies the file to the vault
    2. Creates a metadata .md file in /Needs_Action
    3. Logs the action for audit purposes
    """
    
    def __init__(self, vault_path: str, drop_folder_path: str, check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            drop_folder_path: Path to the folder to monitor for new files
            check_interval: Time in seconds between checks (default: 5)
        """
        super().__init__(vault_path, check_interval)
        
        self.drop_folder = Path(drop_folder_path)
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by hash to avoid duplicates
        self.processed_hashes: set = set()
        
        # Create subfolder for dropped files in vault
        self.dropped_files_dir = self.vault_path / 'Dropped_Files'
        self.dropped_files_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f'Drop folder: {self.drop_folder}')
    
    def check_for_updates(self) -> List[Path]:
        """
        Check for new files in the drop folder.
        
        This method is called by the base class run loop, but for the
        watchdog-based implementation, we use event-driven detection.
        This method scans existing files on startup.
        
        Returns:
            List of new file paths to process
        """
        new_files = []
        
        for file_path in self.drop_folder.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                file_hash = self._get_file_hash(file_path)
                if file_hash not in self.processed_hashes:
                    new_files.append(file_path)
                    self.processed_hashes.add(file_hash)
        
        return new_files
    
    def _get_file_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of a file for duplicate detection.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def process_new_file(self, source_path: Path) -> Optional[Path]:
        """
        Process a newly detected file.
        
        Args:
            source_path: Path to the new file
            
        Returns:
            Path to the created action file, or None if failed
        """
        try:
            # Generate unique ID from file hash
            file_hash = self._get_file_hash(source_path)
            
            # Copy file to vault
            dest_path = self.dropped_files_dir / source_path.name
            shutil.copy2(source_path, dest_path)
            self.logger.info(f'Copied file to vault: {dest_path.name}')
            
            # Create metadata action file
            action_file = self.create_action_file({
                'source_path': source_path,
                'dest_path': dest_path,
                'file_hash': file_hash
            })
            
            # Remove from drop folder after processing (optional)
            # source_path.unlink()
            
            return action_file
            
        except Exception as e:
            self.logger.error(f'Error processing file {source_path}: {e}')
            return None
    
    def create_action_file(self, item: Dict[str, Any]) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: Dictionary containing file information
            
        Returns:
            Path to the created file, or None if creation failed
        """
        try:
            source_path = item['source_path']
            dest_path = item['dest_path']
            file_hash = item['file_hash']
            
            # Get file metadata
            file_stat = source_path.stat()
            file_size = file_stat.st_size
            file_modified = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Generate filename
            filename = self.generate_filename('FILE', source_path.stem[:20])
            filepath = self.needs_action / filename
            
            # Create action file content
            content = f'''{self.create_frontmatter(
                type='file_drop',
                original_name=source_path.name,
                vault_path=str(dest_path.relative_to(self.vault_path)),
                size=file_size,
                size_human=self._format_size(file_size),
                received=datetime.now().isoformat(),
                status='pending',
                priority='medium'
            )}

# File Drop for Processing

## File Information

| Property | Value |
|----------|-------|
| Original Name | `{source_path.name}` |
| File Size | {self._format_size(file_size)} |
| Received | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| File Hash | `{file_hash}` |

## File Location

- **Drop Folder:** `{source_path}`
- **Vault Copy:** `{dest_path}`

## Suggested Actions

- [ ] Review file contents
- [ ] Categorize file type
- [ ] Process or take action
- [ ] Move to /Done when complete

## Notes

```
Add your processing notes here...
```

---
*Auto-generated by FileSystemWatcher*
'''
            
            filepath.write_text(content, encoding='utf-8')
            return filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}')
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f'{size_bytes:.2f} {unit}'
            size_bytes /= 1024.0
        return f'{size_bytes:.2f} PB'
    
    def run(self) -> None:
        """
        Run the file system watcher using watchdog Observer.
        
        Overrides base class to use event-driven detection instead of polling.
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Drop folder: {self.drop_folder}')
        
        # Process any existing files on startup
        existing_files = self.check_for_updates()
        for file_path in existing_files:
            self.process_new_file(file_path)
        
        # Set up watchdog observer
        event_handler = DropFolderHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        self.logger.info(f'Watching for new files in: {self.drop_folder}')
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
            observer.stop()
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            observer.stop()
            raise
        
        observer.join()


def main():
    """Main entry point for the filesystem watcher."""
    if len(sys.argv) < 3:
        print('Usage: python filesystem_watcher.py <vault_path> <drop_folder_path>')
        print('')
        print('Arguments:')
        print('  vault_path       - Path to your Obsidian vault root')
        print('  drop_folder_path - Path to the folder to monitor for new files')
        print('')
        print('Example:')
        print('  python filesystem_watcher.py "C:/Vaults/AI_Employee" "C:/Users/Me/Drop"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder_path = sys.argv[2]
    
    # Validate paths
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create drop folder if it doesn't exist
    Path(drop_folder_path).mkdir(parents=True, exist_ok=True)
    
    # Start the watcher
    watcher = FileSystemWatcher(vault_path, drop_folder_path)
    watcher.run()


if __name__ == '__main__':
    main()
