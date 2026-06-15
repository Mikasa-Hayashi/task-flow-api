from auth_kit.core.dependencies import get_current_user
from auth_kit.db.session import get_db
from auth_kit.models.user import User
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_flow_api.models.enums import ProjectRole
from task_flow_api.models.project_member import ProjectMember

_ROLE_RANK: dict[ProjectRole, int] = {
    ProjectRole.VIEWER: 0,
    ProjectRole.MEMBER: 1,
    ProjectRole.ADMIN: 2,
}


async def get_project_member(
    project_id: str = Path(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProjectMember:
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
        )
    )
    member = result.scalar_one_or_none()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return member


def require_role(minimum_role: ProjectRole):
    async def checker(
        member: ProjectMember = Depends(get_project_member),
    ) -> ProjectMember:
        if _ROLE_RANK[member.role] < _ROLE_RANK[minimum_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this action",
            )
        return member

    return checker
