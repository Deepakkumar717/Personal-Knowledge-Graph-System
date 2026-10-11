import os
import sqlite3
import datetime
from pathlib import Path
from typing import List, Optional
from app.core.config import settings
from app.schemas.safety import BackupItem

class BackupService:
    def __init__(self, db_path: Optional[Path] = None, backups_dir: Optional[Path] = None):
        self.db_path = db_path or settings.DATABASE_PATH
        self.backups_dir = backups_dir or settings.BACKUPS_DIR
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, reason: str = "manual") -> Optional[str]:
        """Creates an atomic backup of the database using SQLite's backup API."""
        if not self.db_path.exists():
            return None

        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_filename = f"knowledge_{ts}_{reason}.db"
        backup_path = self.backups_dir / backup_filename

        src_conn = None
        dst_conn = None
        try:
            src_conn = sqlite3.connect(str(self.db_path))
            dst_conn = sqlite3.connect(str(backup_path))
            src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()

            # Maintain only newest 20 backups
            self.prune_backups(keep=20)
            return backup_filename
        except Exception as e:
            if dst_conn:
                try: dst_conn.close()
                except: pass
            if src_conn:
                try: src_conn.close()
                except: pass
            print(f"[BackupService] Backup failed: {e}")
            return None

    def list_backups(self) -> List[BackupItem]:
        """List all available backup files ordered by newest first."""
        items: List[BackupItem] = []
        if not self.backups_dir.exists():
            return items

        files = sorted(self.backups_dir.glob("knowledge_*.db"), key=os.path.getmtime, reverse=True)
        for f in files:
            stat = f.stat()
            created_at = datetime.datetime.fromtimestamp(stat.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            items.append(BackupItem(
                filename=f.name,
                created_at=created_at,
                size_bytes=stat.st_size,
            ))
        return items

    def restore_backup(self, filename: str) -> bool:
        """Restores a specified backup file after taking a pre-restore safety backup."""
        # Sanitize filename
        safe_name = Path(filename).name
        target_backup = self.backups_dir / safe_name
        if not target_backup.exists() or not target_backup.is_file():
            raise FileNotFoundError(f"Backup file '{safe_name}' not found.")

        # Safety backup of current state
        self.create_backup(reason="pre_restore")

        # Atomic restore via SQLite backup API
        src_conn = None
        dst_conn = None
        try:
            src_conn = sqlite3.connect(str(target_backup))
            dst_conn = sqlite3.connect(str(self.db_path))
            src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()
            return True
        except Exception as e:
            if dst_conn:
                try: dst_conn.close()
                except: pass
            if src_conn:
                try: src_conn.close()
                except: pass
            raise RuntimeError(f"Restore failed: {e}")

    def prune_backups(self, keep: int = 20) -> None:
        """Keep only the latest `keep` backups."""
        files = sorted(self.backups_dir.glob("knowledge_*.db"), key=os.path.getmtime, reverse=True)
        for old_file in files[keep:]:
            try:
                old_file.unlink()
            except Exception:
                pass

backup_service = BackupService()
