"""Replay recorder for capturing agent executions"""

import json
import hashlib
import zstandard as zstd
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class ReplayRecorder:
    """Record agent executions for deterministic replay"""
    
    def __init__(self, storage_path: str = "./data/replays"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.compressor = zstd.ZstdCompressor()
        self.decompressor = zstd.ZstdDecompressor()
    
    def record_boundary(
        self,
        execution_id: str,
        boundary_type: str,
        input_data: Any,
        output_data: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Record a non-deterministic boundary (LLM call, tool call, etc.)
        
        Args:
            execution_id: Execution identifier
            boundary_type: Type of boundary (llm, tool, database, etc.)
            input_data: Input to the boundary
            output_data: Output from the boundary
            metadata: Additional metadata
            
        Returns:
            Fixture ID (content-addressed)
        """
        # Create fixture
        fixture = {
            "execution_id": execution_id,
            "boundary_type": boundary_type,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Serialize and compress
        fixture_json = json.dumps(fixture, default=str)
        fixture_hash = hashlib.sha256(fixture_json.encode()).hexdigest()
        
        # Store compressed fixture
        fixture_path = self.storage_path / f"{fixture_hash}.zst"
        compressed = self.compressor.compress(fixture_json.encode())
        
        with open(fixture_path, "wb") as f:
            f.write(compressed)
        
        return fixture_hash
    
    def load_fixture(self, fixture_id: str) -> Dict[str, Any]:
        """
        Load a recorded fixture
        
        Args:
            fixture_id: Fixture identifier (SHA-256 hash)
            
        Returns:
            Fixture data
        """
        fixture_path = self.storage_path / f"{fixture_id}.zst"
        
        if not fixture_path.exists():
            raise ValueError(f"Fixture not found: {fixture_id}")
        
        with open(fixture_path, "rb") as f:
            compressed = f.read()
        
        decompressed = self.decompressor.decompress(compressed)
        fixture = json.loads(decompressed.decode())
        
        return fixture
    
    def record_execution(
        self,
        execution_id: str,
        boundaries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Record a complete execution with all boundaries
        
        Args:
            execution_id: Execution identifier
            boundaries: List of boundary recordings
            
        Returns:
            Recording metadata
        """
        fixture_ids = []
        
        for boundary in boundaries:
            fixture_id = self.record_boundary(
                execution_id=execution_id,
                boundary_type=boundary["type"],
                input_data=boundary["input"],
                output_data=boundary["output"],
                metadata=boundary.get("metadata"),
            )
            fixture_ids.append(fixture_id)
        
        # Create recording manifest
        manifest = {
            "execution_id": execution_id,
            "fixture_ids": fixture_ids,
            "boundary_types": [b["type"] for b in boundaries],
            "recorded_at": datetime.utcnow().isoformat(),
        }
        
        # Save manifest
        manifest_path = self.storage_path / f"{execution_id}_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        return manifest
    
    def load_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Load a complete execution recording
        
        Args:
            execution_id: Execution identifier
            
        Returns:
            Recording manifest with fixtures
        """
        manifest_path = self.storage_path / f"{execution_id}_manifest.json"
        
        if not manifest_path.exists():
            raise ValueError(f"Recording not found: {execution_id}")
        
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        
        # Load all fixtures
        fixtures = []
        for fixture_id in manifest["fixture_ids"]:
            fixture = self.load_fixture(fixture_id)
            fixtures.append(fixture)
        
        manifest["fixtures"] = fixtures
        
        return manifest


# Global recorder instance
replay_recorder = ReplayRecorder()
