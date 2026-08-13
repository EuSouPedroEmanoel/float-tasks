import factory.fuzzy

from todolist.models import Task, TasksStates


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TasksStates)
    user_id = 1
