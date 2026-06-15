from auth_kit.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_flow_api.models.enums import ProjectRole
from task_flow_api.models.project import Project
from task_flow_api.models.project_member import ProjectMember
from task_flow_api.schemas.project import ProjectCreate, ProjectMemberCreate


async def create_project(
    db: AsyncSession, data: ProjectCreate, creator: User
) -> Project:
    project = Project(
        name=data.name,
        description=data.description,
        created_by=creator.id,
    )
    db.add(project)
    await db.flush()

    membership = ProjectMember(
        project_id=project.id,
        user_id=creator.id,
        role=ProjectRole.ADMIN,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(project)

    return project


async def add_member(
    db: AsyncSession, project_id: str, data: ProjectMemberCreate
) -> ProjectMember:
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == data.user_id,
        )
    )
    existing: ProjectMember | None = result.scalar_one_or_none()

    if existing is not None:
        existing.role = data.role
        await db.commit()
        await db.refresh(existing)
        return existing

    membership = ProjectMember(
        project_id=project_id,
        user_id=data.user_id,
        role=data.role,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)

    return membership
