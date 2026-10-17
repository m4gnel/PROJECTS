from dataclasses import dataclass
from typing import TypeVar, Generic, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


T = TypeVar("T")


@dataclass
class PageParams:
    page: int = 1
    size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


async def paginate(session: AsyncSession, query, params: PageParams):
    result = await session.execute(query.offset(params.offset).limit(params.size))
    return result.scalars().all()
