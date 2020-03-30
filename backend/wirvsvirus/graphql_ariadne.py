import inspect
import asyncio
import requests
from typing import Type, Dict, List, Union, Optional
from pathlib import Path

from ariadne import (
    gql,
    load_schema_from_path,
    snake_case_fallback_resolvers,
    convert_kwargs_to_snake_case,
)
from ariadne.asgi import GraphQL, Request
from ariadne.types import Extension
from ariadne import MutationType, ObjectType, QueryType, make_executable_schema
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from wirvsvirus import db, models, crud, auth
from wirvsvirus.settings import settings
from bson import ObjectId


type_defs = load_schema_from_path(Path(__file__).parent / "schema.graphql")

# Ariadne uses dedicated objects
query = QueryType()
mutation = MutationType()
profile = ObjectType("Profile")
hospital = ObjectType("Hospital")
helper = ObjectType("Helper")
match = ObjectType("Match")
personnel_requirement = ObjectType("PersonnelRequirement")


ModelType = Type[BaseModel]


class ModelLink(BaseModel):
    model: ModelType  # pydantic model
    collection: str  # database collection
    graphql_type_name: str


model_links = [
    ModelLink(
        model=models.Hospital, collection="hospitals", graphql_type_name="Hospital"
    ),
    ModelLink(model=models.Helper, collection="helpers", graphql_type_name="Helper"),
    ModelLink(model=models.Match, collection="matches", graphql_type_name="Match"),
    ModelLink(model=models.Profile, collection="profiles", graphql_type_name="Profile"),
    ModelLink(
        model=models.PersonnelRequirement,
        collection="personnel_requirements",
        graphql_type_name="PersonnelRequirement",
    ),
]
model_link_map: Dict[ModelType, ModelLink] = {link.model: link for link in model_links}
graphql_type_link_map: Dict[str, ModelLink] = {
    link.graphql_type_name: link for link in model_links
}


@query.field("hospital")
async def resolve_hospital(_, info) -> models.Hospital:
    profile: models.Profile = await info.context["auth"].get_profile()
    if profile.type != models.ProfileType.hospital:
        raise ValueError(f"User with doesn't have a hospital profile")
    return await models.Hospital.get_by_id(profile.hospital_id)


@query.field("hospitals")
async def resolve_all_hospitals(_, info) -> List[models.Hospital]:
    return await models.Hospital.find({})


@query.field("helper")
async def resolve_helper(_, info):
    profile: models.Profile = await info.context["auth"].get_profile()
    if not profile.type == models.ProfileType.helper:
        raise ValueError(f"User with doesn't have a helper profile")
    return await models.Helper.get_by_id(profile.helper_id)


# Resolvers for object types


@profile.field("helper")
@match.field("helper")
async def resolve_child_helper(
    obj: Union[models.Profile, models.Match], info
) -> models.Helper:
    result = await models.Helper.get_by_id(obj.helper_id)
    return result


@helper.field("matches")
async def resolve_helper_matches(obj: models.Helper, info) -> List[models.Match]:
    result = await models.Match.find({"helper_id": obj.id})
    return result


@profile.field("hospital")
@personnel_requirement.field("hospital")
async def resolve_child_hospital(
    obj: Union[models.Profile, models.PersonnelRequirement], info
) -> models.Hospital:
    return await models.Hospital.get_by_id(obj.hospital_id)


@hospital.field("matches")
async def resolve_hospital_matches(obj, info) -> List[models.Match]:
    personnel_requirements = await models.PersonnelRequirement.find(
        {"hospital_id": obj.id}
    )
    matches: List[models.Match] = []
    # TODO: do this with "$in" bin i'm to stupid
    for personnel_requirement in personnel_requirements:
        sub_matches = await models.Match.find(
            {"personnel_requirement_id": personnel_requirement.id}
        )
        matches.extend(sub_matches)
    return matches


@hospital.field("personnelRequirements")
async def resolve_hosital_personnel_requirements(
    obj: models.Hospital, info
) -> List[models.PersonnelRequirement]:
    return await models.PersonnelRequirement.find({"hospital_id": obj.id})


