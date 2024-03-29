import graphene
from datetime import datetime
import json


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required=False)


class Query(graphene.ObjectType):
    users = graphene.List(User, first=graphene.Int())
    is_staff = graphene.Boolean()
    goodbye = graphene.String()

    def resolve_is_staff(root, info):
        return True

    def resolve_users(self, info, first):
        return [
            User(username='Alice', last_login=datetime.now()),
            User(username='Bob', last_login=datetime.now()),
            User(username='Steven', last_login=datetime.now()),
        ][:first]

    def resolve_goodbye(root, info):
        return 'See ya!'


class CreateUser(graphene.Mutation):

    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        if info.context.get('is_vip'):
            username = username.upper()
        user = User(username=username)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

result = schema.execute(
    '''
    mutation createUser($username: String) {
        createUser(username: $username){
            user {
                username
            }
        }
    }
    ''',
    variable_values={'username': 'Alice'},
    context={'is_vip': False}
)

items = dict(result.data.items())
print(json.dumps(items, indent=4))
