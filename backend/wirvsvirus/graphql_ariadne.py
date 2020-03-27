import inspect
import asyncio
from typing import Type, Dict, List
from pathlib import Path

from ariadne import gql, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL, Request
from ariadne.types import Extension
from ariadne import ObjectType, QueryType, make_executable_schema
from pydantic import BaseModel

from wirvsvirus import db, models, crud, auth
from bson import ObjectId


type_defs = load_schema_from_path(Path(__file__).parent / "schema.graphql")

# Ariadne uses dedicated objects
query = QueryType()
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
    ModelLink(model=models.Hospital, collection='hospitals',
              graphql_type_name='Hospital'),
    ModelLink(model=models.Helper, collection='helpers',
              graphql_type_name='Helper'),
    ModelLink(model=models.Match, collection='matches',
              graphql_type_name='Match'),
    ModelLink(model=models.Profile, collection='profiles',
              graphql_type_name='Profile'),
    ModelLink(model=models.PersonnelRequirement, collection='personnel_requirements',
              graphql_type_name='PersonnelRequirement'),
]
model_link_map: Dict[ModelType, ModelLink] = {
    link.model: link for link in model_links
}
graphql_type_link_map: Dict[str, ModelLink] = {
    link.graphql_type_name: link for link in model_links
}



@query.field("hospital")
async def resolve_hospital(_, info):
    profile: models.Profile = await info.context['auth'].get_profile()
    if profile.type != models.ProfileType.hospital:
        raise ValueError(f"User with doesn't have a hospital profile")
    return await _resolve_by_id(profile.hospital_id, models.Hospital)


@query.field("hospitals")
async def resolve_all_hospitals(_, info):
    documents = await crud.find('hospitals', {})
    return [models.Hospital(**d) for d in documents]


@query.field("helper")
async def resolve_helper(_, info):
    profile: models.Profile = await info.context['auth'].get_profile()
    if not profile.type == models.ProfileType.helper:
        raise ValueError(f"User with doesn't have a helper profile")
    result = await _resolve_by_id(profile.helper_id, models.Helper)
    return result


# Resolvers for object types

@profile.field('helper')
@match.field('helper')
async def resolve_child_helper(obj, info):
    result = await _resolve_by_id(obj.helper_id, models.Helper)
    return result

@helper.field('matches')
async def resolve_helper_matches(obj, info):
    documents = await crud.find('matches', {'helper_id': str(obj.id)})
    return [models.Match(**d) for d in documents]


@profile.field('hospital')
@personnel_requirement.field('hospital')
async def resolve_child_hospital(obj, info):
    return await _resolve_by_id(obj.hospital_id, models.Hospital)


@hospital.field('matches')
async def resolve_hospital_matches(obj, info):
    pr_documents = await crud.find('personnel_requirements', {'hospital_id': str(obj.id)})
    personnel_requirements_ids = [str(d['_id']) for d in pr_documents]
    documents = []
    # TODO: do this with "$in" bin i'm to stupid
    for pr_id in personnel_requirements_ids:
        sub_documents = await crud.find('matches', {'personnel_requirement_id': pr_id})
        documents.extend(sub_documents)
    return [models.Match(**d) for d in documents]


@hospital.field('personnelRequirements')
async def resolve_hosital_personnel_requirements(obj, info):
    documents = await crud.find('personnel_requirements', {'hospital_id': str(obj.id)})
    return [models.PersonnelRequirement(**d) for d in documents]


@match.field('personnelRequirement')
async def resolve_child_personnel_requirements(obj, info):
    return await _resolve_by_id(ObjectId(obj.personnel_requirement_id), models.PersonnelRequirement)


async def _resolve_by_id(id: str, model_cls: Type[BaseModel]):
    if not id:
        return
    object_id = ObjectId(id)
    model_link = model_link_map[model_cls]
    document = await crud.get_item(model_link.collection, object_id)
    if not document:
        raise ValueError(
            f'{model_link.graphql_type_name} with id {id} not found')
    return model_cls(**document)


class GraphQLAuth:
    def __init__(self, request: Request):
        self.request = request
        self._jwt_payload: auth.JWTPayload = None
        self._profile: models.Profile = None

    async def get_jwt_payload(self) -> auth.JWTPayload:
        if not self._jwt_payload:
            self._jwt_payload = await auth.auth(self.request)
        return self._jwt_payload

    async def get_profile(self) -> models.Profile:
        if self._profile:
            return self._profile
        jwt_payload = await self.get_jwt_payload()
        user_id = jwt_payload.sub
        result = await db.get_database().profiles.find_one({'user_id': user_id})
        if not result:
            raise ValueError(f'No profile found for user {user_id}')
        self._profile = models.Profile(**result)
        return self._profile


async def auth_middleware(resolver, obj, info, *args, **kwargs):
    auth_context = info.context.get('auth')
    if not auth_context:
        graphql_auth = GraphQLAuth(info.context['request'])
        await graphql_auth.get_jwt_payload()
        info.context['auth'] = graphql_auth

    result = resolver(obj, info, *args, **kwargs)

    # handle async results if needed
    if inspect.isawaitable(result):
        result = await result

    return result


schema = make_executable_schema(
    type_defs, query, profile, hospital, helper, match, personnel_requirement, 
    snake_case_fallback_resolvers)
graphql_app = GraphQL(schema, middleware=[auth_middleware])
