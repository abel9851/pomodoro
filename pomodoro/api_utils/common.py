from typing import Type

from rest_framework.exceptions import NotFound

from django.db.models import Model


def get_model_model_instance_by_pk_or_not_found(model: Type[Model], pk: int) -> Model:
    """
    pk와 model로 model instance를 get.
    존재하지 않는다면 NotFound 예외 발생.
    """
    try:
        instance = model.objects.get(pk=pk)

    except model.DoesNotExist:
        raise NotFound()

    return instance
