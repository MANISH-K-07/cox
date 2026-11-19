from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str
    entity_type: str
    description: str = ""


class Relationship(BaseModel):
    source_entity: str
    relationship: str
    target_entity: str

    evidence: str
    source_chunk_id: str

    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class GraphExtraction(BaseModel):
    entities: list[Entity] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
