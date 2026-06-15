from auth_kit.core.dependencies import get_current_user
from auth_kit.db.session import get_db
from auth_kit.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from task_flow_api.api.deps import require_role
from task_flow_api.models.enums import ProjectRole
from task_flow_api.models.project_member import ProjectMember
from task_flow_api.schemas.project import (
    ProjectCreate,
    ProjectMemberCreate,
    ProjectMemberResponse,
    ProjectResponse,
)
from task_flow_api.services.project import add_member, create_project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project_endpoint(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    project = await create_project(db, data, current_user)
    return ProjectResponse.model_validate(project)


@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_member_endpoint(
    data: ProjectMemberCreate,
    db: AsyncSession = Depends(get_db),
    _admin: ProjectMember = Depends(require_role(ProjectRole.ADMIN)),
) -> ProjectMemberResponse:
    try:
        membership = await add_member(db, _admin.project_id, data)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return ProjectMemberResponse.model_validate(membership)
