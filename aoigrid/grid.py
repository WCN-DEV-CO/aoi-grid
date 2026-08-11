"""
Spatial hash grid for efficient 2D/3D neighbor queries.
O(1) insert, O(k) neighbor lookup where k = nearby cells.
"""
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field
import math


@dataclass
class GridCell:
    key: Tuple[int, ...]
    items: List[Any] = field(default_factory=list)


class SpatialGrid:
    """Uniform spatial hash grid for 2D or 3D spatial queries."""

    def __init__(self, cell_size: float, dimensions: int = 2):
        self.cell_size = float(cell_size)
        self.dimensions = dimensions
        self.cells: Dict[Tuple[int, ...], GridCell] = {}

    def _hash(self, point: Tuple[float, ...]) -> Tuple[int, ...]:
        return tuple(int(math.floor(p / self.cell_size)) for p in point[:self.dimensions])

    def insert(self, item: Any, position: Tuple[float, ...]):
        key = self._hash(position)
        if key not in self.cells:
            self.cells[key] = GridCell(key=key)
        self.cells[key].items.append((item, position))

    def remove(self, item: Any, position: Tuple[float, ...]):
        key = self._hash(position)
        if key in self.cells:
            self.cells[key].items = [(i, p) for i, p in self.cells[key].items if i != item]

    def query_radius(self, center: Tuple[float, ...], radius: float) -> List[Any]:
        """Return all items within radius of center."""
        results = []
        center_hash = self._hash(center)
        cell_range = int(math.ceil(radius / self.cell_size))
        for dx in range(-cell_range, cell_range + 1):
            for dy in range(-cell_range, cell_range + 1):
                if self.dimensions == 3:
                    for dz in range(-cell_range, cell_range + 1):
                        key = (center_hash[0]+dx, center_hash[1]+dy, center_hash[2]+dz)
                        if key in self.cells:
                            for item, pos in self.cells[key].items:
                                dist = math.sqrt(sum((p - c) ** 2 for p, c in zip(pos[:self.dimensions], center[:self.dimensions])))
                                if dist <= radius:
                                    results.append(item)
                else:
                    key = (center_hash[0]+dx, center_hash[1]+dy)
                    if key in self.cells:
                        for item, pos in self.cells[key].items:
                            dist = math.sqrt(sum((p - c) ** 2 for p, c in zip(pos[:2], center[:2])))
                            if dist <= radius:
                                results.append(item)
        return results

    def query_nearest(self, center: Tuple[float, ...], k: int = 1) -> List[Tuple[Any, float]]:
        """Return k nearest items as (item, distance) tuples."""
        all_items = self.query_radius(center, self.cell_size * 10)
        scored = []
        for item in all_items:
            # Need position — find it
            for cell in self.cells.values():
                for i, pos in cell.items:
                    if i == item:
                        dist = math.sqrt(sum((p - c) ** 2 for p, c in zip(pos[:self.dimensions], center[:self.dimensions])))
                        scored.append((item, dist))
                        break
        scored.sort(key=lambda x: x[1])
        return scored[:k]

    def clear(self):
        self.cells.clear()

    def __len__(self):
        return sum(len(c.items) for c in self.cells.values())


if __name__ == "__main__":
    grid = SpatialGrid(cell_size=10.0, dimensions=2)
    grid.insert("player", (5, 5))
    grid.insert("enemy1", (8, 3))
    grid.insert("enemy2", (50, 50))
    grid.insert("npc", (12, 8))
    nearby = grid.query_radius((5, 5), radius=15)
    print(f"Items within 15 of (5,5): {nearby}")
    print(f"Total items in grid: {len(grid)}")
