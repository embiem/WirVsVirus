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

from wirvsvirus import models, db
from wirvsvirus import auth

logger = logging.getLogger(__name__)


class Helper(PydanticObjectType):
    class Meta:
        model = models.Helper


class PersonnelRequirement(PydanticObjectType):

    matches = graphene.List(lambda: Match)

    class Meta:
        model = models.PersonnelRequirement


class Hospital(PydanticObjectType):

    personnel_requirements = graphene.List(PersonnelRequirement)

    async def resolve_personnel_requirements(self, info):
        document = await db.get_database().personnel_requirements.find({'hospital_id': ObjectId(self.id)})
        return models.Hospital(**document)

    class Meta:
        model = models.Hospital


class Match(PydanticObjectType):
    class Meta:
        model = models.Match


class Query(graphene.ObjectType):
    hospital = graphene.Field(Hospital, id=graphene.ID())

    helper = graphene.Field(Hospital, id=graphene.ID())

    async def resolve_hospital(self, info, id):
        document = await db.get_database().hospitals.find_one({'_id': ObjectId(id)})
        if not document:
            raise GraphQLError()
        return models.Hospital(**document)

    async def resolve_helper(self, info, id):
        document = await db.get_database().helpers.find_one({'_id': ObjectId(id)})
        return models.Helper(**document)


router = APIRouter()


class AuthenticatedGraphQLApp(GraphQLApp):
    async def handle_graphql(self, request: Request):
        await auth.auth(request)
        return await super().handle_graphql(request)

graphql_app = AuthenticatedGraphQLApp(schema=graphene.Schema(query=Query), executor_class=AsyncioExecutor)
