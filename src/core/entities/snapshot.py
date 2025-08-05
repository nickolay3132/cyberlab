from dataclasses import dataclass
from typing import List


@dataclass
class Snapshot:
    name: str
    description: str
    timestamp: int
    is_current: bool
    children: List['Snapshot']

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'timestamp': self.timestamp,
            'is_current': self.is_current,
            'children': [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data: dict) -> 'Snapshot':
        children = [Snapshot.from_dict(child) for child in data.get('children', [])]
        return Snapshot(
            name=data['name'],
            description=data['description'],
            timestamp=data['timestamp'],
            is_current=data['is_current'],
            children=children
        )