@match.field("personnelRequirement")
async def resolve_child_personnel_requirements(
    obj: models.Match, info
) -> models.PersonnelRequirement:
    return await models.PersonnelRequirement.get_by_id(obj.personnel_requirement_id)


# Mutations


@mutation.field("createHelperProfile")
@convert_kwargs_to_snake_case
async def resolve_helper_profile_creation(obj, info, **kwargs) -> models.Profile:
    jwt_payload = await info.context["auth"].get_jwt_payload()
    user_info: auth.UserInfo = await info.context["auth"].get_user_info()
    existing_profiles = await models.Profile.find({"user_id": jwt_payload.sub})
    if existing_profiles:
        raise ValueError(f"Profile with user id {jwt_payload.sub} already exists.")

    # use email from the account we signed in with
    kwargs["email"] = user_info.email
    helper = models.Helper.parse_obj(kwargs)
    profile = models.Profile(
        user_id=jwt_payload.sub,
        type=models.ProfileType.helper,
        helper_id=helper.id,
        email=helper.email,
    )
    await helper.create()
    await profile.create()
    return profile


@mutation.field("createHospitalProfile")
@convert_kwargs_to_snake_case
async def resolve_hospital_profile_creation(obj, info, hospital_id: str) -> models.Profile:
    jwt_payload = await info.context["auth"].get_jwt_payload()
    user_info: auth.UserInfo = await info.context["auth"].get_user_info()
    existing_profiles = await models.Profile.find({"user_id": jwt_payload.sub})
    if existing_profiles:
        raise ValueError(f"Profile with user id {jwt_payload.sub} already exists.")

    hospital = await models.Hospital.get_by_id(db.ObjectIdStr(hospital_id))
    if not hospital:
        raise ValueError(f"Hospital with id {hospital_id} could not be found")

    profile = models.Profile(
        user_id=jwt_payload.sub,
        type=models.ProfileType.hospital,
        hospital_id=hospital.id,
        email=user_info.email,
    )
    await profile.create()
    return profile


@mutation.field("updateHospital")
@convert_kwargs_to_snake_case
async def resolve_update_hospital(obj, info, **kwargs) -> models.Hospital:
    """Update the current users hospital."""
    profile: models.Profile = await info.context["auth"].get_profile()
    if profile.type != models.ProfileType.hospital:
        raise ValueError("Can only update hospitals for users with hospital profiles.")

    hospital = await models.Hospital.get_by_id(profile.hospital_id)
    if not hospital:
        raise ValueError(
            f"Couldn't find profiles hospital with id {profile.hospital_id}"
        )
    # update the hospital with the given keyword arguments
    hospital = models.Hospital.parse_obj(hospital.copy(update=kwargs))
    await hospital.update()  # write to db
    return hospital


@mutation.field("updateHelper")
@convert_kwargs_to_snake_case
async def resolve_update_helper(obj, info, **kwargs) -> models.Helper:
    """Update the current users helper."""
    profile: models.Profile = await info.context["auth"].get_profile()
    if profile.type != models.ProfileType.helper:
        raise ValueError("Can only update helper for users with helper profiles.")

    helper = await models.Helper.get_by_id(profile.helper_id)
    if not helper:
        raise ValueError(f"Couldn't find profiles helper with id {profile.helper_id}")
    # update the helper with the given keyword arguments
    helper = models.Helper.parse_obj(helper.copy(update=kwargs))
    await helper.update()  # write to db
    return helper


@mutation.field("requestHelper")
@convert_kwargs_to_snake_case
async def resolve_request_helper(obj, info, **kwargs) -> models.Match:
    """Request a specific helper to fullfill a personnel requirement."""
    profile: models.Profile = await info.context["auth"].get_profile()
    if profile.type != models.ProfileType.hospital:
        raise ValueError("Can only request helper for users with hospital profiles.")

    new_match = models.Match(**kwargs)
    await new_match.create()
    return new_match


