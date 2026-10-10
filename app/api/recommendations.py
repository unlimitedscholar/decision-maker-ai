
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    require_tenant_role,
)
from app.models.company import Company
from app.models.icp_profile import ICPProfile
from app.models.identity import MembershipRole
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_query_service import (
    get_recommendation,
    list_recommendations,
)
from app.services.recommendation_service import (
    create_recommendation,
)


router = APIRouter(
    prefix="/tenants/{tenant_id}/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "/companies/{company_id}",
    response_model=RecommendationResponse,
)
def generate_recommendation(
    tenant_id: UUID,
    company_id: UUID,
    icp_profile_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db),
    membership=Depends(
        require_tenant_role(MembershipRole.MEMBER)
    ),
):
    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id,
        )
        .first()
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found.",
        )

    if icp_profile_id is not None:
        icp_profile = (
            db.query(ICPProfile)
            .filter(
                ICPProfile.id == icp_profile_id,
                ICPProfile.tenant_id == tenant_id,
            )
            .first()
        )

        if icp_profile is None:
            raise HTTPException(
                status_code=404,
                detail="ICP profile not found.",
            )

    else:
        icp_profile = (
            db.query(ICPProfile)
            .filter(
                ICPProfile.tenant_id == tenant_id,
            )
            .order_by(
                ICPProfile.created_at.asc()
            )
            .first()
        )

    if icp_profile is None:
        raise HTTPException(
            status_code=400,
            detail="No ICP profile exists for this tenant.",
        )

    return create_recommendation(
        session=db,
        company=company,
        icp_profile=icp_profile,
    )


@router.get(
    "",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    tenant_id: UUID,
    company_id: UUID | None = None,
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
    membership=Depends(
        require_tenant_role(MembershipRole.MEMBER)
    ),
):
    return list_recommendations(
        session=db,
        tenant_id=tenant_id,
        company_id=company_id,
        limit=limit,
    )


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
)
def get_recommendation_detail(
    tenant_id: UUID,
    recommendation_id: UUID,
    db: Session = Depends(get_db),
    membership=Depends(
        require_tenant_role(MembershipRole.MEMBER)
    ),
):
    recommendation = get_recommendation(
        session=db,
        tenant_id=tenant_id,
        recommendation_id=recommendation_id,
    )

    if recommendation is None:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found.",
        )

    return recommendation
