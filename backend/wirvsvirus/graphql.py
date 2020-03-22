import logging

from fastapi import APIRouter, Request, HTTPException
from graphene_pydantic import PydanticObjectType
from graphql import GraphQLError
from graphql.execution.executors.asyncio import AsyncioExecutor
from bson import ObjectId
import graphene
from graphene_pydantic import PydanticObjectType
from starlette.graphql import GraphQLApp
from pydantic import ValidationError

from wirvsvirus import models, db, crud
from wirvsvirus import auth

logger = logging.getLogger(__name__)


class Location(PydanticObjectType):
    class Meta:
        model = models.Location


class Helper(PydanticObjectType):
    class Meta:
        model = models.Helper


class PersonnelRequirement(PydanticObjectType):

    matches = graphene.List(lambda: Match)

    class Meta:
        model = models.PersonnelRequirement


class MongoDbLocation(PydanticObjectType):
    class Meta:
        model = models.MongoDbLocation


class Hospital(PydanticObjectType):

    personnel_requirements = graphene.List(PersonnelRequirement)

    async def resolve_personnel_requirements(self, info):
        documents = await crud.find('personnel_requirements', {'hospital_id': str(self.id)})
        return [models.PersonnelRequirement(**d) for d in documents]

    class Meta:
        model = models.Hospital


class Match(PydanticObjectType):

    helper = Helper
    personnel_requirement = PersonnelRequirement

    def resolve_helper(self, info):
        document = crud.get_item('helpers', id=ObjectId(self.helper_id))
        if not document:
            raise GraphQLError('Helper does not exist.')
        return models.Helper(**document)

    class Meta:
        model = models.Match


class Query(graphene.ObjectType):
    hospital = graphene.Field(Hospital, id=graphene.ID())
    hospitals = graphene.List(Hospital)
    helper = graphene.Field(Hospital, id=graphene.ID())


    async def resolve_hospital(self, info, id):
        document = await crud.get_item('hospitals', ObjectId(id))
        if not document:
            raise GraphQLError('No hospital available for this id.')
        return models.Hospital(**document)

    async def resolve_hospitals(self, info):
        documents = await crud.find('hospitals', {})
        return [models.Hospital(**d) for d in documents]

    async def resolve_helper(self, info, id):
        document = await db.get_database().helpers.find_one({'_id': ObjectId(id)})
        return models.Helper(**document)


router = APIRouter()


class AuthenticatedGraphQLApp(GraphQLApp):
    async def handle_graphql(self, request: Request):
        await auth.auth(request)
        return await super().handle_graphql(request)

graphql_app = AuthenticatedGraphQLApp(schema=graphene.Schema(query=Query), executor_class=AsyncioExecutor)