@mutation.field("updateRequest")
@convert_kwargs_to_snake_case
async def resolve_update_match(obj, info, match_id: str, status: str) -> models.Match:
    """Request a specific helper to fullfill a personnel requirement."""
    profile: models.Profile = await info.context[
        "auth"
    ].get_profile()  # user must have profile
    match = await models.Match.get_by_id(db.ObjectIdStr(match_id))
    if match is None:
        raise ValueError("Match does not exist.")

    match_status = models.MatchStatus[status]

    if profile.type == models.ProfileType.helper:
        if match.helper_id != profile.helper_id:
            raise ValueError("This is not your match.  Please don't touch it!")
    elif profile.type == models.ProfileType.hospital:
        personnel_requirement = models.PersonnelRequirement.get_by_id(
            match.personnel_requirement_id
        )
        if (
            not personnel_requirement
            or personnel_requirement.hospital_id != profile.hospital_id
        ):
            raise ValueError(
                "Personnel requirement does not exist or does not belong to your hospital."
            )
        if match_status == models.MatchStatus.accepted:
            raise ValueError("Only helpers can accept matches!")
    else:
        raise ValueError("Invalid profile type.")

    match.status = match_status
    await match.update()
    return match


@mutation.field("setPersonnelRequirement")
@convert_kwargs_to_snake_case
async def resolve_set_personnel_requirement(
    obj, info, activity_id: str, count_required: int
) -> models.PersonnelRequirement:
    """Request a specific helper to fullfill a personnel requirement."""
    profile: models.Profile = await info.context[
        "auth"
    ].get_profile()  # user must have profile
    if profile.type != models.ProfileType.hospital:
        raise ValueError("Can set personnel requirements with hospital profile.")

    try:
        count_required = int(count_required)
    except (ValueError, TypeError):
        raise TypeError("Must provide valid integer for count required.")
    if count_required < 0:
        raise ValueError("Count required must be >=0")

    personnel_requirements = models.PersonnelRequirement.find(
        {"hospital_id": profile.hospital_id, "activityId": activity_id}
    )
    if personnel_requirements:
        personnel_requirement = personnel_requirements[0]
        personnel_requirement.value = count_required
        await personnel_requirement.update()
    else:
        personnel_requirement = models.PersonnelRequirement(
            hospital_id=profile.hospital_id,
            activity_id=activity_id,
            count_required=count_required,
        )
        await personnel_requirement.create()
    return personnel_requirement


class GraphQLAuth:
    def __init__(self, request: Request):
        self.request = request
        self._jwt_payload: auth.JWTPayload = None
        self._user_info: models.UserInfo = None
        self._profile: models.Profile = None

    async def get_jwt_payload(self) -> auth.JWTPayload:
        try:
            if not self._jwt_payload:
                self._jwt_payload = await auth.auth(self.request)
        except HTTPException as e:
            raise ValueError(f"Authentication failed: {e.detail}")
        return self._jwt_payload

    async def get_profile(self) -> models.Profile:
        if self._profile:
            return self._profile
        jwt_payload = await self.get_jwt_payload()
        user_id = jwt_payload.sub
        result = await models.Profile.get_collection().find_one({"user_id": user_id})
        if not result:
            raise ValueError(f"No profile found for user {user_id}")
        self._profile = models.Profile.parse_obj(result)
        return self._profile

    async def get_user_info(self) -> auth.UserInfo:
        """Obtain userinfo from auth0."""
        if self._user_info:
            return self._user_info
        jwt_payload = await self.get_jwt_payload()
        self._user_info = await auth.get_user_info(jwt_payload.token)
        return self._user_info


async def auth_middleware(resolver, obj, info, *args, **kwargs):
    auth_context = info.context.get("auth")
    if not auth_context and not info.path.as_list()[0] == "__schema":
        graphql_auth = GraphQLAuth(info.context["request"])
        await graphql_auth.get_jwt_payload()
        info.context["auth"] = graphql_auth

    result = resolver(obj, info, *args, **kwargs)

    # handle async results if needed
    if inspect.isawaitable(result):
        result = await result

    return result


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    profile,
    hospital,
    helper,
    match,
    personnel_requirement,
    snake_case_fallback_resolvers,
)
graphql_app = GraphQL(schema, middleware=[auth_middleware])  # type: ignore
