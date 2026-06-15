from datetime import datetime

from pydantic import BaseModel, ConfigDict

from task_flow_api.models.enums import ProjectRole


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str | None
    created_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberCreate(BaseModel):
    user_id: str
    role: ProjectRole


class ProjectMemberResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    role: ProjectRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)
